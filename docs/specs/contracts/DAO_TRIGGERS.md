# DAO Milestone Triggers & Governance Framework

**Status**: Implementation-Ready  
**Version**: 1.0  
**Purpose**: Define milestone-based unlock accelerators and emergency controls

---

## Overview

The DAO controls bonus coin releases (33B tokens) through milestone-based voting. Each phase requires specific network health metrics before DAO can approve unlock acceleration.

---

## Milestone Definitions

### Market Cap Milestones

| Milestone | Market Cap Target | Bonus Unlock | Sustained Period |
|-----------|------------------|--------------|-----------------|
| MC-100M | $100M | +1% bonus early | 30 days |
| MC-250M | $250M | +2% bonus early | 30 days |
| MC-500M | $500M | +3% bonus early | 30 days |
| MC-1B | $1B | +5% bonus early | 30 days |

### TVL Milestones

| Milestone | TVL Target | Bonus Unlock | Sustained Period |
|-----------|-----------|--------------|-----------------|
| TVL-50M | $50M | +2% bonus early | 14 days |
| TVL-100M | $100M | +3% bonus early | 14 days |
| TVL-250M | $250M | +5% bonus early | 14 days |

### Network Growth Milestones

| Milestone | Target | Bonus Unlock | Measurement |
|-----------|--------|--------------|-------------|
| WALLETS-100K | 100K active wallets | +1% bonus early | Monthly average |
| WALLETS-500K | 500K active wallets | +2% bonus early | Monthly average |
| WALLETS-1M | 1M active wallets | +3% bonus early | Monthly average |

### Infrastructure Milestones

| Milestone | Target | Bonus Unlock | Verification |
|-----------|--------|--------------|-------------|
| HARDWARE-ALL | All X30/X100 delivered | +3% bonus early | Verified delivery |
| CEX-5 | 5 Top-50 CEX listings | +2% bonus early | Confirmed listings |
| CEX-10 | 10 Top-50 CEX listings | +3% bonus early | Confirmed listings |

---

## Smart Contract Implementation

