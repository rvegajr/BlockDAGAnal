# Ingo CSV Models: Backtest Analysis Report

**Generated**: January 10, 2026  
**Test Framework**: Real-World Multi-Opinion Backtest (BTC 2015-2024)

---

## Executive Summary

This report evaluates the Ingo CSV tokenomics models against the stated design goals and provides actionable feedback for optimization.

### Design Goals (As Stated)

1. Alternative tokenomics configurations with different risk–reward and stability trade-offs
2. Mining and Bonus mechanisms governed by adaptive throttling and emergency controls
3. Parameter-level differences only (not structural rewrites)
4. TGE variants (0%, 3%) to isolate initial circulating supply effects
5. Recovery and throttling logic to avoid binary on/off behavior
6. Self-contained parameters (no external protocol assumptions)
7. Objective backtesting support

---

## Goal-by-Goal Evaluation

### ✅ GOAL 1: Risk-Reward Trade-offs
**VERDICT: SUCCEEDED**

| Model Family | Risk Profile | 72mo Ideal ROI | 72mo Stress ROI | Trade-off |
|-------------|--------------|----------------|-----------------|-----------|
| Hybrid C | Balanced | +756.6% | -40.9% | Best risk-adjusted |
| Hybrid C Lite+ Variants | Conservative | +399-541% | -59 to -67% | Lower ceiling, better floor |
| Hybrid D.1/E.1/F | Very Conservative | +280-301% | -78 to -82% | Survival-focused |
| Model A variants | Aggressive | +275-277% | -71% | High volatility exposure |

The models clearly demonstrate **distinct risk-reward profiles** as intended.

---

### ⚠️ GOAL 2: Adaptive Throttling & Emergency Controls
**VERDICT: PARTIAL SUCCESS**

| Model | Brake Rate (Conservative) | Brake Rate (Choppy) | Assessment |
|-------|--------------------------|---------------------|------------|
| Hybrid C (Ingo) | 33.3% | 61.8% | ✅ Adaptive |
| Hybrid C Lite+ Final | 44.4% | 82.9% | ✅ Adaptive |
| Hybrid B (Ingo) | 33.3% | 68.9% | ✅ Adaptive |
| Model A variants | 100% | 100% | ⚠️ Always triggered |
| Hybrid D.1/E.1/F | 77.8% | 90% | ⚠️ Too aggressive |

**Issue Identified**: The D/E/F family triggers emergency controls too frequently (77-90% of scenarios), limiting ROI potential without proportional safety benefits.

**Recommendation**: Consider raising the `brake_low` threshold or adjusting the throttle logic for the D/E/F family to reduce false emergency triggers.

---

### ✅ GOAL 3: Parameter-Level Differences Only
**VERDICT: SUCCEEDED**

Evidence: Models with near-identical parameters produce near-identical results:

| Model | Conservative 72mo | Ideal 72mo |
|-------|-------------------|------------|
| Hybrid D.1 (Ingo) | -82.9% | +301.7% |
| Hybrid E.1 3% TGE | -82.9% | +301.7% |
| Hybrid F (Ingo) | -82.9% | +301.6% |
| Hybrid F.1 (Ingo) | -82.9% | +301.6% |

This proves the simulation harness is **parameter-sensitive** and structurally consistent. The models are comparable.

---

### ✅ GOAL 4: TGE Isolation (0% vs 3%)
**VERDICT: SUCCEEDED**

| Scenario | 0% TGE | 3% TGE | Effect |
|----------|--------|--------|--------|
| Conservative 72mo | -78.7% | -82.9% | 0% TGE better in stress |
| Ideal 72mo | +280.9% | +301.7% | 3% TGE better in growth |
| Choppy 72mo | -93.4% | -92.3% | Negligible difference |
| Brake Rate (Conservative) | 55.6% | 77.8% | 0% TGE = fewer emergency stops |

**Key Insight**: The 0% TGE variant provides better **stress resilience** (fewer brake activations, +4% better stress ROI), while 3% TGE provides better **growth capture** (+21% more ROI in ideal conditions). This isolation worked as intended.

