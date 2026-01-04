# BlockDAG Vesting Solution

## Start Here: All-Model Comparison (recommended)

- **All models compared (second opinion, order-book + sell-pressure)**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)

### All models (topline) — ROI / Value / Verdict

This table is generated from the **second-opinion** results (order-book + sell-pressure) at **$32M liquidity**, using a **$9,000 reference investment**:

> Note on “why invest”: this harness is a **conservative stress-test** (persistent sell pressure + order-book impact). **Positive ROI is rare** here and (so far) only appears in a small number of **Protocol v3.0** runs at **Month 24/36** under the **volatile** market generator; **no choppy/crash scenario** produces positive ROI. See the multi-horizon detail: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md).

| Model | Month-12 ROI (avg) | Month-12 Value (avg) | Brake rate | Verdict |
|---|---:|---:|---:|---|
| [Protocol v3.0](#protocol-v30) | -64.1% | $3,227 | 44.0% | Best ROI + best choppy; access risk (brakes) |
| [Hybrid Tokenomics (Solvency-Anchored)](#hybrid-tokenomics-solvency-anchored) | -86.8% | $1,190 | 2.0% | Best balance (ROI + access) |
| [Hybrid B](#hybrid-b) | -91.3% | $782 | 9.0% | Conservative; weaker ROI than Hybrid Tokenomics |
| [Protocol v2.6](#protocol-v26) | -78.9% | $1,899 | 99.0% | High gate/brake risk (often “stuck”) |
| [Protocol v3.1 (Adjusted)](#protocol-v31-adjusted) | -79.4% | $1,850 | 100.0% | High gate/brake risk (often “stuck”) |
| [Hybrid Model](#hybrid-model) | -85.4% | $1,314 | 100.0% | High brake risk (often “stuck”) |
| [Original Model](#original-model) | -95.6% | $400 | 1.0% | Most stable; lowest ROI |

Full evidence + per-market + choppy breakdown: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md).

### Model Index (what each does + sources)

Each model name above links here. For full tables, see [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md).

#### Original Model
- **What it does**: time-based long vesting (2% TGE + long cliff) with conservative schedule.
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)

#### Hybrid Model
- **What it does**: time-based vesting with emergency-brake style protections (can pause/“freeze” under stress in our harness).
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)

#### Protocol v2.6
- **What it does**: 3% solvency + **oracle price gate** (hard gate behavior below target).
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md), [`docs/vesting/PROTOCOL_V26_COMPARISON.md`](docs/vesting/PROTOCOL_V26_COMPARISON.md)
- **Source**: [BlockDag Launch Protocol v2.6](https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/)

#### Protocol v3.0
- **What it does**: oracle gate + emergency brake + drip/volume-peg style throttling + mining locks (stronger at high liquidity tiers).
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md), [`docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md`](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md)
- **Source**: [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/)

#### Protocol v3.1 (Adjusted)
- **What it does**: 3% solvency + oracle gate + emergency brake + **volume pegging** + **volume-capped mining**.
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)
- **Source**: [Protocol v3.1 Adjusted](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/)

#### Hybrid B
- **What it does**: state-gated issuance under caps; more conservative than time-based unlocks; less aggressive than Hybrid Tokenomics locks.
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)

#### Hybrid Tokenomics (Solvency-Anchored)
- **What it does**: state-driven vesting/mining/bonus under monthly circulation caps + heavier staking/locks (designed to reduce structural sell pressure).
- **Evidence**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md), [`HYBRID_TOKENOMICS_COMPREHENSIVE_VALIDATION.md`](HYBRID_TOKENOMICS_COMPREHENSIVE_VALIDATION.md)

## 💰 Real-World Investor Comparison (Based on 10 Years BTC History)

**Data source**: BTC prices 2015-2024 (COVID crash, FTX collapse, bull runs, bear markets — all included)

### If You Invest Today, What Do You Get Back?