```solidity
import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

contract BlockDAGDAO is Governor, GovernorVotes, GovernorTimelockControl {
    
    struct Milestone {
        string name;
        uint256 marketCapTarget;
        uint256 tvlTarget;
        uint256 walletCountTarget;
        bool hardwareDelivered;
        uint256 cexListingCount;
        bool achieved;
        uint256 achievementTimestamp;
        uint256 bonusUnlockPercent;
        uint256 sustainedDays;
        uint256 startTimestamp;
    }
    
    mapping(string => Milestone) public milestones;
    mapping(string => bool) public milestoneProposals;
    
    // Oracle addresses
    address public priceOracle;
    address public tvlOracle;
    address public walletOracle;
    
    constructor(
        IVotes _token,
        TimelockController _timelock,
        address _priceOracle,
        address _tvlOracle,
        address _walletOracle
    ) Governor("BlockDAG DAO") GovernorVotes(_token) GovernorTimelockControl(_timelock) {
        priceOracle = _priceOracle;
        tvlOracle = _tvlOracle;
        walletOracle = _walletOracle;
        
        initializeMilestones();
    }
    
    function initializeMilestones() internal {
        // Market cap milestones
        milestones["MC-100M"] = Milestone({
            name: "MC-100M",
            marketCapTarget: 100_000_000 * 1e6, // $100M (6 decimals)
            tvlTarget: 0,
            walletCountTarget: 0,
            hardwareDelivered: false,
            cexListingCount: 0,
            achieved: false,
            achievementTimestamp: 0,
            bonusUnlockPercent: 1,
            sustainedDays: 30,
            startTimestamp: 0
        });
        
        // ... initialize other milestones
    }
    
    function checkMilestone(string memory milestoneName) external {
        Milestone storage milestone = milestones[milestoneName];
        require(!milestone.achieved, "Milestone already achieved");
        
        bool conditionsMet = true;
        
        // Check market cap
        if (milestone.marketCapTarget > 0) {
            uint256 currentMarketCap = getMarketCap();
            if (currentMarketCap < milestone.marketCapTarget) {
                conditionsMet = false;
            } else {
                // Start tracking sustained period
                if (milestone.startTimestamp == 0) {
                    milestone.startTimestamp = block.timestamp;
                }
                uint256 daysSustained = (block.timestamp - milestone.startTimestamp) / 1 days;
                if (daysSustained < milestone.sustainedDays) {
                    conditionsMet = false;
                }
            }
        }
        
        // Check TVL
        if (milestone.tvlTarget > 0) {
            uint256 currentTVL = getTVL();
            if (currentTVL < milestone.tvlTarget) {
                conditionsMet = false;
            }
        }
        
        // Check wallet count
        if (milestone.walletCountTarget > 0) {
            uint256 currentWallets = getActiveWalletCount();
            if (currentWallets < milestone.walletCountTarget) {
                conditionsMet = false;
            }
        }
        
        // Check hardware delivery
        if (milestone.hardwareDelivered) {
            bool allHardwareDelivered = checkHardwareDelivery();
            if (!allHardwareDelivered) {
                conditionsMet = false;
            }
        }
        
        // Check CEX listings
        if (milestone.cexListingCount > 0) {
            uint256 currentListings = getCEXListingCount();
            if (currentListings < milestone.cexListingCount) {
                conditionsMet = false;
            }
        }
        
        if (conditionsMet) {
            milestone.achieved = true;
            milestone.achievementTimestamp = block.timestamp;
            
            // Create proposal to accelerate bonus unlock
            string memory description = string(abi.encodePacked(
                "Milestone achieved: ", milestoneName,
                ". Accelerate bonus unlock by ", 
                Strings.toString(milestone.bonusUnlockPercent), "%"
            ));
            
            bytes memory data = abi.encodeWithSignature(
                "accelerateBonusUnlock(uint256)",
                milestone.bonusUnlockPercent
            );
            
            propose(
                getTargets(),
                getValues(),
                new string[](0),
                new bytes[](0),
                description
            );
            
            emit MilestoneAchieved(milestoneName, block.timestamp);
        }
    }
    
    function accelerateBonusUnlock(uint256 percent) external onlyGovernance {
        // This function is called by successful DAO proposal
        require(percent > 0 && percent <= 10, "Invalid percent");
        
        // Accelerate next bonus phase
        vestingContract.accelerateNextPhase(percent);
        
        emit BonusUnlockAccelerated(percent, block.timestamp);
    }
    
    // Oracle integration functions
    function getMarketCap() public view returns (uint256) {
        // Query price oracle
        uint256 price = IPriceOracle(priceOracle).getPrice();
        uint256 circulatingSupply = token.totalSupply() - token.balanceOf(address(vestingContract));
        return price * circulatingSupply / 1e18;
    }
    
    function getTVL() public view returns (uint256) {
        return ITVLOracle(tvlOracle).getTotalValueLocked();
    }
    
    function getActiveWalletCount() public view returns (uint256) {
        return IWalletOracle(walletOracle).getActiveWalletCount(30 days);
    }
    
    function checkHardwareDelivery() public view returns (bool) {
        // Check with hardware delivery oracle/registry
        return IHardwareRegistry(hardwareRegistry).allDelivered();
    }
    
    function getCEXListingCount() public view returns (uint256) {
        return ICEXRegistry(cexRegistry).getTop50ListingCount();
    }
}
```

---

## Voting Requirements

### Proposal Thresholds

| Proposal Type | Minimum Voting Power | Quorum | Approval Threshold |
|---------------|---------------------|--------|-------------------|
| Bonus Phase Approval | 10% of staked tokens | 5% | 67% supermajority |
| Milestone Acceleration | 5% of staked tokens | 3% | 60% majority |
| Emergency Pause | 15% of staked tokens | 10% | 75% supermajority |
| Parameter Change | 10% of staked tokens | 5% | 67% supermajority |

### Voting Periods

- **Standard Proposal**: 7 days voting + 2 days execution delay
- **Emergency Proposal**: 48 hours voting + 24 hours execution delay
- **Milestone Acceleration**: 5 days voting + 1 day execution delay

---

## Emergency Controls

### Price-Based Emergency Brake

```solidity
function proposeEmergencyPause() external {
    uint256 currentPrice = getCurrentPrice();
    uint256 priceThreshold = 0.02 * 1e6; // $0.02
    
    require(currentPrice < priceThreshold, "Price above threshold");
    require(block.timestamp - lastEmergencyProposal > 7 days, "Cooldown active");
    
    // Create emergency proposal
    proposeEmergency(
        "Pause all vesting due to price drop",
        abi.encodeWithSignature("pauseAllVesting()")
    );
}
```

