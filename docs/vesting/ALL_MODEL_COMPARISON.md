# All Model Comparison: Investor Returns (Second Opinion, Order-Book + Sell Pressure)

**Generated**: 2026-01-05T23:05:35.591127

This document mirrors the *format/style* of `docs/vesting/THREE_MODEL_COMPARISON.md`, but covers **all models** currently tested.

## Methodology (Second Opinion)
- **Pricing**: baseline (Liquidity / Circulating) + order-book depth + sell-pressure impacts
- **Liquidity base**: $32,000,000
- **Investment reference**: $9,000
- **ROI horizons**: 12, 24, 36, 48, 72 months
- **Runs**: 100 sims/model across bull/bear/normal/volatile + 100 runs/model per each of 10 choppy scenarios

## Executive Summary (multi-horizon)
### Overall winner (raw ROI) by horizon

| Horizon | Winner | Avg ROI |
|---:|---|---:|
| Month 12 | **Protocol v5.7** | **-61.0%** |
| Month 24 | **Protocol v3.0** | **-34.7%** |
| Month 36 | **Protocol v3.0** | **-33.8%** |
| Month 48 | **Protocol v3.0** | **-49.3%** |
| Month 72 | **Protocol v3.0** | **-65.2%** |

### Best balance (ROI + access) by horizon

| Horizon | Best balance | Avg ROI | Brake rate |
|---:|---|---:|---:|
| Month 12 | **Hybrid Tokenomics (Solvency-Anchored)** | -86.4% | 3.0% |
| Month 24 | **Hybrid Tokenomics (Solvency-Anchored)** | -84.7% | 8.0% |
| Month 36 | **Protocol v3.0** | -33.8% | 98.0% |
| Month 48 | **Protocol v3.0** | -49.3% | 100.0% |
| Month 72 | **Protocol v3.0** | -65.2% | 100.0% |

### Avg choppy-market ROI (10 scenarios) by horizon

| Horizon | Winner | Avg choppy ROI |
|---:|---|---:|
| Month 12 | **Protocol v5.5** | **-77.1%** |
| Month 24 | **Protocol v3.0** | **-55.4%** |
| Month 36 | **Protocol v3.0** | **-56.3%** |
| Month 48 | **Protocol v3.0** | **-67.6%** |
| Month 72 | **Protocol v3.0** | **-78.6%** |

## Model Parameters (high level)
For full model mechanics and definitions see:
- `scripts/hybrid_tokenomics_second_opinion_compare.py`
- `HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`
- Protocol v3.1 reference: `https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/`

## Month-12 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v5.7 | -61.0% | $3,512 | -63.2% | -76.9%..-46.6% | 68.0% | Best ROI (raw), but check brake risk |
| Protocol v5.3 | -61.2% | $3,494 | -63.0% | -76.4%..-49.4% | 70.0% | Trade-off: ROI vs access |
| Protocol v5.5 | -63.3% | $3,302 | -63.6% | -76.9%..-48.6% | 71.0% | Trade-off: ROI vs access |
| Protocol v3.0 | -63.8% | $3,259 | -66.6% | -76.8%..-46.7% | 43.0% | Trade-off: ROI vs access |
| Protocol v5.8 | -64.2% | $3,221 | -63.4% | -76.8%..-49.2% | 72.0% | Trade-off: ROI vs access |
| Protocol v3.1 (Adjusted) | -78.3% | $1,952 | -79.4% | -87.9%..-69.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -79.7% | $1,827 | -80.2% | -88.1%..-68.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -84.9% | $1,360 | -85.7% | -91.5%..-77.1% | 99.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -86.4% | $1,222 | -87.1% | -92.3%..-79.6% | 3.0% | Stable/accessible, weaker ROI |
| HybridC | -89.0% | $990 | -88.9% | -93.8%..-83.0% | 3.0% | Stable/accessible, weaker ROI |
| Hybrid B | -90.4% | $865 | -91.3% | -94.7%..-86.0% | 5.0% | Stable/accessible, weaker ROI |
| Harris Model | -91.0% | $813 | -91.4% | -94.7%..-86.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -95.7% | $383 | -95.9% | -97.6%..-93.6% | 5.0% | Stable/accessible, weaker ROI |