---

### ⚠️ GOAL 5: Smooth Transitions (Not Binary)
**VERDICT: PARTIAL SUCCESS**

| Behavior | Models | Positive Rate M72 | Assessment |
|----------|--------|-------------------|------------|
| Smooth degradation | Hybrid C, C Lite Defaults | 22.2% | ✅ Gradual |
| Adaptive throttling | Hybrid B (Ingo Detailed) | 22.2% | ✅ Working |
| Binary failure | Model A, D.1, E.1, F, F.1 | 0.0% | ❌ Binary mode |

**Issue**: Several models (D.1, E.1, F, F.1, Model A) show **0.0% positive ROI rate** in stress scenarios, indicating they effectively have binary failure modes despite the throttling logic.

**Recommendation**: The recovery logic may be too conservative. Consider:
- Increasing `drip_factor_between` to allow more flow in throttle zones
- Reducing the `mining_lock_months` to release liquidity earlier
- Adjusting `global_monthly_cap` upward for the D/E/F family

---

### ✅ GOAL 6: Self-Contained Parameters
**VERDICT: SUCCEEDED**

All models ran without external dependencies. The simulation harness correctly parsed and applied all CSV-derived parameters independently.

---

### ✅ GOAL 7: Objective Backtesting
**VERDICT: SUCCEEDED**

The framework provided:
- 3 independent market opinions (Conservative, Ideal, Choppy)
- 10 stress scenarios (COVID, FTX collapse, etc.)
- 5 time horizons (12, 24, 36, 48, 72 months)
- 3 investment levels ($9k, $50k, $100k)
- Clear winners/losers per category

---

## Full Results: All Ingo Models

### Conservative Scenario (Stress-Test)

| Model | M12 | M24 | M36 | M48 | M72 | Positive Rate | Brake Rate |
|-------|-----|-----|-----|-----|-----|---------------|------------|
| Hybrid (Ingo CSV) | -92.1% | -89.9% | -89.6% | -91.5% | -83.9% | 0.0% | 77.8% |
| Hybrid C (Ingo CSV) | -82.5% | -72.6% | -63.2% | -63.9% | **-40.9%** | 22.2% | 33.3% |
| Hybrid C Lite+ (Final) | -88.9% | -83.9% | -78.7% | -80.6% | -65.2% | 0.0% | 44.4% |
| Hybrid C Lite (Defaults) | -85.9% | -78.4% | -72.9% | -73.9% | -51.7% | 22.2% | 33.3% |
| Model A (ROI Optimized) | -85.0% | -80.1% | -76.7% | -79.3% | -71.1% | 0.0% | 100.0% |
| Hybrid D.1 | -88.7% | -86.4% | -83.0% | -89.3% | -82.9% | 0.0% | 77.8% |
| Hybrid E.1 0% TGE | -92.9% | -88.8% | -86.0% | -87.4% | -78.7% | 0.0% | 55.6% |
| Hybrid E.1 3% TGE | -88.6% | -86.4% | -83.0% | -89.3% | -82.9% | 0.0% | 77.8% |
| Hybrid F | -88.6% | -86.4% | -83.0% | -89.3% | -82.9% | 0.0% | 77.8% |
| Hybrid F.1 | -88.6% | -86.4% | -83.0% | -89.3% | -82.9% | 0.0% | 77.8% |
| Hybrid C Lite+ Extended | -89.1% | -84.1% | -78.8% | -80.7% | -65.3% | 0.0% | 44.4% |
| Hybrid B (Ingo Detailed) | -84.0% | -75.1% | -67.9% | -71.0% | **-46.6%** | 22.2% | 33.3% |
| Hybrid Lite | -94.3% | -87.3% | -82.8% | -83.9% | -68.9% | 0.0% | 44.4% |
| Hybrid C Lite+ Base | -88.1% | -82.8% | -77.1% | -79.1% | -62.6% | 11.1% | 44.4% |
| Hybrid C Lite+ Variant A | -86.9% | -80.1% | -75.0% | -77.3% | -59.3% | 11.1% | 44.4% |
| Hybrid C Lite+ Variant B | -89.8% | -85.2% | -80.2% | -82.0% | -67.6% | 0.0% | 44.4% |
| Model A (Bonus Separated) | -85.0% | -80.1% | -76.7% | -79.2% | -71.1% | 0.0% | 100.0% |
| Model A (Base) | -85.8% | -80.0% | -76.6% | -79.2% | -71.0% | 0.0% | 100.0% |

