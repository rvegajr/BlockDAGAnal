#!/usr/bin/env python3
"""
40% TGE SIMULATION - AT $32M LIQUIDITY
======================================
"40% at launch as promised" - with actual $32M liquidity

This is what happens when you honor 40% TGE with the real liquidity number.
"""

import json
from datetime import datetime

# =============================================================================
# PARAMETERS - 40% TGE WITH $32M LIQUIDITY
# =============================================================================

LIQUIDITY = 32_000_000  # $32M - the ACTUAL number
BASE_COINS = 17_000_000_000  # 17B base coins only (no bonus)
TGE_PERCENT = 0.40  # 40% as promised
VESTING_PERCENT = 0.60  # 60% vested

# Calculate launch metrics
TGE_TOKENS = BASE_COINS * TGE_PERCENT  # 6.8B tokens
LAUNCH_PRICE = LIQUIDITY / TGE_TOKENS  # Price calculation

# Mining
DAILY_MINING = 10_500_000  # 10.5M/day from hardware miners
MINING_STAKING_RATE = 0.50  # 50% auto-staked

# Emergency brake thresholds (adjusted for lower price)
PRICE_THRESHOLD = 0.002  # $0.002 
LIQUIDITY_THRESHOLD = 10_000_000  # $10M

# Vesting schedule
CLIFF_MONTHS = 6
VESTING_MONTHS = 30
MONTHLY_VEST_RATE = VESTING_PERCENT / VESTING_MONTHS

print("=" * 70)
print("40% TGE @ $32M LIQUIDITY - THE REAL NUMBERS")
print("=" * 70)
print(f"\nLaunch Parameters:")
print(f"  Liquidity:        ${LIQUIDITY:,.0f}")
print(f"  Base Coins:       {BASE_COINS/1e9:.1f}B")
print(f"  TGE Unlock:       {TGE_PERCENT*100:.0f}%")
print(f"  TGE Tokens:       {TGE_TOKENS/1e9:.2f}B")
print(f"  LAUNCH PRICE:     ${LAUNCH_PRICE:.6f}")
print(f"  Vesting:          {VESTING_PERCENT*100:.0f}% over {VESTING_MONTHS} months")
print(f"  Emergency Brake:  ${PRICE_THRESHOLD} price / ${LIQUIDITY_THRESHOLD/1e6:.0f}M liquidity")

# Compare to 2% TGE
tge_2pct_tokens = BASE_COINS * 0.02
tge_2pct_price = LIQUIDITY / tge_2pct_tokens
print(f"\nFor comparison - 2% TGE:")
print(f"  TGE Tokens:       {tge_2pct_tokens/1e6:.0f}M")
print(f"  Launch Price:     ${tge_2pct_price:.4f}")
print(f"  Price difference: {((LAUNCH_PRICE/tge_2pct_price)-1)*100:+.1f}%")

# =============================================================================
# MARKET SCENARIOS
# =============================================================================