### Month-12 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v5.7 | -50.6% (4%) | -75.8% (100%) | -63.2% (100%) | -54.3% (68%) |
| Protocol v5.3 | -51.5% (8%) | -75.7% (100%) | -62.7% (100%) | -54.8% (72%) |
| Protocol v5.5 | -50.8% (4%) | -75.5% (100%) | -63.1% (100%) | -63.9% (80%) |
| Protocol v3.0 | -48.3% (0%) | -75.5% (100%) | -66.2% (0%) | -65.2% (72%) |
| Protocol v5.8 | -50.9% (0%) | -75.7% (100%) | -63.0% (100%) | -67.3% (88%) |
| Protocol v3.1 (Adjusted) | -69.9% (100%) | -87.4% (100%) | -80.1% (100%) | -75.9% (100%) |
| Protocol v2.6 | -68.5% (100%) | -87.2% (100%) | -79.4% (100%) | -83.6% (100%) |
| Hybrid Model | -77.5% (100%) | -91.0% (100%) | -85.4% (100%) | -85.6% (96%) |
| Hybrid Tokenomics (Solvency-Anchored) | -80.2% (0%) | -91.9% (0%) | -87.0% (0%) | -86.6% (12%) |
| HybridC | -83.3% (0%) | -93.2% (0%) | -89.0% (0%) | -90.5% (12%) |
| Hybrid B | -86.3% (0%) | -94.5% (0%) | -91.3% (0%) | -89.5% (20%) |
| Harris Model | -86.5% (100%) | -94.5% (100%) | -91.2% (100%) | -91.7% (100%) |
| Original Model | -93.7% (0%) | -97.4% (0%) | -95.9% (0%) | -96.0% (20%) |

### Month-12 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 | Protocol v5.5 | Protocol v5.7 | Protocol v5.8 | HybridC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -95.9% | -85.4% | -79.6% | -66.3% | -80.1% | -91.1% | -87.0% | -91.2% | -63.0% | -63.0% | -63.0% | -63.1% | -89.1% |
| May 2021-Style Crash | -98.4% | -94.2% | -91.8% | -80.0% | -91.8% | -97.8% | -94.8% | -96.5% | -83.3% | -83.3% | -83.3% | -83.3% | -97.3% |
| FTX Collapse | -98.8% | -95.6% | -93.9% | -85.0% | -93.8% | -98.3% | -97.6% | -97.4% | -87.5% | -87.5% | -87.5% | -87.5% | -98.0% |
| COVID Black Swan | -99.2% | -97.1% | -95.9% | -90.0% | -95.9% | -98.9% | -98.4% | -98.2% | -91.5% | -91.5% | -91.6% | -91.5% | -98.6% |
| Gradual Bear Market | -97.7% | -91.7% | -88.4% | -77.5% | -88.5% | -94.9% | -92.6% | -95.0% | -77.5% | -77.5% | -77.5% | -77.5% | -93.8% |
| Bull Run Then Crash | -97.5% | -91.2% | -87.7% | -82.1% | -88.2% | -94.6% | -92.4% | -94.7% | -77.0% | -77.0% | -77.0% | -77.1% | -93.6% |
| High Volatility | -97.8% | -92.2% | -89.1% | -78.8% | -89.2% | -97.0% | -93.0% | -95.3% | -79.3% | -79.2% | -79.2% | -79.2% | -94.2% |
| Stable Growth | -94.9% | -81.9% | -74.6% | -58.1% | -75.6% | -89.0% | -83.8% | -89.0% | -57.3% | -57.3% | -57.5% | -57.4% | -86.4% |
| Early Crash with Recovery | -96.2% | -86.4% | -80.9% | -67.3% | -80.8% | -92.3% | -89.0% | -91.8% | -63.1% | -63.1% | -63.1% | -63.1% | -90.2% |
| Multiple Crashes | -99.1% | -96.9% | -95.6% | -90.2% | -95.6% | -98.8% | -98.2% | -98.1% | -91.0% | -91.0% | -91.0% | -91.0% | -98.5% |

