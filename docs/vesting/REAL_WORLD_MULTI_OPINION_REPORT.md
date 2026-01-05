# Real-World Multi-Opinion Backtest Report

**Generated**: 2026-01-04T22:55:09.886621

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
| Conservative (Stress-Test) | 12 | **Protocol v3.0** | -58.2% | 0.0% | $3,764 | $20,912 | $41,823 |
| Conservative (Stress-Test) | 24 | **Protocol v3.0** | -0.9% | 40.0% | $8,920 | $49,555 | $99,111 |
| Conservative (Stress-Test) | 36 | **Protocol v3.0** | +40.1% | 40.0% | $12,608 | $70,047 | $140,094 |
| Conservative (Stress-Test) | 48 | **Protocol v3.0** | -2.9% | 20.0% | $8,735 | $48,526 | $97,052 |
| Conservative (Stress-Test) | 72 | **Protocol v3.0** | +26.5% | 60.0% | $11,382 | $63,235 | $126,470 |
| Ideal (Growth Scenario) | 12 | **Protocol v3.0** | -42.4% | 0.0% | $5,184 | $28,799 | $57,598 |
| Ideal (Growth Scenario) | 24 | **Protocol v3.0** | +72.7% | 68.7% | $15,542 | $86,343 | $172,687 |
| Ideal (Growth Scenario) | 36 | **Protocol v3.0** | +209.2% | 100.0% | $27,827 | $154,594 | $309,189 |
| Ideal (Growth Scenario) | 48 | **Hybrid Model** | +223.7% | 100.0% | $29,137 | $161,874 | $323,747 |
| Ideal (Growth Scenario) | 72 | **Original Model** | +1244.4% | 100.0% | $120,993 | $672,184 | $1,344,369 |
| Choppy Stress Overlay (10 scenarios aggregated) | 12 | **Protocol v3.0** | -69.7% | 0.0% | $2,730 | $15,168 | $30,336 |
| Choppy Stress Overlay (10 scenarios aggregated) | 24 | **Protocol v3.0** | -21.5% | 28.0% | $7,069 | $39,273 | $78,546 |
| Choppy Stress Overlay (10 scenarios aggregated) | 36 | **Protocol v3.0** | +6.6% | 32.0% | $9,595 | $53,307 | $106,614 |
| Choppy Stress Overlay (10 scenarios aggregated) | 48 | **Protocol v3.0** | -26.8% | 16.0% | $6,586 | $36,588 | $73,176 |
| Choppy Stress Overlay (10 scenarios aggregated) | 72 | **Protocol v3.0** | -7.2% | 38.0% | $8,352 | $46,402 | $92,803 |

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
| Original Model | -92.0% | -62.4% | -44.7% | -49.6% | +3.0% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.5% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 14.0% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +40.1% | -2.9% | +26.5% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.7% | -46.4% | -64.4% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.7% | -58.3% | -64.8% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.6% | -66.6% | -71.8% | -48.2% | 20.0% | 100.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.7% | -49.6% | +3.0% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.5% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 14.0% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +40.1% | -2.9% | +26.5% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.7% | -46.4% | -64.4% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.7% | -58.3% | -64.8% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.6% | -66.6% | -71.8% | -48.2% | 20.0% | 100.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.7% | -49.6% | +3.0% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.5% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.7% | -32.3% | -41.0% | -61.8% | -49.4% | 14.0% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +40.1% | -2.9% | +26.5% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.7% | -46.4% | -64.4% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.6% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.7% | -58.3% | -64.8% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.6% | -66.6% | -71.8% | -48.2% | 20.0% | 100.0% |


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
| Original Model | -87.2% | -6.3% | +113.2% | +191.7% | +1244.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.0% | +152.9% | +223.7% | +1241.3% | 100.0% | 60.0% |
| Protocol v2.6 | -50.6% | +37.7% | +86.4% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.4% | +72.7% | +209.2% | +160.5% | +645.6% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.4% | +19.3% | +44.7% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.8% | -17.6% | +68.2% | +120.6% | +879.7% | 100.0% | 0.0% |
| Harris Model | -72.5% | -34.3% | +29.4% | +63.2% | +576.9% | 100.0% | 100.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.3% | +113.2% | +191.7% | +1244.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.0% | +152.9% | +223.7% | +1241.3% | 100.0% | 60.0% |
| Protocol v2.6 | -50.6% | +37.7% | +86.4% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.4% | +72.7% | +209.2% | +160.5% | +645.6% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.4% | +19.3% | +44.7% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.8% | -17.6% | +68.2% | +120.6% | +879.7% | 100.0% | 0.0% |
| Harris Model | -72.5% | -34.3% | +29.4% | +63.2% | +576.9% | 100.0% | 100.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.3% | +113.2% | +191.7% | +1244.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +21.0% | +152.9% | +223.7% | +1241.3% | 100.0% | 60.0% |
| Protocol v2.6 | -50.6% | +37.7% | +86.4% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.4% | +72.7% | +209.2% | +160.5% | +645.6% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.4% | +19.3% | +44.7% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.4% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.8% | -17.6% | +68.2% | +120.6% | +879.7% | 100.0% | 0.0% |
| Harris Model | -72.5% | -34.3% | +29.4% | +63.2% | +576.9% | 100.0% | 100.0% |


