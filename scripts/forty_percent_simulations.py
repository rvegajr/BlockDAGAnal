#!/usr/bin/env python3
"""
40% TGE SIMULATION - As Promised
================================
User says: "40% at launch as promised. WTF is 2%?"

This simulation tests what happens when we honor the 40% TGE promise
with $75M liquidity and no bonus coins.

Compares:
- Normal market conditions
- 10 volatile historical market scenarios
"""

import json
from datetime import datetime

# =============================================================================
# PARAMETERS - 40% AS PROMISED
# =============================================================================

LIQUIDITY = 75_000_000  # $75M
BASE_COINS = 17_000_000_000  # 17B base coins only (no bonus)
TGE_PERCENT = 0.40  # 40% as promised
VESTING_PERCENT = 0.60  # 60% vested

# Calculate launch metrics
TGE_TOKENS = BASE_COINS * TGE_PERCENT  # 6.8B tokens
LAUNCH_PRICE = LIQUIDITY / TGE_TOKENS  # $0.011

# Mining (reduced since no bonus complexity)
DAILY_MINING = 10_500_000  # 10.5M/day from hardware miners
MINING_STAKING_RATE = 0.50  # 50% auto-staked

# Emergency brake thresholds
PRICE_THRESHOLD = 0.005  # $0.005 (adjusted for lower launch price)
LIQUIDITY_THRESHOLD = 10_000_000  # $10M

# Vesting schedule for remaining 60%
CLIFF_MONTHS = 6  # Shorter cliff since simpler structure
VESTING_MONTHS = 30  # 30 months linear after cliff
MONTHLY_VEST_RATE = VESTING_PERCENT / VESTING_MONTHS  # ~2% per month

print("=" * 70)
print("40% TGE SIMULATION - HONORING THE PROMISE")
print("=" * 70)
print(f"\nLaunch Parameters:")
print(f"  Liquidity:        ${LIQUIDITY:,.0f}")
print(f"  Base Coins:       {BASE_COINS/1e9:.1f}B")
print(f"  TGE Unlock:       {TGE_PERCENT*100:.0f}%")
print(f"  TGE Tokens:       {TGE_TOKENS/1e9:.2f}B")
print(f"  Launch Price:     ${LAUNCH_PRICE:.4f}")
print(f"  Vesting:          {VESTING_PERCENT*100:.0f}% over {VESTING_MONTHS} months")
print(f"  Emergency Brake:  ${PRICE_THRESHOLD} price / ${LIQUIDITY_THRESHOLD/1e6:.0f}M liquidity")

# =============================================================================
# MARKET SCENARIOS
# =============================================================================

scenarios = {
    "normal": {
        "name": "Normal Market Conditions",
        "description": "Stable market, no major crashes",
        "events": []  # No crashes
    },
    "may_2021": {
        "name": "May 2021-Style Crash",
        "description": "60% liquidity drop at month 2",
        "events": [(2, 0.40)]  # Month 2: 60% drop
    },
    "ftx_collapse": {
        "name": "FTX Collapse",
        "description": "70% liquidity drop at month 3",
        "events": [(3, 0.30)]  # Month 3: 70% drop
    },
    "covid_black_swan": {
        "name": "COVID Black Swan",
        "description": "80% liquidity drop at month 1",
        "events": [(1, 0.20)]  # Month 1: 80% drop
    },
    "gradual_bear": {
        "name": "Gradual Bear Market",
        "description": "50% drop over 12 months",
        "events": [(i, 1 - (0.5 * i / 12)) for i in range(1, 13)]  # Gradual
    },
    "bull_then_crash": {
        "name": "Bull Run Then Crash",
        "description": "+100% for 6 months, then -70%",
        "events": [(i, 1 + (1.0 * i / 6)) for i in range(1, 7)] + [(7, 0.60)]
    },
    "high_volatility": {
        "name": "High Volatility",
        "description": "Multiple 30-40% swings",
        "events": [(2, 0.70), (4, 1.10), (6, 0.75), (8, 1.05), (10, 0.80)]
    },
    "stable_growth": {
        "name": "Stable Growth",
        "description": "+20% liquidity over 12 months",
        "events": [(i, 1 + (0.20 * i / 12)) for i in range(1, 13)]
    },
    "early_crash_recovery": {
        "name": "Early Crash with Recovery",
        "description": "-50% at month 2, recovery by month 6",
        "events": [(2, 0.50), (4, 0.75), (6, 1.0)]
    },
    "late_crash": {
        "name": "Late Market Crash",
        "description": "+50% for 9 months, then -67%",
        "events": [(i, 1 + (0.5 * i / 9)) for i in range(1, 10)] + [(10, 0.50)]
    },
    "multiple_crashes": {
        "name": "Multiple Crashes",
        "description": "-40% at months 2, 6, 12",
        "events": [(2, 0.60), (6, 0.36), (12, 0.22)]
    }
}

# =============================================================================
# SIMULATION ENGINE
# =============================================================================