| Investment | Conservative (Stress) | Ideal (Growth) | With Crashes |
|------------|----------------------|----------------|--------------|
| | _3 Years / 6 Years_ | _3 Years / 6 Years_ | _3 Years / 6 Years_ |
| **$9,000** | $12,616 / $11,390 | **$27,745 / $67,110** | $9,565 / $8,346 |
| **$50,000** | $70,089 / $63,277 | **$154,137 / $372,835** | $53,140 / $46,369 |
| **$100,000** | $140,177 / $126,555 | **$308,273 / $745,670** | $106,279 / $92,737 |

_Values shown for **Protocol v3.0** (best performer across scenarios)_

### ROI by Year (Protocol v3.0)

| Scenario | Year 1 | Year 2 | Year 3 | Year 6 |
|----------|-------:|-------:|-------:|-------:|
| **Conservative** | -58% | -1% | **+40%** | **+27%** |
| **Ideal (Growth)** | -43% | **+72%** | **+208%** | **+646%** |
| **With Crashes** | -70% | -22% | **+6%** | -7% |

### Key Findings

✅ **Positive ROI is achievable** — Protocol v3.0 reaches +40% ROI by Year 3 even in conservative scenario  
✅ **$100k → $308k** in 3 years (Ideal), **$100k → $745k** in 6 years  
✅ **60% of conservative runs** show positive ROI by Year 6  
✅ **100% of ideal runs** show positive ROI by Year 3+  

**Full investor comparison**: [`docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md`](docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md)  
**Multi-opinion report**: [`docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md`](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md)  
**Run your own backtest**: [`docs/vesting/REAL_WORLD_BACKTEST_PLAN.md`](docs/vesting/REAL_WORLD_BACKTEST_PLAN.md)

---

## Latest Update (Jan 2026): Final Summary (Option A → B → C)

We now have **three independent simulation "opinions"** (different methodologies) and the latest model set includes:
- **Hybrid Tokenomics (Solvency‑Anchored, State‑Driven)**
- **Hybrid B**
- **Protocol v3.0**
- **Protocol v3.1 (Adjusted)** ([source](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/))

### Models we challenged (brief “what it does”)