---

## Choppy Stress Overlay (10 scenarios aggregated)

- **choppy_scenarios**: ['Normal Market Conditions', 'May 2021-Style Crash', 'FTX Collapse', 'COVID Black Swan', 'Gradual Bear Market', 'Bull Run Then Crash', 'High Volatility', 'Stable Growth', 'Early Crash with Recovery', 'Multiple Crashes']

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.4% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.8% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.4% | -59.8% | -64.5% | -76.9% | -69.6% | 3.0% | 100.0% |
| Protocol v3.0 | -69.7% | -21.5% | +6.6% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -87.9% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.9% | -83.0% | -68.8% | 4.0% | 100.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.4% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.8% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.4% | -59.8% | -64.5% | -76.9% | -69.6% | 3.0% | 100.0% |
| Protocol v3.0 | -69.7% | -21.5% | +6.6% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -87.9% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.9% | -83.0% | -68.8% | 4.0% | 100.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.4% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.8% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.4% | -59.8% | -64.5% | -76.9% | -69.6% | 3.0% | 100.0% |
| Protocol v3.0 | -69.7% | -21.5% | +6.6% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -87.9% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.9% | -83.0% | -68.8% | 4.0% | 100.0% |

### Per-Scenario Breakdown (Month 72 ROI @ $9,000)

| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | +3.1% | +2.8% | -49.4% | +26.6% | -54.1% | -43.6% | -27.4% | -48.3% |
| May 2021-Style Crash | -58.8% | -58.9% | -79.7% | -21.3% | -79.7% | -96.9% | -85.8% | -79.3% |
| FTX Collapse | -68.6% | -68.8% | -84.6% | -31.9% | -84.5% | -97.7% | -97.0% | -84.2% |
| COVID Black Swan | -78.6% | -78.6% | -89.4% | -47.0% | -89.4% | -98.4% | -97.9% | -89.2% |
| Gradual Bear Market | -41.4% | -41.5% | -71.1% | -3.6% | -71.5% | -84.3% | -64.3% | -70.5% |
| Bull Run Then Crash | -37.9% | -37.9% | -69.9% | -2.6% | -70.2% | -83.3% | -62.1% | -68.9% |
| High Volatility | -44.9% | -44.9% | -72.8% | -7.3% | -73.1% | -85.2% | -66.4% | -72.2% |
| Stable Growth | +28.1% | +27.6% | -38.2% | +38.4% | -47.2% | -29.9% | -9.7% | -35.6% |
| Early Crash with Recovery | -3.3% | -3.7% | -52.6% | +21.4% | -56.0% | -47.1% | -31.9% | -51.4% |
| Multiple Crashes | -77.0% | -77.1% | -88.7% | -44.7% | -88.7% | -98.3% | -97.8% | -88.5% |