### Liquidity-Based Emergency Brake

```solidity
function checkLiquidityEmergency() external {
    uint256 currentLiquidity = getCurrentLiquidity();
    uint256 liquidityThreshold = 10_000_000 * 1e6; // $10M
    
    if (currentLiquidity < liquidityThreshold) {
        // Automatic pause (no vote required for critical emergencies)
        vestingContract.pauseAllVesting();
        emit EmergencyPauseActivated("Low liquidity", block.timestamp);
    }
}
```

---

## Bonus Phase Approval Process

Each bonus phase (1-6) requires DAO approval before release:

```solidity
function proposeBonusPhaseRelease(uint256 phaseNumber) external {
    require(phaseNumber >= 1 && phaseNumber <= 6, "Invalid phase");
    
    BonusVestingPhase storage phase = vestingContract.bonusPhases(phaseNumber);
    
    // Check timing
    uint256 monthsSinceTGE = (block.timestamp - vestingContract.startTime()) / 30 days;
    require(monthsSinceTGE >= phase.startMonth, "Phase not started");
    
    // Check if already approved
    require(!phase.daoApproved, "Already approved");
    
    // Create proposal
    string memory description = string(abi.encodePacked(
        "Approve release of Bonus Phase ", Strings.toString(phaseNumber),
        " (", Strings.toString(phase.percentage), "% of bonus coins)"
    ));
    
    bytes memory data = abi.encodeWithSignature(
        "approveBonusPhase(uint256)",
        phaseNumber
    );
    
    propose(
        getTargets(),
        getValues(),
        new string[](0),
        new bytes[](0),
        description
    );
}
```

---

## Oracle Integration

### Price Oracle Interface

```solidity
interface IPriceOracle {
    function getPrice() external view returns (uint256); // 6 decimals
    function getPriceHistory(uint256 days) external view returns (uint256[] memory);
    function isPriceStable(uint256 threshold, uint256 days) external view returns (bool);
}
```

### TVL Oracle Interface

```solidity
interface ITVLOracle {
    function getTotalValueLocked() external view returns (uint256); // 6 decimals
    function getTVLByProtocol(string memory protocol) external view returns (uint256);
    function getTVLHistory(uint256 days) external view returns (uint256[] memory);
}
```

### Wallet Oracle Interface

```solidity
interface IWalletOracle {
    function getActiveWalletCount(uint256 period) external view returns (uint256);
    function getUniqueWallets(uint256 period) external view returns (uint256);
    function getWalletGrowthRate() external view returns (uint256); // Percentage
}
```

---

## Governance Token Weighting

Voting power based on staked tokens with lock duration multiplier:

```solidity
function getVotingPower(address voter) external view returns (uint256) {
    uint256 stakedAmount = stakingContract.getUserTotalStaked(voter);
    
    // Apply lock duration multiplier
    uint256 multiplier = stakingContract.getStakeWeight(voter);
    
    return (stakedAmount * multiplier) / 10000;
}
```

---

## Proposal Types

1. **Bonus Phase Approval**: Approve release of bonus coin phase
2. **Milestone Acceleration**: Accelerate unlock based on achieved milestone
3. **Emergency Pause**: Pause all vesting due to emergency conditions
4. **Parameter Adjustment**: Change emission rates, staking APY, etc.
5. **Treasury Allocation**: Allocate treasury funds for development/marketing
6. **Contract Upgrade**: Upgrade vesting/staking contracts (requires timelock)

---

## Security Considerations

1. **Timelock**: All proposals execute after timelock delay (minimum 24 hours)
2. **Quorum Requirements**: Prevent minority from controlling DAO
3. **Oracle Security**: Multiple oracle sources for critical data
4. **Emergency Override**: Admin can pause in extreme emergencies (with community notification)
5. **Proposal Limits**: Maximum 5 active proposals at once

---

## References

- [Vesting Contract Spec](./VESTING_CONTRACT_SPEC.md)
- [Staking Contract Spec](./STAKING_CONTRACT_SPEC.md)
- [Emergency Brake Logic](./EMERGENCY_BRAKE.md)


