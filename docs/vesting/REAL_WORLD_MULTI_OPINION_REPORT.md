# Real-World Multi-Opinion Backtest Report

**Generated**: 2026-01-05T22:20:50.920951

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
| Conservative (Stress-Test) | 12 | **Protocol v5.5 (Maxime)** | -37.3% | 1.3% | $5,641 | $31,337 | $62,674 |
| Conservative (Stress-Test) | 24 | **Protocol v5.5 (Maxime)** | +12.7% | 48.7% | $10,147 | $56,372 | $112,743 |
| Conservative (Stress-Test) | 36 | **Protocol v3.0** | +39.8% | 40.0% | $12,585 | $69,918 | $139,835 |
| Conservative (Stress-Test) | 48 | **Protocol v3.0** | -3.0% | 20.0% | $8,734 | $48,520 | $97,040 |
| Conservative (Stress-Test) | 72 | **Protocol v3.0** | +26.7% | 60.0% | $11,400 | $63,333 | $126,666 |
| Ideal (Growth Scenario) | 12 | **Protocol v5.5 (Maxime)** | -20.2% | 25.3% | $7,181 | $39,894 | $79,789 |
| Ideal (Growth Scenario) | 24 | **Protocol v5.5 (Maxime)** | +107.6% | 64.7% | $18,686 | $103,809 | $207,618 |
| Ideal (Growth Scenario) | 36 | **Protocol v3.0** | +208.9% | 100.0% | $27,802 | $154,458 | $308,916 |
| Ideal (Growth Scenario) | 48 | **Hybrid Model** | +223.6% | 100.0% | $29,121 | $161,781 | $323,563 |
| Ideal (Growth Scenario) | 72 | **Original Model** | +1245.4% | 100.0% | $121,089 | $672,720 | $1,345,439 |
| Choppy Stress Overlay (10 scenarios aggregated) | 12 | **Protocol v5.8 (Maxime)** | -55.6% | 3.0% | $3,998 | $22,208 | $44,417 |
| Choppy Stress Overlay (10 scenarios aggregated) | 24 | **Protocol v5.5 (Maxime)** | -11.5% | 30.0% | $7,965 | $44,251 | $88,502 |
| Choppy Stress Overlay (10 scenarios aggregated) | 36 | **Protocol v3.0** | +6.4% | 32.0% | $9,577 | $53,205 | $106,410 |
| Choppy Stress Overlay (10 scenarios aggregated) | 48 | **Protocol v3.0** | -26.8% | 16.0% | $6,586 | $36,589 | $73,177 |
| Choppy Stress Overlay (10 scenarios aggregated) | 72 | **Protocol v3.0** | -7.2% | 38.0% | $8,353 | $46,405 | $92,810 |

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
| Original Model | -92.0% | -62.4% | -44.8% | -49.6% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.8% | -32.3% | -41.0% | -61.8% | -49.4% | 14.7% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +39.8% | -3.0% | +26.7% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.6% | -46.2% | -64.3% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.1% | -68.4% | -73.0% | -43.5% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.3% | -64.7% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.7% | -66.6% | -71.8% | -48.1% | 20.0% | 100.0% |
| Protocol v5.3 (Maxime) | -50.4% | +10.0% | +3.4% | -25.6% | -15.2% | 40.7% | 100.0% |
| Protocol v5.5 (Maxime) | -37.3% | +12.7% | +7.4% | -23.5% | -14.0% | 41.3% | 100.0% |
| Protocol v5.7 (Maxime) | -50.3% | +9.9% | +3.8% | -25.7% | -15.3% | 40.0% | 100.0% |
| Protocol v5.8 (Maxime) | -37.7% | +12.2% | +6.9% | -23.8% | -14.4% | 40.7% | 100.0% |
| HybridC (Ingo) | -82.9% | -73.5% | -66.1% | -71.5% | -41.4% | 20.0% | 20.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.8% | -49.6% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.8% | -32.3% | -41.0% | -61.8% | -49.4% | 14.7% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +39.8% | -3.0% | +26.7% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.6% | -46.2% | -64.3% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.5% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.3% | -64.7% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.7% | -66.6% | -71.8% | -48.1% | 20.0% | 100.0% |
| Protocol v5.3 (Maxime) | -50.4% | +10.0% | +3.4% | -25.6% | -15.2% | 40.7% | 100.0% |
| Protocol v5.5 (Maxime) | -37.3% | +12.7% | +7.4% | -23.5% | -14.0% | 41.3% | 100.0% |
| Protocol v5.7 (Maxime) | -50.3% | +9.9% | +3.8% | -25.7% | -15.3% | 40.0% | 100.0% |
| Protocol v5.8 (Maxime) | -37.7% | +12.2% | +6.9% | -23.8% | -14.4% | 40.7% | 100.0% |
| HybridC (Ingo) | -82.9% | -73.5% | -66.1% | -71.5% | -41.4% | 20.0% | 20.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -92.0% | -62.4% | -44.8% | -49.6% | +3.1% | 40.0% | 100.0% |
| Hybrid Model | -71.6% | -51.4% | -34.5% | -44.1% | +2.8% | 40.0% | 100.0% |
| Protocol v2.6 | -64.8% | -32.3% | -41.0% | -61.8% | -49.4% | 14.7% | 100.0% |
| Protocol v3.0 | -58.2% | -0.9% | +39.8% | -3.0% | +26.7% | 60.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -65.9% | -40.6% | -46.2% | -64.3% | -54.0% | 0.0% | 100.0% |
| Hybrid B | -85.6% | -76.0% | -68.4% | -73.0% | -43.5% | 20.0% | 20.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -79.5% | -67.6% | -58.3% | -64.7% | -27.4% | 40.0% | 20.0% |
| Harris Model | -82.9% | -73.7% | -66.6% | -71.8% | -48.1% | 20.0% | 100.0% |
| Protocol v5.3 (Maxime) | -50.4% | +10.0% | +3.4% | -25.6% | -15.2% | 40.7% | 100.0% |
| Protocol v5.5 (Maxime) | -37.3% | +12.7% | +7.4% | -23.5% | -14.0% | 41.3% | 100.0% |
| Protocol v5.7 (Maxime) | -50.3% | +9.9% | +3.8% | -25.7% | -15.3% | 40.0% | 100.0% |
| Protocol v5.8 (Maxime) | -37.7% | +12.2% | +6.9% | -23.8% | -14.4% | 40.7% | 100.0% |
| HybridC (Ingo) | -82.9% | -73.5% | -66.1% | -71.5% | -41.4% | 20.0% | 20.0% |


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
| Original Model | -87.2% | -6.4% | +113.4% | +191.8% | +1245.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +20.8% | +152.8% | +223.6% | +1240.2% | 100.0% | 60.0% |
| Protocol v2.6 | -50.7% | +37.8% | +86.3% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.6% | +72.7% | +208.9% | +160.1% | +646.0% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.3% | +19.5% | +44.4% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.6% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.5% | +68.3% | +120.6% | +879.8% | 100.0% | 0.0% |
| Harris Model | -72.6% | -34.3% | +28.9% | +63.1% | +576.6% | 100.0% | 100.0% |
| Protocol v5.3 (Maxime) | -35.8% | +81.7% | +125.1% | +85.9% | +572.8% | 100.0% | 60.0% |
| Protocol v5.5 (Maxime) | -20.2% | +107.6% | +129.7% | +90.5% | +595.6% | 100.0% | 57.3% |
| Protocol v5.7 (Maxime) | -36.1% | +81.0% | +124.1% | +85.8% | +572.5% | 100.0% | 60.0% |
| Protocol v5.8 (Maxime) | -20.3% | +106.0% | +127.8% | +90.0% | +595.7% | 100.0% | 58.0% |
| HybridC (Ingo) | -72.3% | -32.6% | +36.7% | +78.5% | +690.2% | 100.0% | 0.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.4% | +113.4% | +191.8% | +1245.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +20.8% | +152.8% | +223.6% | +1240.2% | 100.0% | 60.0% |
| Protocol v2.6 | -50.7% | +37.8% | +86.3% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.6% | +72.7% | +208.9% | +160.1% | +646.0% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.3% | +19.5% | +44.4% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.6% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.5% | +68.3% | +120.6% | +879.8% | 100.0% | 0.0% |
| Harris Model | -72.6% | -34.3% | +28.9% | +63.1% | +576.6% | 100.0% | 100.0% |
| Protocol v5.3 (Maxime) | -35.8% | +81.7% | +125.1% | +85.9% | +572.8% | 100.0% | 60.0% |
| Protocol v5.5 (Maxime) | -20.2% | +107.6% | +129.7% | +90.5% | +595.6% | 100.0% | 57.3% |
| Protocol v5.7 (Maxime) | -36.1% | +81.0% | +124.1% | +85.8% | +572.5% | 100.0% | 60.0% |
| Protocol v5.8 (Maxime) | -20.3% | +106.0% | +127.8% | +90.0% | +595.7% | 100.0% | 58.0% |
| HybridC (Ingo) | -72.3% | -32.6% | +36.7% | +78.5% | +690.2% | 100.0% | 0.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -87.2% | -6.4% | +113.4% | +191.8% | +1245.4% | 100.0% | 20.0% |
| Hybrid Model | -54.7% | +20.8% | +152.8% | +223.6% | +1240.2% | 100.0% | 60.0% |
| Protocol v2.6 | -50.7% | +37.8% | +86.3% | +82.0% | +305.7% | 100.0% | 80.0% |
| Protocol v3.0 | -42.6% | +72.7% | +208.9% | +160.1% | +646.0% | 100.0% | 20.0% |
| Protocol v3.1 (Adjusted) | -54.3% | +19.5% | +44.4% | +23.9% | +287.4% | 100.0% | 100.0% |
| Hybrid B | -76.7% | -38.9% | +27.5% | +69.2% | +661.6% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -66.7% | -17.5% | +68.3% | +120.6% | +879.8% | 100.0% | 0.0% |
| Harris Model | -72.6% | -34.3% | +28.9% | +63.1% | +576.6% | 100.0% | 100.0% |
| Protocol v5.3 (Maxime) | -35.8% | +81.7% | +125.1% | +85.9% | +572.8% | 100.0% | 60.0% |
| Protocol v5.5 (Maxime) | -20.2% | +107.6% | +129.7% | +90.5% | +595.6% | 100.0% | 57.3% |
| Protocol v5.7 (Maxime) | -36.1% | +81.0% | +124.1% | +85.8% | +572.5% | 100.0% | 60.0% |
| Protocol v5.8 (Maxime) | -20.3% | +106.0% | +127.8% | +90.0% | +595.7% | 100.0% | 58.0% |
| HybridC (Ingo) | -72.3% | -32.6% | +36.7% | +78.5% | +690.2% | 100.0% | 0.0% |


