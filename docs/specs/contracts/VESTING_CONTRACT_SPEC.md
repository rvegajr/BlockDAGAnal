# BlockDAG Presale Vesting Contract Specification

**Status**: Implementation-Ready  
**Version**: 1.0  
**Target Launch Price**: $0.05  
**Max Circulating at Launch**: 640M tokens (1.28% of 50B supply)

---

## Overview

This contract implements the aggressive vesting schedule required to maintain $0.05 launch price with $32M liquidity. The contract manages two token pools:

- **Base Coins**: 17B tokens (34% of presale)
- **Bonus Coins**: 33B tokens (66% of presale)

**Critical Constraint**: Only 2% of base coins (340M) unlock at TGE. Remaining 98% vest over 5-8 years with DAO-controlled releases.

---

## Contract Architecture

### Core Components

```
VestingContract
├── BaseCoinVesting (17B tokens)
│   ├── TGE Release: 2% (340M)
│   ├── Cliff: 12 months
│   └── Linear Release: Months 13-60 (98% over 48 months)
│
├── BonusCoinVesting (33B tokens)
│   ├── TGE Release: 0%
│   ├── Cliff: 24 months
│   └── DAO-Gated Release: Months 25-96 (100% over 72 months)
│
└── EmergencyBrake
    ├── Price-Based Pause
    ├── Liquidity-Based Pause
    └── DAO Override
```

---

## Base Coin Vesting Schedule

| Phase | Timing | % Released | Tokens | Unlock Type |
|-------|--------|------------|--------|-------------|
| TGE | Day 0 | 2% | 340M | Immediate claim |
| Cliff | Months 1-12 | 0% | 0 | Locked |
| Phase 1 | Months 13-24 | 8% | 1.36B | Linear monthly (113.3M/month) |
| Phase 2 | Months 25-36 | 15% | 2.55B | Linear monthly (212.5M/month) |
| Phase 3 | Months 37-48 | 25% | 4.25B | Linear monthly (354.2M/month) |
| Phase 4 | Months 49-60 | 50% | 8.5B | Linear monthly (708.3M/month) |
| **Total** | **60 months** | **100%** | **17B** | |

### Implementation Details

```solidity
struct BaseVestingSchedule {
    uint256 totalAmount;           // Total base coins allocated
    uint256 tgeAmount;             // 2% unlocked at TGE
    uint256 cliffDuration;          // 12 months in seconds
    uint256 vestingDuration;       // 48 months in seconds
    uint256 startTime;              // TGE timestamp
    uint256 released;               // Total released so far
    bool paused;                    // Emergency brake status
}

function claimBaseCoins(uint256 amount) external {
    require(!baseSchedule.paused, "Vesting paused");
    require(block.timestamp >= baseSchedule.startTime, "Not started");
    
    uint256 claimable = calculateBaseClaimable(msg.sender);
    require(amount <= claimable, "Exceeds claimable");
    
    // Update state
    baseSchedule.released += amount;
    userBaseClaimed[msg.sender] += amount;
    
    // Transfer tokens
    token.transfer(msg.sender, amount);
    
    emit BaseCoinsClaimed(msg.sender, amount, block.timestamp);
}

function calculateBaseClaimable(address user) public view returns (uint256) {
    uint256 totalAllocated = userBaseAllocation[user];
    uint256 alreadyClaimed = userBaseClaimed[user];
    
    // TGE unlock (2%)
    uint256 tgeUnlock = totalAllocated * 2 / 100;
    
    // Check if still in cliff
    if (block.timestamp < baseSchedule.startTime + baseSchedule.cliffDuration) {
        return tgeUnlock - alreadyClaimed;
    }
    
    // Calculate linear vesting after cliff
    uint256 elapsed = block.timestamp - (baseSchedule.startTime + baseSchedule.cliffDuration);
    uint256 vestingProgress = (elapsed * 98) / baseSchedule.vestingDuration;
    if (vestingProgress > 98) vestingProgress = 98;
    
    uint256 totalVested = tgeUnlock + (totalAllocated * vestingProgress / 100);
    return totalVested - alreadyClaimed;
}
```

---

## Bonus Coin Vesting Schedule

