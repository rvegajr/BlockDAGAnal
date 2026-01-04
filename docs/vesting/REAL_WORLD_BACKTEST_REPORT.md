# Real-World Backtest Report (Second Opinion Replay)

**Generated**: 2026-01-04T16:45:49.337748

**Input**: `scripts/_smoke_btc_daily.csv`

**Windows**: 1 rolling windows, 72 months each (step 12)

**Runs/window/model**: 3

**Investment levels**: $9,000, $50,000, $100,000

## Winner by horizon (avg ROI across all rolling windows)

| Horizon | Winner (by ROI) | Avg ROI | Avg positive rate | Avg value @ $9k | Avg value @ $50k | Avg value @ $100k |
|---:|---|---:|---:|---:|---:|---:|
| Month 12 | **Protocol v3.0** | -61.4% | 0.0% | $3,476 | $19,311 | $38,623 |
| Month 24 | **Protocol v3.0** | -55.0% | 0.0% | $4,054 | $22,522 | $45,044 |
| Month 36 | **Protocol v3.0** | -20.0% | 0.0% | $7,199 | $39,995 | $79,990 |
| Month 48 | **Protocol v3.0** | -23.8% | 0.0% | $6,857 | $38,095 | $76,191 |
| Month 72 | **Protocol v3.0** | +111.2% | 100.0% | $19,006 | $105,590 | $211,180 |

## Notes
- This is still a *tokenomics stress test* (it includes sell pressure + order-book impact). It becomes more “real-world” by replaying historical market regimes into liquidity/buy-support.
- For true realism you’d also want: project-specific demand modeling (users, fees, incentives), exchange listings, and actual DEX liquidity growth curves.
