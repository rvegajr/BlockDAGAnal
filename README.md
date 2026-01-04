# BlockDAG Vesting Solution

## Start Here: All-Model Comparison (recommended)

- **All models compared (second opinion, order-book + sell-pressure)**: [`docs/vesting/ALL_MODEL_COMPARISON.md`](docs/vesting/ALL_MODEL_COMPARISON.md)

## Latest Update (Jan 2026): Final Summary (Option A → B → C)

We now have **three independent simulation “opinions”** (different methodologies) and the latest model set includes:
- **Hybrid Tokenomics (Solvency‑Anchored, State‑Driven)**
- **Hybrid B**
- **Protocol v3.0**
- **Protocol v3.1 (Adjusted)** ([source](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/))

### Models we challenged (brief “what it does”)

- **Original Model**: Long, time-based schedule (2% TGE, long cliff). Prioritizes predictability; tends to underperform on investor ROI but avoids frequent gate/brake behavior.
- **Hybrid Model**: Time-based vesting + emergency-brake style protection. Better ROI in some conditions, but can “freeze” under stress depending on triggers.
- **Protocol v2.6**: **Hard oracle gate** at target price (e.g. $0.05). Releases can halt entirely if price is below the gate; strong protection but high “stuck” risk.
- **Protocol v3.0**: Oracle gate + **emergency brake** + **drip between bands** (reduced vesting when price is between $0.02 and $0.05) + **mining lock**. Designed to do well when liquidity is deep enough for gates/drip to function.
- **Protocol v3.1 (Adjusted)**: 3% solvency + oracle gate + emergency brake + **volume pegging** (release limited by a % of volume when below target) + **volume-capped mining**. Spec reference: [Protocol v3.1 Adjusted](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/).
- **Hybrid B**: Market-state driven issuance with time only defining review windows (in concept). In our harness it behaves as state-gated release under global caps; typically more conservative than time-based unlocks.
- **Hybrid Tokenomics (Solvency‑Anchored)**: State-driven vesting/mining/bonus under hard monthly circulation caps, plus heavier staking/locks (designed to minimize structural sell pressure and reduce brake frequency).

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
| **$20M–$75M** | **Hybrid Tokenomics (Solvency‑Anchored)** | Lowest brake rate + strong scenario survival while liquidity is fragile | [`HYBRID_TOKENOMICS_COMPREHENSIVE_VALIDATION.md`](HYBRID_TOKENOMICS_COMPREHENSIVE_VALIDATION.md) |
| **$100M–$150M** | **Protocol v3.0** | Stronger ROI once liquidity is deep enough for gates/drip to function | [`docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md`](docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md) and [`HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md) |

Notes:
- Hybrid Tokenomics liquidity sweep and scenario survival are documented in `HYBRID_TOKENOMICS_COMPREHENSIVE_VALIDATION.md`.
- Protocol v3.0 liquidity-tier behavior comes from the tier harness documented in `docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md`.

---

## 🏆 Liquidity Tier Winner (Legacy 4-model tier harness)

This section is from a **legacy liquidity-tier harness** that compares **Original / Hybrid Model / Protocol v2.6 / Protocol v3.0** (it does **not** include Hybrid Tokenomics). Use it for v3.0/v2.6 historical tier behavior, and use **Option C** above for the current “all-models” recommendation set.

We added **Protocol 3.0 (Hybrid Optimized)** and re-ran:
- **100 sims/model** under bull/bear/normal/volatile markets
- **20,000 sims** across **5 liquidity tiers × 10 historical crash scenarios × 4 models**

**What we found:** the “winner” changes by liquidity tier.

| Liquidity | Winner | Why |
|----------:|--------|-----|
| **$32M – $75M** | **Hybrid Model** | Protection dominates when liquidity is fragile |
| **$100M – $150M** | **Protocol v3.0** | Oracle gate + brake + drip dominates when liquidity is strong |

**Optimal (within tiers tested): $150M + Protocol v3.0**  
- Avg Month-12 ROI: **+0.79%**  
- Avg Month-12 Value: **$9,070.81** (on $9k reference)  
- Survival rate: **100%** (no breach below $0.02)  

**[Liquidity Tier Analysis v2 →](docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md)**  
**[Protocol 3.0 Simulation Comparison →](docs/vesting/PROTOCOL_3_0_SIMULATION_COMPARISON.md)**

---

## ⭐ Recommended Parameters (Protocol v3.0 @ $100M+ Liquidity)

| Parameter | Value | Source |
|-----------|-------|--------|
| **TGE Unlock** | 3% | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Cliff Period** | 3 months | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Vesting Duration** | **36 months total (drip to Month 36)** | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Oracle Price Gate** | **$0.05** | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Emergency Brake** | **$0.02** | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Mining Emission Cap** | **20%** | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| **Volume Pegging (Drip)** | **2% of 24h volume** | [Protocol 3.0](https://a-changer-plus-tard.github.io/Protocol-3.0/) |

### 📊 Quick Results Snapshot

| Test | Result |
|------|--------|
| **Moderate markets (100 sims/model @ $32M)** | Protocol v3.0 best avg Month-12 ROI (**-49.8%**) |
| **Historical crashes (20,000 sims across tiers)** | Protocol v3.0 wins at **$100M–$150M**, Hybrid wins at **$32M–$75M** |

### 📄 Detailed Docs

- **[Protocol 3.0 Simulation Comparison →](docs/vesting/PROTOCOL_3_0_SIMULATION_COMPARISON.md)**
- **[Four Model Comparison →](docs/vesting/FOUR_MODEL_COMPARISON.md)**
- **[Liquidity Tier Analysis v2 →](docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md)**

---

## ✅ Validated: 100 Simulations + 10 Market Scenarios

**Comprehensive Testing Complete:** We tested **101 parameter combinations** and validated against **10 historical market crashes**.

### Key Finding: Survival vs. Investor ROI Trade-off

| Model | Survival Rate | Investor ROI | Verdict |
|-------|---------------|--------------|---------|
| Top Model (10% TGE, 12mo cliff) | 70% | -50.6% | Survives but investors lose |
| **Hybrid Model (3% TGE, 3mo cliff)** | **0%** | **Better ROI** | **Brake protects, honest expectations** |

**Our Hybrid Model Rank: #56 out of 101**

**Why #56?** The scoring prioritized "survival metrics" over investor returns. Our model triggers the emergency brake in all scenarios (by design - it protects value), but provides better investor returns and realistic expectations.

**Reality:** No model survives severe crashes (COVID, FTX) without triggering the brake. The top model also triggers in 3/10 scenarios.

**[Full Validation Analysis →](docs/vesting/HYBRID_MODEL_VALIDATION.md)**

---

## 🏆 Liquidity Tier Comparison (Legacy 3-model harness): 1,500 Simulations

**Note**: This section is from an older harness that tested **3 models only** (Original / Hybrid / Protocol v2.6). For the current **all-model** recommendation set, use the **Option A/B/C** summary at the top and the linked all-model reports.

**1,500 Simulations Complete:** Tested three legacy models across **5 liquidity tiers** ($32M-$150M) and **10 historical market scenarios**.

### Key Discovery: Liquidity Determines Winner

| Liquidity | Winner | Month 12 Value | Survival Rate |
|-----------|--------|----------------|---------------|
| **$32M** | **Hybrid Model** | $2,596 | 60% |
| **$50M** | **Hybrid Model** | $3,371 | 80% |
| **$75M** | **Hybrid Model** | $4,290 | 80% |
| **$100M** | **Hybrid Model** | **$5,106** ✅ | 80% |
| **$150M** | **Protocol v2.6** | $4,949 | 60% |

**🏆 Optimal: Hybrid Model at $100M** (Fairness Score: 52.4/100)

**Why Hybrid Model Wins at Lower Liquidity:**
- ✅ Emergency brake protects value in crashes
- ✅ Emission cap prevents supply flood
- ✅ Mandatory staking reduces circulating supply
- ✅ Best performance in critical scenarios (COVID, FTX)

**Why Protocol v2.6 Wins at $150M:**
- ✅ Higher liquidity supports faster vesting
- ✅ No emission cap allows full network activity
- ✅ Oracle price gate sufficient at high liquidity

**[Full Liquidity Tier Analysis →](docs/vesting/LIQUIDITY_TIER_ANALYSIS.md)**  
**Legacy 3-model report**: [Three Model Comparison →](docs/vesting/THREE_MODEL_COMPARISON.md)

---

## 📈 Legacy Notes: Why Protocol v2.6 “Won” in the earlier 3-model comparison

### ✅ Context

This was an earlier conclusion from the **3-model-only harness** (Original vs Hybrid vs Protocol v2.6). It does **not** reflect the newer all-model comparisons that now include Hybrid Tokenomics, Hybrid B, Protocol v3.0, and Protocol v3.1.

For up-to-date “all models” results, see:
- **Second opinion (order-book + sell-pressure)**: [`SECOND_OPINION_COMPARE_REPORT_V31.md`](SECOND_OPINION_COMPARE_REPORT_V31.md)
- **All-model compare/contrast**: [`HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)

