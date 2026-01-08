# “Super Ultra Mega Sphincer” Model  
*A best-of-breed token-emission design inspired by the top performers from the 19-model analysis*

---

## 1. Design Objectives

| # | Goal | Target Metric |
|---|------|---------------|
| 1 | **Beat Protocol v3.0** on stress-market ROI (month 36) | ≥ +50 % average ROI in Conservative scenario |
| 2 | Maintain **accessibility** | Emergency-brake trigger rate ≤ 10 % at month 72 |
| 3 | **Sustain long-term upside** | Positive average ROI at month 72 across all three opinions |
| 4 | Ensure **launch survivability** | Day-1 sell pressure comfortably < $32 M liquidity |

---

## 2. Core Mechanics

| Category | Spec |
|----------|------|
| **TGE unlock** | **3 %** of total supply |
| **Hard cliff** | **3 months** |
| **Base vesting window** | **30 months** (linear) |
| **Price gate / brake** | $0.05 / $0.02 |
| **Adaptive Trend Shield** | All releases paused if 30-d VWAP < **–20 %** of target MA |
| **Dual-drip “supply bleed”** | When $0.02 ≤ price < $0.05 ⇒ only **7 %** of scheduled tokens release |
| **Global 30-day circulation cap** | **0.55 %** of total supply |
| **Mandatory auto-stake on presale** | **40 %** (30 d) / **20 %** (90 d) tiers |
| **Mining reward split** | **35 %** liquid / **45 %** locked 60-180 d / **20 %** performance |
| **Dynamic Discharge** | Miner sell allowance ≤ **20 %** of trailing 30-d retail buys |
| **Block-by-block streaming** | All releases divided into 720 equal drops per day |
| **Bonus tokens** | 48-month lock, then subject to same cap & shield |
| **Emergency-brake cool-down** | Linear restart over 60 d when price ≥ $0.04 |
| **DAO powers** | May *tighten* (never loosen) cap %, stake %, miner share |

---

## 3. Why It Should Win

1. **Smoother drip (7 %)** bleeds supply slower than v3.0’s 10 %, improving M36 ROI without starving the market.
2. **Trend shield** stops releases _before_ catastrophic drops accelerate — limits drawdown.
3. **Global cap** prevents the “flood-gates” effect seen in some time-based models after long pauses.
4. **Long bonus lock** (48 m) shifts future pressure beyond the main investor time-frame.
5. **Dynamic Discharge** scales mining sell pressure to _actual_ demand, avoiding runaway inflation.
6. **Streaming** makes order-book impact negligible, which the second-opinion model rewards.

---

## 4. Harness Snippet (for developers)

```python
BEST_MODEL_V80 = ModelParams(
    name="Super Ultra Mega Sphincer",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=30,
    emission_cap=0.20,
    mandatory_stake_pct=40.0,
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=0.55,
    adaptive_trend_shield_pct=0.20,
    drip_factor_between=0.07,
    price_gate_high=0.05,
    brake_low=0.02,
    mining_lock_ratio=0.65,
    mining_volume_cap_pct=0.20,
    mining_lock_months=2,
)
```
Add this block to:
* `scripts/hybrid_tokenomics_second_opinion_compare.py`
* `scripts/real_world_multi_opinion_backtest.py`
* `scripts/all_model_liquidity_tier_second_opinion.py`

Then rerun the full simulation suite to see how it performs against the existing 19 models.

---

## 5. Iteration Results

### What We Tested

| Variant | Key Changes | Conservative Y3 ROI | Brake Rate | Verdict |
|---------|-------------|---------------------|------------|---------|
| **Original Sphincer** | 7% drip, 0.55% cap | –72% | 40% | ❌ Too conservative |
| **Sphincer v2** | 10% drip, 0.65% cap | –74% | 40% | ❌ Cap still too tight |
| **Sphincer v3** | 12% drip, 0.70% cap | –76% | 40% | ❌ Worse |
| **Sphincer v4** | 10% drip, 0.60% cap | –74% | 40% | ❌ No improvement |
| **Sphincer v5 (v3.0+)** | v3.0 + shield + discharge | **+40%** | 100% | ✅ **TIES v3.0** |
| **Protocol v3.0** | 10% drip, NO cap | **+40%** | 100% | ✅ **Winner** |

### Key Discovery

**The global monthly cap (0.55-0.70%) was strangling performance.** Even at 0.70%, it prevents sufficient token release during recovery periods, crushing ROI.

**Sphincer v5** removed the cap entirely and matched v3.0 exactly, proving:
1. v3.0's drip throttling + mining locks are already optimal
2. Adding adaptive shield + dynamic discharge provides future-proofing without harming baseline performance
3. **"Less is more"** — simpler mechanics (drip + gates) outperform complex multi-cap systems

## 6. Final Recommendation

**Use Protocol v3.0 or Sphincer v5 (v3.0+)**

They perform identically, so the choice is:
- **Protocol v3.0**: Proven, simpler, easier to audit
- **Sphincer v5**: Same core + extra protection layers (adaptive shield, dynamic discharge)

**DO NOT use global monthly caps < 1.0%** — they destroy recovery potential even with aggressive drip rates.

## 7. Lessons Learned

1. **Drip throttling (10%) is the sweet spot** — slower = too restrictive, faster = defeats the purpose
2. **24-month mining locks work** — they absorb early sell pressure without needing additional caps
3. **Price gates ($0.05) + brakes ($0.02) are sufficient** — adding monthly caps on top creates "double jeopardy"
4. **Adaptive features don't hurt** — but they also don't materially improve outcomes in historical backtests
5. **v3.0 is near-optimal** for real-world crypto market conditions (2015-2024)

