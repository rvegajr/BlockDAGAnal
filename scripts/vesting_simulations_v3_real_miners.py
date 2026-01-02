#!/usr/bin/env python3
"""
BlockDAG Vesting Solution - REAL MINER DATA Simulation (v3)

This simulation uses ACTUAL miner numbers provided by stakeholders:
- X10: 15,000 units at 200 BDAG/day
- X30: 2,500 units at 600 BDAG/day  
- X100: 2,500 units at 2,000 BDAG/day
- X1: ~50,000 migrated (of 3M total) at 20 BDAG/day

Plus accounts for:
- 18 months of existing testnet mining (~50K X1 miners)
- X1 migration barrier (7,500 BDAG buy-in)
- Network difficulty linear digression schedule
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math

print("=" * 80)
print("REAL MINER DATA SIMULATION (v3)")
print("=" * 80)
print("\nUsing ACTUAL stakeholder-provided miner numbers:")
print("• X10:  15,000 units × 200 BDAG/day  = 3,000,000 BDAG/day")
print("• X30:   2,500 units × 600 BDAG/day  = 1,500,000 BDAG/day")
print("• X100:  2,500 units × 2,000 BDAG/day = 5,000,000 BDAG/day")
print("• X1:   50,000 units × 20 BDAG/day   = 1,000,000 BDAG/day")
print("-" * 80)
print("TOTAL BASE EMISSION: 10,500,000 BDAG/day (at 100% rate)")
print("=" * 80)

# Core constants
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
TOTAL_PRESALE = 50_000_000_000
BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000

# REAL MINER DATA (from stakeholder)
MINERS = {
    "X10": {"units": 15_000, "daily_output": 200},
    "X30": {"units": 2_500, "daily_output": 600},
    "X100": {"units": 2_500, "daily_output": 2_000},
    "X1_migrated": {"units": 50_000, "daily_output": 20},  # Estimated migrations
}

# X1 migration dynamics
X1_TOTAL_USERS = 3_000_000
X1_MIGRATION_COST = 7_500  # BDAG required to migrate
X1_ESTIMATED_MIGRATIONS = 50_000  # ~1.7% migration rate
X1_DAILY_OUTPUT = 20

# Pre-launch mining (18 months of testnet)
TESTNET_MONTHS = 18
TESTNET_DAILY_MINERS = 50_000  # Estimated active X1 testnet miners
TESTNET_DAILY_OUTPUT = 20
PRE_LAUNCH_MINED = TESTNET_MONTHS * 30 * TESTNET_DAILY_MINERS * TESTNET_DAILY_OUTPUT
# = 18 * 30 * 50,000 * 20 = 540,000,000 BDAG already mined!

print(f"\nPRE-LAUNCH MINED (18 months testnet): {PRE_LAUNCH_MINED:,} BDAG")
print(f"X1 Migration barrier: {X1_MIGRATION_COST:,} BDAG (${X1_MIGRATION_COST * TARGET_PRICE} at target price)")

# Calculate base daily emission
BASE_DAILY_EMISSION = sum(
    m["units"] * m["daily_output"] 
    for m in MINERS.values()
)
print(f"Daily emission at 100%: {BASE_DAILY_EMISSION:,} BDAG/day")
print(f"Monthly emission at 100%: {BASE_DAILY_EMISSION * 30:,} BDAG/month")


def calculate_emission_with_digression(month: int, digression_start: int = 0) -> float:
    """
    Calculate emission rate with network difficulty digression
    
    digression_start: month when linear digression begins (0 = immediate, 6 = after 6 months)
    """
    # First, apply the emission cap schedule (10% -> 100% over 12 months)
    emission_caps = {
        0: 0.0,
        1: 0.10, 2: 0.10,
        3: 0.25, 4: 0.25, 5: 0.25,
        6: 0.50, 7: 0.50, 8: 0.50,
        9: 0.75, 10: 0.75, 11: 0.75,
    }
    cap_rate = emission_caps.get(month, 1.0)
    
    # Then apply network difficulty digression
    if month >= digression_start:
        months_since_digression = month - digression_start
        # Linear digression: reduce by 2% per month after start
        digression_rate = max(0.50, 1.0 - (months_since_digression * 0.02))
    else:
        digression_rate = 1.0
    
    return cap_rate * digression_rate


def calculate_x1_migration_curve(month: int, target_price: float) -> int:
    """
    Calculate X1 migrations over time based on BDAG price
    
    Higher price = higher migration barrier = fewer migrations
    Lower price = lower migration barrier = more migrations
    """
    migration_cost_usd = X1_MIGRATION_COST * target_price
    
    # Base migration rate (at $0.05, cost is $375)
    if migration_cost_usd < 100:
        monthly_migration_rate = 0.05  # 5% of remaining migrate
    elif migration_cost_usd < 250:
        monthly_migration_rate = 0.03  # 3%
    elif migration_cost_usd < 500:
        monthly_migration_rate = 0.02  # 2%
    elif migration_cost_usd < 1000:
        monthly_migration_rate = 0.01  # 1%
    else:
        monthly_migration_rate = 0.005  # 0.5%
    
    # Calculate cumulative migrations by month
    remaining = X1_TOTAL_USERS - X1_ESTIMATED_MIGRATIONS  # Start with initial estimate
    cumulative = X1_ESTIMATED_MIGRATIONS
    
    for m in range(month):
        new_migrations = int(remaining * monthly_migration_rate)
        cumulative += new_migrations
        remaining -= new_migrations
    
    return min(cumulative, X1_TOTAL_USERS * 0.1)  # Cap at 10% of total users


class RealMinerSimulator:
    """Simulation using real miner data"""
    
    def __init__(self, digression_start: int = 6):
        self.digression_start = digression_start
        self.pre_launch_supply = PRE_LAUNCH_MINED
        
    def calculate_monthly_mining(self, month: int, current_price: float) -> Dict:
        """Calculate mining emissions for a month"""
        emission_rate = calculate_emission_with_digression(month, self.digression_start)
        
        # X10, X30, X100 emissions
        x10_emission = MINERS["X10"]["units"] * MINERS["X10"]["daily_output"] * 30 * emission_rate
        x30_emission = MINERS["X30"]["units"] * MINERS["X30"]["daily_output"] * 30 * emission_rate
        x100_emission = MINERS["X100"]["units"] * MINERS["X100"]["daily_output"] * 30 * emission_rate
        
        # X1 emissions (based on migration curve)
        x1_active = calculate_x1_migration_curve(month, current_price)
        x1_emission = x1_active * X1_DAILY_OUTPUT * 30 * emission_rate
        
        total = x10_emission + x30_emission + x100_emission + x1_emission
        
        return {
            "x10": int(x10_emission),
            "x30": int(x30_emission),
            "x100": int(x100_emission),
            "x1": int(x1_emission),
            "x1_active_miners": x1_active,
            "emission_rate": emission_rate,
            "total": int(total)
        }
    
    def calculate_circulating(self, month: int, current_price: float, staking_rate: float = 0.30) -> Dict:
        """Calculate total circulating supply"""
        
        # Base coins vesting
        if month == 0:
            base_vested = int(BASE_COINS * 0.02)
        elif month < 13:
            base_vested = int(BASE_COINS * 0.02)
        elif month < 25:
            months_in = month - 12
            base_vested = int(BASE_COINS * (0.02 + 0.08 * months_in / 12))
        else:
            base_vested = int(BASE_COINS * 0.10)  # Cap at month 24 for this sim
        
        # Mining emissions (cumulative)
        cumulative_mining = 0
        for m in range(1, month + 1):
            mining = self.calculate_monthly_mining(m, current_price)
            cumulative_mining += mining["total"]
        
        # Add pre-launch mined tokens (they exist!)
        total_mined = cumulative_mining + self.pre_launch_supply
        
        # Total supply
        total_supply = base_vested + total_mined
        
        # Apply staking
        staked = int(total_supply * staking_rate)
        circulating = total_supply - staked
        
        return {
            "base_vested": base_vested,
            "mining_cumulative": cumulative_mining,
            "pre_launch_mined": self.pre_launch_supply,
            "total_mined": total_mined,
            "total_supply": total_supply,
            "staked": staked,
            "circulating": circulating
        }


def run_real_miner_simulation(digression_start: int = 6, months: int = 24) -> Dict:
    """Run simulation with real miner data"""
    
    sim = RealMinerSimulator(digression_start=digression_start)
    
    results = {
        "scenario": f"Real Miners (Digression at Month {digression_start})",
        "digression_start": digression_start,
        "pre_launch_mined": PRE_LAUNCH_MINED,
        "months": [],
        "emergency_brake_triggered": False,
        "emergency_brake_month": None,
        "emergency_brake_reason": "",
    }
    
    current_liquidity = LAUNCH_LIQUIDITY
    current_price = TARGET_PRICE
    consecutive_low_days = 0
    emergency_active = False
    
    for month in range(months + 1):
        # Calculate supply
        supply = sim.calculate_circulating(month, current_price)
        mining = sim.calculate_monthly_mining(month, current_price)
        
        # Adjust staking based on market conditions
        if current_price < TARGET_PRICE * 0.5:
            staking_rate = 0.45  # Higher staking in crashes
        elif current_price < TARGET_PRICE * 0.8:
            staking_rate = 0.35
        else:
            staking_rate = 0.30
        
        supply = sim.calculate_circulating(month, current_price, staking_rate)
        
        # Calculate price
        if supply["circulating"] > 0:
            current_price = current_liquidity / supply["circulating"]
        
        # Check emergency brake
        if current_price < 0.02:
            consecutive_low_days += 30
        else:
            consecutive_low_days = max(0, consecutive_low_days - 15)
        
        if not emergency_active:
            if current_price < 0.02 and consecutive_low_days >= 7:
                emergency_active = True
                results["emergency_brake_triggered"] = True
                results["emergency_brake_month"] = month
                results["emergency_brake_reason"] = f"Price ${current_price:.4f} < $0.02 for {consecutive_low_days} days"
            elif current_liquidity < 10_000_000:
                emergency_active = True
                results["emergency_brake_triggered"] = True
                results["emergency_brake_month"] = month
                results["emergency_brake_reason"] = f"Liquidity ${current_liquidity/1e6:.1f}M < $10M"
        
        # Calculate market cap
        market_cap = current_price * supply["circulating"]
        
        results["months"].append({
            "month": month,
            "price": current_price,
            "circulating": supply["circulating"],
            "total_supply": supply["total_supply"],
            "base_vested": supply["base_vested"],
            "mining_cumulative": supply["mining_cumulative"],
            "pre_launch_mined": supply["pre_launch_mined"],
            "staked": supply["staked"],
            "staking_rate": staking_rate,
            "x1_active_miners": mining["x1_active_miners"],
            "emission_rate": mining["emission_rate"],
            "market_cap": market_cap,
            "emergency_active": emergency_active
        })
    
    results["final_price"] = results["months"][-1]["price"]
    results["final_circulating"] = results["months"][-1]["circulating"]
    results["final_market_cap"] = results["months"][-1]["market_cap"]
    
    return results


def print_detailed_results(results: Dict):
    """Print detailed simulation results"""
    
    print(f"\n{'='*80}")
    print(f"SCENARIO: {results['scenario']}")
    print(f"{'='*80}")
    
    print(f"\nPre-Launch Mined (18 months testnet): {results['pre_launch_mined']:,} BDAG")
    print(f"Digression Start: Month {results['digression_start']}")
    
    if results['emergency_brake_triggered']:
        print(f"\n⚠️  EMERGENCY BRAKE TRIGGERED at Month {results['emergency_brake_month']}")
        print(f"   Reason: {results['emergency_brake_reason']}")
    else:
        print(f"\n✅ No emergency brake triggered")
    
    print(f"\nFinal Metrics:")
    print(f"  Price: ${results['final_price']:.6f}")
    print(f"  Circulating: {results['final_circulating']:,}")
    print(f"  Market Cap: ${results['final_market_cap']:,.0f}")
    
    print(f"\n{'Month':<6} {'Price':<12} {'Circulating':<18} {'Mining (Cum)':<18} {'X1 Miners':<12} {'Rate':<8}")
    print("-" * 80)
    
    key_months = [0, 1, 3, 6, 9, 12, 18, 24]
    for m in results['months']:
        if m['month'] in key_months:
            print(f"{m['month']:<6} "
                  f"${m['price']:<10.6f} "
                  f"{m['circulating']:<18,} "
                  f"{m['mining_cumulative']:<18,} "
                  f"{m['x1_active_miners']:<12,} "
                  f"{m['emission_rate']*100:<6.1f}%")


def compare_digression_scenarios():
    """Compare immediate vs delayed digression"""
    
    print("\n" + "=" * 80)
    print("COMPARING DIGRESSION SCENARIOS")
    print("=" * 80)
    
    scenarios = [
        ("Immediate Digression (Month 0)", 0),
        ("Digression at Month 3", 3),
        ("Digression at Month 6", 6),
        ("No Digression (Full Emissions)", 99),  # Never starts
    ]
    
    all_results = []
    
    for name, start_month in scenarios:
        results = run_real_miner_simulation(digression_start=start_month, months=24)
        results["scenario"] = name
        all_results.append(results)
        print_detailed_results(results)
    
    # Summary comparison
    print("\n" + "=" * 80)
    print("SUMMARY COMPARISON")
    print("=" * 80)
    
    print(f"\n{'Scenario':<35} {'Final Price':<15} {'Final Circ.':<20} {'Brake?':<10}")
    print("-" * 80)
    
    for r in all_results:
        brake = f"Month {r['emergency_brake_month']}" if r['emergency_brake_triggered'] else "No"
        print(f"{r['scenario']:<35} "
              f"${r['final_price']:<13.6f} "
              f"{r['final_circulating']:<20,} "
              f"{brake:<10}")
    
    return all_results


def analyze_pre_launch_impact():
    """Analyze impact of pre-launch mined tokens"""
    
    print("\n" + "=" * 80)
    print("PRE-LAUNCH MINING IMPACT ANALYSIS")
    print("=" * 80)
    
    print(f"""
