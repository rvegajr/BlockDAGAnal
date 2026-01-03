# Liquidity Tier Analysis v2 (Including Protocol 3.0)

**Date**: January 2026  
**Runs**: 100 per (model × liquidity × scenario) = **20,000 simulations**  
**Script**: `scripts/liquidity_tier_comparison_v2_four_models.py`  
**Raw results**: `liquidity_tier_comparison_v2_results.json`

**Protocol 3.0 Source**: [Official Launch Protocol v3.0 (Hybrid Optimized)](https://a-changer-plus-tard.github.io/Protocol-3.0/)

---

## What Changed vs v1

- Added **Protocol v3.0**
- Added **Monte Carlo noise** (±2% monthly liquidity drift) on top of the 10 historical crash events, so “100 simulations” aren’t identical repeats.

---

## Winners by Liquidity Tier (Month-12 Value, $9k Reference)

| Liquidity | Winner | Avg Month-12 Value | Notes |
|----------:|--------|-------------------:|------|
| **$32M** | **Hybrid Model** | ~$1,772 | Protection helps at low liquidity |
| **$50M** | **Hybrid Model** | ~$2,916 | Protection still dominates |
| **$75M** | **Hybrid Model** | ~$3,922 | Protection still dominates |
| **$100M** | **Protocol v3.0** | ~$5,971 | Gate + drip becomes dominant |
| **$150M** | **Protocol v3.0** | ~$9,071 | Highest value + survivability |

---

## “Optimal Fair Liquidity” (within tested tiers)

The top-ranked fairness configuration was:

- **$150M + Protocol v3.0**
  - Avg Month-12 ROI: **+0.79%**
  - Avg Month-12 Value: **$9,070.81**
  - Survival rate (no breach below $0.02): **100%**
  - Fairness score: **80.2/100**

---

## Key Interpretation

- **Below ~$100M liquidity**, crash-resilience mechanisms dominate outcomes → **Hybrid Model tends to win**.
- **At ~$100M+ liquidity**, the combined **oracle gate + emergency brake + controlled drip** structure in **Protocol 3.0** dominates outcomes.


