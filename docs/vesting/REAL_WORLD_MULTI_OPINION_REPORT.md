# Real-World Multi-Opinion Backtest Report

**Generated**: 2026-01-04T16:52:29.476870

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
| Conservative (Stress-Test) | 12 | **Protocol v3.0** | -71.8% | 0.0% | $2,536 | $14,090 | $28,180 |
| Conservative (Stress-Test) | 24 | **Protocol v3.0** | -57.7% | 0.0% | $3,806 | $21,143 | $42,287 |
| Conservative (Stress-Test) | 36 | **Protocol v3.0** | -55.3% | 0.0% | $4,025 | $22,360 | $44,721 |
| Conservative (Stress-Test) | 48 | **Protocol v3.0** | -71.4% | 0.0% | $2,571 | $14,282 | $28,564 |
| Conservative (Stress-Test) | 72 | **Protocol v3.0** | -71.2% | 0.0% | $2,592 | $14,399 | $28,799 |
| Ideal (Growth Scenario) | 12 | **Protocol v3.0** | -53.6% | 0.0% | $4,176 | $23,201 | $46,401 |
| Ideal (Growth Scenario) | 24 | **Protocol v3.0** | -18.6% | 0.0% | $7,327 | $40,703 | $81,406 |
| Ideal (Growth Scenario) | 36 | **Protocol v3.0** | +24.9% | 100.0% | $11,242 | $62,456 | $124,912 |
| Ideal (Growth Scenario) | 48 | **Protocol v3.0** | +18.8% | 100.0% | $10,688 | $59,381 | $118,761 |
| Ideal (Growth Scenario) | 72 | **Protocol v3.0** | +130.8% | 100.0% | $20,774 | $115,412 | $230,823 |
| Choppy Stress Overlay (10 scenarios aggregated) | 12 | **Protocol v3.0** | -81.1% | 0.0% | $1,700 | $9,443 | $18,887 |
| Choppy Stress Overlay (10 scenarios aggregated) | 24 | **Protocol v3.0** | -71.2% | 0.0% | $2,596 | $14,420 | $28,839 |
| Choppy Stress Overlay (10 scenarios aggregated) | 36 | **Protocol v3.0** | -70.7% | 0.0% | $2,634 | $14,633 | $29,265 |
| Choppy Stress Overlay (10 scenarios aggregated) | 48 | **Protocol v3.0** | -81.6% | 0.0% | $1,657 | $9,207 | $18,413 |
| Choppy Stress Overlay (10 scenarios aggregated) | 72 | **Protocol v3.0** | -81.7% | 0.0% | $1,643 | $9,130 | $18,260 |

---

## Conservative (Stress-Test)

- **liquidity_cagr_annual**: 0.0
- **net_inflow_monthly_pct**: 0.0
- **choppy_overlay**: None
- **window_months**: 72
- **runs_per_window**: 5

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -96.6% | -92.9% | -91.7% | -92.6% | -88.3% | 0.0% | 100.0% |
| Hybrid Model | -87.7% | -90.9% | -90.2% | -91.8% | -88.3% | 0.0% | 100.0% |
| Protocol v2.6 | -82.9% | -87.1% | -91.0% | -94.3% | -94.2% | 0.0% | 100.0% |
| Protocol v3.0 | -71.8% | -57.7% | -55.3% | -71.4% | -71.2% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -83.3% | -87.2% | -91.1% | -94.3% | -94.3% | 0.0% | 100.0% |
| Hybrid B | -93.7% | -98.4% | -98.8% | -99.2% | -99.1% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -91.0% | -97.8% | -98.4% | -98.9% | -98.9% | 0.0% | 100.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -96.6% | -92.9% | -91.7% | -92.6% | -88.3% | 0.0% | 100.0% |
| Hybrid Model | -87.7% | -90.9% | -90.2% | -91.8% | -88.3% | 0.0% | 100.0% |
| Protocol v2.6 | -82.9% | -87.1% | -91.0% | -94.3% | -94.2% | 0.0% | 100.0% |
| Protocol v3.0 | -71.8% | -57.7% | -55.3% | -71.4% | -71.2% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -83.3% | -87.2% | -91.1% | -94.3% | -94.3% | 0.0% | 100.0% |
| Hybrid B | -93.7% | -98.4% | -98.8% | -99.2% | -99.1% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -91.0% | -97.8% | -98.4% | -98.9% | -98.9% | 0.0% | 100.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -96.6% | -92.9% | -91.7% | -92.6% | -88.3% | 0.0% | 100.0% |
| Hybrid Model | -87.7% | -90.9% | -90.2% | -91.8% | -88.3% | 0.0% | 100.0% |
| Protocol v2.6 | -82.9% | -87.1% | -91.0% | -94.3% | -94.2% | 0.0% | 100.0% |
| Protocol v3.0 | -71.8% | -57.7% | -55.3% | -71.4% | -71.2% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -83.3% | -87.2% | -91.1% | -94.3% | -94.3% | 0.0% | 100.0% |
| Hybrid B | -93.7% | -98.4% | -98.8% | -99.2% | -99.1% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -91.0% | -97.8% | -98.4% | -98.9% | -98.9% | 0.0% | 100.0% |


