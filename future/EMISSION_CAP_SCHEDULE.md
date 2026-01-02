# Mining Emission Cap Schedule

**Status**: Implementation-Ready  
**Version**: 1.0  
**Target Launch Price**: $0.05  
**Max Monthly Emission**: 45M tokens (Month 1)

---

## Overview

To maintain $0.05 launch price with 640M circulating supply cap, mining emissions must be severely restricted initially. This document specifies the staged emission schedule that ramps from 10% to 100% over 12 months.

---

## The Emission Problem

### Unrestricted Mining Scenarios

| Miner Scenario | Daily Emission | Monthly Emission | Impact on 640M Cap |
|----------------|----------------|------------------|-------------------|
| Conservative | 3.93M/day | 118M/month | **Exceeds cap by 73M** |
| Moderate | 10.6M/day | 318M/month | **Exceeds cap by 273M** |
| Aggressive | 22.58M/day | 677M/month | **Exceeds cap by 632M** |

**Conclusion**: Full mining emissions would destroy price stability within days.

---

## Staged Emission Schedule

### Month-by-Month Breakdown

| Month | Emission Rate | Daily Cap | Monthly Cap | Cumulative Emission |
|-------|--------------|-----------|-------------|---------------------|
| 0 (TGE) | 0% | 0 | 0 | 0 |
| 1 | 10% | 1.0M | 30M | 30M |
| 2 | 10% | 1.0M | 30M | 60M |
| 3 | 25% | 2.5M | 75M | 135M |
| 4 | 25% | 2.5M | 75M | 210M |
| 5 | 25% | 2.5M | 75M | 285M |
| 6 | 50% | 5.0M | 150M | 435M |
| 7 | 50% | 5.0M | 150M | 585M |
| 8 | 50% | 5.0M | 150M | 735M |
| 9 | 75% | 7.5M | 225M | 960M |
| 10 | 75% | 7.5M | 225M | 1.185B |
| 11 | 75% | 7.5M | 225M | 1.41B |
| 12 | 100% | 10.0M | 300M | 1.71B |

**Assumption**: Moderate miner scenario (10.6M/day at 100% rate)

---

## Implementation: Per-Miner Caps

### Miner Type Emission Limits

| Miner | Base Daily Output | Month 1-2 (10%) | Month 3-5 (25%) | Month 6-8 (50%) | Month 9-11 (75%) | Month 12+ (100%) |
|-------|-------------------|-----------------|-----------------|-----------------|------------------|------------------|
| X1 | 20 BDAG | 2 BDAG | 5 BDAG | 10 BDAG | 15 BDAG | 20 BDAG |
| X10 | 200 BDAG | 20 BDAG | 50 BDAG | 100 BDAG | 150 BDAG | 200 BDAG |
| X30 | 600 BDAG | 60 BDAG | 150 BDAG | 300 BDAG | 450 BDAG | 600 BDAG |
| X100 | 2,000 BDAG | 200 BDAG | 500 BDAG | 1,000 BDAG | 1,500 BDAG | 2,000 BDAG |

### Smart Contract Implementation

```solidity
contract MiningEmissionController {
    uint256 public constant BASE_X1_DAILY = 20 * 1e18;
    uint256 public constant BASE_X10_DAILY = 200 * 1e18;
    uint256 public constant BASE_X30_DAILY = 600 * 1e18;
    uint256 public constant BASE_X100_DAILY = 2000 * 1e18;
    
    uint256 public launchTimestamp;
    uint256 public currentEmissionRate; // Basis points (10000 = 100%)
    
    enum MinerType { X1, X10, X30, X100 }
    
    mapping(address => MinerType) public minerTypes;
    mapping(address => uint256) public dailyEmissionUsed;
    mapping(uint256 => uint256) public dailyGlobalEmission; // timestamp => total emitted
    
    function getCurrentEmissionRate() public view returns (uint256) {
        uint256 monthsSinceLaunch = (block.timestamp - launchTimestamp) / 30 days;
        
        if (monthsSinceLaunch < 1) return 0;      // Month 0: 0%
        if (monthsSinceLaunch < 3) return 1000;   // Month 1-2: 10%
        if (monthsSinceLaunch < 6) return 2500;   // Month 3-5: 25%
        if (monthsSinceLaunch < 9) return 5000;   // Month 6-8: 50%
        if (monthsSinceLaunch < 12) return 7500;  // Month 9-11: 75%
        return 10000;                              // Month 12+: 100%
    }
    
    function getMinerDailyCap(address miner) public view returns (uint256) {
        MinerType mType = minerTypes[miner];
        uint256 rate = getCurrentEmissionRate();
        
        uint256 baseCap;
        if (mType == MinerType.X1) baseCap = BASE_X1_DAILY;
        else if (mType == MinerType.X10) baseCap = BASE_X10_DAILY;
        else if (mType == MinerType.X30) baseCap = BASE_X30_DAILY;
        else if (mType == MinerType.X100) baseCap = BASE_X100_DAILY;
        else revert("Invalid miner type");
        
        return (baseCap * rate) / 10000;
    }
    
    function canMine(address miner, uint256 amount) public view returns (bool) {
        uint256 dailyCap = getMinerDailyCap(miner);
        uint256 used = dailyEmissionUsed[miner];
        
        // Reset daily counter if new day
        uint256 today = block.timestamp / 1 days;
        uint256 lastUsedDay = used / 1e18; // Store day in upper bits
        if (today > lastUsedDay) {
            return amount <= dailyCap;
        }
        
        return (used + amount) <= dailyCap;
    }
    
    function recordMining(address miner, uint256 amount) external onlyMiningPool {
        require(canMine(miner, amount), "Exceeds daily cap");
        
        uint256 today = block.timestamp / 1 days;
        dailyEmissionUsed[miner] += amount;
        dailyGlobalEmission[today] += amount;
        
        // Check global daily cap
        uint256 globalCap = getGlobalDailyCap();
        require(dailyGlobalEmission[today] <= globalCap, "Global cap exceeded");
        
        emit MiningRecorded(miner, amount, block.timestamp);
    }
    
    function getGlobalDailyCap() public view returns (uint256) {
        uint256 rate = getCurrentEmissionRate();
        // Based on moderate scenario: 10.6M/day at 100%
        uint256 baseDaily = 10600000 * 1e18;
        return (baseDaily * rate) / 10000;
    }
}
```