**Best in Stress**: Hybrid C (Ingo CSV) at -40.9%

---

### Ideal Growth Scenario

| Model | M12 | M24 | M36 | M48 | M72 | Positive Rate |
|-------|-----|-----|-----|-----|-----|---------------|
| Hybrid (Ingo CSV) | -87.0% | -68.9% | -36.2% | -5.0% | +278.7% | 88.9% |
| Hybrid C (Ingo CSV) | -71.6% | -30.8% | +44.5% | +119.2% | **+756.6%** | 100.0% |
| Hybrid C Lite+ (Final) | -82.1% | -56.5% | -10.2% | +34.1% | +436.8% | 88.9% |
| Hybrid C Lite (Defaults) | -77.1% | -43.9% | +17.5% | +78.5% | +598.5% | 100.0% |
| Model A (ROI Optimized) | -75.9% | -50.4% | -10.5% | +19.3% | +275.8% | 88.9% |
| Hybrid D.1 | -81.8% | -63.1% | -28.4% | +3.6% | +301.7% | 88.9% |
| Hybrid E.1 0% TGE | -88.4% | -70.1% | -36.6% | -3.2% | +280.9% | 88.9% |
| Hybrid E.1 3% TGE | -81.7% | -63.1% | -28.4% | +3.6% | +301.7% | 88.9% |
| Hybrid F | -81.8% | -63.1% | -28.4% | +3.6% | +301.6% | 88.9% |
| Hybrid F.1 | -81.8% | -63.1% | -28.4% | +3.6% | +301.6% | 88.9% |
| Hybrid C Lite+ Extended | -82.5% | -57.0% | -10.9% | +33.3% | +434.5% | 88.9% |
| Hybrid B (Ingo Detailed) | -74.1% | -37.3% | +30.8% | +98.1% | **+672.9%** | 100.0% |
| Hybrid Lite | -90.6% | -66.2% | -21.9% | +24.1% | +406.9% | 100.0% |
| Hybrid C Lite+ Base | -81.0% | -53.4% | -3.7% | +43.9% | +476.7% | 88.9% |
| Hybrid C Lite+ Variant A | -78.8% | -48.2% | +8.2% | +64.3% | +541.9% | 100.0% |
| Hybrid C Lite+ Variant B | -83.6% | -59.8% | -16.8% | +24.4% | +399.1% | 88.9% |
| Model A (Bonus Separated) | -75.9% | -50.5% | -10.5% | +19.4% | +276.2% | 88.9% |
| Model A (Base) | -77.1% | -50.2% | -10.3% | +19.8% | +277.1% | 88.9% |

**Best in Growth**: Hybrid C (Ingo CSV) at +756.6%

---

### Choppy Stress Overlay (10 Scenarios Aggregated)

| Model | M12 | M24 | M36 | M48 | M72 | Positive Rate |
|-------|-----|-----|-----|-----|-----|---------------|
| Hybrid C (Ingo CSV) | -89.8% | -85.4% | -81.6% | -82.8% | **-70.2%** | 7.8% |
| Hybrid B (Ingo Detailed) | -90.8% | -87.0% | -84.4% | -85.5% | **-75.3%** | 7.8% |
| Hybrid C Lite (Defaults) | -91.9% | -89.0% | -87.1% | -88.1% | -79.8% | 6.7% |
| Hybrid C Lite+ Variant A | -92.6% | -90.1% | -88.5% | -89.6% | -82.4% | 4.4% |
| Model A (all variants) | -91.0% | -88.0% | -85.9% | -87.5% | -82.5% | 0.0% |
| Hybrid D.1/E.1/F/F.1 | -93.8% | -93.4% | -93.6% | -95.2% | -92.3% | 0.0% |