---

## Choppy Stress Overlay (10 scenarios aggregated)

- **choppy_scenarios**: ['Normal Market Conditions', 'May 2021-Style Crash', 'FTX Collapse', 'COVID Black Swan', 'Gradual Bear Market', 'Bull Run Then Crash', 'High Volatility', 'Stable Growth', 'Early Crash with Recovery', 'Multiple Crashes']

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.3% | +6.4% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.8% | -82.9% | -68.8% | 4.0% | 100.0% |
| Protocol v5.3 (Maxime) | -66.7% | -21.1% | -21.3% | -44.0% | -32.9% | 24.3% | 100.0% |
| Protocol v5.5 (Maxime) | -55.7% | -11.5% | -14.8% | -40.7% | -30.8% | 25.3% | 100.0% |
| Protocol v5.7 (Maxime) | -67.2% | -21.3% | -21.6% | -44.1% | -32.9% | 22.7% | 100.0% |
| Protocol v5.8 (Maxime) | -55.6% | -12.5% | -14.6% | -40.7% | -30.7% | 26.0% | 100.0% |
| HybridC (Ingo) | -90.0% | -85.8% | -83.7% | -87.3% | -74.6% | 8.0% | 68.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.3% | +6.4% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.8% | -82.9% | -68.8% | 4.0% | 100.0% |
| Protocol v5.3 (Maxime) | -66.7% | -21.1% | -21.3% | -44.0% | -32.9% | 24.3% | 100.0% |
| Protocol v5.5 (Maxime) | -55.7% | -11.5% | -14.8% | -40.7% | -30.8% | 25.3% | 100.0% |
| Protocol v5.7 (Maxime) | -67.2% | -21.3% | -21.6% | -44.1% | -32.9% | 22.7% | 100.0% |
| Protocol v5.8 (Maxime) | -55.6% | -12.5% | -14.6% | -40.7% | -30.7% | 26.0% | 100.0% |
| HybridC (Ingo) | -90.0% | -85.8% | -83.7% | -87.3% | -74.6% | 8.0% | 68.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -95.2% | -77.3% | -66.7% | -69.5% | -37.9% | 18.0% | 98.0% |
| Hybrid Model | -82.9% | -70.7% | -60.5% | -66.2% | -38.1% | 18.0% | 100.0% |
| Protocol v2.6 | -78.3% | -59.8% | -64.5% | -76.9% | -69.6% | 2.7% | 100.0% |
| Protocol v3.0 | -69.6% | -21.3% | +6.4% | -26.8% | -7.2% | 38.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -79.2% | -62.6% | -66.4% | -77.9% | -71.4% | 0.0% | 100.0% |
| Hybrid B | -91.7% | -88.1% | -86.3% | -88.8% | -76.5% | 8.0% | 70.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -88.0% | -81.9% | -78.0% | -82.2% | -64.0% | 12.0% | 56.0% |
| Harris Model | -89.7% | -84.1% | -79.8% | -82.9% | -68.8% | 4.0% | 100.0% |
| Protocol v5.3 (Maxime) | -66.7% | -21.1% | -21.3% | -44.0% | -32.9% | 24.3% | 100.0% |
| Protocol v5.5 (Maxime) | -55.7% | -11.5% | -14.8% | -40.7% | -30.8% | 25.3% | 100.0% |
| Protocol v5.7 (Maxime) | -67.2% | -21.3% | -21.6% | -44.1% | -32.9% | 22.7% | 100.0% |
| Protocol v5.8 (Maxime) | -55.6% | -12.5% | -14.6% | -40.7% | -30.7% | 26.0% | 100.0% |
| HybridC (Ingo) | -90.0% | -85.8% | -83.7% | -87.3% | -74.6% | 8.0% | 68.0% |

