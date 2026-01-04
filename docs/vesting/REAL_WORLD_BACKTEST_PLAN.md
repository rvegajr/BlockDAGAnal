# Real-World ROI Backtest Plan (Historical Replay)

## Goal

Test **realistic ROI behavior** by replaying **historical crypto market regimes** (returns/volatility/volume) into our **second-opinion** microstructure harness (sell pressure + order-book impact), across **rolling windows** since early crypto history.

This answers:
- “Under what historical regimes do we ever see positive ROI?”
- “Which tokenomics model is best across *real* regime mixes (2013–today style windows)?”

## What “real-world” means here

Our current harness is conservative by design (sell pressure + slippage). This backtest adds realism by:
- Driving **liquidity** with historical market returns (risk-on / risk-off cycles)
- Optionally adding a **buy-support proxy** from positive returns (and optionally market volume)

It still does *not* model:
- project-specific demand growth (users/fees/utility)
- listing effects / market-maker programs
- chain-specific liquidity provisioning mechanics

## Data requirement (CSV)

Provide a daily CSV with these columns:
- `date` (YYYY-MM-DD)
- `close` (USD price)
- `volume` (optional but recommended)

Example header:

```csv
date,close,volume
2018-01-01,13412.44,22160000000
...
```

You can use BTC or ETH history; BTC is typically best as a “whole-market” regime driver.

## How the replay works (high level)

The script converts daily data → monthly data:
- month-end close
- monthly return
- within-month volatility proxy
- monthly volume (sum), if provided

Then it replays month-by-month:
- **Liquidity path** follows market returns (with volatility penalty)
- Optional **buy support** offsets some sell pressure in risk-on months

## Running the backtest

```bash
python3 scripts/real_world_backtest_second_opinion.py \
  --csv /path/to/btc_daily.csv \
  --launch-liquidity 32000000 \
  --window-months 72 \
  --step-months 1 \
  --runs 50 \
  --use-volume
```

### Outputs

- `backtest_second_opinion_results.json`
- `docs/vesting/REAL_WORLD_BACKTEST_REPORT.md`

## Recommended defaults (starting point)

- **window**: 72 months (6 years)
- **step**: 1 month (rolling)
- **runs**: 50 per window per model
- **use volume**: on (if you have volume)

If runtime is too slow:
- increase `--step-months` to 3 or 6
- reduce `--runs` to 20


