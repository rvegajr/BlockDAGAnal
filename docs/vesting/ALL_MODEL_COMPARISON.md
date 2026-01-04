# All Model Comparison: Investor Returns (Second Opinion, Order-Book + Sell Pressure)

**Generated**: 2026-01-04T16:20:31.854718

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
| Month 12 | **Protocol v3.0** | **-63.8%** |
| Month 24 | **Protocol v3.0** | **-34.7%** |
| Month 36 | **Protocol v3.0** | **-33.8%** |
| Month 48 | **Protocol v3.0** | **-49.3%** |
| Month 72 | **Protocol v3.0** | **-65.2%** |

### When do we ever see **positive ROI**?

Under this **second-opinion harness** (baseline liquidity/circulating + sell-pressure + order-book impact), **positive ROI is rare**:
- **Observed**: only in the **market-type Monte Carlo** (bull/bear/normal/volatile), and only for **Protocol v3.0** at **Month 24 (3/100 runs)** and **Month 36 (2/100 runs)** — driven entirely by the **volatile** market generator.
- **Not observed**: **0 positive runs** in any of the **10 choppy scenarios** at **any** horizon (12/24/36/48/72).

Why this happens (in plain English): this harness is intentionally conservative because it **models persistent sell pressure** and prices tokens off **launch liquidity vs circulating supply** (plus order-book slippage). Without sustained *external buy demand / liquidity growth* overwhelming unlock/mining sell pressure, ROI stays negative.

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
| Month 12 | **Protocol v3.0** | **-77.5%** |
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
| Protocol v3.0 | -63.8% | $3,259 | -66.6% | -76.8%..-46.7% | 43.0% | Best ROI (raw), but check brake risk |
| Protocol v3.1 (Adjusted) | -78.3% | $1,952 | -79.4% | -87.9%..-69.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -79.7% | $1,827 | -80.2% | -88.1%..-68.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -84.9% | $1,360 | -85.7% | -91.5%..-77.1% | 99.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -86.4% | $1,222 | -87.1% | -92.3%..-79.6% | 3.0% | Best balance (ROI + access) |
| Hybrid B | -90.4% | $865 | -91.3% | -94.7%..-86.0% | 5.0% | Stable/accessible, weaker ROI |
| Original Model | -95.7% | $383 | -95.9% | -97.6%..-93.6% | 5.0% | Stable/accessible, weaker ROI |

### Month-12 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -48.3% (0%) | -75.5% (100%) | -66.2% (0%) | -65.2% (72%) |
| Protocol v3.1 (Adjusted) | -69.9% (100%) | -87.4% (100%) | -80.1% (100%) | -75.9% (100%) |
| Protocol v2.6 | -68.5% (100%) | -87.2% (100%) | -79.4% (100%) | -83.6% (100%) |
| Hybrid Model | -77.5% (100%) | -91.0% (100%) | -85.4% (100%) | -85.6% (96%) |
| Hybrid Tokenomics (Solvency-Anchored) | -80.2% (0%) | -91.9% (0%) | -87.0% (0%) | -86.6% (12%) |
| Hybrid B | -86.3% (0%) | -94.5% (0%) | -91.3% (0%) | -89.5% (20%) |
| Original Model | -93.7% (0%) | -97.4% (0%) | -95.9% (0%) | -96.0% (20%) |

### Month-12 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -95.9% | -85.4% | -79.6% | -66.3% | -80.1% | -91.1% | -87.0% |
| May 2021-Style Crash | -98.4% | -94.2% | -91.8% | -80.0% | -91.8% | -97.8% | -94.8% |
| FTX Collapse | -98.8% | -95.6% | -93.9% | -85.0% | -93.8% | -98.3% | -97.6% |
| COVID Black Swan | -99.2% | -97.1% | -95.9% | -90.0% | -95.9% | -98.9% | -98.4% |
| Gradual Bear Market | -97.7% | -91.7% | -88.4% | -77.5% | -88.5% | -94.9% | -92.6% |
| Bull Run Then Crash | -97.5% | -91.2% | -87.7% | -82.1% | -88.2% | -94.6% | -92.4% |
| High Volatility | -97.8% | -92.2% | -89.1% | -78.8% | -89.2% | -97.0% | -93.0% |
| Stable Growth | -94.9% | -81.9% | -74.6% | -58.1% | -75.6% | -89.0% | -83.8% |
| Early Crash with Recovery | -96.2% | -86.4% | -80.9% | -67.3% | -80.8% | -92.3% | -89.0% |
| Multiple Crashes | -99.1% | -96.9% | -95.6% | -90.2% | -95.6% | -98.8% | -98.2% |

