# How BlockDAG Reaches $0.03: Based on Raw Specifications

## Executive Summary

**Based on the official BlockDAG specifications (not models), $0.03 is the recovery threshold for the emergency brake system. When price drops below $0.02 and triggers the emergency brake, it must recover to $0.03 and sustain it for 3 days before vesting can resume.**

---

## Source: Emergency Brake Specification

**File:** `docs/specs/contracts/EMERGENCY_BRAKE.md`  
**Lines:** 21, 97

### The Official Mechanism

| Threshold | Duration | Action | Recovery Requirement |
|-----------|----------|--------|---------------------|
| **< $0.02** | 7 consecutive days | **Pause all vesting** | **Price ≥ $0.03 for 3 days** |

---

## How $0.03 Works (From Raw Specs)

### Step 1: Emergency Brake Activation

**From EMERGENCY_BRAKE.md (Line 95-100):**

```solidity
priceCondition = PriceCondition({
    threshold: 0.02 * 1e6,        // $0.02 - activation threshold
    consecutiveDays: 7,
    recoveryThreshold: 0.03 * 1e6, // $0.03 - recovery threshold
    recoveryDays: 3,
    active: true
});
```

**What happens:**
- Price drops below $0.02
- Stays below $0.02 for 7 consecutive days
- Emergency brake activates automatically
- **All vesting pauses** (base coins, bonus coins, team, management, founders)

---

### Step 2: Recovery Requirement

**From EMERGENCY_BRAKE.md (Line 132-139):**

```solidity
// Check if price recovered
if (currentPrice >= priceCondition.recoveryThreshold) {
    consecutiveRecoveryDays++;
    consecutiveLowPriceDays = 0;
    
    // Auto-resume if recovery sustained
    if (consecutiveRecoveryDays >= priceCondition.recoveryDays && emergencyActive) {
        deactivateEmergency("Price recovered");
    }
}
```

**What happens:**
- Price must reach **$0.03 or higher**
- Must stay at **$0.03+ for 3 consecutive days**
- Only then can vesting resume automatically

---

## Why $0.03? (Design Rationale)

### Price Structure from Specs

| Price Level | Purpose | Source |
|-------------|---------|--------|
| **$0.05** | Target launch price | VESTING_CONTRACT_SPEC.md Line 5 |
| **$0.03** | Recovery threshold | EMERGENCY_BRAKE.md Line 97 |
| **$0.02** | Emergency brake trigger | EMERGENCY_BRAKE.md Line 95 |
| **$0.01** | Presale price | Not in specs, but referenced in models |

### The Logic

**$0.03 = 60% of target price ($0.05)**
- Recovery threshold is set at 60% of launch price
- Provides buffer above emergency trigger ($0.02)
- Ensures meaningful recovery before resuming vesting

**$0.02 = 40% of target price ($0.05)**
- Emergency brake triggers at 40% drop
- Protects against catastrophic price collapse
- Gives time for market to stabilize

---

## The Complete Flow (From Specs)

### Normal Operation

```
Price: $0.05 (target)
Status: Vesting active
Action: Normal vesting continues
```

### Price Decline

```
Price: $0.05 → $0.04 → $0.03 → $0.02
Status: Vesting active (no brake yet)
Action: Monitoring price daily
```

### Emergency Brake Activation

```
Price: < $0.02 for 7 consecutive days
Status: Emergency brake ACTIVATED
Action: ALL vesting paused automatically
Source: EMERGENCY_BRAKE.md Line 145-147
```

### Recovery Process

```
Price: $0.02 → $0.03
Status: Emergency brake ACTIVE
Action: Counting recovery days
Requirement: Price ≥ $0.03 for 3 consecutive days
Source: EMERGENCY_BRAKE.md Line 132-139
```

### Auto-Resume

```
Price: ≥ $0.03 for 3 consecutive days
Status: Emergency brake DEACTIVATED
Action: Vesting resumes automatically
Source: EMERGENCY_BRAKE.md Line 137-139
```

---

## Alert System (From Specs)

**From EMERGENCY_BRAKE.md (Line 336-340):**

| Alert Level | Condition | Action |
|-------------|-----------|--------|
| **Warning** | Price < $0.03 for 3 days | Notify DAO |
| **Critical** | Price < $0.02 for 5 days | Prepare emergency pause |
| **Emergency** | Price < $0.02 for 7 days | Automatic pause |

**Key Point:** $0.03 is the **warning threshold** - DAO gets notified if price stays below $0.03 for 3 days, even before emergency brake activates.

---

## Manual Recovery (From Specs)

**From EMERGENCY_BRAKE.md (Line 238-241):**

