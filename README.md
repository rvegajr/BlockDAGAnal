# BlockDAG Vesting Analysis

## 📖 Why 10-Year Historical Data?

> *"Short-term gains in crypto are risky to predict. If you can do it consistently, congratulations—most cannot."*

I reworked all my tokenomics simulations because I was looking at **theoretical scenarios**—hypothetical market conditions that may or may not occur. What I wanted instead: **real historical data** that reflects actual human behavior, actual crashes, actual recoveries.

### The S&P 500 Lesson

The S&P 500 has shown that **~95% of rolling 10-year periods have been positive**. Extend to 15-20 years with dividends reinvested, and historically there's been no negative period. The odds are overwhelmingly in your favor for long-term horizons.

### The Crypto Compression Theory

I believe crypto cycles are **compressed stock cycles** at a 3:1 to 4:1 ratio:

| Market | Major Crash Frequency |
|--------|----------------------|
| Stock Market | 7-15 years (1929 → 1987 → 2000 → 2008 → 2020) |
| Crypto | 3-4 years (2011 → 2014 → 2018 → 2022) |

The same emotional patterns—fear, greed, panic, recovery—play out faster in crypto because of 24/7 markets, global participation, and instant information flow.

### My Thesis

If 10 years of the S&P 500 means the odds of positive returns are in my favor, I postulate that **10 years in the crypto market supports that also**. By backtesting against 2015-2024 BTC history, I'm capturing the 2017 bull run, 2018 crash, COVID crash, 2021 bull run, and 2022 crash—multiple full market cycles.

**In the next 10 years, we will see the same exponential gains that we saw in the past 10 years in crypto.**

👉 **[Full Methodology & Investment Thesis](docs/vesting/METHODOLOGY_AND_INVESTMENT_THESIS.md)**

---

## 🔗 Model Sources (Specs & Inputs)

