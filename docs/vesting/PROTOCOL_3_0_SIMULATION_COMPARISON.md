# Protocol 3.0 (Hybrid Optimized) — Simulations & Comparison

**Date**: January 2026  
**Scope**: Adds “Protocol 3.0” to our prior comparisons and re-runs:
- **100 simulations** per model under bull/bear/normal/volatile conditions
- **100 simulations per (model × liquidity tier × historical scenario)** across the **10 historical market events**

**Protocol 3.0 Source**: [Official Launch Protocol v3.0 (Hybrid Optimized)](https://a-changer-plus-tard.github.io/Protocol-3.0/)

---

## Key Parameters We Modeled (Protocol 3.0)

From the Protocol 3.0 page:
- **TGE**: 3%
- **Cliff**: 3 months
- **Vesting**: Month 4–36 (modeled as **33 months** for remaining 97%)
- **Oracle gate**: Vesting only proceeds if price stays above **$0.05**
- **Emergency brake**: If price falls below **$0.02**, vesting pauses immediately
- **Mining emission cap**: **20%**
- **“Miners locked for 2 years”**: Modeled as mining emissions excluded from circulating for 24 months (doesn’t affect month 0–12 price in our model, but included for correctness)
- **Volume pegging**: “2% of 24h trading volume” drip modeled as a **reduced vesting rate** when \(0.02 \le price < 0.05\) (approximation)

---

## Results A: Moderate Market Conditions (400 sims total)

Script: `scripts/four_model_comparison.py`  
Raw data: `four_model_comparison_results.json`

**Month 12 ROI (Average)**
- **Protocol v3.0**: **-49.8%**
- **Protocol v2.6**: -77.9%
- **Hybrid Model**: -84.9%
- **Original Model**: -95.7%

**Interpretation**: In moderate conditions, Protocol 3.0’s “gate + brake + drip” structure meaningfully improves investor outcomes versus v2.6 and our earlier models.

---

## Results B: 10 Historical Market Events × Liquidity Tiers (20,000 sims total)

Script: `scripts/liquidity_tier_comparison_v2_four_models.py`  
Raw data: `liquidity_tier_comparison_v2_results.json`

### Winners by Liquidity Tier (Month-12 Value on $9k reference)

- **$32M**: **Hybrid Model** wins (avg month-12 value ≈ $1,772)
- **$50M**: **Hybrid Model** wins (avg month-12 value ≈ $2,916)
- **$75M**: **Hybrid Model** wins (avg month-12 value ≈ $3,922)
- **$100M**: **Protocol v3.0** wins (avg month-12 value ≈ $5,971)
- **$150M**: **Protocol v3.0** wins (avg month-12 value ≈ $9,071)

### “Optimal Fair Liquidity” (within tiers tested)

Using the same fairness scoring approach (ROI + survival + value), the best configuration in the tested tiers is:

- **$150M liquidity + Protocol v3.0**
  - **Avg month-12 ROI**: **+0.79%**
  - **Avg month-12 value**: **$9,070.81**
  - **Survival rate (no price-floor breach)**: **100%**
  - **Fairness score**: **80.2/100**

---

## Why Protocol 3.0 “Wins” (When It Does)

Protocol 3.0 combines the strongest parts of v2.6 and our protective modeling:
- **Oracle price gate at $0.05** (prevents aggressive vesting when price is weak)
- **Emergency brake at $0.02** (hard floor protection)
- **Drip/volume pegging** (controlled release rather than “all-or-nothing” gating)
- **Emission cap** (reduces inflation pressure compared to uncapped assumptions)

This combination performs especially well once liquidity is large enough that price is less fragile under shocks.

---

## Files

- **Protocol 3.0 analysis doc**: `docs/vesting/PROTOCOL_3_0_SIMULATION_COMPARISON.md` (this file)
- **Moderate markets**:
  - Script: `scripts/four_model_comparison.py`
  - Results: `four_model_comparison_results.json`
- **Historical events + liquidity tiers**:
  - Script: `scripts/liquidity_tier_comparison_v2_four_models.py`
  - Results: `liquidity_tier_comparison_v2_results.json`


