# Real-World Multi-Opinion Backtest Report

**Generated**: 2026-01-04T17:01:31.215180

## Methodology

Three independent 'opinions' on the same historical market data:
1. **Conservative (Stress-Test)**: raw historical regimes, no adoption overlay
2. **Ideal (Growth Scenario)**: historical regimes + 50% annual liquidity CAGR + 1% monthly inflow
3. **Choppy Stress Overlay**: historical regimes with 10 choppy crash shocks overlaid

**Investment levels**: $9,000, $50,000, $100,000

**ROI horizons**: 12, 24, 36, 48, 72 months

## Executive Summary: Winners by Opinion & Horizon

| Opinion | Horizon | Winner (ROI) | Avg ROI | Positive Rate | Value ($9k) | Value ($50k) | Value ($100k) |
|---|---:|---|---:|---:|---:|---:|---:|
| Conservative (Stress-Test) | 12 | **Protocol v3.0** | -58.2% | 0.0% | $3,762 | $20,897 | $41,795 |
| Conservative (Stress-Test) | 24 | **Protocol v3.0** | -1.0% | 40.0% | $8,908 | $49,487 | $98,974 |
| Conservative (Stress-Test) | 36 | **Protocol v3.0** | +40.2% | 40.0% | $12,616 | $70,089 | $140,177 |
| Conservative (Stress-Test) | 48 | **Protocol v3.0** | -2.9% | 20.0% | $8,735 | $48,528 | $97,055 |
| Conservative (Stress-Test) | 72 | **Protocol v3.0** | +26.6% | 60.0% | $11,390 | $63,277 | $126,555 |
| Ideal (Growth Scenario) | 12 | **Protocol v3.0** | -42.7% | 0.0% | $5,160 | $28,665 | $57,331 |
| Ideal (Growth Scenario) | 24 | **Protocol v3.0** | +72.0% | 64.7% | $15,480 | $86,002 | $172,005 |
| Ideal (Growth Scenario) | 36 | **Protocol v3.0** | +208.3% | 100.0% | $27,745 | $154,137 | $308,273 |
| Ideal (Growth Scenario) | 48 | **Hybrid Model** | +223.4% | 100.0% | $29,102 | $161,678 | $323,357 |
| Ideal (Growth Scenario) | 72 | **Original Model** | +1244.7% | 100.0% | $121,020 | $672,333 | $1,344,667 |
| Choppy Stress Overlay (10 scenarios aggregated) | 12 | **Protocol v3.0** | -69.6% | 0.0% | $2,737 | $15,203 | $30,407 |
| Choppy Stress Overlay (10 scenarios aggregated) | 24 | **Protocol v3.0** | -21.5% | 28.0% | $7,067 | $39,264 | $78,527 |
| Choppy Stress Overlay (10 scenarios aggregated) | 36 | **Protocol v3.0** | +6.3% | 32.0% | $9,565 | $53,140 | $106,279 |
| Choppy Stress Overlay (10 scenarios aggregated) | 48 | **Protocol v3.0** | -26.9% | 16.0% | $6,581 | $36,563 | $73,126 |
| Choppy Stress Overlay (10 scenarios aggregated) | 72 | **Protocol v3.0** | -7.3% | 38.0% | $8,346 | $46,369 | $92,737 |

---

## Conservative (Stress-Test)

- **liquidity_cagr_annual**: 0.0
- **net_inflow_monthly_pct**: 0.0
- **choppy_overlay**: None
- **window_months**: 72
- **runs_per_window**: 30

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.7% | -49.5% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.9% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 13.3% | 100.0% |
| Protocol v3.0 | -58.2% | -1.0% | +40.2% | -2.9% | +26.6% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.8% | -40.4% | -46.2% | -64.3% | -54.1% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.2% | -64.8% | -27.4% | 40.0% | 20.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.7% | -49.5% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.9% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 13.3% | 100.0% |
| Protocol v3.0 | -58.2% | -1.0% | +40.2% | -2.9% | +26.6% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.8% | -40.4% | -46.2% | -64.3% | -54.1% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.2% | -64.8% | -27.4% | 40.0% | 20.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.7% | -49.5% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.9% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 13.3% | 100.0% |
| Protocol v3.0 | -58.2% | -1.0% | +40.2% | -2.9% | +26.6% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.8% | -40.4% | -46.2% | -64.3% | -54.1% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.2% | -64.8% | -27.4% | 40.0% | 20.0% |