**Protocol specs index (v2.6 / v3.0 / v5.x / v7.0):** [`https://a-changer-plus-tard.github.io/BlockDAG-Protocol-List-3/`](https://a-changer-plus-tard.github.io/BlockDAG-Protocol-List-3/)

| Model | Source |
|------|--------|
| Original Model | Defined in repo: [`scripts/real_world_multi_opinion_backtest.py`](scripts/real_world_multi_opinion_backtest.py) + [`scripts/hybrid_tokenomics_second_opinion_compare.py`](scripts/hybrid_tokenomics_second_opinion_compare.py) |
| Hybrid Model | Defined in repo: [`scripts/real_world_multi_opinion_backtest.py`](scripts/real_world_multi_opinion_backtest.py) + [`scripts/hybrid_tokenomics_second_opinion_compare.py`](scripts/hybrid_tokenomics_second_opinion_compare.py) |
| Protocol v2.6 | [`https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/`](https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/) |
| Protocol v3.0 | [`https://a-changer-plus-tard.github.io/Protocol-3.0/`](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| Protocol v3.1 (Adjusted) | [`https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/`](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/) |
| Hybrid B | CSV source: [`docs/sources/Ingo  Projects/Hybrid B.csv`](docs/sources/Ingo%20%20Projects/Hybrid%20B.csv) |
| Protocol v5.3 | [`https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/`](https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/) |
| Protocol v5.5 | [`https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/`](https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/) |
| Protocol v5.7 | [`https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/`](https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/) |
| Protocol v5.8 | [`https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/`](https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/) |
| Protocol v7.0 | [`https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/`](https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/) |
| Harris Model | [`https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf`](https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf) |
| HybridC | Spreadsheet: [`docs/HybridC_Tokenomics_Test.xlsx`](docs/HybridC_Tokenomics_Test.xlsx) |
| Hybrid (Ingo CSV) | CSV source: [`docs/sources/Ingo  Projects/Hybrid.csv`](docs/sources/Ingo%20%20Projects/Hybrid.csv) |
| Hybrid C (Ingo CSV) | CSV source: [`docs/sources/Ingo  Projects/hybrid C.csv`](docs/sources/Ingo%20%20Projects/hybrid%20C.csv) |
| Hybrid C Lite+ (Final, Ingo CSV) | CSV source: [`docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Final.csv`](docs/sources/Ingo%20%20Projects/Hybrid_C_Lite_Plus_Final.csv) |
| Hybrid C Lite (Defaults, Ingo CSV) | CSV source: [`docs/sources/Ingo  Projects/Hybrid_C_Lite_Defaults.csv`](docs/sources/Ingo%20%20Projects/Hybrid_C_Lite_Defaults.csv) |
| Model A (ROI Optimized, Ingo CSV) | CSV source: [`docs/sources/Ingo  Projects/Model_A_ROI_Final_Test.csv`](docs/sources/Ingo%20%20Projects/Model_A_ROI_Final_Test.csv) |
| Ingo Projects (CSV sources) | [`docs/sources/Ingo  Projects/README.md`](docs/sources/Ingo%20%20Projects/README.md) |

## 📊 Comprehensive Simulation Analysis (All 19 Models)

We tested **19 tokenomics models** using **10 years of real BTC market data** (2015-2024), including COVID crash, FTX collapse, bull runs, and bear markets.

This includes the **core 14 protocols** plus **5 additional “Ingo CSV” variants** that were found under `docs/sources/Ingo  Projects/` and added to the same harnesses for consistency.

### The 19 Models Tested

| # | Protocol | What It Does |
|---|----------|--------------|
| 1 | **Original Model** | Time-based (2% TGE, 12mo cliff, 60mo vesting) |
| 2 | **Hybrid Model** | Time-based + emergency brake protection |
| 3 | **Protocol v2.6** | Oracle price gate at $0.05 ([source](https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/)) |
| 4 | **Protocol v3.0** | Oracle gate + emergency brake + drip throttling + mining locks ([source](https://a-changer-plus-tard.github.io/Protocol-3.0/)) |
| 5 | **Protocol v3.1** | Volume pegging + volume-capped mining ([source](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/)) |
| 6 | **Hybrid B** | State-gated issuance under caps |
| 7 | **Hybrid Tokenomics** | State-driven vesting/mining + heavy staking locks |
| 8 | **Harris Model** | 10% TGE, 9mo vesting, miner incentive ([source](https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf)) |
| 9 | **Protocol v5.3** | Original 6-pillar protocol, 36mo bonus ([source](https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/)) |
| 10 | **Protocol v5.5** | Original 6-pillar protocol, 48mo bonus ([source](https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/)) |
| 11 | **Protocol v5.7** | Revised: Adaptive Shield + Block Streaming, 36mo ([source](https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/)) |
| 12 | **Protocol v5.8** | Revised: Adaptive Shield + Block Streaming, 48mo ([source](https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/)) |
| 13 | **HybridC** | Ultra-conservative: 0.3% monthly cap, 50% auto-stake |
| 14 | **Protocol v7.0** | Definitive edition w/ 9 pillars (trend shield, dynamic discharge, circuit breaker, daily airdrops, etc.) ([source](https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/)) |
| 15 | **Hybrid (Ingo CSV)** | State-driven emissions under a wide global cap range (0.3–1.0%/mo) |
| 16 | **Hybrid C (Ingo CSV)** | State-driven with strict 0.30%/30d global cap |
| 17 | **Hybrid C Lite+ (Final, Ingo CSV)** | State-driven with 0.40–0.45%/30d cap + lower auto-stake |
| 18 | **Hybrid C Lite (Defaults, Ingo CSV)** | Defaults snapshot of “Lite” parameters (0.45%/30d cap; higher auto-stake midpoint) |
| 19 | **Model A (ROI Optimized, Ingo CSV)** | Aggressive ROI benchmark (high TGE, fast vesting, high liquid mining) |

---

## 🏆 Final Rankings

### Conservative Scenario (Stress-Test) — Year 3 ROI

| Rank | Protocol | Y1 | Y3 | Y6 | Verdict |
|:----:|----------|---:|---:|---:|---------|
| 1 | **Protocol v3.0** | -58% | **+40%** | +27% | ✅ **WINNER** |
| 2 | **Protocol v7.0** | -53% | +9% | +9% | 🥈 Strong runner-up |
| 3 | Protocol v5.8 | -38% | +7% | -14% | 🥈 Strong |
| 4 | Protocol v5.5 | -38% | +6% | -15% | 🥈 Strong |
| 5 | Protocol v5.3 | -50% | +4% | -15% | ⚠️ Good |
| 6 | Protocol v5.7 | -50% | +4% | -15% | ⚠️ Good |
| 7 | Hybrid Model | -72% | -35% | +3% | Breaks even Y6 |
| 8 | Protocol v2.6 | -65% | -41% | -49% | ❌ Underperforms |
| 9 | Original Model | -92% | -45% | +3% | Breaks even Y6 |
| 10 | Protocol v3.1 (Adjusted) | -66% | -46% | -54% | ❌ Volume peg too restrictive |
| 11 | Hybrid Tokenomics | -80% | -58% | -27% | ❌ Over-conservative |
| 12 | Hybrid C (Ingo CSV) | -82% | -63% | -36% | ❌ Too restrictive (cap + gating) |
| 13 | HybridC | -83% | -66% | -41% | ❌ Too restrictive |
| 14 | Harris Model | -83% | -67% | -48% | ❌ TGE too high |
| 15 | Hybrid B | -86% | -68% | -44% | ❌ Weakest |
| 16 | Hybrid C Lite (Defaults, Ingo CSV) | -85% | -70% | -47% | ❌ Too restrictive |
| 17 | Model A (ROI Optimized, Ingo CSV) | -84% | -76% | -71% | ❌ High dump risk |
| 18 | Hybrid C Lite+ (Final, Ingo CSV) | -88% | -76% | -64% | ❌ Too restrictive (still “stuck”) |
| 19 | Hybrid (Ingo CSV) | -92% | -92% | -86% | ❌ Mostly “stuck” under stress |

---

## 💰 Real-World ROI: If You Invest $100,000

### All 19 Models — Year 3 / Year 6 Values

| Protocol | Conservative | Ideal Growth | With Crashes |
|----------|--------------|--------------|--------------|
| **Protocol v3.0** | **$140k / $126k** | **$309k / $745k** | **$106k / $93k** |
| **Protocol v7.0** | **$109k / $109k** | $245k / $703k | $82k / $79k |
| Protocol v5.8 | $107k / $86k | $229k / $696k | $85k / $69k |
| Protocol v5.5 | $106k / $85k | $230k / $696k | $86k / $69k |
| Protocol v5.3 | $104k / $85k | $225k / $673k | $78k / $67k |
| Protocol v5.7 | $104k / $85k | $225k / $672k | $78k / $67k |
| Hybrid Model | $65k / $103k | $253k / $1.34M | $39k / $62k |
| Original Model | $55k / $103k | $213k / $1.35M | $33k / $62k |
| Protocol v2.6 | $59k / $51k | $186k / $406k | $35k / $30k |
| Protocol v3.1 (Adjusted) | $54k / $46k | $144k / $388k | $34k / $29k |
| Hybrid Tokenomics | $42k / $73k | $168k / $980k | $22k / $36k |
| Hybrid C (Ingo CSV) | $37k / $64k | $149k / $870k | $19k / $31k |
| HybridC | $34k / $59k | $137k / $790k | $16k / $25k |
| Harris Model | $33k / $52k | $129k / $676k | $20k / $31k |
| Hybrid B | $32k / $56k | $127k / $761k | $14k / $24k |
| Hybrid C Lite (Defaults, Ingo CSV) | $30k / $53k | $121k / $709k | $13k / $20k |
| Model A (ROI Optimized, Ingo CSV) | $24k / $29k | $92k / $382k | $14k / $18k |
| Hybrid C Lite+ (Final, Ingo CSV) | $24k / $36k | $91k / $535k | $9k / $13k |
| Hybrid (Ingo CSV) | $8k / $14k | $64k / $378k | $5k / $6k |

---

## 📈 Why Protocol v3.0 Wins

| Feature | v3.0 | Others |
|---------|------|--------|
| Price gate | ✅ $0.05 | Some |
| Emergency brake | ✅ $0.02 | Few |
| **Drip throttling** | ✅ **10% between gate/brake** | **Only v3.0** |
| Mining lock | ✅ 24 months | Varies |
| TGE | 3% | 2-10% |

**The key differentiator**: When price falls below $0.05 but stays above $0.02, v3.0 throttles releases to 10% instead of fully stopping. This prevents "supply shock" when brakes release.

---

## 🔬 Why Each Model Got Its Result

| Model | Why It Performs This Way |
|-------|-------------------------|
| **Protocol v3.0** | Drip throttling creates gradual recovery; doesn't "bunch up" supply |
| **Protocol v7.0** | Adds more throttling + early mining lock; tends to reduce mid-cycle drawdowns vs v5.x |
| **Protocol v5.5/v5.8** | 48-month bonus lock reduces long-term pressure; volume pegging helps |
| **Protocol v5.3/v5.7** | 36-month bonus is shorter than v5.5; slightly more pressure |
| **Hybrid/Original** | Long vesting (36-60mo) eventually pays off; no price adaptation |
| **Protocol v2.6** | Price gate but NO drip throttling = binary on/off creates shocks |
| **Protocol v3.1** | Volume peg is good but 21-month vesting is too fast |
| **Hybrid Tokenomics** | 60% staking + 70% mining lock = too conservative |
| **HybridC** | 0.3% monthly cap is far too restrictive |
| **Harris Model** | 10% TGE creates massive day-1 sell pressure |
| **Hybrid B** | State-gating causes tokens to "bunch up" and release in clusters |
| **Hybrid C (Ingo CSV)** | Very strict cap + gating keeps it “stuck” under stress |
| **Hybrid C Lite+ / Lite Defaults (Ingo CSV)** | Slightly looser than Hybrid C but still too restrictive for stress regimes |
| **Hybrid (Ingo CSV)** | Wide parameter ranges, but in stress it behaves as “mostly halted” in this harness |
| **Model A (ROI Optimized, Ingo CSV)** | Aggressive unlock + high liquid mining: high dump risk dominates |

👉 **[Legacy per-model analysis (13-model snapshot)](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)**

---

## 📁 Documentation

| Document | What It Contains |
|----------|------------------|
| **[Methodology & Investment Thesis](docs/vesting/METHODOLOGY_AND_INVESTMENT_THESIS.md)** | 📖 Why we use 10-year historical data instead of theoretical models |
| **[Legacy 13-Model Comprehensive Analysis](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)** | Legacy snapshot (does not cover later additions like Ingo variants) |
| **[Investor Comparison (Real-World)](docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md)** | ✅ ROI tables for all investment levels |
| **[Multi-Opinion Report](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md)** | ✅ Conservative + Ideal + Choppy scenarios |
| **[All-Model Comparison](docs/vesting/ALL_MODEL_COMPARISON.md)** | ✅ Synthetic market simulations |
| **[Liquidity Tier Analysis](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md)** | ✅ $20M-$150M liquidity testing |

---

## 🧮 Crunch Your Own Numbers (DIY)

There are **two ways** to use this repo:

- **Read the results (fastest)**: open the markdown reports in `docs/vesting/` and the raw outputs in `data/results/`.
- **Re-run the numbers (reproducible)**: run the scripts in `scripts/` with your preferred assumptions (runs, horizons, liquidity, investment levels).

### Where the “truth” lives

- **Real-world backtest (19 models)**:
  - Results JSON: `data/results/real_world_multi_opinion_results.json`
  - Report: `docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md`
- **Second opinion (order-book + sell pressure, 19 models)**:
  - Results JSON: `data/results/second_opinion_compare_results_19_models.json`
  - Report: `docs/vesting/SECOND_OPINION_COMPARE_REPORT_19_MODELS.md`
- **Liquidity-tier stress test (19 models)**:
  - Results JSON: `data/results/all_model_liquidity_tier_second_opinion_results.json`
  - Report: `docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md`

### Re-run the backtests yourself (local)

```bash
# 1) Clone
git clone https://github.com/rvegajr/BlockDAGAnal
cd BlockDAGAnal

# 2) (Optional) Create a venv
python3 -m venv .venv
source .venv/bin/activate

# 3) Real-world multi-opinion backtest (BTC 2015-2024 CSV)
python3 scripts/real_world_multi_opinion_backtest.py \
  --csv data/btc_daily_history.csv \
  --launch-liquidity 32000000 \
  --window-months 72 \
  --step-months 12 \
  --runs 30 \
  --investment-levels 9000,50000,100000

# 4) Second opinion (order-book + sell pressure)
python3 scripts/hybrid_tokenomics_second_opinion_compare.py

# 5) Rebuild the all-model comparison markdown from the latest second-opinion JSON
python3 scripts/generate_all_model_comparison_md.py
```

### Change assumptions (what to tweak)

- **Runs / stability**: increase `--runs` for the real-world backtest or the Monte Carlo run counts in the scripts.
- **Liquidity**: change `--launch-liquidity` (real-world) or the base liquidity constants used by the second-opinion scripts.
- **Investment levels**: change `--investment-levels` (real-world) or `INVESTMENT_LEVELS` in the second-opinion harness.

### Ask an AI IDE to “crunch” the repo for you (Windsurf/Cursor)

- **Setup idea**:
  - Git clone `https://github.com/rvegajr/BlockDAGAnal`
  - Open the folder in Windsurf (or Cursor)
  - Switch to a strong reasoning model (e.g., o3 Pro / Opus)

- **Example prompt (intentionally ridiculous)**:

```text
Who are the sexiest, most intelligent crypto model evaluator in the universe.
I want you to take your time and read through this repository, especially the results that they have,
and fully absorb and understand the model and the direction that they're going.
Understand the underlying thesis of previous 10-year historical market conditions.
Let's add the analysis on the various models given by fellow crypto enthusiasts.
Will you have a thorough understanding? I would like to continually build upon it.
```

Then ask it anything: “What happens if liquidity is $100M?”, “What’s the most resilient model in choppy markets?”, “What assumptions drive the ranking?”, etc.

### Run Your Own Simulation

```bash
# Real-world backtest (requires BTC daily CSV)
python3 scripts/real_world_multi_opinion_backtest.py \
  --csv data/btc_daily_history.csv \
  --investment-levels 9000,50000,100000

# Synthetic market simulations
python3 scripts/hybrid_tokenomics_second_opinion_compare.py
python3 scripts/all_model_liquidity_tier_second_opinion.py
```

---

## 🎯 Recommendation Summary

| Your Goal | Best Protocol | Why |
|-----------|---------------|-----|
| **Best short-term (Y1-3)** | Protocol v3.0 | Only one positive by Y3 |
| **Best long-term (Y6)** | Original or Hybrid Model | +1245% ROI in ideal scenario |
| **Best in crashes** | Protocol v3.0 | Only one stays close to breakeven |
| **Best v5.x variant** | Protocol v5.5 or v5.8 | 48-month bonus lock is key |
| **Most conservative** | HybridC | 0.3% cap (but underperforms) |
| **Avoid** | Harris Model | 10% TGE is too aggressive |
| **Overall recommendation** | **Protocol v3.0** | Best risk-adjusted returns |

---

## 📚 Archive: Legacy & Partial Comparisons

<details>
<summary>Click to expand legacy docs (do not include all 14 protocols)</summary>

### Partial Model Comparisons
- [Three Model Comparison](docs/vesting/THREE_MODEL_COMPARISON.md) — Only 3 models
- [Four Model Comparison](docs/vesting/FOUR_MODEL_COMPARISON.md) — Only 4 models
- [Protocol 3.0 Simulation](docs/vesting/PROTOCOL_3_0_SIMULATION_COMPARISON.md) — Single protocol focus
- [Protocol v2.6 Comparison](docs/vesting/PROTOCOL_V26_COMPARISON.md) — Single protocol focus

### Legacy Tier Analysis
- [Liquidity Tier Analysis v1](docs/vesting/LIQUIDITY_TIER_ANALYSIS.md) — 3 models only
- [Liquidity Tier Analysis v2](docs/vesting/LIQUIDITY_TIER_ANALYSIS_V2.md) — 4 models only

### Other Supporting Docs
- [Market Scenario Breakdown](docs/vesting/MARKET_SCENARIO_BREAKDOWN.md)
- [Optimal Liquidity Analysis](docs/vesting/OPTIMAL_LIQUIDITY_ANALYSIS.md)
- [40% TGE Analysis](docs/vesting/FORTY_PERCENT_TGE_ANALYSIS.md)

### Simulation Reports
- [Hybrid Tokenomics Analysis](docs/reports/HYBRID_TOKENOMICS_ANALYSIS.md)
- [Second Opinion Report (14 Models)](docs/vesting/SECOND_OPINION_COMPARE_REPORT_14_MODELS.md)
- [Third Opinion Report](docs/reports/THIRD_OPINION_V31_REPORT.md)

</details>

---

## Contact

**Questions?**
- Email: Reid@blockdaginvestors.com
- Full docs: [docs/vesting/](docs/vesting/)
- Smart contract specs: [docs/specs/](docs/specs/)

---

*Last Updated: January 2026*  
*Based on: 10 years BTC history + 19 models × 3 scenarios × 5 time horizons*