## Month-24 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -34.7% | $5,876 | -36.4% | -49.0%..-18.0% | 70.0% | Best ROI (raw), but check brake risk |
| Protocol v3.1 (Adjusted) | -76.2% | $2,142 | -77.5% | -86.9%..-66.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -78.1% | $1,969 | -78.7% | -87.3%..-65.6% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -83.8% | $1,459 | -84.6% | -90.8%..-75.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -84.7% | $1,377 | -85.1% | -91.1%..-76.4% | 8.0% | Trade-off: ROI vs access |
| Original Model | -87.5% | $1,127 | -87.9% | -92.9%..-81.2% | 97.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -89.7% | $925 | -89.4% | -97.7%..-83.3% | 32.0% | Trade-off: ROI vs access |

### Month-24 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -20.6% (0%) | -46.1% (100%) | -36.2% (100%) | -36.0% (80%) |
| Protocol v3.1 (Adjusted) | -66.8% (100%) | -86.3% (100%) | -78.2% (100%) | -73.4% (100%) |
| Protocol v2.6 | -66.1% (100%) | -86.3% (100%) | -77.8% (100%) | -82.4% (100%) |
| Hybrid Model | -75.8% (100%) | -90.3% (100%) | -84.3% (100%) | -84.6% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -77.0% (0%) | -90.6% (0%) | -85.0% (0%) | -86.2% (32%) |
| Original Model | -81.5% (100%) | -92.4% (100%) | -87.9% (100%) | -88.1% (88%) |
| Hybrid B | -83.6% (0%) | -97.6% (100%) | -89.4% (0%) | -88.4% (28%) |

### Month-24 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -88.0% | -84.4% | -78.0% | -36.9% | -78.3% | -89.2% | -84.9% |
| May 2021-Style Crash | -95.2% | -93.8% | -91.2% | -56.0% | -91.2% | -98.5% | -97.8% |
| FTX Collapse | -96.4% | -95.3% | -93.4% | -67.0% | -93.3% | -98.8% | -98.4% |
| COVID Black Swan | -97.6% | -96.9% | -95.6% | -78.0% | -95.6% | -99.2% | -98.9% |
| Gradual Bear Market | -93.2% | -91.1% | -87.5% | -50.6% | -87.5% | -97.8% | -91.4% |
| Bull Run Then Crash | -92.7% | -90.6% | -86.7% | -60.7% | -87.0% | -97.7% | -91.1% |
| High Volatility | -93.6% | -91.7% | -88.2% | -53.5% | -88.3% | -97.9% | -97.1% |
| Stable Growth | -85.0% | -80.6% | -72.6% | -35.5% | -73.2% | -86.5% | -81.2% |
| Early Crash with Recovery | -88.7% | -85.4% | -79.4% | -37.0% | -79.3% | -90.3% | -86.6% |
| Multiple Crashes | -97.4% | -96.6% | -95.2% | -78.5% | -95.2% | -99.2% | -98.8% |

## Month-36 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -33.8% | $5,956 | -33.3% | -52.2%..-15.9% | 98.0% | Best ROI (raw), but check brake risk |
| Hybrid Model | -83.5% | $1,486 | -84.3% | -90.6%..-75.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v3.1 (Adjusted) | -84.2% | $1,418 | -85.1% | -91.4%..-77.5% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -85.5% | $1,301 | -84.1% | -97.6%..-74.9% | 33.0% | Trade-off: ROI vs access |
| Protocol v2.6 | -85.6% | $1,296 | -86.0% | -91.6%..-77.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -86.1% | $1,254 | -86.6% | -92.2%..-78.9% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -90.9% | $815 | -97.1% | -98.2%..-81.6% | 56.0% | Trade-off: ROI vs access |