```solidity
function manualDeactivate() external onlyRole(DAO_ROLE) {
    require(emergencyActive, "Not in emergency");
    deactivateEmergency("Manual override by DAO");
}
```

**What this means:**
- DAO can manually resume vesting
- But still requires recovery conditions:
  - Price ≥ $0.03
  - Liquidity ≥ $15M
- Source: EMERGENCY_BRAKE.md Line 217-221

---

## Oracle Requirements (From Specs)

**From EMERGENCY_BRAKE.md (Line 303-310):**

### Price Oracle Must Provide:
- Current BDAG/USD price (6 decimals)
- Price stability metrics
- Historical price data

**Recommended:** Chainlink Price Feed or RedStone Oracle

**How $0.03 is checked:**
```solidity
uint256 currentPrice = IPriceOracle(priceOracle).getPrice();
if (currentPrice >= priceCondition.recoveryThreshold) {
    // $0.03 threshold met
}
```

---

## Comparison: Specs vs Models

| Aspect | Raw Specs | Models (Your Simulations) |
|--------|-----------|--------------------------|
| **$0.03 Purpose** | Recovery threshold | Buyback trigger |
| **$0.03 Source** | EMERGENCY_BRAKE.md | ADDRESSING_LIQUIDITY_CONCERNS.md |
| **Mechanism** | Auto-resume vesting | Treasury buyback |
| **Duration** | 3 days sustained | 14 days sustained |

**Key Difference:**
- **Specs say:** $0.03 is recovery threshold for emergency brake
- **Models say:** $0.03 is buyback trigger for treasury intervention

**Both can coexist:**
- Emergency brake recovery at $0.03 (from specs)
- Buyback fund activation at $0.03 (from models)
- Two different mechanisms, same threshold

---

## How Price Gets to $0.03 (Market Dynamics)

### From Launch Price ($0.05)

**Specs don't define HOW price moves, but they define WHEN mechanisms activate:**

1. **Normal Market:** Price stays above $0.03
   - No emergency brake
   - Vesting continues normally
   - No intervention needed

2. **Price Decline:** Price drops to $0.03
   - Warning alert to DAO (3 days below $0.03)
   - Emergency brake NOT activated yet
   - Vesting continues (still above $0.02)

3. **Further Decline:** Price drops below $0.02
   - Emergency brake activates (after 7 days)
   - All vesting pauses
   - Price must recover to $0.03 to resume

---

## The Recovery Requirement (Detailed)

**From EMERGENCY_BRAKE.md (Line 217-221):**

```solidity
require(
    currentPrice >= priceCondition.recoveryThreshold &&
    currentLiquidity >= liquidityCondition.recoveryThreshold,
    "Recovery conditions not met"
);
```

**Both conditions must be met:**
1. Price ≥ $0.03 (recovery threshold)
2. Liquidity ≥ $15M (recovery threshold)

**Duration:** 3 consecutive days

**Then:** Vesting resumes automatically

---

## Summary: $0.03 from Raw Specs

### What $0.03 Is:

1. **Recovery Threshold**
   - Price that must be reached to deactivate emergency brake
   - Set at 60% of target launch price ($0.05)

2. **Warning Threshold**
   - DAO gets notified if price stays below $0.03 for 3 days
   - Early warning before emergency brake activates

3. **Auto-Resume Condition**
   - After emergency brake activates, price must reach $0.03
   - Must sustain for 3 consecutive days
   - Then vesting resumes automatically

### What $0.03 Is NOT (In Raw Specs):

- ❌ Not a buyback trigger (that's in models, not specs)
- ❌ Not a launch price (launch is $0.05)
- ❌ Not an emergency brake trigger (that's $0.02)

---

## Key Takeaways

**From the official BlockDAG specifications:**

1. ✅ **$0.05** = Target launch price (VESTING_CONTRACT_SPEC.md)
2. ✅ **$0.03** = Recovery threshold for emergency brake (EMERGENCY_BRAKE.md)
3. ✅ **$0.02** = Emergency brake activation threshold (EMERGENCY_BRAKE.md)

**The mechanism:**
- Price drops below $0.02 → Emergency brake activates
- Price recovers to $0.03 → Recovery process begins
- Price stays at $0.03+ for 3 days → Vesting resumes

**$0.03 is the recovery gate, not a buyback trigger (in the raw specs).**

---

*Document Version: 1.0*  
*Based On: Raw BlockDAG Specifications*  
*Source Files:*
- `docs/specs/contracts/EMERGENCY_BRAKE.md`
- `docs/specs/contracts/VESTING_CONTRACT_SPEC.md`
- `docs/specs/contracts/DAO_TRIGGERS.md`