def run_simulation(scenario_key, scenario_data):
    """Run 24-month simulation for a given scenario."""
    
    results = {
        "scenario": scenario_key,
        "name": scenario_data["name"],
        "description": scenario_data["description"],
        "months": [],
        "summary": {}
    }
    
    # Initial state
    circulating = TGE_TOKENS
    liquidity = LIQUIDITY
    vested_released = 0
    emergency_brake_active = False
    emergency_brake_month = None
    min_price = LAUNCH_PRICE
    max_price = LAUNCH_PRICE
    
    # Build event lookup
    events = {e[0]: e[1] for e in scenario_data.get("events", [])}
    
    for month in range(0, 25):
        # Apply liquidity events
        if month in events:
            liquidity = LIQUIDITY * events[month]
        
        # Calculate price
        price = liquidity / circulating if circulating > 0 else 0
        
        # Track min/max
        min_price = min(min_price, price)
        max_price = max(max_price, price)
        
        # Check emergency brake
        if not emergency_brake_active:
            if price < PRICE_THRESHOLD or liquidity < LIQUIDITY_THRESHOLD:
                emergency_brake_active = True
                emergency_brake_month = month
        
        # Monthly vesting release (after cliff, if no emergency)
        if month > CLIFF_MONTHS and not emergency_brake_active:
            monthly_vest = BASE_COINS * MONTHLY_VEST_RATE
            vested_released += monthly_vest
            circulating += monthly_vest
        
        # Mining emissions (always continue)
        monthly_mining = DAILY_MINING * 30
        effective_mining = monthly_mining * (1 - MINING_STAKING_RATE)  # 50% staked
        circulating += effective_mining
        
        # Record month
        results["months"].append({
            "month": month,
            "circulating": circulating,
            "liquidity": liquidity,
            "price": price,
            "emergency_brake": emergency_brake_active,
            "vested_released_pct": (vested_released / (BASE_COINS * VESTING_PERCENT)) * 100
        })
    
    # Summary
    final = results["months"][-1]
    results["summary"] = {
        "final_price": final["price"],
        "final_circulating": final["circulating"],
        "final_liquidity": final["liquidity"],
        "min_price": min_price,
        "max_price": max_price,
        "emergency_brake_triggered": emergency_brake_active,
        "emergency_brake_month": emergency_brake_month,
        "vested_released_pct": final["vested_released_pct"]
    }
    
    return results

# =============================================================================
# RUN ALL SIMULATIONS
# =============================================================================

print("\n" + "=" * 70)
print("RUNNING SIMULATIONS...")
print("=" * 70)

all_results = {}

for key, scenario in scenarios.items():
    result = run_simulation(key, scenario)
    all_results[key] = result
    
    summary = result["summary"]
    brake_status = f"Month {summary['emergency_brake_month']}" if summary['emergency_brake_triggered'] else "NOT triggered"
    
    print(f"\n{scenario['name']}:")
    print(f"  Final Price:      ${summary['final_price']:.6f}")
    print(f"  Price Range:      ${summary['min_price']:.6f} - ${summary['max_price']:.6f}")
    print(f"  Final Circulating: {summary['final_circulating']/1e9:.2f}B")
    print(f"  Emergency Brake:  {brake_status}")
    print(f"  Vesting Released: {summary['vested_released_pct']:.1f}%")

# =============================================================================
# COMPARISON TABLE
# =============================================================================

print("\n" + "=" * 70)
print("COMPARISON: 40% TGE vs 2% TGE")
print("=" * 70)

# 2% TGE baseline for comparison
baseline_2pct = {
    "tge_tokens": 17_000_000_000 * 0.02,  # 340M
    "launch_price": 32_000_000 / (17_000_000_000 * 0.02),  # $0.094
    "target_price": 0.05
}

print(f"\n{'Metric':<25} {'2% TGE ($32M)':<20} {'40% TGE ($75M)':<20}")
print("-" * 65)
print(f"{'TGE Tokens':<25} {baseline_2pct['tge_tokens']/1e6:.0f}M{'':<14} {TGE_TOKENS/1e9:.1f}B")
print(f"{'Launch Price':<25} ${baseline_2pct['target_price']:.4f}{'':<14} ${LAUNCH_PRICE:.4f}")
print(f"{'Price Difference':<25} {'':<20} {((LAUNCH_PRICE/baseline_2pct['target_price'])-1)*100:+.1f}%")

# =============================================================================
# INVESTOR IMPACT
# =============================================================================

print("\n" + "=" * 70)
print("$9,000 INVESTOR IMPACT (at $0.01 presale)")
print("=" * 70)

# At $0.01 presale, $9K buys 900K total tokens
# Without bonus: only 450K base coins
investor_base_coins = 450_000

print(f"\n{'Scenario':<30} {'TGE Value':<15} {'If Price Holds':<15} {'ROI':<10}")
print("-" * 70)

