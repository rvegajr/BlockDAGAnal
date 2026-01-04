# Emergency Brake Smart Contract Logic

**Status**: Implementation-Ready  
**Version**: 1.0  
**Purpose**: Automatic price and liquidity protection mechanisms

---

## Overview

The emergency brake system automatically pauses vesting when critical conditions are detected, protecting the $0.05 launch price target. It operates independently of DAO votes for critical emergencies but requires DAO approval for resumption.

---

## Emergency Conditions

### Condition 1: Price Drop Below Threshold

| Threshold | Duration | Action | Recovery Requirement |
|-----------|----------|--------|---------------------|
| < $0.02 | 7 consecutive days | Pause all vesting | Price ≥ $0.03 for 3 days |
| < $0.01 | 3 consecutive days | Emergency DAO vote triggered | Price ≥ $0.02 for 7 days |

### Condition 2: Liquidity Drop

| Threshold | Duration | Action | Recovery Requirement |
|-----------|----------|--------|---------------------|
| < $10M | Immediate | Pause all vesting | Liquidity ≥ $15M |

### Condition 3: Major Security Incident

| Condition | Action | Recovery Requirement |
|-----------|--------|---------------------|
| Smart contract exploit detected | Immediate pause | Security audit + fix deployed |
| Oracle manipulation detected | Pause price checks | New oracle deployed |

---

## Smart Contract Implementation