### Month-36 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -17.8% (100%) | -49.2% (100%) | -33.1% (100%) | -35.2% (92%) |
| Hybrid Model | -75.4% (100%) | -90.2% (100%) | -84.1% (100%) | -84.3% (100%) |
| Protocol v3.1 (Adjusted) | -78.0% (100%) | -91.0% (100%) | -85.6% (100%) | -82.4% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -75.5% (0%) | -97.5% (100%) | -84.0% (0%) | -85.2% (32%) |
| Protocol v2.6 | -77.7% (100%) | -91.0% (100%) | -85.4% (100%) | -88.4% (100%) |
| Original Model | -79.3% (100%) | -91.6% (100%) | -86.6% (100%) | -86.8% (100%) |
| Hybrid B | -82.0% (0%) | -98.2% (100%) | -94.9% (76%) | -88.8% (48%) |

### Month-36 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -86.6% | -84.1% | -85.5% | -33.7% | -85.6% | -97.0% | -83.9% |
| May 2021-Style Crash | -94.6% | -93.6% | -94.2% | -62.6% | -94.2% | -98.8% | -98.4% |
| FTX Collapse | -96.0% | -95.2% | -95.7% | -72.0% | -95.6% | -99.1% | -98.8% |
| COVID Black Swan | -97.3% | -96.8% | -97.1% | -81.3% | -97.1% | -99.4% | -99.2% |
| Gradual Bear Market | -92.4% | -91.0% | -91.8% | -53.6% | -91.8% | -98.3% | -97.7% |
| Bull Run Then Crash | -91.9% | -90.4% | -91.3% | -59.1% | -91.4% | -98.2% | -97.6% |
| High Volatility | -92.8% | -91.5% | -92.3% | -56.4% | -92.3% | -98.4% | -97.8% |
| Stable Growth | -83.3% | -80.2% | -82.0% | -28.0% | -82.2% | -85.3% | -80.0% |
| Early Crash with Recovery | -87.4% | -85.1% | -86.4% | -35.1% | -86.4% | -97.3% | -85.5% |
| Multiple Crashes | -97.1% | -96.6% | -96.9% | -80.9% | -96.9% | -99.4% | -99.1% |

## Month-48 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -49.3% | $4,561 | -49.5% | -65.5%..-32.7% | 100.0% | Best ROI (raw), but check brake risk |
| Hybrid Model | -83.9% | $1,452 | -84.7% | -90.8%..-75.7% | 100.0% | High gate/brake risk (often “stuck”) |
| Original Model | -85.5% | $1,306 | -86.0% | -91.8%..-78.0% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -86.2% | $1,244 | -83.5% | -98.1%..-73.9% | 42.0% | Trade-off: ROI vs access |
| Protocol v3.1 (Adjusted) | -88.2% | $1,060 | -88.9% | -93.5%..-83.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -89.3% | $965 | -89.6% | -93.7%..-83.1% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -92.1% | $712 | -97.6% | -98.6%..-80.6% | 68.0% | Trade-off: ROI vs access |

### Month-48 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -34.4% (100%) | -63.3% (100%) | -49.2% (100%) | -50.5% (100%) |
| Hybrid Model | -76.0% (100%) | -90.4% (100%) | -84.4% (100%) | -84.7% (100%) |
| Original Model | -78.5% (100%) | -91.2% (100%) | -86.0% (100%) | -86.2% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -74.6% (0%) | -98.0% (100%) | -84.9% (12%) | -87.3% (56%) |
| Protocol v3.1 (Adjusted) | -83.6% (100%) | -93.3% (100%) | -89.3% (100%) | -86.8% (100%) |
| Protocol v2.6 | -83.4% (100%) | -93.3% (100%) | -89.1% (100%) | -91.3% (100%) |
| Hybrid B | -81.0% (0%) | -98.5% (100%) | -97.6% (100%) | -91.3% (72%) |