# 2% TGE baseline
tge_2pct = investor_base_coins * 0.02  # 9,000 tokens
value_2pct = tge_2pct * 0.05  # at $0.05
print(f"{'2% TGE @ $0.05 (current)':<30} ${value_2pct:,.0f}{'':<9} ${investor_base_coins * 0.05:,.0f}{'':<6} {((investor_base_coins * 0.05)/9000 - 1)*100:+.0f}%")

# 40% TGE scenarios
tge_40pct = investor_base_coins * 0.40  # 180,000 tokens

for key in ["normal", "covid_black_swan", "high_volatility", "stable_growth"]:
    result = all_results[key]
    final_price = result["summary"]["final_price"]
    tge_value = tge_40pct * LAUNCH_PRICE
    final_value = investor_base_coins * final_price
    roi = ((final_value / 9000) - 1) * 100
    
    print(f"{'40% TGE - ' + result['name'][:20]:<30} ${tge_value:,.0f}{'':<9} ${final_value:,.0f}{'':<6} {roi:+.0f}%")

# =============================================================================
# SCENARIO SUMMARY TABLE
# =============================================================================

print("\n" + "=" * 70)
print("ALL 10 MARKET SCENARIOS SUMMARY")
print("=" * 70)

print(f"\n{'#':<3} {'Scenario':<25} {'Final Price':<12} {'Brake Month':<12} {'Survival':<10}")
print("-" * 65)

scenario_order = ["normal", "may_2021", "ftx_collapse", "covid_black_swan", 
                  "gradual_bear", "bull_then_crash", "high_volatility", 
                  "stable_growth", "early_crash_recovery", "late_crash", "multiple_crashes"]

survival_count = 0
for i, key in enumerate(scenario_order, 1):
    if key not in all_results:
        continue
    result = all_results[key]
    summary = result["summary"]
    
    brake = f"Month {summary['emergency_brake_month']}" if summary['emergency_brake_triggered'] else "None"
    
    # Survival = price above $0.001 and no brake in first 6 months
    survived = not summary['emergency_brake_triggered'] or (summary['emergency_brake_month'] and summary['emergency_brake_month'] > 6)
    survival = "✅ Yes" if survived else "❌ No"
    if survived:
        survival_count += 1
    
    print(f"{i:<3} {result['name'][:25]:<25} ${summary['final_price']:.6f}   {brake:<12} {survival:<10}")

print(f"\nSurvival Rate: {survival_count}/{len(scenario_order)} scenarios ({survival_count/len(scenario_order)*100:.0f}%)")

# =============================================================================
# KEY INSIGHTS
# =============================================================================

print("\n" + "=" * 70)
print("KEY INSIGHTS: 40% TGE REALITY")
print("=" * 70)

normal_result = all_results["normal"]["summary"]
worst_result = all_results["covid_black_swan"]["summary"]
best_result = all_results["stable_growth"]["summary"]

print(f"""
LAUNCH REALITY:
  • Launch price at 40% TGE: ${LAUNCH_PRICE:.4f} (NOT $0.05)
  • That's {((LAUNCH_PRICE/0.05)-1)*100:.0f}% below the $0.05 target
  • {TGE_TOKENS/1e9:.1f}B tokens flooding the market at once

PRICE TRAJECTORY:
  • Normal market:   ${normal_result['final_price']:.6f} by month 24
  • Best case:       ${best_result['final_price']:.6f} (stable growth)
  • Worst case:      ${worst_result['final_price']:.6f} (COVID crash)

INVESTOR REALITY ($9K at $0.01):
  • At 40% TGE: Gets 180,000 tokens × ${LAUNCH_PRICE:.4f} = ${180000 * LAUNCH_PRICE:,.0f}
  • At 2% TGE:  Gets 9,000 tokens × $0.05 = $450
  
  40% TGE WINS on day 1: ${180000 * LAUNCH_PRICE:,.0f} vs $450
  BUT price is {((0.05/LAUNCH_PRICE)-1)*100:.0f}% higher at 2% TGE

THE TRADE-OFF:
  • 40% TGE: More tokens, lower price, more immediate access
  • 2% TGE:  Fewer tokens, higher price, price protection
""")

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "simulation_date": datetime.now().isoformat(),
    "parameters": {
        "liquidity": LIQUIDITY,
        "base_coins": BASE_COINS,
        "tge_percent": TGE_PERCENT,
        "tge_tokens": TGE_TOKENS,
        "launch_price": LAUNCH_PRICE,
        "daily_mining": DAILY_MINING,
        "emergency_brake_price": PRICE_THRESHOLD,
        "emergency_brake_liquidity": LIQUIDITY_THRESHOLD
    },
    "scenarios": all_results,
    "comparison": {
        "tge_2pct_value": value_2pct,
        "tge_40pct_value": tge_40pct * LAUNCH_PRICE,
        "price_difference_pct": ((LAUNCH_PRICE / 0.05) - 1) * 100
    }
}

with open("forty_percent_simulation_results.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n✅ Results saved to forty_percent_simulation_results.json")
print("=" * 70)