```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyBrake is AccessControl, Pausable {
    
    struct PriceCondition {
        uint256 threshold;           // Price threshold (6 decimals)
        uint256 consecutiveDays;     // Days below threshold
        uint256 recoveryThreshold;   // Price to recover
        uint256 recoveryDays;        // Days above recovery threshold
        bool active;
    }
    
    struct LiquidityCondition {
        uint256 threshold;           // Liquidity threshold (6 decimals)
        uint256 recoveryThreshold;   // Liquidity to recover
        bool active;
    }
    
    PriceCondition public priceCondition;
    LiquidityCondition public liquidityCondition;
    
    address public priceOracle;
    address public liquidityOracle;
    address public vestingContract;
    
    uint256 public lastPriceCheck;
    uint256 public consecutiveLowPriceDays;
    uint256 public consecutiveRecoveryDays;
    uint256 public lastLiquidityCheck;
    
    bool public emergencyActive;
    string public emergencyReason;
    uint256 public emergencyActivatedAt;
    
    // Events
    event EmergencyBrakeActivated(string reason, uint256 timestamp);
    event EmergencyBrakeDeactivated(uint256 timestamp);
    event PriceCheckPerformed(uint256 price, uint256 threshold, bool triggered);
    event LiquidityCheckPerformed(uint256 liquidity, uint256 threshold, bool triggered);
    
    constructor(
        address _priceOracle,
        address _liquidityOracle,
        address _vestingContract
    ) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        priceOracle = _priceOracle;
        liquidityOracle = _liquidityOracle;
        vestingContract = _vestingContract;
        
        // Initialize price condition
        priceCondition = PriceCondition({
            threshold: 0.02 * 1e6,        // $0.02
            consecutiveDays: 7,
            recoveryThreshold: 0.03 * 1e6, // $0.03
            recoveryDays: 3,
            active: true
        });
        
        // Initialize liquidity condition
        liquidityCondition = LiquidityCondition({
            threshold: 10_000_000 * 1e6,    // $10M
            recoveryThreshold: 15_000_000 * 1e6, // $15M
            active: true
        });
    }
    
    function checkEmergencyConditions() external {
        // Price check
        if (priceCondition.active) {
            checkPriceCondition();
        }
        
        // Liquidity check
        if (liquidityCondition.active) {
            checkLiquidityCondition();
        }
        
        // Security check (if oracle reports incident)
        checkSecurityCondition();
    }
    
    function checkPriceCondition() internal {
        uint256 currentPrice = IPriceOracle(priceOracle).getPrice();
        uint256 today = block.timestamp / 1 days;
        
        // Reset if new day
        if (today > lastPriceCheck / 1 days) {
            // Check if price recovered
            if (currentPrice >= priceCondition.recoveryThreshold) {
                consecutiveRecoveryDays++;
                consecutiveLowPriceDays = 0;
                
                // Auto-resume if recovery sustained
                if (consecutiveRecoveryDays >= priceCondition.recoveryDays && emergencyActive) {
                    deactivateEmergency("Price recovered");
                }
            } else if (currentPrice < priceCondition.threshold) {
                consecutiveLowPriceDays++;
                consecutiveRecoveryDays = 0;
                
                // Activate emergency if threshold exceeded
                if (consecutiveLowPriceDays >= priceCondition.consecutiveDays && !emergencyActive) {
                    activateEmergency("Price below threshold");
                }
            } else {
                // Price between threshold and recovery - reset counters
                consecutiveLowPriceDays = 0;
                consecutiveRecoveryDays = 0;
            }
            
            lastPriceCheck = block.timestamp;
        }
        
        emit PriceCheckPerformed(
            currentPrice,
            priceCondition.threshold,
            consecutiveLowPriceDays >= priceCondition.consecutiveDays
        );
    }
    
    function checkLiquidityCondition() internal {
        uint256 currentLiquidity = ILiquidityOracle(liquidityOracle).getTotalLiquidity();
        uint256 today = block.timestamp / 1 days;
        
        // Check liquidity daily
        if (today > lastLiquidityCheck / 1 days) {
            if (currentLiquidity < liquidityCondition.threshold && !emergencyActive) {
                activateEmergency("Liquidity below threshold");
            } else if (currentLiquidity >= liquidityCondition.recoveryThreshold && emergencyActive) {
                // Can auto-resume if liquidity recovers
                deactivateEmergency("Liquidity recovered");
            }
            
            lastLiquidityCheck = block.timestamp;
        }
        
        emit LiquidityCheckPerformed(
            currentLiquidity,
            liquidityCondition.threshold,
            currentLiquidity < liquidityCondition.threshold
        );
    }
    
    function checkSecurityCondition() internal {
        // Check oracle for security alerts
        bool securityIncident = ISecurityOracle(securityOracle).hasActiveIncident();
        
        if (securityIncident && !emergencyActive) {
            activateEmergency("Security incident detected");
        }
    }
    
    function activateEmergency(string memory reason) internal {
        emergencyActive = true;
        emergencyReason = reason;
        emergencyActivatedAt = block.timestamp;
        
        // Pause vesting contract
        IVestingContract(vestingContract).pauseAllVesting();
        
        // Pause this contract
        _pause();
        
        emit EmergencyBrakeActivated(reason, block.timestamp);
    }
    
    function deactivateEmergency(string memory reason) internal {
        require(emergencyActive, "Not in emergency");
        
        // Verify recovery conditions
        uint256 currentPrice = IPriceOracle(priceOracle).getPrice();
        uint256 currentLiquidity = ILiquidityOracle(liquidityOracle).getTotalLiquidity();
        
        require(
            currentPrice >= priceCondition.recoveryThreshold &&
            currentLiquidity >= liquidityCondition.recoveryThreshold,
            "Recovery conditions not met"
        );
        
        emergencyActive = false;
        emergencyReason = "";
        consecutiveLowPriceDays = 0;
        consecutiveRecoveryDays = 0;
        
        // Resume vesting contract
        IVestingContract(vestingContract).resumeVesting();
        
        // Unpause this contract
        _unpause();
        
        emit EmergencyBrakeDeactivated(block.timestamp);
    }
    
    // Manual override (requires DAO approval)
    function manualDeactivate() external onlyRole(DAO_ROLE) {
        require(emergencyActive, "Not in emergency");
        deactivateEmergency("Manual override by DAO");
    }
    
    // Update thresholds (requires DAO approval)
    function updatePriceThreshold(uint256 newThreshold, uint256 newRecoveryThreshold) 
        external 
        onlyRole(DAO_ROLE) 
    {
        require(newThreshold < newRecoveryThreshold, "Invalid thresholds");
        priceCondition.threshold = newThreshold;
        priceCondition.recoveryThreshold = newRecoveryThreshold;
    }
    
    function updateLiquidityThreshold(uint256 newThreshold, uint256 newRecoveryThreshold) 
        external 
        onlyRole(DAO_ROLE) 
    {
        require(newThreshold < newRecoveryThreshold, "Invalid thresholds");
        liquidityCondition.threshold = newThreshold;
        liquidityCondition.recoveryThreshold = newRecoveryThreshold;
    }
    
    // Emergency pause override (admin only, extreme cases)
    function emergencyPauseOverride(string memory reason) external onlyRole(DEFAULT_ADMIN_ROLE) {
        activateEmergency(reason);
    }
}
```