- **[Original Model](#original-model)**: Long, time-based schedule (2% TGE, long cliff). Prioritizes predictability; tends to underperform on investor ROI but avoids frequent gate/brake behavior.
- **[Hybrid Model](#hybrid-model)**: Time-based vesting + emergency-brake style protection. Better ROI in some conditions, but can “freeze” under stress depending on triggers.
- **[Protocol v2.6](#protocol-v26)**: **Hard oracle gate** at target price (e.g. $0.05). Releases can halt entirely if price is below the gate; strong protection but high “stuck” risk.
- **[Protocol v3.0](#protocol-v30)**: Oracle gate + **emergency brake** + **drip between bands** (reduced vesting when price is between $0.02 and $0.05) + **mining lock**. Designed to do well when liquidity is deep enough for gates/drip to function.
- **[Protocol v3.1 (Adjusted)](#protocol-v31-adjusted)**: 3% solvency + oracle gate + emergency brake + **volume pegging** (release limited by a % of volume when below target) + **volume-capped mining**. Spec reference: [Protocol v3.1 Adjusted](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/).
- **[Hybrid B](#hybrid-b)**: Market-state driven issuance with time only defining review windows (in concept). In our harness it behaves as state-gated release under global caps; typically more conservative than time-based unlocks.
- **[Hybrid Tokenomics (Solvency‑Anchored)](#hybrid-tokenomics-solvency-anchored)**: State-driven vesting/mining/bonus under hard monthly circulation caps, plus heavier staking/locks (designed to minimize structural sell pressure and reduce brake frequency).

**Second-opinion (order-book + sell-pressure) artifacts**:
- **Report**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)
- **Raw results**: [`second_opinion_compare_results_v31.json`](second_opinion_compare_results_v31.json)

**Cross-model comparison artifact**:
- [`HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)

---

## Option A — Single Winner (one pick)

### **Winner: Protocol v3.0**

**Why**: It has the **best Month‑12 ROI** and the **best choppy-market average ROI** under the **second-opinion** (order-book + sell-pressure) methodology, and it also ranks #1 on our simple access-adjusted score.

- **Justification (numbers + tables)**: `SECOND_OPINION_COMPARE_REPORT_V31.md`
- **Justification (broad compare/contrast across all models + liquidity notes)**: `HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`
- **Protocol v3.1 spec reference (included in comparisons)**: [Protocol v3.1 Adjusted](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/)

---

## Option B — Best-by-Category (multiple winners)

All of these are from the **second opinion @ $32M** (100 sims/model).

- **Best raw ROI (Month‑12 avg)**: **Protocol v3.0** (ROI **-64.1%**)  
  - **Justification**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)

- **Best balance (low brake + solid ROI)**: **Hybrid Tokenomics (Solvency‑Anchored)** (ROI **-86.8%**, brake **2.0%**)  
  - **Justification**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)
  - **Deeper rationale + cross-model comparison**: [`HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)

- **Best choppy markets (avg ROI across 10 scenarios)**: **Protocol v3.0** (avg choppy ROI **-77.5%**)  
  - **Justification**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)

- **Best “access-adjusted” rank (ROI penalized by brake rate)**: **Protocol v3.0**  
  - **Justification**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)

---

## Option C — Liquidity-Tier Winner

The “winner” depends on **launch liquidity**.

### Practical tier guidance

| Liquidity tier | Winner | Why | Justification |
|---:|---|---|---|
| **$20M–$150M** | **See per-tier winners** | Tier winners vary by model mechanics and brake behavior | [`docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md`](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md) |

Notes:
- This section now references an **all-model** liquidity-tier analysis (not a legacy 3-model/4-model harness).

---

## 📈 Protocol Mechanics Notes (applies across all-model comparisons)

### ✅ Key Advantages (Protocol v2.6 example)

1. **Faster Vesting (21 months)**
   - Investors access tokens 15 months earlier than Hybrid Model
   - More tokens available during price appreciation periods

2. **No Emission Cap**
   - Allows full mining network activity
   - More network participation = potential price support

3. **Voluntary Staking (40% APY)**
   - No mandatory lock = more tokens available to investors
   - High APY incentivizes holding without forcing it

4. **Oracle Price Gate at $0.05**
   - Prevents unlocks during price declines
   - Protects value without frequent emergency brake activation

### ⚠️ Trade-offs

- **No emission cap**: Requires monitoring of mining emissions
- **No mandatory staking**: Relies on voluntary participation
- **Faster vesting**: More supply pressure, but better investor access

### ❌ What We Rejected

- 2% TGE (too aggressive, Protocol v2.6 proved 3% works)
- 40% TGE (mathematically impossible at $32M)
- No vesting (immediate crash to $0.001)
- "Cannot crash" claims (irresponsible)

---

## 🛡️ Protection Mechanisms

```
TRIPLE PROTECTION:

1. ORACLE PRICE GATE
   └── Vesting only proceeds if price ≥ $0.02

2. EMERGENCY BRAKE
   ├── Price < $0.02 for 7 days → PAUSE
   ├── Liquidity < $10M → PAUSE
   └── Staking rewards +50% during pause

3. EMISSION CAP
   └── Max 2.1M tokens/day regardless of miners
```

---

## 📊 Complete Vesting Schedule (Protocol v2.6)

### Investors

| Category | TGE | Cliff | Total Vesting | Notes |
|----------|-----|-------|---------------|-------|
| **Base Coins** | 3% | 3 mo | **21 months** | Oracle price gate at $0.05 |
| **Bonus Coins** | 0% | 12 mo | 48 months | Oracle price gate at $0.05 |

### Insiders (LONGER Than Investors)

| Category | TGE | Cliff | Total Vesting |
|----------|-----|-------|---------------|
| **Team** | 0% | 18 mo | 66 months |
| **Management** | 0% | 24 mo | 84 months |
| **Founders** | 0% | 24 mo | 96 months |

---

## ⛏️ Mining Rewards

| Miner | Daily Output | Status |
|-------|--------------|--------|
| X1 | 20 BDAG | ✅ Unchanged |
| X10 | 200 BDAG | ✅ Unchanged |
| X30 | 600 BDAG | ✅ Unchanged |
| X100 | 2,000 BDAG | ✅ Unchanged |

**What's New:** 50% of rewards auto-staked for 90 days. You earn the full amount.

**Emission Cap:** After Month 6, total network emissions capped at 2.1M/day (20% of max).

---

## 📉 Market Scenarios (10 Tested)

| Scenario | Price Impact | Emergency Brake | Survival |
|----------|--------------|-----------------|----------|
| COVID Crash (-80%) | Month 1 | Activated | ✅ Protected |
| FTX Collapse (-70%) | Month 3 | Activated | ✅ Protected |
| May 2021 (-60%) | Month 9 | Activated | ✅ Protected |
| Gradual Bear (-50%) | Month 10 | Activated | ✅ Protected |
| **Stable Growth** | Month 15 | Activated | ⭐ Best Case |
| **High Volatility** | Month 15 | Activated | ⭐ Best Case |

**100% of scenarios trigger emergency brake** - this is by design. The brake protects value.

---

## 💡 Key Insights

### The Honest Truth

| Reality | Impact |
|---------|--------|
| Launch price ~$0.037 | Not $0.05 (based on 3% TGE math) |
| Year 1 price decline | Expected as supply grows |
| 3-year hold recommended | Best ROI for presale investors |
| No "guaranteed" prices | Crypto is volatile |

### What Makes Protocol v2.6 Work

1. **Day 1 solvency** - 3% TGE covered by $32M liquidity
2. **Faster vesting** - 21 months vs 36 months = earlier investor access
3. **Sell pressure reduction** - 40% APY incentivizes voluntary staking
4. **Oracle protection** - Price gate at $0.05 prevents unlocks during declines
5. **No emission cap** - Full mining network activity supports price
6. **Aligned incentives** - Insiders vest longer than investors

---

## 📁 Documentation Index

### Core Documents

| Document | Description |
|----------|-------------|
| **[All-Model Liquidity Tier Analysis](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md)** | ✅ *All models* tested across liquidity tiers × choppy scenarios |
| **[All-Model Comparison (Second Opinion)](docs/vesting/ALL_MODEL_COMPARISON.md)** | ✅ *All models* compared (v2.6/v3.0/v3.1/Hybrid B/Hybrid Tokenomics/etc) using order-book + sell-pressure |
| **[Real-World Backtest Plan](docs/vesting/REAL_WORLD_BACKTEST_PLAN.md)** | 🚧 How to run a historical replay (BTC/ETH) to estimate ROI across rolling windows |
| **[All-Model Comparison (Hybrid Tokenomics focus)](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)** | ✅ Compares Hybrid Tokenomics vs *all* past tested models (incl. v3.0/v3.1) |
| **[Second Opinion Report (All models @ $32M)](SECOND_OPINION_COMPARE_REPORT_V31.md)** | ✅ Order-book + sell-pressure methodology across all models |
| **[Third Opinion Report (adds Protocol v3.1)](THIRD_OPINION_V31_REPORT.md)** | ✅ Path-dependent harness including v3.1 volume peg/caps |
| **[Protocol v2.6 Comparison](docs/vesting/PROTOCOL_V26_COMPARISON.md)** | Second opinion analysis |
| **[Hybrid Model Validation](docs/vesting/HYBRID_MODEL_VALIDATION.md)** | ⭐ 100 simulations + 10 market scenarios |
| [Protocol v2.6 Comparison](docs/vesting/PROTOCOL_V26_COMPARISON.md) | Second opinion analysis |
| [Optimal Liquidity Analysis](docs/vesting/OPTIMAL_LIQUIDITY_ANALYSIS.md) | 360 simulations |
| [Utility Conversion Analysis](docs/vesting/UTILITY_CONVERSION_ANALYSIS.md) | Bonus token proposal |
| [40% TGE Analysis](docs/vesting/FORTY_PERCENT_TGE_ANALYSIS.md) | Why 40% doesn't work |

### Simulations & Data

| Document | Description |
|----------|-------------|
| [Market Scenario Breakdown](docs/vesting/MARKET_SCENARIO_BREAKDOWN.md) | All 10 scenarios detailed |
| [Model Comparison](docs/vesting/MODEL_COMPARISON.md) | 4 models compared |
| [Vesting Summary](docs/vesting/VESTING_REWORK_SUMMARY.md) | Implementation overview |
| [Investor Communication](docs/vesting/PRESALE_INVESTOR_COMMUNICATION.md) | Ready materials |

### Smart Contracts

| Document | Description |
|----------|-------------|
| [Vesting Contract](docs/specs/contracts/VESTING_CONTRACT_SPEC.md) | Vesting logic |
| [Staking Contract](docs/specs/contracts/STAKING_CONTRACT_SPEC.md) | Staking tiers |
| [DAO Triggers](docs/specs/contracts/DAO_TRIGGERS.md) | Milestone releases |
| [Emergency Brake](docs/specs/contracts/EMERGENCY_BRAKE.md) | Auto protection |

### Run Simulations

```bash
# All-model comparisons (recommended)
python3 scripts/hybrid_tokenomics_comparison.py                 # Primary all-model harness (Hybrid Tokenomics included)
python3 scripts/hybrid_tokenomics_second_opinion_compare.py     # Second opinion (order-book + sell pressure, includes v3.0/v3.1)
python3 scripts/third_opinion_protocol_v31_compare.py           # Third opinion (adds Protocol v3.1 volume peg/caps)
python3 scripts/all_model_liquidity_tier_second_opinion.py      # All-model liquidity tiers × choppy scenarios
python3 scripts/real_world_backtest_second_opinion.py --csv /path/to/btc_daily.csv --use-volume  # Real-world historical replay (rolling windows)

# Other supporting simulations
python3 scripts/hybrid_model_validation.py                      # Parameter search + scenario validation (legacy hybrid focus)
python3 scripts/vesting_simulations_v3_real_miners.py           # Real miner data harness
python3 scripts/burn_market_stress_test.py                      # Historical crash harness
python3 scripts/optimal_liquidity_analysis.py                   # Liquidity grid search

# All scripts
python3 scripts/vesting_simulations.py
python3 scripts/vesting_simulations_v2.py
python3 scripts/vesting_simulations_v4_real_miners_v2.py
python3 scripts/burn_poe_simulations.py
python3 scripts/burn_poe_simulations_v2.py
python3 scripts/fairness_optimization.py
python3 scripts/forty_percent_32m_simulations.py
```

---

## 🎯 The Bottom Line

### For Presale Investors

Use the **Option A/B/C** summary at the top of this README (all-model comparison), and see the linked evidence:
- [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)
- [`HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)

### For the Project

The best choice depends on what you optimize for (raw ROI vs access vs liquidity tier). Use **Option A/B/C** at the top and the linked reports for the full all-model evidence set.

---

## Contact

**Questions?**
- Email: Reid@blockdaginvestors.com
- Docs: [docs/vesting/](docs/vesting/)
- Specs: [docs/specs/](docs/specs/)

---

*Last Updated: January 2025*  
*Status: **PROTOCOL V2.6 - WINNING MODEL (VALIDATED)***  
*Based on: 400+ simulations comparing Original, Hybrid, and Protocol v2.6 models*