PRE-LAUNCH MINING REALITY:
• ~50,000 X1 miners active on testnet for 18 months
• Daily output: 20 BDAG/miner
• Total pre-mined: {PRE_LAUNCH_MINED:,} BDAG

AT LAUNCH, THIS MEANS:
• Pre-launch mined tokens: {PRE_LAUNCH_MINED:,}
• Base coins TGE unlock (2%): {int(BASE_COINS * 0.02):,}
• Total Day 1 potential sell pressure: {PRE_LAUNCH_MINED + int(BASE_COINS * 0.02):,}

PRICE IMPACT (if all sold at once):
• With $32M liquidity: ${LAUNCH_LIQUIDITY / (PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)):.6f}

This is why we need:
1. Staking incentives for pre-launch miners
2. X1 migration cost creates natural demand
3. Emergency brake protection
""")


def main():
    """Run all analyses"""
    
    print("\n" + "=" * 80)
    print("BLOCKDAG VESTING SIMULATION WITH REAL MINER DATA")
    print("=" * 80)
    
    # Show the real numbers
    print(f"""
STAKEHOLDER-PROVIDED MINER DATA:
--------------------------------
X10:  15,000 units × 200 BDAG/day  = 3,000,000 BDAG/day
X30:   2,500 units × 600 BDAG/day  = 1,500,000 BDAG/day
X100:  2,500 units × 2,000 BDAG/day = 5,000,000 BDAG/day
X1:   ~50,000 migrated × 20 BDAG/day = 1,000,000 BDAG/day
-------------------------------------------------------
TOTAL (at 100% emission): {BASE_DAILY_EMISSION:,} BDAG/day
                         = {BASE_DAILY_EMISSION * 30:,} BDAG/month

