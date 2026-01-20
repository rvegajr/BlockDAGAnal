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
| Original Model | Defined in repo: [`scripts/real_world_multi_opinion_backtest.py`](scripts/real_world_multi_opinion_backtest.py) |
| Hybrid Model | Defined in repo: [`scripts/real_world_multi_opinion_backtest.py`](scripts/real_world_multi_opinion_backtest.py) |
| Protocol v2.6 | [`a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6`](https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/) |
| Protocol v3.0 | [`a-changer-plus-tard.github.io/Protocol-3.0`](https://a-changer-plus-tard.github.io/Protocol-3.0/) |
| Protocol v3.1 | [`a-changer-plus-tard.github.io/Protocol-3.1-Ajusted`](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/) |
| Protocol v5.3 | [`a-changer-plus-tard.github.io/Protocol-v5.3-Original`](https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/) |
| Protocol v5.5 | [`a-changer-plus-tard.github.io/Protocol-v5.5-Original`](https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/) |
| Protocol v5.7 | [`a-changer-plus-tard.github.io/Protocol-v5.7-Revised`](https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/) |
| Protocol v5.8 | [`a-changer-plus-tard.github.io/Protocol-v5.8-Revised`](https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/) |
| Protocol v7.0 | [`a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0`](https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/) |
| Harris Model | [`github.com/harrisjustinhagen-oss`](https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf) |
| HybridC | Spreadsheet: [`docs/HybridC_Tokenomics_Test.xlsx`](docs/HybridC_Tokenomics_Test.xlsx) |
| Community CSV Models (17) | [`docs/sources/Ingo Projects/`](docs/sources/Ingo%20%20Projects/) — See [analysis](docs/reports/INGO_MODEL_ANALYSIS.md) |

## 📊 Comprehensive Simulation Analysis (All 31 Models)

We tested **31 tokenomics models** using **10 years of real BTC market data** (2015-2024), including COVID crash, FTX collapse, bull runs, and bear markets.

This includes the **core 14 protocols** plus **17 community-submitted variants** from CSV specifications.

### The 31 Models Tested

| # | Protocol | What It Does |
|---|----------|--------------|
| 1 | **Original Model** | Time-based (2% TGE, 12mo cliff, 60mo vesting) |
| 2 | **Hybrid Model** | Time-based + emergency brake protection |
| 3 | **Protocol v2.6** | Oracle price gate at $0.05 |
| 4 | **Protocol v3.0** | Oracle gate + emergency brake + drip throttling + mining locks |
| 5 | **Protocol v3.1** | Volume pegging + volume-capped mining |
| 6 | **Hybrid B** | State-gated issuance under caps |
| 7 | **Hybrid Tokenomics** | State-driven vesting/mining + heavy staking locks |
| 8 | **Harris Model** | 10% TGE, 9mo vesting, miner incentive |
| 9 | **Protocol v5.3** | Original 6-pillar protocol, 36mo bonus |
| 10 | **Protocol v5.5** | Original 6-pillar protocol, 48mo bonus |
| 11 | **Protocol v5.7** | Revised: Adaptive Shield + Block Streaming, 36mo |
| 12 | **Protocol v5.8** | Revised: Adaptive Shield + Block Streaming, 48mo |
| 13 | **HybridC** | Ultra-conservative: 0.3% monthly cap, 50% auto-stake |
| 14 | **Protocol v7.0** | Definitive edition w/ 9 pillars |
| 15-31 | **Community CSV Models** | 17 variants with different risk-reward profiles (see [full list](docs/sources/Ingo%20%20Projects/README.md)) |

---

## 🏆 Final Rankings

### Conservative Scenario (Stress-Test) — 72-Month ROI

| Rank | Protocol | M12 | M36 | M72 | Verdict |
|:----:|----------|----:|----:|----:|---------|
| 1 | **Protocol v3.0** | -54% | **+34%** | **+23%** | ✅ **WINNER** |
| 2 | **Protocol v7.0** | -50% | +5% | +4% | 🥈 Strong runner-up |
| 3 | Protocol v5.8 | -31% | +4% | -18% | 🥈 Best early returns |
| 4 | Protocol v5.5 | -32% | +4% | -18% | 🥈 Strong |
| 5 | Protocol v5.3 | -48% | 0% | -19% | ⚠️ Good |
| 6 | Protocol v5.7 | -48% | 0% | -19% | ⚠️ Good |
| 7 | Original Model | -92% | -46% | +2% | Long-term recovery |
| 8 | Hybrid Model | -73% | -36% | +2% | Long-term recovery |
| 9 | Hybrid Tokenomics | -80% | -59% | -30% | ❌ Over-conservative |
| 10 | Protocol v2.6 | -65% | -42% | -50% | ❌ Binary gate problem |
| 11 | Protocol v3.1 | -66% | -48% | -55% | ❌ Volume peg too restrictive |
| 12+ | Community CSV Models | -82% to -94% | -63% to -90% | -41% to -84% | Varies by config |

---

## 💰 Real-World ROI: If You Invest $100,000

### Top 14 Core Models — M36 / M72 Values

| Protocol | Conservative | Ideal Growth | Choppy Stress |
|----------|--------------|--------------|---------------|
| **Protocol v3.0** | **$134k / $123k** | **$292k / $733k** | **$102k / $90k** |
| **Protocol v7.0** | **$105k / $104k** | $232k / $684k | $79k / $76k |
| Protocol v5.8 | $104k / $82k | $212k / $685k | $82k / $67k |
| Protocol v5.5 | $104k / $82k | $212k / $685k | $82k / $67k |
| Protocol v5.3 | $100k / $81k | $210k / $662k | $75k / $65k |
| Protocol v5.7 | $100k / $81k | $210k / $662k | $75k / $65k |
| Hybrid Model | $64k / $102k | $245k / $1.32M | $39k / $61k |
| Original Model | $54k / $102k | $207k / $1.32M | $33k / $61k |
| Protocol v2.6 | $58k / $50k | $179k / $406k | $35k / $30k |
| Protocol v3.1 | $52k / $45k | $139k / $379k | $32k / $28k |
| Hybrid Tokenomics | $42k / $70k | $163k / $965k | $21k / $35k |
| HybridC | $33k / $54k | $132k / $778k | $16k / $25k |
| Harris Model | $33k / $51k | $125k / $666k | $20k / $31k |
| Hybrid B | $29k / $52k | $124k / $750k | $14k / $23k |

*31 models tested total. See [Multi-Opinion Report](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md) for complete results.*

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
| **Protocol v7.0** | Adds more throttling + early mining lock; reduces mid-cycle drawdowns |
| **Protocol v5.5/v5.8** | 48-month bonus lock reduces long-term pressure; volume pegging helps |
| **Protocol v5.3/v5.7** | 36-month bonus is shorter than v5.5; slightly more pressure |
| **Hybrid/Original** | Long vesting (36-60mo) eventually pays off; no price adaptation |
| **Protocol v2.6** | Price gate but NO drip throttling = binary on/off creates shocks |
| **Protocol v3.1** | Volume peg is good but 21-month vesting is too fast |
| **Hybrid Tokenomics** | 60% staking + 70% mining lock = too conservative |
| **HybridC** | 0.3% monthly cap is far too restrictive |
| **Harris Model** | 10% TGE creates massive day-1 sell pressure |
| **Hybrid B** | State-gating causes tokens to "bunch up" and release in clusters |
| **Community CSV Models** | Various configurations; see [Multi-Opinion Report](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md) |

👉 **[Legacy per-model analysis (13-model snapshot)](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)**

---

## 📁 Documentation

| Document | What It Contains |
|----------|------------------|
| **[Methodology & Investment Thesis](docs/vesting/METHODOLOGY_AND_INVESTMENT_THESIS.md)** | 📖 Why we use 10-year historical data instead of theoretical models |
| **[Multi-Opinion Report (31 Models)](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md)** | ✅ Conservative + Ideal + Choppy scenarios |
| **[Investor Comparison (Real-World)](docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md)** | ✅ ROI tables for all investment levels |
| **[All-Model Comparison](docs/vesting/ALL_MODEL_COMPARISON.md)** | ✅ Synthetic market simulations |
| **[Liquidity Tier Analysis](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md)** | ✅ $20M-$150M liquidity testing |
| **[Community Model Analysis](docs/reports/INGO_MODEL_ANALYSIS.md)** | 📊 Deep-dive on community CSV submissions |
| **[Legacy 13-Model Analysis](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)** | Legacy snapshot (historical reference) |
| **[Unlimited Approval Security Analysis](docs/reports/UNLIMITED_APPROVAL_SECURITY_ANALYSIS.md)** | 🔒 Investigation of "wallet drainer" FUD - DEBUNKED |
| **[Euler Network Investigation](docs/reports/EULER_NETWORK_INVESTIGATION.md)** | 🔍 Full investigative report on BlockDAG/Euler Network rebrand |
| **[Crypto Due Diligence Guide](docs/reports/CRYPTO_DUE_DILIGENCE_GUIDE.md)** | 📝 Medium-style article: 5-minute checklist to spot crypto scams |

---

## 🧮 Crunch Your Own Numbers (DIY)

There are **two ways** to use this repo:

- **Read the results (fastest)**: open the markdown reports in `docs/vesting/` and the raw outputs in `data/results/`.
- **Re-run the numbers (reproducible)**: run the scripts in `scripts/` with your preferred assumptions (runs, horizons, liquidity, investment levels).

### Where the "truth" lives

- **Real-world backtest (31 models)**:
  - Results JSON: `data/results/real_world_multi_opinion_results.json`
  - Report: `docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md`
- **Second opinion (order-book + sell pressure)**:
  - Results JSON: `data/results/second_opinion_compare_results_19_models.json`
  - Report: `docs/vesting/SECOND_OPINION_COMPARE_REPORT_19_MODELS.md`
- **Liquidity-tier stress test**:
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
| **Best short-term (M12-24)** | Protocol v5.8 | Best early ROI (-18% vs -54% others at M12) |
| **Best mid-term (M36)** | Protocol v3.0 | Only one positive (+34%) in stress |
| **Best long-term (M72)** | Original or Hybrid Model | +1224% ROI in ideal scenario |
| **Best in crashes** | Protocol v3.0 | Best choppy resilience (-10% vs -35% avg) |
| **Best v5.x variant** | Protocol v5.5 or v5.8 | 48-month bonus lock is key |
| **Most conservative** | HybridC | 0.3% cap (but underperforms) |
| **Avoid** | Harris Model | 10% TGE is too aggressive |
| **Overall recommendation** | **Protocol v3.0** | Best risk-adjusted returns across all scenarios |

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

*Last Updated: January 19, 2026*  
*Based on: 10 years BTC history + 31 models × 3 opinions × 10 choppy scenarios × 5 time horizons*