## Month-24 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -34.7% | $5,876 | -36.4% | -49.0%..-18.0% | 70.0% | Best ROI (raw), but check brake risk |
| Protocol v5.3 | -39.8% | $5,414 | -40.2% | -62.2%..-21.0% | 98.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.7 | -39.9% | $5,409 | -40.6% | -63.2%..-19.1% | 98.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.5 | -42.2% | $5,198 | -41.1% | -63.4%..-20.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.8 | -43.6% | $5,076 | -41.1% | -63.1%..-21.0% | 99.0% | High gate/brake risk (often “stuck”) |
| Protocol v3.1 (Adjusted) | -76.2% | $2,142 | -77.5% | -86.9%..-66.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -78.1% | $1,969 | -78.7% | -87.3%..-65.6% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -83.8% | $1,459 | -84.6% | -90.8%..-75.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -84.7% | $1,377 | -85.1% | -91.1%..-76.4% | 8.0% | Trade-off: ROI vs access |
| Original Model | -87.5% | $1,127 | -87.9% | -92.9%..-81.2% | 97.0% | High gate/brake risk (often “stuck”) |
| HybridC | -89.1% | $985 | -87.4% | -97.5%..-80.5% | 35.0% | Trade-off: ROI vs access |
| Hybrid B | -89.7% | $925 | -89.4% | -97.7%..-83.3% | 32.0% | Trade-off: ROI vs access |
| Harris Model | -91.3% | $780 | -91.6% | -95.0%..-86.9% | 100.0% | High gate/brake risk (often “stuck”) |

### Month-24 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -20.6% (0%) | -46.1% (100%) | -36.2% (100%) | -36.0% (80%) |
| Protocol v5.3 | -22.4% (100%) | -61.3% (100%) | -39.9% (100%) | -35.7% (92%) |
| Protocol v5.7 | -21.6% (100%) | -61.6% (100%) | -40.7% (100%) | -35.7% (92%) |
| Protocol v5.5 | -21.7% (100%) | -61.1% (100%) | -40.6% (100%) | -45.7% (100%) |
| Protocol v5.8 | -21.7% (100%) | -61.4% (100%) | -40.3% (100%) | -51.0% (96%) |
| Protocol v3.1 (Adjusted) | -66.8% (100%) | -86.3% (100%) | -78.2% (100%) | -73.4% (100%) |
| Protocol v2.6 | -66.1% (100%) | -86.3% (100%) | -77.8% (100%) | -82.4% (100%) |
| Hybrid Model | -75.8% (100%) | -90.3% (100%) | -84.3% (100%) | -84.6% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -77.0% (0%) | -90.6% (0%) | -85.0% (0%) | -86.2% (32%) |
| Original Model | -81.5% (100%) | -92.4% (100%) | -87.9% (100%) | -88.1% (88%) |
| HybridC | -80.9% (0%) | -97.0% (96%) | -87.5% (0%) | -90.8% (44%) |
| Hybrid B | -83.6% (0%) | -97.6% (100%) | -89.4% (0%) | -88.4% (28%) |
| Harris Model | -87.1% (100%) | -94.8% (100%) | -91.5% (100%) | -92.0% (100%) |

### Month-24 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 | Protocol v5.5 | Protocol v5.7 | Protocol v5.8 | HybridC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -88.0% | -84.4% | -78.0% | -36.9% | -78.3% | -89.2% | -84.9% | -91.6% | -40.4% | -40.4% | -40.3% | -40.4% | -87.6% |
| May 2021-Style Crash | -95.2% | -93.8% | -91.2% | -56.0% | -91.2% | -98.5% | -97.8% | -96.6% | -74.1% | -74.1% | -74.1% | -74.1% | -98.2% |
| FTX Collapse | -96.4% | -95.3% | -93.4% | -67.0% | -93.3% | -98.8% | -98.4% | -97.5% | -80.5% | -80.5% | -80.5% | -80.5% | -98.7% |
| COVID Black Swan | -97.6% | -96.9% | -95.6% | -78.0% | -95.6% | -99.2% | -98.9% | -98.3% | -86.9% | -86.9% | -86.9% | -86.9% | -99.1% |
| Gradual Bear Market | -93.2% | -91.1% | -87.5% | -50.6% | -87.5% | -97.8% | -91.4% | -95.2% | -64.5% | -64.5% | -64.4% | -64.4% | -97.5% |
| Bull Run Then Crash | -92.7% | -90.6% | -86.7% | -60.7% | -87.0% | -97.7% | -91.1% | -94.9% | -63.3% | -63.3% | -63.3% | -63.3% | -97.4% |
| High Volatility | -93.6% | -91.7% | -88.2% | -53.5% | -88.3% | -97.9% | -97.1% | -95.5% | -67.0% | -67.0% | -67.0% | -67.0% | -97.6% |
| Stable Growth | -85.0% | -80.6% | -72.6% | -35.5% | -73.2% | -86.5% | -81.2% | -89.5% | -29.8% | -29.7% | -30.0% | -29.9% | -84.5% |
| Early Crash with Recovery | -88.7% | -85.4% | -79.4% | -37.0% | -79.3% | -90.3% | -86.6% | -92.1% | -41.5% | -41.6% | -41.5% | -41.6% | -88.6% |
| Multiple Crashes | -97.4% | -96.6% | -95.2% | -78.5% | -95.2% | -99.2% | -98.8% | -98.2% | -86.0% | -86.0% | -86.0% | -86.0% | -99.0% |