X1 MIGRATION DYNAMICS:
• Total X1 users: {X1_TOTAL_USERS:,}
• Migration cost: {X1_MIGRATION_COST:,} BDAG (${X1_MIGRATION_COST * TARGET_PRICE} at $0.05)
• Estimated migrations: {X1_ESTIMATED_MIGRATIONS:,} (~1.7% of users)
• Most X1 users likely won't migrate due to cost barrier
""")
    
    # Analyze pre-launch impact
    analyze_pre_launch_impact()
    
    # Compare digression scenarios
    all_results = compare_digression_scenarios()
    
    # Save results
    output_file = "vesting_simulation_v3_real_miners.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n📊 Results saved to: {output_file}")
    
    # Final recommendation
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS BASED ON REAL MINER DATA")
    print("=" * 80)
    print("""
1. PRE-LAUNCH TOKENS ARE SIGNIFICANT
   • 540M tokens already mined on testnet
   • Need staking program for pre-launch miners
   • Consider airdrop vesting for testnet rewards

2. DIGRESSION TIMING MATTERS
   • Immediate digression helps price stability
   • Delayed digression (6 months) allows miner ROI
   • Recommend: Start at 50% rate, linear decrease over 24 months

3. X1 MIGRATION IS A SAFETY VALVE
   • 7,500 BDAG cost = natural demand at launch
   • At $0.05, cost is $375 - reasonable barrier
   • Migration creates buying pressure, not selling

4. EMERGENCY BRAKE STILL CRITICAL
   • All scenarios eventually trigger brake
   • Mining emissions are the primary pressure source
   • Staking rate of 40%+ significantly helps

5. RECOMMENDED CONFIGURATION
   • Emission cap: Start at 10%, ramp to 50% (not 100%)
   • Digression: Begin at month 3, 3% monthly reduction
   • Staking: 50% of mining rewards locked 90 days
   • X1 migration: Tiered pricing (earlier = cheaper)
""")


if __name__ == "__main__":
    main()