### Per-Scenario Breakdown (Month 72 ROI @ $9,000)

| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) | Harris Model | Protocol v5.3 (Maxime) | Protocol v5.5 (Maxime) | Protocol v5.7 (Maxime) | Protocol v5.8 (Maxime) | HybridC (Ingo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | +3.1% | +2.7% | -49.4% | +26.6% | -53.9% | -43.6% | -27.4% | -48.2% | -16.4% | -14.4% | -15.2% | -14.7% | -41.4% |
| May 2021-Style Crash | -58.8% | -58.8% | -79.7% | -21.3% | -79.7% | -96.9% | -85.8% | -79.3% | -37.6% | -35.3% | -37.3% | -35.3% | -96.8% |
| FTX Collapse | -68.7% | -68.7% | -84.6% | -31.8% | -84.5% | -97.7% | -97.0% | -84.3% | -46.8% | -42.2% | -46.8% | -42.4% | -97.6% |
| COVID Black Swan | -78.6% | -78.6% | -89.4% | -47.1% | -89.4% | -98.4% | -97.9% | -89.2% | -57.4% | -53.9% | -57.5% | -53.8% | -98.3% |
| Gradual Bear Market | -41.4% | -41.6% | -71.1% | -3.5% | -71.5% | -84.3% | -64.3% | -70.5% | -28.9% | -29.1% | -29.1% | -28.4% | -83.7% |
| Bull Run Then Crash | -37.8% | -38.0% | -69.9% | -2.6% | -70.3% | -83.3% | -62.2% | -68.7% | -28.9% | -27.1% | -29.1% | -27.5% | -73.3% |
| High Volatility | -44.9% | -45.0% | -72.8% | -7.3% | -73.1% | -85.2% | -66.4% | -72.3% | -30.9% | -29.4% | -30.9% | -29.8% | -84.7% |
| Stable Growth | +28.1% | +28.0% | -38.2% | +38.5% | -47.1% | -29.8% | -9.7% | -35.6% | -9.2% | -8.2% | -9.8% | -7.7% | -27.2% |
| Early Crash with Recovery | -3.3% | -3.6% | -52.6% | +21.5% | -55.8% | -47.1% | -31.9% | -51.3% | -15.9% | -16.1% | -16.8% | -15.1% | -45.1% |
| Multiple Crashes | -77.0% | -77.1% | -88.7% | -44.7% | -88.7% | -98.3% | -97.8% | -88.4% | -56.5% | -52.2% | -56.5% | -52.6% | -98.2% |