---

## Miner Queuing System

For periods when demand exceeds caps, implement a priority queue:

### Priority Tiers

1. **Tier 1**: X100 miners (highest priority)
2. **Tier 2**: X30 miners
3. **Tier 3**: X10 miners
4. **Tier 4**: X1 miners

### Queue Implementation

```solidity
struct MinerQueue {
    address[] x100Queue;
    address[] x30Queue;
    address[] x10Queue;
    address[] x1Queue;
    mapping(address => uint256) queuePosition;
}

function addToQueue(address miner) external {
    MinerType mType = minerTypes[miner];
    
    if (mType == MinerType.X100) {
        minerQueue.x100Queue.push(miner);
        minerQueue.queuePosition[miner] = minerQueue.x100Queue.length - 1;
    }
    // ... similar for other types
}

function processQueue() external {
    // Process in priority order
    processTier(minerQueue.x100Queue, MinerType.X100);
    processTier(minerQueue.x30Queue, MinerType.X30);
    processTier(minerQueue.x10Queue, MinerType.X10);
    processTier(minerQueue.x1Queue, MinerType.X1);
}
```

---

## Difficulty Adjustment Integration

As network hashrate grows, difficulty should increase to maintain block times while respecting emission caps:

```solidity
function adjustDifficulty() external {
    uint256 targetBlockTime = 1 seconds; // BlockDAG target
    uint256 currentBlockTime = getAverageBlockTime();
    
    if (currentBlockTime < targetBlockTime) {
        // Increase difficulty
        difficultyMultiplier = (difficultyMultiplier * 110) / 100; // 10% increase
    } else if (currentBlockTime > targetBlockTime * 2) {
        // Decrease difficulty (but maintain emission caps)
        difficultyMultiplier = (difficultyMultiplier * 95) / 100; // 5% decrease
    }
    
    // Emission caps remain regardless of difficulty
    // Higher difficulty = fewer blocks = same total emissions
}
```

---

## Staking Integration

To further reduce circulating supply from mining, require staking:

```solidity
contract MiningStakingRequirement {
    uint256 public constant STAKING_REQUIREMENT_PERCENT = 50; // 50% must be staked
    
    function distributeMiningReward(address miner, uint256 amount) external {
        uint256 stakingAmount = (amount * STAKING_REQUIREMENT_PERCENT) / 100;
        uint256 immediateAmount = amount - stakingAmount;
        
        // Immediate release (50%)
        token.transfer(miner, immediateAmount);
        
        // Staked portion (50%)
        stake(miner, stakingAmount, 90 days); // 90-day lock
        
        emit MiningRewardDistributed(miner, immediateAmount, stakingAmount);
    }
}
```

---

## Monitoring & Reporting

### Daily Metrics

- Total daily emissions
- Emissions by miner type
- Queue length by tier
- Average block time
- Network hashrate

### Weekly Reports

- Cumulative emissions vs. schedule
- Price impact analysis
- Miner migration rates
- Staking participation rate

---

## Emergency Adjustments

DAO can adjust emission schedule if conditions change:

```solidity
function adjustEmissionSchedule(uint256 newRate, uint256 duration) external onlyDAO {
    require(newRate <= 10000, "Rate cannot exceed 100%");
    require(duration <= 12 weeks, "Duration too long");
    
    currentEmissionRate = newRate;
    scheduleAdjustmentEnd = block.timestamp + duration;
    
    emit EmissionScheduleAdjusted(newRate, duration, block.timestamp);
}
```

---

## Migration Considerations

### X1 Migration Barrier

The 7,500 BDAG buy-in requirement creates natural demand:

- At $0.05: $375 buy-in (moderate barrier)
- At $0.10: $750 buy-in (significant barrier)

**Recommendation**: Implement tiered migration windows:
- Early (Month 1-2): 5,000 BDAG
- Standard (Month 3-6): 7,500 BDAG
- Late (Month 7+): 10,000 BDAG

---

## References

- [Vesting Contract Spec](../contracts/VESTING_CONTRACT_SPEC.md)
- [Staking Contract Spec](../contracts/STAKING_CONTRACT_SPEC.md)
- [DAO Triggers](../contracts/DAO_TRIGGERS.md)

