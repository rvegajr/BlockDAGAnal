# Vesting Solution - Market Simulations

## Quick Start

Run 10 different market scenario simulations:

```bash
python3 scripts/vesting_simulations.py
```

This will:
1. Simulate 10 different market scenarios over 24 months
2. Show emergency brake activation in each scenario
3. Generate detailed JSON results file
4. Display summary comparison

## Scenarios Included

1. **May 2021-Style Crash** - Major crypto crash 2 months after launch
2. **FTX Collapse** - Exchange collapse 3 months after launch
3. **COVID-Style Black Swan** - Black swan event 1 month after launch
4. **Gradual Bear Market** - Slow decline over 12 months
5. **Bull Run Then Crash** - Strong growth then 70% crash
6. **High Volatility** - Multiple 30-40% swings
7. **Stable Growth** - Gradual 20% liquidity increase
8. **Early Crash with Recovery** - Crash then recovery
9. **Late Market Crash** - Crash at month 9 after growth
10. **Worst Case** - Multiple crashes at months 2, 6, 12

## Key Metrics Tracked

- **Circulating Supply** - Total tokens in circulation (after staking)
- **Price** - Calculated from liquidity ÷ circulating supply
- **Market Cap** - Price × circulating supply
- **Emergency Brake Status** - Whether protection mechanisms activated
- **Staking Rate** - Percentage of supply staked

## Results

See [SIMULATION_RESULTS.md](./SIMULATION_RESULTS.md) for detailed analysis.

## Customizing Simulations

Edit `scripts/vesting_simulations.py` to:
- Change launch date
- Adjust liquidity amounts
- Modify staking rates
- Add custom market events
- Extend simulation period

## Understanding the Output

### Emergency Brake Activation

If you see `⚠️ EMERGENCY BRAKE TRIGGERED`, this means:
- ✅ Protection mechanisms are working
- ✅ Vesting unlocks have been paused
- ✅ System is protecting against further sell pressure

### Price Drops

Price drops are expected when:
- Liquidity decreases (market crash)
- Circulating supply grows (mining emissions)
- Both occur simultaneously

**This is normal market behavior** - the emergency brake prevents additional pressure from vesting unlocks.

### Recovery Potential

Scenarios show recovery is possible when:
- Liquidity returns to market
- Staking participation increases
- Network utility grows

---

*For questions or custom scenarios, see the simulation script source code.*