### Month-48 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -86.0% | -84.5% | -89.2% | -49.5% | -89.3% | -97.6% | -83.3% |
| May 2021-Style Crash | -94.4% | -93.8% | -95.7% | -74.1% | -95.7% | -99.0% | -98.7% |
| FTX Collapse | -95.8% | -95.3% | -96.8% | -80.6% | -96.8% | -99.3% | -99.0% |
| COVID Black Swan | -97.2% | -96.9% | -97.8% | -87.0% | -97.8% | -99.5% | -99.4% |
| Gradual Bear Market | -92.0% | -91.2% | -93.9% | -66.5% | -93.9% | -98.6% | -98.2% |
| Bull Run Then Crash | -91.6% | -90.6% | -93.5% | -69.0% | -93.6% | -98.6% | -98.1% |
| High Volatility | -92.5% | -91.7% | -94.2% | -68.5% | -94.2% | -98.7% | -98.3% |
| Stable Growth | -82.6% | -80.7% | -86.6% | -43.5% | -86.7% | -97.0% | -79.3% |
| Early Crash with Recovery | -86.9% | -85.5% | -89.9% | -51.1% | -89.9% | -97.8% | -97.1% |
| Multiple Crashes | -97.0% | -96.6% | -97.7% | -86.5% | -97.7% | -99.5% | -99.3% |

## Month-72 Results (All Models) — $9,000 Reference

| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Protocol v3.0 | -65.2% | $3,133 | -66.0% | -77.8%..-52.0% | 100.0% | Best ROI (raw), but check brake risk |
| Original Model | -85.0% | $1,353 | -85.6% | -91.5%..-77.2% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Model | -85.0% | $1,352 | -85.7% | -91.4%..-77.3% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid Tokenomics (Solvency-Anchored) | -90.2% | $881 | -97.7% | -98.6%..-72.9% | 70.0% | Trade-off: ROI vs access |
| Protocol v3.1 (Adjusted) | -92.2% | $704 | -92.6% | -95.7%..-88.8% | 100.0% | High gate/brake risk (often “stuck”) |
| Protocol v2.6 | -92.9% | $639 | -93.1% | -95.9%..-88.8% | 100.0% | High gate/brake risk (often “stuck”) |
| Hybrid B | -97.1% | $262 | -98.3% | -99.0%..-97.3% | 97.0% | High gate/brake risk (often “stuck”) |

### Month-72 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -53.3% (100%) | -76.4% (100%) | -65.6% (100%) | -65.5% (100%) |
| Original Model | -77.7% (100%) | -90.9% (100%) | -85.6% (100%) | -85.7% (100%) |
| Hybrid Model | -77.6% (100%) | -91.0% (100%) | -85.5% (100%) | -85.8% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -73.5% (0%) | -98.6% (100%) | -97.7% (100%) | -91.0% (80%) |
| Protocol v3.1 (Adjusted) | -89.1% (100%) | -95.5% (100%) | -92.9% (100%) | -91.2% (100%) |
| Protocol v2.6 | -89.0% (100%) | -95.5% (100%) | -92.8% (100%) | -94.3% (100%) |
| Hybrid B | -97.3% (100%) | -98.9% (100%) | -98.3% (100%) | -93.8% (88%) |

### Month-72 Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -85.5% | -85.5% | -92.9% | -65.8% | -92.9% | -98.3% | -97.7% |
| May 2021-Style Crash | -94.2% | -94.2% | -97.1% | -83.9% | -97.1% | -99.3% | -99.1% |
| FTX Collapse | -95.7% | -95.7% | -97.9% | -87.9% | -97.9% | -99.5% | -99.3% |
| COVID Black Swan | -97.1% | -97.1% | -98.6% | -92.0% | -98.6% | -99.7% | -99.5% |
| Gradual Bear Market | -91.8% | -91.8% | -95.9% | -78.5% | -95.9% | -99.0% | -98.7% |
| Bull Run Then Crash | -91.3% | -91.3% | -95.7% | -79.2% | -95.7% | -98.9% | -98.6% |
| High Volatility | -92.2% | -92.3% | -96.2% | -79.8% | -96.2% | -99.1% | -98.8% |
| Stable Growth | -82.0% | -82.0% | -91.1% | -60.5% | -91.2% | -97.8% | -97.2% |
| Early Crash with Recovery | -86.4% | -86.5% | -93.3% | -67.3% | -93.3% | -98.4% | -97.9% |
| Multiple Crashes | -96.9% | -96.9% | -98.5% | -91.5% | -98.5% | -99.6% | -99.5% |