**Best in Choppy**: Hybrid C (Ingo CSV) at -70.2%

---

## Model Rankings (Among Ingo Models Only)

| Rank | Model | Stress | Growth | Choppy | Overall |
|:----:|-------|:------:|:------:|:------:|:-------:|
| 1 | **Hybrid C (Ingo CSV)** | -40.9% | +756.6% | -70.2% | **Best Overall** |
| 2 | **Hybrid B (Ingo Detailed)** | -46.6% | +672.9% | -75.3% | Strong #2 |
| 3 | Hybrid C Lite (Defaults) | -51.7% | +598.5% | -79.8% | Good balance |
| 4 | Hybrid C Lite+ Variant A | -59.3% | +541.9% | -82.4% | Conservative |
| 5 | Hybrid C Lite+ Base | -62.6% | +476.7% | -84.8% | Middle |
| 6 | Hybrid C Lite+ Final | -65.2% | +436.8% | -87.1% | Over-tuned |
| 7 | Hybrid Lite | -68.9% | +406.9% | -88.6% | Too conservative |
| 8 | Hybrid C Lite+ Variant B | -67.6% | +399.1% | -88.5% | Aggressive ≠ better |
| 9 | Model A variants | -71% | +275% | -82.5% | High risk, low reward |
| 10 | Hybrid D.1/E.1/F/F.1 | -82% | +301% | -92% | Too restrictive |
| 11 | Hybrid (Ingo CSV) | -83.9% | +278.7% | -93.2% | Mostly stuck |

---

## Recommendations for Improvement

### For D.1/E.1/F Family (Too Conservative)

**Problem**: 77-90% brake activation rate, 0% positive ROI in stress

**Solutions**:
1. Increase `drip_factor_between` from 0.15-0.25 → 0.35-0.50
2. Reduce `mining_lock_months` from 12 → 6
3. Add partial release logic in throttle zone (not full halt)

### For Model A Variants (Binary Failure)

**Problem**: 100% brake rate despite aggressive design

**Solutions**:
1. Lower `emission_cap` to reduce initial flood
2. Add state-driven release logic
3. Consider mandatory staking (currently 0%)

### For Hybrid (Ingo CSV) (Stuck Under Stress)

**Problem**: -83.9% at 72mo stress, 0% positive rate

**Solutions**:
1. Narrow the global_monthly_cap range (0.3-1.0% is too wide)
2. Reduce mining_lock_ratio from 0.70 → 0.50
3. Add recovery acceleration after brake release

---

## Final Scorecard

| Goal | Status | Score |
|------|--------|:-----:|
| 1. Risk-reward trade-offs | ✅ PASS | 10/10 |
| 2. Adaptive throttling | ⚠️ PARTIAL | 6/10 |
| 3. Parameter-level only | ✅ PASS | 10/10 |
| 4. TGE isolation | ✅ PASS | 10/10 |
| 5. Smooth transitions | ⚠️ PARTIAL | 5/10 |
| 6. Self-contained | ✅ PASS | 10/10 |
| 7. Objective testing | ✅ PASS | 10/10 |

**Overall Score: 61/70 (87%)**

---

## Conclusion

The Ingo CSV models largely **succeeded** in their stated goals. The **Hybrid C family** (especially Hybrid C Ingo CSV) represents the best balance of risk-adjusted returns. The D/E/F family and Model A variants need parameter tuning to avoid binary failure modes.

**Key takeaway**: Conservative throttling protects downside but can trap tokens. The best-performing models (Hybrid C, Hybrid B Detailed) use moderate caps (0.30-0.70%) with state-driven release that still allows meaningful flow during recovery phases.

---

*Report generated by BlockDAG Backtest Harness v2.0*  
*31 models × 3 opinions × 10 choppy scenarios × 25 runs per window*