---

## Ideal (Growth Scenario)

- **liquidity_cagr_annual**: 0.5
- **net_inflow_monthly_pct**: 0.01
- **choppy_overlay**: None
- **window_months**: 72
- **runs_per_window**: 5

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -94.3% | -81.2% | -64.6% | -50.8% | +80.2% | 100.0% | 100.0% |
| Hybrid Model | -80.0% | -75.7% | -58.0% | -45.4% | +80.2% | 100.0% | 100.0% |
| Protocol v2.6 | -71.8% | -65.4% | -61.9% | -62.1% | -11.3% | 0.0% | 100.0% |
| Protocol v3.0 | -53.6% | -18.6% | +24.9% | +18.8% | +130.8% | 100.0% | 0.0% |
| Protocol v3.1 (Adjusted) | -73.1% | -66.2% | -62.5% | -62.6% | -12.0% | 0.0% | 100.0% |
| Hybrid B | -89.6% | -87.6% | -78.9% | -71.5% | +1.7% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -85.2% | -83.4% | -72.1% | -62.9% | +30.9% | 100.0% | 0.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -94.3% | -81.2% | -64.6% | -50.8% | +80.2% | 100.0% | 100.0% |
| Hybrid Model | -80.0% | -75.7% | -58.0% | -45.4% | +80.2% | 100.0% | 100.0% |
| Protocol v2.6 | -71.8% | -65.4% | -61.9% | -62.1% | -11.3% | 0.0% | 100.0% |
| Protocol v3.0 | -53.6% | -18.6% | +24.9% | +18.8% | +130.8% | 100.0% | 0.0% |
| Protocol v3.1 (Adjusted) | -73.1% | -66.2% | -62.5% | -62.6% | -12.0% | 0.0% | 100.0% |
| Hybrid B | -89.6% | -87.6% | -78.9% | -71.5% | +1.7% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -85.2% | -83.4% | -72.1% | -62.9% | +30.9% | 100.0% | 0.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -94.3% | -81.2% | -64.6% | -50.8% | +80.2% | 100.0% | 100.0% |
| Hybrid Model | -80.0% | -75.7% | -58.0% | -45.4% | +80.2% | 100.0% | 100.0% |
| Protocol v2.6 | -71.8% | -65.4% | -61.9% | -62.1% | -11.3% | 0.0% | 100.0% |
| Protocol v3.0 | -53.6% | -18.6% | +24.9% | +18.8% | +130.8% | 100.0% | 0.0% |
| Protocol v3.1 (Adjusted) | -73.1% | -66.2% | -62.5% | -62.6% | -12.0% | 0.0% | 100.0% |
| Hybrid B | -89.6% | -87.6% | -78.9% | -71.5% | +1.7% | 100.0% | 0.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -85.2% | -83.4% | -72.1% | -62.9% | +30.9% | 100.0% | 0.0% |


---

## Choppy Stress Overlay (10 scenarios aggregated)