### ✅ Key Advantages

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
| **[Liquidity Tier Analysis](docs/vesting/LIQUIDITY_TIER_ANALYSIS.md)** | ⭐ 1,500 simulations: Optimal liquidity and protocol selection |
| **[All-Model Comparison (Second Opinion)](docs/vesting/ALL_MODEL_COMPARISON.md)** | ✅ *All models* compared (v2.6/v3.0/v3.1/Hybrid B/Hybrid Tokenomics/etc) using order-book + sell-pressure |
| **[All-Model Comparison (Hybrid Tokenomics focus)](HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md)** | ✅ Compares Hybrid Tokenomics vs *all* past tested models (incl. v3.0/v3.1) |
| **[Second Opinion Report (All models @ $32M)](SECOND_OPINION_COMPARE_REPORT_V31.md)** | ✅ Order-book + sell-pressure methodology across all models |
| **[Third Opinion Report (adds Protocol v3.1)](THIRD_OPINION_V31_REPORT.md)** | ✅ Path-dependent harness including v3.1 volume peg/caps |
| **Legacy: [Three Model Comparison](docs/vesting/THREE_MODEL_COMPARISON.md)** | Historical harness: Original vs Hybrid vs Protocol v2.6 |
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

# Legacy harnesses (historical)
python3 scripts/three_model_comparison.py                       # Legacy 3-model comparison
python3 scripts/liquidity_tier_comparison_v2_four_models.py      # Legacy 4-model liquidity tier harness (includes v3.0)
python3 scripts/liquidity_tier_comparison.py                    # Older liquidity tier harness

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
