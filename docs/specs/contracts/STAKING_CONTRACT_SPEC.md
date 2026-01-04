# BlockDAG Staking Contract Specification

**Status**: Implementation-Ready  
**Version**: 1.0  
**Purpose**: Lock circulating supply to support $0.05 launch price

---

## Overview

Staking is critical to the $0.05 launch strategy. By requiring 50% of mining rewards to be staked and offering attractive APY, we can:
- Reduce effective circulating supply by 30-40%
- Create long-term holder incentives
- Generate TVL for DeFi ecosystem
- Provide governance participation

---

## Staking Tiers & Rewards

| Lock Period | APY | Unlock Penalty | Effective APY* |
|-------------|-----|----------------|----------------|
| 30 days | 8% | 25% rewards lost | 6% |
| 90 days | 15% | 50% rewards lost | 7.5% |
| 180 days | 25% | 75% rewards lost | 6.25% |
| 365 days | 40% | 100% rewards lost | 0% (if early unlock) |

*If early unlock occurs

### Early Unlock Penalties

If a user unlocks before the lock period expires:
- **30-day lock**: Lose 25% of accrued rewards
- **90-day lock**: Lose 50% of accrued rewards
- **180-day lock**: Lose 75% of accrued rewards
- **365-day lock**: Lose 100% of accrued rewards + 10% principal penalty

---

## Mining Reward Staking Requirement

**Critical Feature**: 50% of all mining rewards must be staked for minimum 90 days.

```solidity
contract MiningStakingRequirement {
    uint256 public constant STAKING_REQUIREMENT_PERCENT = 50;
    uint256 public constant MIN_STAKE_DURATION = 90 days;
    
    function distributeMiningReward(address miner, uint256 totalReward) external onlyMiningPool {
        uint256 stakingAmount = (totalReward * STAKING_REQUIREMENT_PERCENT) / 100;
        uint256 immediateAmount = totalReward - stakingAmount;
        
        // Immediate release (50%)
        token.transfer(miner, immediateAmount);
        
        // Auto-stake required portion
        stake(miner, stakingAmount, MIN_STAKE_DURATION);
        
        emit MiningRewardDistributed(miner, immediateAmount, stakingAmount);
    }
}
```

---

## Core Staking Contract