- **choppy_scenarios**: ['Normal Market Conditions', 'May 2021-Style Crash', 'FTX Collapse', 'COVID Black Swan', 'Gradual Bear Market', 'Bull Run Then Crash', 'High Volatility', 'Stable Growth', 'Early Crash with Recovery', 'Multiple Crashes']

### Investment: $9,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -97.9% | -95.7% | -94.9% | -95.4% | -92.8% | 0.0% | 100.0% |
| Hybrid Model | -92.7% | -94.4% | -94.0% | -94.9% | -92.8% | 0.0% | 100.0% |
| Protocol v2.6 | -89.7% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Protocol v3.0 | -81.1% | -71.2% | -70.7% | -81.6% | -81.7% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -89.9% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Hybrid B | -96.9% | -99.0% | -99.2% | -99.5% | -99.5% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -95.1% | -98.6% | -99.0% | -99.3% | -99.3% | 0.0% | 100.0% |

### Investment: $50,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -97.9% | -95.7% | -94.9% | -95.4% | -92.8% | 0.0% | 100.0% |
| Hybrid Model | -92.7% | -94.4% | -94.0% | -94.9% | -92.8% | 0.0% | 100.0% |
| Protocol v2.6 | -89.7% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Protocol v3.0 | -81.1% | -71.2% | -70.7% | -81.6% | -81.7% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -89.9% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Hybrid B | -96.9% | -99.0% | -99.2% | -99.5% | -99.5% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -95.1% | -98.6% | -99.0% | -99.3% | -99.3% | 0.0% | 100.0% |

### Investment: $100,000

| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Original Model | -97.9% | -95.7% | -94.9% | -95.4% | -92.8% | 0.0% | 100.0% |
| Hybrid Model | -92.7% | -94.4% | -94.0% | -94.9% | -92.8% | 0.0% | 100.0% |
| Protocol v2.6 | -89.7% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Protocol v3.0 | -81.1% | -71.2% | -70.7% | -81.6% | -81.7% | 0.0% | 100.0% |
| Protocol v3.1 (Adjusted) | -89.9% | -92.1% | -94.5% | -96.5% | -96.4% | 0.0% | 100.0% |
| Hybrid B | -96.9% | -99.0% | -99.2% | -99.5% | -99.5% | 0.0% | 100.0% |
| Hybrid Tokenomics (Solvency-Anchored) | -95.1% | -98.6% | -99.0% | -99.3% | -99.3% | 0.0% | 100.0% |

### Per-Scenario Breakdown (Month 72 ROI @ $9,000)

| Scenario | Original Model | Hybrid Model | Protocol v2.6 | Protocol v3.0 | Protocol v3.1 (Adjusted) | Hybrid B | Hybrid Tokenomics (Solvency-Anchored) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal Market Conditions | -88.3% | -88.4% | -94.2% | -71.2% | -94.3% | -99.1% | -98.9% |
| May 2021-Style Crash | -95.3% | -95.4% | -97.7% | -87.0% | -97.7% | -99.7% | -99.6% |
| FTX Collapse | -96.5% | -96.5% | -98.3% | -90.3% | -98.3% | -99.7% | -99.7% |
| COVID Black Swan | -96.5% | -96.6% | -98.3% | -90.4% | -98.3% | -99.7% | -99.7% |
| Gradual Bear Market | -93.4% | -93.4% | -96.7% | -82.4% | -96.7% | -99.5% | -99.4% |
| Bull Run Then Crash | -92.9% | -92.9% | -96.5% | -83.2% | -96.5% | -99.5% | -99.3% |
| High Volatility | -93.7% | -93.7% | -96.9% | -83.7% | -96.9% | -99.5% | -99.4% |
| Stable Growth | -85.4% | -85.4% | -92.8% | -65.7% | -92.9% | -98.9% | -98.6% |
| Early Crash with Recovery | -89.0% | -89.0% | -94.6% | -72.7% | -94.6% | -99.2% | -99.0% |
| Multiple Crashes | -96.6% | -96.6% | -98.3% | -90.7% | -98.3% | -99.7% | -99.7% |

