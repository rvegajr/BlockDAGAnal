# All Model Comparison: Investor Returns (Second Opinion, Order-Book + Sell Pressure)

**Generated**: 2026-01-03T23:16:39.207499

This document mirrors the *format/style* of `docs/vesting/THREE_MODEL_COMPARISON.md`, but covers **all models** currently tested.

## Methodology (Second Opinion)
- **Pricing**: baseline (Liquidity / Circulating) + order-book depth + sell-pressure impacts
- **Liquidity base**: $32,000,000
- **Investment reference**: $9,000 (ROI is scale-invariant in this harness; the report still lists multiple levels)
- **Runs**: 100 sims/model across bull/bear/normal/volatile + 100 runs/model per each of 10 choppy scenarios

## Executive Summary
### Overall winner (raw Month-12 ROI)
- **Protocol v3.0** with **-64.1%** avg Month-12 ROI

### Best balance (ROI + access)
We also track **brake rate** (how often the emergency condition is hit).
- **Hybrid Tokenomics (Solvency-Anchored)**: ROI **-86.8%**, brake **2.0%**

### Avg choppy-market ROI (10 scenarios)
- **Protocol v3.0**: avg choppy ROI **-77.5%**

## Model Parameters (high level)
For full model mechanics and definitions see:
- `scripts/hybrid_tokenomics_second_opinion_compare.py`
- `HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`
- Protocol v3.1 reference: https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/

## Month-12 Results (All Models) — $9,000 Reference
| Model | Avg ROI | Median ROI | P10..P90 ROI | Brake rate |
|---|---:|---:|---:|---:|
| Protocol v3.0 | -64.1% | -67.0% | -76.7%..-46.6% | 44.0% |
| Protocol v2.6 | -78.9% | -79.6% | -87.9%..-67.4% | 99.0% |
| Protocol v3.1 (Adjusted) | -79.4% | -80.8% | -88.0%..-69.0% | 100.0% |
| Hybrid Model | -85.4% | -85.9% | -91.6%..-77.2% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -86.8% | -87.2% | -92.2%..-79.8% | 2.0% |
| Hybrid B | -91.3% | -91.4% | -94.9%..-86.1% | 9.0% |
| Original Model | -95.6% | -95.9% | -97.5%..-93.4% | 1.0% |

## Month-12 ROI by Market Type (All Models) — Avg ROI / Brake rate
| Model | Bull | Bear | Normal | Volatile |
|---|---:|---:|---:|---:|
| Hybrid B | -86.4% (0%) | -94.4% (0%) | -91.1% (0%) | -93.3% (36%) |
| Hybrid Model | -77.6% (100%) | -91.0% (100%) | -85.4% (100%) | -87.6% (100%) |
| Hybrid Tokenomics (Solvency-Anchored) | -80.0% (0%) | -91.8% (0%) | -86.9% (0%) | -88.3% (8%) |
| Original Model | -93.6% (0%) | -97.4% (0%) | -95.8% (0%) | -95.3% (4%) |
| Protocol v2.6 | -68.1% (100%) | -87.0% (100%) | -79.4% (100%) | -81.1% (96%) |
| Protocol v3.0 | -47.6% (0%) | -75.4% (100%) | -66.6% (0%) | -67.0% (76%) |
| Protocol v3.1 (Adjusted) | -70.0% (100%) | -87.3% (100%) | -80.2% (100%) | -80.2% (100%) |

## Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000
| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -95.9% | -85.5% | -79.6% | -66.3% | -80.1% | -91.1% | -87.0% |
| May 2021-Style Crash | -98.4% | -94.2% | -91.8% | -80.0% | -91.8% | -97.8% | -94.8% |
| FTX Collapse | -98.8% | -95.6% | -93.9% | -85.0% | -93.8% | -98.3% | -97.6% |
| COVID Black Swan | -99.2% | -97.1% | -95.9% | -90.0% | -95.9% | -98.9% | -98.4% |
| Gradual Bear Market | -97.7% | -91.8% | -88.4% | -77.5% | -88.5% | -94.9% | -92.6% |
| Bull Run Then Crash | -97.5% | -91.2% | -87.7% | -82.1% | -88.2% | -94.6% | -92.4% |
| High Volatility | -97.8% | -92.2% | -89.1% | -78.8% | -89.2% | -97.0% | -93.0% |
| Stable Growth | -94.9% | -81.9% | -74.6% | -58.1% | -75.7% | -89.0% | -83.8% |
| Early Crash with Recovery | -96.2% | -86.4% | -80.9% | -67.2% | -80.8% | -92.3% | -89.0% |
| Multiple Crashes | -99.1% | -96.9% | -95.6% | -90.2% | -95.6% | -98.8% | -98.2% |