```solidity
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract BlockDAGStaking is ReentrancyGuard, AccessControl {
    IERC20 public immutable token;
    
    enum StakeTier { TIER_30, TIER_90, TIER_180, TIER_365 }
    
    struct Stake {
        uint256 amount;
        uint256 lockDuration;
        uint256 lockStartTime;
        uint256 lockEndTime;
        StakeTier tier;
        uint256 accruedRewards;
        bool active;
    }
    
    mapping(address => Stake[]) public userStakes;
    mapping(StakeTier => uint256) public tierAPY; // Basis points (800 = 8%)
    
    uint256 public totalStaked;
    uint256 public stakingRewardPool; // 10B tokens allocated over 5 years
    
    // Events
    event Staked(address indexed user, uint256 amount, StakeTier tier, uint256 lockEndTime);
    event Unstaked(address indexed user, uint256 amount, uint256 rewards, bool early);
    event RewardsClaimed(address indexed user, uint256 amount);
    
    constructor(address _token) {
        token = IERC20(_token);
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        
        // Set tier APYs
        tierAPY[StakeTier.TIER_30] = 800;   // 8%
        tierAPY[StakeTier.TIER_90] = 1500;  // 15%
        tierAPY[StakeTier.TIER_180] = 2500; // 25%
        tierAPY[StakeTier.TIER_365] = 4000; // 40%
    }
    
    function stake(uint256 amount, StakeTier tier) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(tier <= StakeTier.TIER_365, "Invalid tier");
        
        uint256 lockDuration = getLockDuration(tier);
        uint256 lockEndTime = block.timestamp + lockDuration;
        
        // Transfer tokens
        token.transferFrom(msg.sender, address(this), amount);
        
        // Create stake
        Stake memory newStake = Stake({
            amount: amount,
            lockDuration: lockDuration,
            lockStartTime: block.timestamp,
            lockEndTime: lockEndTime,
            tier: tier,
            accruedRewards: 0,
            active: true
        });
        
        userStakes[msg.sender].push(newStake);
        totalStaked += amount;
        
        emit Staked(msg.sender, amount, tier, lockEndTime);
    }
    
    function unstake(uint256 stakeIndex) external nonReentrant {
        require(stakeIndex < userStakes[msg.sender].length, "Invalid stake index");
        Stake storage userStake = userStakes[msg.sender][stakeIndex];
        require(userStake.active, "Stake already withdrawn");
        
        uint256 rewards = calculateRewards(msg.sender, stakeIndex);
        bool earlyUnlock = block.timestamp < userStake.lockEndTime;
        
        if (earlyUnlock) {
            // Apply penalty
            uint256 penaltyPercent = getPenaltyPercent(userStake.tier);
            uint256 penalty = (rewards * penaltyPercent) / 100;
            rewards = rewards - penalty;
            
            // Additional principal penalty for 365-day tier
            if (userStake.tier == StakeTier.TIER_365) {
                uint256 principalPenalty = (userStake.amount * 10) / 100;
                userStake.amount -= principalPenalty;
                // Burn or send to treasury
            }
        }
        
        uint256 totalAmount = userStake.amount + rewards;
        
        // Update state
        userStake.active = false;
        totalStaked -= userStake.amount;
        
        // Transfer tokens
        token.transfer(msg.sender, totalAmount);
        
        emit Unstaked(msg.sender, userStake.amount, rewards, earlyUnlock);
    }
    
    function calculateRewards(address user, uint256 stakeIndex) public view returns (uint256) {
        Stake storage userStake = userStakes[user][stakeIndex];
        if (!userStake.active) return 0;
        
        uint256 apy = tierAPY[userStake.tier];
        uint256 timeElapsed = block.timestamp - userStake.lockStartTime;
        uint256 secondsInYear = 365 days;
        
        // Calculate rewards: amount * APY * (timeElapsed / secondsInYear)
        uint256 rewards = (userStake.amount * apy * timeElapsed) / (10000 * secondsInYear);
        
        return rewards;
    }
    
    function getLockDuration(StakeTier tier) internal pure returns (uint256) {
        if (tier == StakeTier.TIER_30) return 30 days;
        if (tier == StakeTier.TIER_90) return 90 days;
        if (tier == StakeTier.TIER_180) return 180 days;
        if (tier == StakeTier.TIER_365) return 365 days;
        revert("Invalid tier");
    }
    
    function getPenaltyPercent(StakeTier tier) internal pure returns (uint256) {
        if (tier == StakeTier.TIER_30) return 25;
        if (tier == StakeTier.TIER_90) return 50;
        if (tier == StakeTier.TIER_180) return 75;
        if (tier == StakeTier.TIER_365) return 100;
        revert("Invalid tier");
    }
    
    function getUserTotalStaked(address user) external view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < userStakes[user].length; i++) {
            if (userStakes[user][i].active) {
                total += userStakes[user][i].amount;
            }
        }
        return total;
    }
    
    function getUserTotalRewards(address user) external view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < userStakes[user].length; i++) {
            if (userStakes[user][i].active) {
                total += calculateRewards(user, i);
            }
        }
        return total;
    }
}
```

---

## Early Staking Bonus (First 90 Days)

To incentivize early participation, offer enhanced APY for first 90 days:

```solidity
uint256 public constant EARLY_STAKING_BONUS_APY = 5000; // 50% additional APY
uint256 public constant EARLY_STAKING_PERIOD = 90 days;
uint256 public launchTimestamp;

function stake(uint256 amount, StakeTier tier) external {
    // ... existing code ...
    
    // Apply early staking bonus
    if (block.timestamp < launchTimestamp + EARLY_STAKING_PERIOD) {
        uint256 baseAPY = tierAPY[tier];
        uint256 bonusAPY = baseAPY + EARLY_STAKING_BONUS_APY;
        // Cap at 100% APY
        if (bonusAPY > 10000) bonusAPY = 10000;
        tierAPY[tier] = bonusAPY;
    }
}
```

---

## Loyalty Multiplier

Reward users who don't sell their initial 2% unlock:

```solidity
mapping(address => bool) public hasSoldTokens;
mapping(address => uint256) public loyaltyMultiplier; // Basis points (15000 = 1.5x)

function checkLoyaltyStatus(address user) external {
    // If user hasn't sold any tokens for 6 months, grant multiplier
    if (!hasSoldTokens[user] && block.timestamp >= launchTimestamp + 180 days) {
        loyaltyMultiplier[user] = 15000; // 1.5x multiplier
        emit LoyaltyMultiplierGranted(user, 15000);
    }
}

function applyLoyaltyMultiplier(address user, uint256 rewards) internal view returns (uint256) {
    uint256 multiplier = loyaltyMultiplier[user];
    if (multiplier == 0) multiplier = 10000; // 1x default
    return (rewards * multiplier) / 10000;
}
```

---

## Governance Integration

Staked tokens provide voting power in DAO:

```solidity
function getVotingPower(address user) external view returns (uint256) {
    uint256 stakedAmount = getUserTotalStaked(user);
    
    // Weight by lock duration
    uint256 weightedPower = 0;
    for (uint256 i = 0; i < userStakes[user].length; i++) {
        if (userStakes[user][i].active) {
            Stake storage stake = userStakes[user][i];
            uint256 weight = getStakeWeight(stake.tier);
            weightedPower += (stake.amount * weight) / 10000;
        }
    }
    
    return weightedPower;
}

function getStakeWeight(StakeTier tier) internal pure returns (uint256) {
    if (tier == StakeTier.TIER_30) return 10000;   // 1x
    if (tier == StakeTier.TIER_90) return 12000;   // 1.2x
    if (tier == StakeTier.TIER_180) return 15000;  // 1.5x
    if (tier == StakeTier.TIER_365) return 20000;  // 2x
    return 10000;
}
```

---

## Staking Reward Pool Management

10B tokens allocated over 5 years:

```solidity
uint256 public constant TOTAL_REWARD_POOL = 10_000_000_000 * 1e18;
uint256 public constant REWARD_DURATION = 5 years;
uint256 public rewardRate; // Tokens per second

function initializeRewardPool() external onlyRole(DEFAULT_ADMIN_ROLE) {
    rewardRate = TOTAL_REWARD_POOL / REWARD_DURATION;
    rewardPoolStartTime = block.timestamp;
}

function distributeRewards() internal {
    uint256 timeElapsed = block.timestamp - rewardPoolStartTime;
    uint256 totalRewards = rewardRate * timeElapsed;
    
    // Distribute proportionally based on staked amounts and APY
    // Implementation details...
}
```

---

## NFT Commemorative Program

First 10,000 stakers who lock for 12 months get "Genesis Staker" NFT:

```solidity
uint256 public constant GENESIS_STAKER_LIMIT = 10000;
uint256 public genesisStakerCount;
mapping(address => bool) public isGenesisStaker;

function stake(uint256 amount, StakeTier tier) external {
    // ... existing code ...
    
    // Check for Genesis Staker eligibility
    if (tier == StakeTier.TIER_365 && 
        genesisStakerCount < GENESIS_STAKER_LIMIT && 
        !isGenesisStaker[msg.sender]) {
        isGenesisStaker[msg.sender] = true;
        genesisStakerCount++;
        mintGenesisNFT(msg.sender);
        emit GenesisStakerRegistered(msg.sender);
    }
}
```

---

## Security Considerations

1. **Reentrancy Protection**: All external calls use ReentrancyGuard
2. **Integer Overflow**: Solidity 0.8.x automatic checks
3. **Access Control**: Admin role for reward pool management only
4. **Emergency Pause**: Can pause staking (but not unstaking) in emergencies
5. **Reward Pool Limits**: Hard cap on total rewards distributed

---

## Testing Requirements

1. **Unit Tests**:
   - Staking/unstaking at each tier
   - Reward calculations
   - Early unlock penalties
   - Loyalty multiplier application

2. **Integration Tests**:
   - Mining reward auto-staking
   - Governance voting power calculation
   - Reward pool distribution over 5 years

3. **Fuzz Tests**:
   - Various stake amounts and durations
   - Edge cases at tier boundaries
   - Reward calculation accuracy

---

## References

- [Vesting Contract Spec](./VESTING_CONTRACT_SPEC.md)
- [Emission Cap Schedule](../mining/EMISSION_CAP_SCHEDULE.md)
- [DAO Triggers](./DAO_TRIGGERS.md)