scenarios = {
    "normal": {
        "name": "Normal Market Conditions",
        "description": "Stable market, no major crashes",
        "events": []
    },
    "may_2021": {
        "name": "May 2021-Style Crash",
        "description": "60% liquidity drop at month 2",
        "events": [(2, 0.40)]
    },
    "ftx_collapse": {
        "name": "FTX Collapse",
        "description": "70% liquidity drop at month 3",
        "events": [(3, 0.30)]
    },
    "covid_black_swan": {
        "name": "COVID Black Swan",
        "description": "80% liquidity drop at month 1",
        "events": [(1, 0.20)]
    },
    "gradual_bear": {
        "name": "Gradual Bear Market",
        "description": "50% drop over 12 months",
        "events": [(i, 1 - (0.5 * i / 12)) for i in range(1, 13)]
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
    results = {
        "scenario": scenario_key,
        "name": scenario_data["name"],
        "description": scenario_data["description"],
        "months": [],
        "summary": {}
    }
    
    circulating = TGE_TOKENS
    liquidity = LIQUIDITY
    vested_released = 0
    emergency_brake_active = False
    emergency_brake_month = None
    min_price = LAUNCH_PRICE
    max_price = LAUNCH_PRICE
    
    events = {e[0]: e[1] for e in scenario_data.get("events", [])}
    
    for month in range(0, 25):
        if month in events:
            liquidity = LIQUIDITY * events[month]
        
        price = liquidity / circulating if circulating > 0 else 0
        
        min_price = min(min_price, price)
        max_price = max(max_price, price)
        
        if not emergency_brake_active:
            if price < PRICE_THRESHOLD or liquidity < LIQUIDITY_THRESHOLD:
                emergency_brake_active = True
                emergency_brake_month = month
        
        if month > CLIFF_MONTHS and not emergency_brake_active:
            monthly_vest = BASE_COINS * MONTHLY_VEST_RATE
            vested_released += monthly_vest
            circulating += monthly_vest
        
        monthly_mining = DAILY_MINING * 30
        effective_mining = monthly_mining * (1 - MINING_STAKING_RATE)
        circulating += effective_mining
        
        results["months"].append({
            "month": month,
            "circulating": circulating,
            "liquidity": liquidity,
            "price": price,
            "emergency_brake": emergency_brake_active,
            "vested_released_pct": (vested_released / (BASE_COINS * VESTING_PERCENT)) * 100 if VESTING_PERCENT > 0 else 0
        })
    
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
print("RUNNING SIMULATIONS - 40% TGE @ $32M...")
print("=" * 70)

all_results = {}

for key, scenario in scenarios.items():
    result = run_simulation(key, scenario)
    all_results[key] = result
    
    summary = result["summary"]
    brake_status = f"Month {summary['emergency_brake_month']}" if summary['emergency_brake_triggered'] else "NOT triggered"
    
    print(f"\n{scenario['name']}:")
    print(f"  Final Price:      ${summary['final_price']:.6f}")
    print(f"  Min/Max Price:    ${summary['min_price']:.6f} / ${summary['max_price']:.6f}")
    print(f"  Emergency Brake:  {brake_status}")

# =============================================================================
# COMPARISON TABLE
# =============================================================================

print("\n" + "=" * 70)
print("HEAD-TO-HEAD: 2% TGE vs 40% TGE (both at $32M)")
print("=" * 70)

print(f"\n{'Metric':<30} {'2% TGE':<20} {'40% TGE':<20}")
print("-" * 70)
print(f"{'Liquidity':<30} {'$32M':<20} {'$32M':<20}")
print(f"{'TGE Tokens':<30} {'340M':<20} {'6.8B':<20}")
print(f"{'Launch Price':<30} {'$0.094':<20} {'$' + f'{LAUNCH_PRICE:.6f}':<20}")
print(f"{'Effective Launch Price':<30} {'$0.05 (capped)':<20} {'$' + f'{LAUNCH_PRICE:.6f}':<20}")

# =============================================================================
# INVESTOR IMPACT
# =============================================================================

print("\n" + "=" * 70)
print("$9,000 INVESTOR AT $0.01 PRESALE")
print("=" * 70)

# No bonus, so only base coins: $9K at $0.01 = 900K tokens
# But wait - with no bonus, they only have base coins
# If original was 50/50, then 450K base coins
investor_base = 450_000  # Base coins only (no bonus)
investor_total_original = 900_000  # What they thought they'd have

print(f"\nOriginal expectation: {investor_total_original:,} tokens (base + bonus)")
print(f"With no bonus:        {investor_base:,} base coins only")

tge_40_tokens = investor_base * 0.40
tge_2_tokens = investor_base * 0.02

print(f"\n{'Scenario':<30} {'Tokens at TGE':<15} {'Price':<12} {'TGE Value':<12}")
print("-" * 70)
print(f"{'2% TGE @ $32M':<30} {tge_2_tokens:,.0f}{'':<7} $0.094{'':<6} ${tge_2_tokens * 0.094:,.0f}")
print(f"{'2% TGE @ $32M (capped $0.05)':<30} {tge_2_tokens:,.0f}{'':<7} $0.05{'':<6} ${tge_2_tokens * 0.05:,.0f}")
print(f"{'40% TGE @ $32M':<30} {tge_40_tokens:,.0f}{'':<4} ${LAUNCH_PRICE:.4f}{'':<4} ${tge_40_tokens * LAUNCH_PRICE:,.0f}")

# =============================================================================
# ALL SCENARIOS SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("ALL 11 MARKET SCENARIOS - 40% TGE @ $32M")
print("=" * 70)

print(f"\n{'#':<3} {'Scenario':<28} {'Final Price':<14} {'Brake':<12} {'Status':<10}")
print("-" * 70)

scenario_order = ["normal", "may_2021", "ftx_collapse", "covid_black_swan", 
                  "gradual_bear", "bull_then_crash", "high_volatility", 
                  "stable_growth", "early_crash_recovery", "late_crash", "multiple_crashes"]

early_brake_count = 0
for i, key in enumerate(scenario_order, 1):
    if key not in all_results:
        continue
    result = all_results[key]
    summary = result["summary"]
    
    brake_month = summary['emergency_brake_month']
    brake = f"Month {brake_month}" if summary['emergency_brake_triggered'] else "None"
    
    # Early brake = within first 3 months
    if brake_month and brake_month <= 3:
        status = "🔴 EARLY"
        early_brake_count += 1
    elif brake_month and brake_month <= 12:
        status = "🟠 MID"
    elif brake_month:
        status = "🟡 LATE"
    else:
        status = "🟢 NONE"
    
    print(f"{i:<3} {result['name'][:28]:<28} ${summary['final_price']:.6f}     {brake:<12} {status:<10}")

print(f"\nEarly Brake (≤3 months): {early_brake_count}/11 scenarios")

# =============================================================================
# THE BRUTAL TRUTH
# =============================================================================

print("\n" + "=" * 70)
print("THE BRUTAL TRUTH: 40% TGE @ $32M")
print("=" * 70)

normal = all_results["normal"]["summary"]
covid = all_results["covid_black_swan"]["summary"]
best = all_results["stable_growth"]["summary"]

print(f"""
THE MATH DOESN'T LIE:

  $32,000,000 ÷ 6,800,000,000 tokens = ${LAUNCH_PRICE:.6f} per token

  That's not even HALF A CENT.
  That's {(LAUNCH_PRICE/0.05)*100:.1f}% of the $0.05 target.

WHAT THIS MEANS FOR INVESTORS:

  $9,000 invested at $0.01 presale:
  ├── Expected: 900K tokens at some price
  ├── 40% TGE: 180K tokens × ${LAUNCH_PRICE:.6f} = ${180000 * LAUNCH_PRICE:,.0f}
  ├── 2% TGE:  9K tokens × $0.05 = $450
  └── DIFFERENCE: ${180000 * LAUNCH_PRICE - 450:+,.0f}

  40% TGE gives MORE money on day 1!
  BUT the price is {(0.05/LAUNCH_PRICE):.0f}x lower.

MARKET SCENARIO RESULTS:

  Normal market:  ${normal['final_price']:.6f} (brake month {normal['emergency_brake_month']})
  Stable growth:  ${best['final_price']:.6f} (brake {'month ' + str(best['emergency_brake_month']) if best['emergency_brake_month'] else 'NONE'})
  COVID crash:    ${covid['final_price']:.6f} (brake month {covid['emergency_brake_month']})

THE REAL QUESTION:

  Do you want:
  A) $450 at $0.05 (higher price, less tokens)
  B) ${180000 * LAUNCH_PRICE:,.0f} at ${LAUNCH_PRICE:.6f} (lower price, more tokens)

  Option B gives you {180000 * LAUNCH_PRICE / 450:.1f}x more money on DAY 1.
  But the PRICE is {0.05 / LAUNCH_PRICE:.0f}x lower.
""")

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "simulation_date": datetime.now().isoformat(),
    "title": "40% TGE at $32M Liquidity Analysis",
    "parameters": {
        "liquidity": LIQUIDITY,
        "base_coins": BASE_COINS,
        "tge_percent": TGE_PERCENT,
        "tge_tokens": TGE_TOKENS,
        "launch_price": LAUNCH_PRICE,
        "comparison_2pct_price": 0.05
    },
    "scenarios": all_results,
    "investor_example": {
        "investment": 9000,
        "presale_price": 0.01,
        "base_coins": investor_base,
        "tge_40pct_tokens": tge_40_tokens,
        "tge_40pct_value": tge_40_tokens * LAUNCH_PRICE,
        "tge_2pct_tokens": tge_2_tokens,
        "tge_2pct_value": tge_2_tokens * 0.05
    }
}

with open("forty_percent_32m_results.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n✅ Results saved to forty_percent_32m_results.json")
print("=" * 70)