## Month-36 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -33.8% | $5,956 | -33.3% | -52.2%..-15.9% | 98.0% | Best ROI (raw), but check brake risk |
| Protocol v5.7 | -52.2% | $4,298 | -53.7% | -71.4%..-34.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.3 | -52.3% | $4,292 | -53.2% | -70.7%..-36.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.5 | -54.2% | $4,118 | -54.0% | -71.8%..-35.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.8 | -55.4% | $4,010 | -54.0% | -71.4%..-36.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -83.5% | $1,486 | -84.3% | -90.6%..-75.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v3.1 (Adjusted) | -84.2% | $1,418 | -85.1% | -91.4%..-77.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -85.5% | $1,301 | -84.1% | -97.6%..-74.9% | 33.0% | Trade-off: ROI vs access |
| Protocol v2.6 | -85.6% | $1,296 | -86.0% | -91.6%..-77.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -86.1% | $1,254 | -86.6% | -92.2%..-78.9% | 100.0% | High gate/brake risk (often “stuck”) |
| HybridC | -89.1% | $985 | -86.6% | -98.1%..-79.4% | 40.0% | Trade-off: ROI vs access |
| Hybrid B | -90.9% | $815 | -97.1% | -98.2%..-81.6% | 56.0% | Trade-off: ROI vs access |
| Harris Model | -91.7% | $749 | -92.0% | -95.2%..-87.4% | 100.0% | High gate/brake risk (often “stuck”) |

### Month-36 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -17.8% (100%) | -49.2% (100%) | -33.1% (100%) | -35.2% (92%) |
| Protocol v5.7 | -36.6% (100%) | -70.3% (100%) | -53.7% (100%) | -48.3% (100%) |
| Protocol v5.3 | -37.3% (100%) | -70.1% (100%) | -53.1% (100%) | -48.8% (100%) |
| Protocol v5.5 | -36.8% (100%) | -69.9% (100%) | -53.6% (100%) | -56.7% (100%) |
| Protocol v5.8 | -36.9% (100%) | -70.1% (100%) | -53.4% (100%) | -61.4% (100%) |
| Hybrid Model | -75.4% (100%) | -90.2% (100%) | -84.1% (100%) | -84.3% (100%) |
| Protocol v3.1 (Adjusted) | -78.0% (100%) | -91.0% (100%) | -85.6% (100%) | -82.4% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -75.5% (0%) | -97.5% (100%) | -84.0% (0%) | -85.2% (32%) |
| Protocol v2.6 | -77.7% (100%) | -91.0% (100%) | -85.4% (100%) | -88.4% (100%) |
| Original Model | -79.3% (100%) | -91.6% (100%) | -86.6% (100%) | -86.8% (100%) |
| HybridC | -79.8% (0%) | -97.9% (100%) | -87.1% (4%) | -91.4% (56%) |
| Hybrid B | -82.0% (0%) | -98.2% (100%) | -94.9% (76%) | -88.8% (48%) |
| Harris Model | -87.5% (100%) | -95.0% (100%) | -91.9% (100%) | -92.3% (100%) |