| Phase | Timing | % Released | Tokens | Unlock Type |
|-------|--------|------------|--------|-------------|
| TGE | Day 0 | 0% | 0 | Locked |
| Cliff | Months 1-24 | 0% | 0 | Locked |
| Phase 1 | Months 25-36 | 5% | 1.65B | DAO vote required |
| Phase 2 | Months 37-48 | 10% | 3.3B | DAO vote required |
| Phase 3 | Months 49-60 | 15% | 4.95B | DAO vote required |
| Phase 4 | Months 61-72 | 20% | 6.6B | DAO vote required |
| Phase 5 | Months 73-84 | 25% | 8.25B | DAO vote required |
| Phase 6 | Months 85-96 | 25% | 8.25B | DAO vote required |
| **Total** | **96 months** | **100%** | **33B** | |

### DAO-Controlled Release

```solidity
struct BonusVestingPhase {
    uint256 phaseNumber;            // 1-6
    uint256 startMonth;             // Months from TGE
    uint256 percentage;             // % of total bonus coins
    uint256 totalTokens;            // Absolute token amount
    bool daoApproved;               // Requires DAO vote
    uint256 approvalTimestamp;     // When DAO approved
    uint256 released;               // Tokens released this phase
}

mapping(uint256 => BonusVestingPhase) public bonusPhases;

function releaseBonusPhase(uint256 phaseNumber) external onlyDAO {
    require(phaseNumber >= 1 && phaseNumber <= 6, "Invalid phase");
    BonusVestingPhase storage phase = bonusPhases[phaseNumber];
    
    // Check timing
    uint256 monthsSinceTGE = (block.timestamp - startTime) / 30 days;
    require(monthsSinceTGE >= phase.startMonth, "Phase not started");
    
    // Require DAO approval
    require(phase.daoApproved, "DAO approval required");
    require(!phase.paused, "Phase paused");
    
    // Calculate releaseable amount
    uint256 releaseable = phase.totalTokens - phase.released;
    
    // Update state
    phase.released = phase.totalTokens;
    bonusSchedule.released += releaseable;
    
    // Enable claims for this phase
    phase.claimable = true;
    
    emit BonusPhaseReleased(phaseNumber, releaseable, block.timestamp);
}

function approveBonusPhase(uint256 phaseNumber) external onlyDAO {
    require(phaseNumber >= 1 && phaseNumber <= 6, "Invalid phase");
    BonusVestingPhase storage phase = bonusPhases[phaseNumber];
    
    // Check milestone requirements (see DAO_TRIGGERS.md)
    require(checkMilestoneRequirements(phaseNumber), "Milestones not met");
    
    phase.daoApproved = true;
    phase.approvalTimestamp = block.timestamp;
    
    emit BonusPhaseApproved(phaseNumber, block.timestamp);
}
```

---

## Emergency Brake Mechanism

The contract includes automatic pause functionality to protect price stability:

```solidity
struct EmergencyBrake {
    bool active;
    uint256 priceThreshold;        // $0.02 in wei (6 decimals)
    uint256 liquidityThreshold;    // $10M in wei
    uint256 priceCheckDuration;    // 7 days
    uint256 lastPriceCheck;
    uint256 consecutiveLowPriceDays;
}

function checkEmergencyConditions() external {
    // Price-based brake
    uint256 currentPrice = getCurrentPrice(); // From oracle/DEX
    if (currentPrice < emergencyBrake.priceThreshold) {
        emergencyBrake.consecutiveLowPriceDays++;
        if (emergencyBrake.consecutiveLowPriceDays >= 7) {
            pauseAllVesting();
        }
    } else {
        emergencyBrake.consecutiveLowPriceDays = 0;
    }
    
    // Liquidity-based brake
    uint256 currentLiquidity = getCurrentLiquidity();
    if (currentLiquidity < emergencyBrake.liquidityThreshold) {
        pauseAllVesting();
    }
}

function pauseAllVesting() internal {
    baseSchedule.paused = true;
    for (uint256 i = 1; i <= 6; i++) {
        bonusPhases[i].paused = true;
    }
    emergencyBrake.active = true;
    
    emit VestingPaused(block.timestamp, "Emergency brake activated");
}

function resumeVesting() external onlyDAO {
    require(emergencyBrake.active, "Not paused");
    
    // Require price recovery
    uint256 currentPrice = getCurrentPrice();
    require(currentPrice >= emergencyBrake.priceThreshold * 150 / 100, "Price not recovered");
    
    baseSchedule.paused = false;
    emergencyBrake.active = false;
    emergencyBrake.consecutiveLowPriceDays = 0;
    
    emit VestingResumed(block.timestamp);
}
```

---

## Milestone-Based Accelerators

DAO can accelerate bonus releases based on network milestones:

```solidity
struct Milestone {
    string name;
    uint256 marketCapTarget;       // In USD (6 decimals)
    uint256 tvlTarget;             // In USD (6 decimals)
    uint256 walletCountTarget;     // Active wallets
    bool achieved;
    uint256 achievementTimestamp;
    uint256 bonusUnlockPercent;    // Additional % to unlock early
}

mapping(string => Milestone) public milestones;

function checkMilestone(string memory milestoneName) external {
    Milestone storage milestone = milestones[milestoneName];
    require(!milestone.achieved, "Already achieved");
    
    // Check market cap
    uint256 currentMarketCap = getMarketCap();
    bool marketCapMet = currentMarketCap >= milestone.marketCapTarget;
    
    // Check TVL
    uint256 currentTVL = getTVL();
    bool tvlMet = currentTVL >= milestone.tvlTarget;
    
    // Check wallet count
    uint256 currentWallets = getActiveWalletCount();
    bool walletsMet = currentWallets >= milestone.walletCountTarget;
    
    if (marketCapMet && tvlMet && walletsMet) {
        milestone.achieved = true;
        milestone.achievementTimestamp = block.timestamp;
        
        // Accelerate next bonus phase
        accelerateNextBonusPhase(milestone.bonusUnlockPercent);
        
        emit MilestoneAchieved(milestoneName, block.timestamp);
    }
}
```

---

## Access Control

```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";

contract VestingContract is AccessControl {
    bytes32 public constant DAO_ROLE = keccak256("DAO_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant ORACLE_ROLE = keccak256("ORACLE_ROLE");
    
    constructor(address dao, address pauser) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(DAO_ROLE, dao);
        _grantRole(PAUSER_ROLE, pauser);
    }
    
    modifier onlyDAO() {
        require(hasRole(DAO_ROLE, msg.sender), "DAO only");
        _;
    }
}
```

---

## Events

```solidity
event BaseCoinsClaimed(address indexed user, uint256 amount, uint256 timestamp);
event BonusCoinsClaimed(address indexed user, uint256 amount, uint256 phase, uint256 timestamp);
event BonusPhaseApproved(uint256 indexed phase, uint256 timestamp);
event BonusPhaseReleased(uint256 indexed phase, uint256 amount, uint256 timestamp);
event VestingPaused(uint256 timestamp, string reason);
event VestingResumed(uint256 timestamp);
event MilestoneAchieved(string milestone, uint256 timestamp);
event EmergencyBrakeActivated(uint256 timestamp, string reason);
```

---

## Security Considerations

1. **Reentrancy Protection**: Use OpenZeppelin ReentrancyGuard
2. **Integer Overflow**: Solidity 0.8.x automatic checks
3. **Access Control**: Multi-role system with timelock for DAO actions
4. **Price Oracle**: Decentralized oracle (Chainlink/RedStone) for price checks
5. **Liquidity Checks**: DEX pool balance queries for liquidity monitoring
6. **Pausability**: Emergency brake independent of DAO (can be triggered by oracle)

---

## Testing Requirements

1. **Unit Tests**:
   - TGE claim (2% base coins)
   - Cliff period enforcement
   - Linear vesting calculations
   - DAO phase approvals
   - Emergency brake triggers

2. **Integration Tests**:
   - Full vesting schedule over 60 months
   - DAO milestone accelerators
   - Price oracle integration
   - Liquidity monitoring

3. **Fuzz Tests**:
   - Claim amounts under various timestamps
   - Edge cases at phase boundaries
   - Emergency brake activation conditions

---

## Deployment Checklist

- [ ] Deploy token contract (ERC-20)
- [ ] Deploy vesting contract
- [ ] Transfer 17B base coins to vesting contract
- [ ] Transfer 33B bonus coins to vesting contract
- [ ] Set TGE timestamp
- [ ] Initialize base vesting schedule
- [ ] Initialize bonus phases (1-6)
- [ ] Configure DAO address
- [ ] Configure price oracle
- [ ] Configure liquidity monitoring
- [ ] Set emergency brake thresholds
- [ ] Grant DAO_ROLE to governance contract
- [ ] Lock admin role (renounce or transfer to timelock)

---

## Gas Optimization

- Use `unchecked` blocks for safe arithmetic after cliff periods
- Batch claims in single transaction when possible
- Cache frequently accessed storage variables
- Use events instead of storage for historical data

---

## References

- [DAO Milestone Triggers](./DAO_TRIGGERS.md)
- [Emergency Brake Logic](./EMERGENCY_BRAKE.md)
- [OpenZeppelin Vesting](https://docs.openzeppelin.com/contracts/4.x/api/finance#VestingWallet)
- [EIP-20 Token Standard](https://eips.ethereum.org/EIPS/eip-20)

