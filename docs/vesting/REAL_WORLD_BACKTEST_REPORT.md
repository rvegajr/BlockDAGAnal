# Real-World Backtest Report (Second Opinion Replay)

**Generated**: 2026-01-04T16:33:00.027890

**Input**: `scripts/_smoke_btc_daily.csv`

**Windows**: 1 rolling windows, 72 months each (step 12)

**Runs/window/model**: 3

**Investment reference**: $9,000

## Winner by horizon (avg ROI across all rolling windows)

| Horizon | Winner | Avg ROI | Avg positive rate |
|---:|---|---:|---:|
| Month 12 | **Protocol v3.0** | -75.9% | 0.0% |
| Month 24 | **Protocol v3.0** | -80.0% | 0.0% |
| Month 36 | **Protocol v3.0** | -80.2% | 0.0% |
| Month 48 | **Protocol v3.0** | -88.5% | 0.0% |
| Month 72 | **Protocol v3.0** | -83.3% | 0.0% |

## Notes
- This is still a *tokenomics stress test* (it includes sell pressure + order-book impact). It becomes more “real-world” by replaying historical market regimes into liquidity/buy-support.
- For true realism you’d also want: project-specific demand modeling (users, fees, incentives), exchange listings, and actual DEX liquidity growth curves.