### Month-36 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 | Protocol v5.5 | Protocol v5.7 | Protocol v5.8 | HybridC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -86.6% | -84.1% | -85.5% | -33.7% | -85.6% | -97.0% | -83.9% | -91.9% | -53.5% | -53.5% | -53.5% | -53.5% | -86.8% |
| May 2021-Style Crash | -94.6% | -93.6% | -94.2% | -62.6% | -94.2% | -98.8% | -98.4% | -96.7% | -80.1% | -80.1% | -80.1% | -80.1% | -98.7% |
| FTX Collapse | -96.0% | -95.2% | -95.7% | -72.0% | -95.6% | -99.1% | -98.8% | -97.6% | -85.1% | -85.1% | -85.1% | -85.1% | -99.0% |
| COVID Black Swan | -97.3% | -96.8% | -97.1% | -81.3% | -97.1% | -99.4% | -99.2% | -98.4% | -90.0% | -90.0% | -90.0% | -90.0% | -99.3% |
| Gradual Bear Market | -92.4% | -91.0% | -91.8% | -53.6% | -91.8% | -98.3% | -97.7% | -95.4% | -72.6% | -72.6% | -72.5% | -72.5% | -98.1% |
| Bull Run Then Crash | -91.9% | -90.4% | -91.3% | -59.1% | -91.4% | -98.2% | -97.6% | -95.1% | -71.5% | -71.5% | -71.5% | -71.5% | -98.1% |
| High Volatility | -92.8% | -91.5% | -92.3% | -56.4% | -92.3% | -98.4% | -97.8% | -95.7% | -74.5% | -74.4% | -74.4% | -74.4% | -98.2% |
| Stable Growth | -83.3% | -80.2% | -82.0% | -28.0% | -82.2% | -85.3% | -80.0% | -89.9% | -44.6% | -44.5% | -44.7% | -44.6% | -83.6% |
| Early Crash with Recovery | -87.4% | -85.1% | -86.4% | -35.1% | -86.4% | -97.3% | -85.5% | -92.4% | -54.8% | -54.9% | -54.9% | -54.9% | -87.9% |
| Multiple Crashes | -97.1% | -96.6% | -96.9% | -80.9% | -96.9% | -99.4% | -99.1% | -98.2% | -89.3% | -89.3% | -89.3% | -89.3% | -99.3% |

## Month-48 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -49.3% | $4,561 | -49.5% | -65.5%..-32.7% | 100.0% | Best ROI (raw), but check brake risk |
| Protocol v5.7 | -60.2% | $3,578 | -61.9% | -76.7%..-45.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.3 | -60.4% | $3,566 | -61.6% | -76.1%..-46.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.5 | -62.1% | $3,411 | -62.3% | -77.1%..-45.7% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.8 | -63.1% | $3,319 | -62.3% | -76.7%..-46.4% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -83.9% | $1,452 | -84.7% | -90.8%..-75.7% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -85.5% | $1,306 | -86.0% | -91.8%..-78.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -86.2% | $1,244 | -83.5% | -98.1%..-73.9% | 42.0% | Trade-off: ROI vs access |
| Protocol v3.1 (Adjusted) | -88.2% | $1,060 | -88.9% | -93.5%..-83.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -89.3% | $965 | -89.6% | -93.7%..-83.1% | 100.0% | High gate/brake risk (often “stuck”) |
| HybridC | -91.8% | $740 | -97.3% | -98.5%..-78.7% | 66.0% | Trade-off: ROI vs access |
| Harris Model | -92.0% | $722 | -92.2% | -95.4%..-87.8% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -92.1% | $712 | -97.6% | -98.6%..-80.6% | 68.0% | Trade-off: ROI vs access |

