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
| Protocol v5.3 | [`https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/`](https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/) |
| Protocol v5.5 | [`https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/`](https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/) |
| Protocol v5.7 | [`https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/`](https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/) |
| Protocol v5.8 | [`https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/`](https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/) |
| Protocol v7.0 | [`https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/`](https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/) |
| Harris Model | [`https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf`](https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf) |
| HybridC | Spreadsheet: [`docs/HybridC_Tokenomics_Test.xlsx`](docs/HybridC_Tokenomics_Test.xlsx) |
| Ingo Projects (CSV sources) | [`docs/sources/Ingo  Projects/README.md`](docs/sources/Ingo%20%20Projects/README.md) |

## 📊 Comprehensive Simulation Analysis (All 14 Protocols)

We tested **14 tokenomics protocols** using **10 years of real BTC market data** (2015-2024), including COVID crash, FTX collapse, bull runs, and bear markets.

### The 14 Protocols Tested

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

---

## 🏆 Final Rankings

### Conservative Scenario (Stress-Test) — Year 3 ROI

| Rank | Protocol | Y1 | Y3 | Y6 | Verdict |
|:----:|----------|---:|---:|---:|---------|
| 1 | **Protocol v3.0** | -58% | **+40%** | +27% | ✅ **WINNER** |
| 2 | **Protocol v7.0** | -52% | +9% | +9% | 🥈 Strong runner-up |
| 3 | Protocol v5.8 | -37% | +7% | -14% | 🥈 Strong |
| 4 | Protocol v5.5 | -38% | +7% | -15% | 🥈 Strong |
| 5 | Protocol v5.7 | -50% | +4% | -15% | ⚠️ Good |
| 6 | Protocol v5.3 | -50% | +4% | -15% | ⚠️ Good |
| 7 | Hybrid Model | -72% | -35% | +3% | Breaks even Y6 |
| 8 | Protocol v2.6 | -65% | -41% | -49% | ❌ Underperforms |
| 9 | Original Model | -92% | -45% | +3% | Breaks even Y6 |
| 10 | Protocol v3.1 | -66% | -47% | -54% | ❌ Volume peg too restrictive |
| 11 | Hybrid Tokenomics | -80% | -58% | -27% | ❌ Over-conservative |
| 12 | HybridC | -83% | -66% | -41% | ❌ Too restrictive |
| 13 | Harris Model | -83% | -67% | -48% | ❌ TGE too high |
| 14 | Hybrid B | -86% | -68% | -44% | ❌ Weakest |

---

## 💰 Real-World ROI: If You Invest $100,000

### All 14 Protocols — Year 3 / Year 6 Values

| Protocol | Conservative | Ideal Growth | With Crashes |
|----------|--------------|--------------|--------------|
| **Protocol v3.0** | **$140k / $126k** | **$309k / $745k** | **$106k / $93k** |
| **Protocol v7.0** | **$109k / $109k** | $245k / $703k | $82k / $79k |
| Protocol v5.8 | $107k / $86k | $229k / $695k | $85k / $69k |
| Protocol v5.5 | $107k / $85k | $229k / $696k | $85k / $69k |
| Protocol v5.7 | $104k / $85k | $224k / $673k | $79k / $67k |
| Protocol v5.3 | $104k / $85k | $225k / $673k | $78k / $67k |
| Hybrid Model | $65k / $103k | $253k / $1.34M | $39k / $62k |
| Original Model | $55k / $103k | $213k / $1.35M | $33k / $62k |
| Protocol v2.6 | $59k / $51k | $186k / $406k | $35k / $30k |
| Protocol v3.1 | $54k / $46k | $145k / $387k | $34k / $29k |
| Hybrid Tokenomics | $42k / $73k | $168k / $980k | $22k / $36k |
| HybridC | $34k / $59k | $137k / $790k | $16k / $25k |
| Harris Model | $33k / $52k | $129k / $676k | $20k / $31k |
| Hybrid B | $32k / $56k | $127k / $761k | $14k / $24k |

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

👉 **[Full per-model analysis with detailed explanations](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)**

---

## 📁 Documentation

| Document | What It Contains |
|----------|------------------|
| **[Methodology & Investment Thesis](docs/vesting/METHODOLOGY_AND_INVESTMENT_THESIS.md)** | 📖 Why we use 10-year historical data instead of theoretical models |
| **[13-Model Comprehensive Analysis](docs/vesting/13_MODEL_COMPREHENSIVE_ANALYSIS.md)** | ✅ Full analysis of the first 13 protocols (v7.0 pending write-up) |
| **[Investor Comparison (Real-World)](docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md)** | ✅ ROI tables for all investment levels |
| **[Multi-Opinion Report](docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md)** | ✅ Conservative + Ideal + Choppy scenarios |
| **[All-Model Comparison](docs/vesting/ALL_MODEL_COMPARISON.md)** | ✅ Synthetic market simulations |
| **[Liquidity Tier Analysis](docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md)** | ✅ $20M-$150M liquidity testing |

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
*Based on: 10 years BTC history + 14 protocols × 3 scenarios × 5 time horizons*