---

## Ideal (Growth Scenario)

- **liquidity_cagr_annual**: 0.5
- **net_inflow_monthly_pct**: 0.01
- **choppy_overlay**: None
- **window_months**: 72
- **runs_per_window**: 30

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.4% | +113.3% | +191.8% | +1244.7% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.1% | +152.6% | +223.4% | +1240.7% | 100.0% | 60.0% |
| Protocol v2.6 | -50.5% | +37.5% | +86.4% | +81.8% | +305.8% | 100.0% | 80.0% |
| Protocol v3.0 | -42.7% | +72.0% | +208.3% | +159.9% | +645.7% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.6% | +20.0% | +45.5% | +24.2% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.4% | +68.2% | +120.6% | +879.8% | 100.0% | 0.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.4% | +113.3% | +191.8% | +1244.7% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.1% | +152.6% | +223.4% | +1240.7% | 100.0% | 60.0% |
| Protocol v2.6 | -50.5% | +37.5% | +86.4% | +81.8% | +305.8% | 100.0% | 80.0% |
| Protocol v3.0 | -42.7% | +72.0% | +208.3% | +159.9% | +645.7% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.6% | +20.0% | +45.5% | +24.2% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.4% | +68.2% | +120.6% | +879.8% | 100.0% | 0.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.4% | +113.3% | +191.8% | +1244.7% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.1% | +152.6% | +223.4% | +1240.7% | 100.0% | 60.0% |
| Protocol v2.6 | -50.5% | +37.5% | +86.4% | +81.8% | +305.8% | 100.0% | 80.0% |
| Protocol v3.0 | -42.7% | +72.0% | +208.3% | +159.9% | +645.7% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.6% | +20.0% | +45.5% | +24.2% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.4% | +68.2% | +120.6% | +879.8% | 100.0% | 0.0% |


---

## Choppy Stress Overlay (10 scenarios aggregated)

- **choppy_scenarios**: ['Normal Market Conditions', 'May 2021-Style Crash', 'FTX Collapse', 'COVID Black Swan', 'Gradual Bear Market', 'Bull Run Then Crash', 'High Volatility', 'Stable Growth', 'Early Crash with Recovery', 'Multiple Crashes']

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.6% | -69.5% | -38.0% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.5% | +6.3% | -26.9% | -7.3% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.1% | -62.5% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.6% | -69.5% | -38.0% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.5% | +6.3% | -26.9% | -7.3% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.1% | -62.5% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.6% | -69.5% | -38.0% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.5% | +6.3% | -26.9% | -7.3% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.1% | -62.5% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |

### Per-Scenario Breakdown (Month 72 ROI @ $9,000)

| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | +2.9% | +2.8% | -49.4% | +27.0% | -54.0% | -43.5% | -27.4% |
| May 2021-Style Crash | -58.8% | -58.9% | -79.7% | -21.3% | -79.7% | -96.9% | -85.8% |
| FTX Collapse | -68.7% | -68.8% | -84.6% | -31.8% | -84.5% | -97.7% | -97.0% |
| COVID Black Swan | -78.6% | -78.7% | -89.4% | -47.1% | -89.4% | -98.4% | -97.9% |
| Gradual Bear Market | -41.4% | -41.5% | -71.1% | -3.5% | -71.5% | -84.3% | -64.3% |
| Bull Run Then Crash | -37.9% | -37.9% | -69.9% | -2.8% | -70.2% | -83.3% | -62.1% |
| High Volatility | -44.8% | -44.9% | -72.8% | -7.5% | -73.1% | -85.2% | -66.4% |
| Stable Growth | +28.0% | +27.8% | -38.2% | +37.4% | -47.3% | -29.8% | -9.7% |
| Early Crash with Recovery | -3.5% | -3.4% | -52.6% | +21.8% | -56.0% | -47.1% | -31.9% |
| Multiple Crashes | -77.0% | -77.1% | -88.7% | -44.8% | -88.7% | -98.3% | -97.8% |