### Month-48 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -34.4% (100%) | -63.3% (100%) | -49.2% (100%) | -50.5% (100%) |
| Protocol v5.7 | -46.8% (100%) | -75.8% (100%) | -62.0% (100%) | -56.3% (100%) |
| Protocol v5.3 | -47.4% (100%) | -75.6% (100%) | -61.5% (100%) | -56.9% (100%) |
| Protocol v5.5 | -47.0% (100%) | -75.5% (100%) | -62.0% (100%) | -63.9% (100%) |
| Protocol v5.8 | -47.1% (100%) | -75.7% (100%) | -61.8% (100%) | -68.0% (100%) |
| Hybrid Model | -76.0% (100%) | -90.4% (100%) | -84.4% (100%) | -84.7% (100%) |
| Original Model | -78.5% (100%) | -91.2% (100%) | -86.0% (100%) | -86.2% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -74.6% (0%) | -98.0% (100%) | -84.9% (12%) | -87.3% (56%) |
| Protocol v3.1 (Adjusted) | -83.6% (100%) | -93.3% (100%) | -89.3% (100%) | -86.8% (100%) |
| Protocol v2.6 | -83.4% (100%) | -93.3% (100%) | -89.1% (100%) | -91.3% (100%) |
| HybridC | -79.1% (0%) | -98.4% (100%) | -97.4% (100%) | -92.3% (64%) |
| Harris Model | -88.0% (100%) | -95.1% (100%) | -92.1% (100%) | -92.6% (100%) |
| Hybrid B | -81.0% (0%) | -98.5% (100%) | -97.6% (100%) | -91.3% (72%) |

### Month-48 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 | Protocol v5.5 | Protocol v5.7 | Protocol v5.8 | HybridC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -86.0% | -84.5% | -89.2% | -49.5% | -89.3% | -97.6% | -83.3% | -92.2% | -61.9% | -61.9% | -61.9% | -61.9% | -97.4% |
| May 2021-Style Crash | -94.4% | -93.8% | -95.7% | -74.1% | -95.7% | -99.0% | -98.7% | -96.9% | -83.9% | -83.9% | -83.9% | -83.9% | -99.0% |
| FTX Collapse | -95.8% | -95.3% | -96.8% | -80.6% | -96.8% | -99.3% | -99.0% | -97.7% | -87.9% | -87.9% | -87.9% | -87.9% | -99.2% |
| COVID Black Swan | -97.2% | -96.9% | -97.8% | -87.0% | -97.8% | -99.5% | -99.4% | -98.4% | -91.9% | -91.9% | -91.9% | -91.9% | -99.5% |
| Gradual Bear Market | -92.0% | -91.2% | -93.9% | -66.5% | -93.9% | -98.6% | -98.2% | -95.5% | -77.7% | -77.7% | -77.6% | -77.6% | -98.5% |
| Bull Run Then Crash | -91.6% | -90.6% | -93.5% | -69.0% | -93.6% | -98.6% | -98.1% | -95.3% | -76.7% | -76.7% | -76.7% | -76.7% | -98.4% |
| High Volatility | -92.5% | -91.7% | -94.2% | -68.5% | -94.2% | -98.7% | -98.3% | -95.8% | -79.2% | -79.1% | -79.1% | -79.1% | -98.6% |
| Stable Growth | -82.6% | -80.7% | -86.6% | -43.5% | -86.7% | -97.0% | -79.3% | -90.3% | -54.2% | -54.2% | -54.3% | -54.3% | -83.1% |
| Early Crash with Recovery | -86.9% | -85.5% | -89.9% | -51.1% | -89.9% | -97.8% | -97.1% | -92.7% | -63.2% | -63.2% | -63.2% | -63.3% | -97.6% |
| Multiple Crashes | -97.0% | -96.6% | -97.7% | -86.5% | -97.7% | -99.5% | -99.3% | -98.3% | -91.3% | -91.3% | -91.3% | -91.3% | -99.4% |

## Month-72 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -65.2% | $3,133 | -66.0% | -77.8%..-52.0% | 100.0% | Best ROI (raw), but check brake risk |
| Protocol v5.7 | -70.2% | $2,684 | -71.9% | -83.0%..-58.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.3 | -70.4% | $2,668 | -71.7% | -82.6%..-59.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.5 | -71.8% | $2,541 | -72.2% | -83.3%..-59.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v5.8 | -72.5% | $2,471 | -72.4% | -83.0%..-59.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -85.0% | $1,353 | -85.6% | -91.5%..-77.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -85.0% | $1,352 | -85.7% | -91.4%..-77.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -90.2% | $881 | -97.7% | -98.6%..-72.9% | 70.0% | Trade-off: ROI vs access |
| Protocol v3.1 (Adjusted) | -92.2% | $704 | -92.6% | -95.7%..-88.8% | 100.0% | High gate/brake risk (often “stuck”) |
| Harris Model | -92.5% | $672 | -92.8% | -95.7%..-88.6% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -92.9% | $639 | -93.1% | -95.9%..-88.8% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -97.1% | $262 | -98.3% | -99.0%..-97.3% | 97.0% | High gate/brake risk (often “stuck”) |
| HybridC | -97.9% | $190 | -98.1% | -98.9%..-97.1% | 99.0% | High gate/brake risk (often “stuck”) |