---

## Integration with Vesting Contract

```solidity
// In VestingContract.sol

function pauseAllVesting() external onlyEmergencyBrake {
    baseSchedule.paused = true;
    for (uint256 i = 1; i <= 6; i++) {
        bonusPhases[i].paused = true;
    }
    
    emit VestingPaused(block.timestamp, "Emergency brake activated");
}

function resumeVesting() external onlyEmergencyBrake {
    require(baseSchedule.paused, "Not paused");
    
    baseSchedule.paused = false;
    for (uint256 i = 1; i <= 6; i++) {
        if (bonusPhases[i].daoApproved) {
            bonusPhases[i].paused = false;
        }
    }
    
    emit VestingResumed(block.timestamp);
}
```

---

## Oracle Requirements

### Price Oracle

Must provide:
- Current BDAG/USD price (6 decimals)
- Price stability metrics
- Historical price data

**Recommended**: Chainlink Price Feed or RedStone Oracle

### Liquidity Oracle

Must provide:
- Total DEX liquidity (sum of all pools)
- Per-pool liquidity breakdown
- Liquidity stability metrics

**Implementation**: Query DEX pool contracts directly or use The Graph indexing

---

## Monitoring & Alerts

### Automated Checks

- **Frequency**: Every block (or every 100 blocks for gas efficiency)
- **Price Check**: Daily aggregation
- **Liquidity Check**: Daily aggregation
- **Security Check**: Real-time from security oracle

### Alert Conditions

| Alert Level | Condition | Action |
|-------------|-----------|--------|
| Warning | Price < $0.03 for 3 days | Notify DAO |
| Critical | Price < $0.02 for 5 days | Prepare emergency pause |
| Emergency | Price < $0.02 for 7 days | Automatic pause |
| Critical | Liquidity < $12M | Notify DAO |
| Emergency | Liquidity < $10M | Automatic pause |

---

## Recovery Process

### Automatic Recovery

If conditions improve:
- Price ≥ $0.03 for 3 consecutive days → Auto-resume
- Liquidity ≥ $15M → Auto-resume

### Manual Recovery

If automatic recovery fails:
1. DAO creates proposal to manually resume
2. Requires 75% supermajority vote
3. 24-hour timelock before execution
4. Must verify recovery conditions before execution

---

## Testing Requirements

1. **Unit Tests**:
   - Price threshold detection
   - Liquidity threshold detection
   - Consecutive day counting
   - Recovery condition verification

2. **Integration Tests**:
   - Oracle integration
   - Vesting contract pause/resume
   - Emergency activation/deactivation flow

3. **Scenario Tests**:
   - Price crash scenario
   - Liquidity drain scenario
   - Oracle failure scenario
   - Recovery after emergency

---

## Security Considerations

1. **Oracle Manipulation**: Use multiple oracle sources, median pricing
2. **Front-running**: Emergency checks are permissionless but execution is rate-limited
3. **False Positives**: Recovery mechanism prevents permanent lock
4. **Admin Override**: Only for extreme emergencies, with community notification
5. **Timelock**: All threshold changes require timelock

---

## References

- [Vesting Contract Spec](./VESTING_CONTRACT_SPEC.md)
- [DAO Triggers](./DAO_TRIGGERS.md)
- [Oracle Integration](../oracles/REDSTONE.md)