### Month-72 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -53.3% (100%) | -76.4% (100%) | -65.6% (100%) | -65.5% (100%) |
| Protocol v5.7 | -59.8% (100%) | -82.3% (100%) | -72.1% (100%) | -66.6% (100%) |
| Protocol v5.3 | -60.3% (100%) | -82.2% (100%) | -71.7% (100%) | -67.2% (100%) |
| Protocol v5.5 | -59.9% (100%) | -82.1% (100%) | -72.1% (100%) | -73.0% (100%) |
| Protocol v5.8 | -60.0% (100%) | -82.2% (100%) | -71.9% (100%) | -76.0% (100%) |
| Original Model | -77.7% (100%) | -90.9% (100%) | -85.6% (100%) | -85.7% (100%) |
| Hybrid Model | -77.6% (100%) | -91.0% (100%) | -85.5% (100%) | -85.8% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -73.5% (0%) | -98.6% (100%) | -97.7% (100%) | -91.0% (80%) |
| Protocol v3.1 (Adjusted) | -89.1% (100%) | -95.5% (100%) | -92.9% (100%) | -91.2% (100%) |
| Harris Model | -88.9% (100%) | -95.5% (100%) | -92.7% (100%) | -93.1% (100%) |
| Protocol v2.6 | -89.0% (100%) | -95.5% (100%) | -92.8% (100%) | -94.3% (100%) |
| Hybrid B | -97.3% (100%) | -98.9% (100%) | -98.3% (100%) | -93.8% (88%) |
| HybridC | -97.2% (100%) | -98.8% (100%) | -98.1% (100%) | -97.4% (96%) |

### Month-72 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 | Protocol v5.5 | Protocol v5.7 | Protocol v5.8 | HybridC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -85.5% | -85.5% | -92.9% | -65.8% | -92.9% | -98.3% | -97.7% | -92.7% | -72.0% | -72.0% | -72.0% | -72.0% | -98.1% |
| May 2021-Style Crash | -94.2% | -94.2% | -97.1% | -83.9% | -97.1% | -99.3% | -99.1% | -97.1% | -88.3% | -88.3% | -88.3% | -88.3% | -99.3% |
| FTX Collapse | -95.7% | -95.7% | -97.9% | -87.9% | -97.9% | -99.5% | -99.3% | -97.8% | -91.3% | -91.3% | -91.3% | -91.3% | -99.4% |
| COVID Black Swan | -97.1% | -97.1% | -98.6% | -92.0% | -98.6% | -99.7% | -99.5% | -98.5% | -94.1% | -94.1% | -94.1% | -94.1% | -99.6% |
| Gradual Bear Market | -91.8% | -91.8% | -95.9% | -78.5% | -95.9% | -99.0% | -98.7% | -95.8% | -83.7% | -83.7% | -83.7% | -83.7% | -98.9% |
| Bull Run Then Crash | -91.3% | -91.3% | -95.7% | -79.2% | -95.7% | -98.9% | -98.6% | -95.6% | -82.9% | -82.9% | -82.9% | -82.9% | -98.9% |
| High Volatility | -92.2% | -92.3% | -96.2% | -79.8% | -96.2% | -99.1% | -98.8% | -96.1% | -84.8% | -84.8% | -84.8% | -84.8% | -99.0% |
| Stable Growth | -82.0% | -82.0% | -91.1% | -60.5% | -91.2% | -97.8% | -97.2% | -90.9% | -66.0% | -66.0% | -66.1% | -66.1% | -97.7% |
| Early Crash with Recovery | -86.4% | -86.5% | -93.3% | -67.3% | -93.3% | -98.4% | -97.9% | -93.2% | -73.2% | -73.2% | -73.2% | -73.2% | -98.3% |
| Multiple Crashes | -96.9% | -96.9% | -98.5% | -91.5% | -98.5% | -99.6% | -99.5% | -98.4% | -93.7% | -93.7% | -93.7% | -93.7% | -99.6% |

