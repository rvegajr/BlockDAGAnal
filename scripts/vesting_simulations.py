#!/usr/bin/env python3
"""
BlockDAG Vesting Solution - Market Scenario Simulations

Simulates the vesting model under various market conditions including:
- Major crypto market crashes
- Bull market runs
- Stagnant markets
- Volatile periods

Outputs detailed analysis of circulating supply, price impact, and emergency brake triggers.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import math

# Constants from the vesting model
LAUNCH_LIQUIDITY = 32_000_000  # $32M
TARGET_PRICE = 0.05
MAX_CIRCULATING_LAUNCH = 640_000_000  # 640M tokens
TOTAL_PRESALE = 50_000_000_000  # 50B tokens
BASE_COINS = 17_000_000_000  # 17B
BONUS_COINS = 33_000_000_000  # 33B

# Mining emission rates (monthly)
EMISSION_SCHEDULE = {
    0: 0.0,    # Month 0: 0%
    1: 0.10,   # Month 1-2: 10%
    2: 0.10,
    3: 0.25,   # Month 3-5: 25%
    4: 0.25,
    5: 0.25,
    6: 0.50,   # Month 6-8: 50%
    7: 0.50,
    8: 0.50,
    9: 0.75,   # Month 9-11: 75%
    10: 0.75,
    11: 0.75,
    12: 1.0,   # Month 12+: 100%
}

# Moderate miner scenario (10.6M/day at 100%)
BASE_DAILY_EMISSION = 10_600_000  # tokens/day at 100%


class VestingSimulator:
    def __init__(self, launch_date: datetime = datetime(2025, 3, 1)):
        self.launch_date = launch_date
        self.base_vested = 0
        self.bonus_vested = 0
        self.mining_emitted = 0
        self.staked_amount = 0
        self.staking_rate = 0.30  # 30% default
        
    def calculate_base_vesting(self, months_since_launch: int) -> int:
        """Calculate base coins vested up to given month"""
        if months_since_launch == 0:
            return int(BASE_COINS * 0.02)  # 2% TGE
        
        if months_since_launch < 13:
            return int(BASE_COINS * 0.02)  # Still in cliff
        
        # Phase 1: Months 13-24 (8% total = 0.67% per month)
        if months_since_launch < 25:
            months_in_phase = months_since_launch - 12
            phase_vested = BASE_COINS * 0.08 * (months_in_phase / 12)
            return int(BASE_COINS * 0.02 + phase_vested)
        
        # Phase 2: Months 25-36 (15% total = 1.25% per month)
        if months_since_launch < 37:
            months_in_phase = months_since_launch - 24
            phase_vested = BASE_COINS * 0.15 * (months_in_phase / 12)
            return int(BASE_COINS * 0.02 + BASE_COINS * 0.08 + phase_vested)
        
        # Phase 3: Months 37-48 (25% total = 2.08% per month)
        if months_since_launch < 49:
            months_in_phase = months_since_launch - 36
            phase_vested = BASE_COINS * 0.25 * (months_in_phase / 12)
            return int(BASE_COINS * 0.02 + BASE_COINS * 0.08 + BASE_COINS * 0.15 + phase_vested)
        
        # Phase 4: Months 49-60 (50% total = 4.17% per month)
        if months_since_launch < 61:
            months_in_phase = months_since_launch - 48
            phase_vested = BASE_COINS * 0.50 * (months_in_phase / 12)
            return int(BASE_COINS * 0.02 + BASE_COINS * 0.08 + BASE_COINS * 0.15 + BASE_COINS * 0.25 + phase_vested)
        
        # Fully vested
        return BASE_COINS
    
    def calculate_bonus_vesting(self, months_since_launch: int, dao_approved: bool = False) -> int:
        """Calculate bonus coins vested (requires DAO approval)"""
        if months_since_launch < 25:
            return 0  # 24-month cliff
        
        if not dao_approved:
            return 0  # Requires DAO vote
        
        # Simplified: assume DAO approves phases on schedule
        if months_since_launch < 37:
            return int(BONUS_COINS * 0.05)  # Phase 1: 5%
        if months_since_launch < 49:
            return int(BONUS_COINS * 0.15)  # Phase 1+2: 15%
        if months_since_launch < 61:
            return int(BONUS_COINS * 0.30)  # Phase 1-3: 30%
        if months_since_launch < 73:
            return int(BONUS_COINS * 0.50)  # Phase 1-4: 50%
        if months_since_launch < 85:
            return int(BONUS_COINS * 0.75)  # Phase 1-5: 75%
        
        return BONUS_COINS  # Fully vested
    
    def calculate_mining_emission(self, months_since_launch: int) -> int:
        """Calculate total mining emissions up to given month"""
        total = 0
        for month in range(1, months_since_launch + 1):
            rate = EMISSION_SCHEDULE.get(min(month, 12), 1.0)
            monthly_emission = BASE_DAILY_EMISSION * 30 * rate
            total += monthly_emission
        return int(total)
    
    def calculate_circulating_supply(self, months_since_launch: int, staking_rate: float = 0.30) -> int:
        """Calculate net circulating supply after staking"""
        base = self.calculate_base_vesting(months_since_launch)
        bonus = self.calculate_bonus_vesting(months_since_launch, dao_approved=True)
        mining = self.calculate_mining_emission(months_since_launch)
        
        total = base + bonus + mining
        staked = int(total * staking_rate)
        circulating = total - staked
        
        return circulating, total, staked
    
    def calculate_price(self, circulating_supply: int, liquidity: float = LAUNCH_LIQUIDITY) -> float:
        """Calculate price based on circulating supply and liquidity"""
        if circulating_supply == 0:
            return TARGET_PRICE
        return liquidity / circulating_supply
    
    def check_emergency_brake(self, price: float, liquidity: float, consecutive_days: int = 0) -> Tuple[bool, str]:
        """Check if emergency brake should trigger"""
        if price < 0.02 and consecutive_days >= 7:
            return True, f"Price below $0.02 for {consecutive_days} days"
        if liquidity < 10_000_000:
            return True, f"Liquidity below $10M"
        return False, ""


class MarketScenario:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.events = []  # List of (date, event_type, impact)
    
    def add_event(self, date: datetime, event_type: str, impact: float, description: str = ""):
        """Add a market event
        impact: multiplier for liquidity (1.0 = no change, 0.5 = 50% drop, 2.0 = 100% increase)
        """
        self.events.append({
            'date': date,
            'type': event_type,
            'impact': impact,
            'description': description
        })


def simulate_scenario(scenario: MarketScenario, months: int = 24) -> Dict:
    """Run simulation for a given scenario"""
    simulator = VestingSimulator()
    results = {
        'scenario': scenario.name,
        'description': scenario.description,
        'months': [],
        'emergency_brake_triggered': False,
        'emergency_brake_reason': '',
        'min_price': TARGET_PRICE,
        'max_price': TARGET_PRICE,
        'final_price': TARGET_PRICE,
        'final_circulating': 0,
        'final_market_cap': 0
    }
    
    current_liquidity = LAUNCH_LIQUIDITY
    consecutive_low_price_days = 0
    emergency_active = False
    
    for month in range(months + 1):
        # Apply market events
        month_date = simulator.launch_date + timedelta(days=30 * month)
        for event in scenario.events:
            if event['date'] <= month_date:
                current_liquidity = LAUNCH_LIQUIDITY * event['impact']
        
        # Calculate supply
        circulating, total, staked = simulator.calculate_circulating_supply(month)
        
        # Adjust staking based on market conditions
        if current_liquidity < LAUNCH_LIQUIDITY * 0.7:
            staking_rate = 0.40  # Higher staking in bad markets
        else:
            staking_rate = 0.30
        
        circulating_adjusted = int(total * (1 - staking_rate))
        
        # Calculate price
        price = simulator.calculate_price(circulating_adjusted, current_liquidity)
        
        # Check emergency brake
        if not emergency_active:
            brake_triggered, reason = simulator.check_emergency_brake(
                price, current_liquidity, consecutive_low_price_days
            )
            if brake_triggered:
                emergency_active = True
                results['emergency_brake_triggered'] = True
                results['emergency_brake_reason'] = reason
                results['emergency_brake_month'] = month
        
        # Track price
        if price < results['min_price']:
            results['min_price'] = price
        if price > results['max_price']:
            results['max_price'] = price
        
        # Track consecutive low price days
        if price < 0.02:
            consecutive_low_price_days += 30  # Approximate month as 30 days
        else:
            consecutive_low_price_days = max(0, consecutive_low_price_days - 30)
        
        results['months'].append({
            'month': month,
            'circulating': circulating_adjusted,
            'total_supply': total,
            'staked': staked,
            'price': price,
            'liquidity': current_liquidity,
            'market_cap': price * circulating_adjusted,
            'emergency_active': emergency_active
        })
    
    results['final_price'] = results['months'][-1]['price']
    results['final_circulating'] = results['months'][-1]['circulating']
    results['final_market_cap'] = results['months'][-1]['market_cap']
    
    return results


def create_scenarios() -> List[MarketScenario]:
    """Create 10 different market scenarios"""
    launch_date = datetime(2025, 3, 1)
    scenarios = []
    
    # Scenario 1: May 2021 Crypto Crash (Terra Luna collapse reference)
    s1 = MarketScenario(
        "May 2021-Style Crash",
        "Major crypto crash 2 months after launch, 60% liquidity drop"
    )
    s1.add_event(launch_date + timedelta(days=60), "crash", 0.40, "Major crypto crash")
    scenarios.append(s1)
    
    # Scenario 2: November 2022 FTX Collapse
    s2 = MarketScenario(
        "FTX Collapse Scenario",
        "Exchange collapse 3 months after launch, 70% liquidity drop"
    )
    s2.add_event(launch_date + timedelta(days=90), "exchange_collapse", 0.30, "FTX-style collapse")
    scenarios.append(s2)
    
    # Scenario 3: March 2020 COVID Crash
    s3 = MarketScenario(
        "COVID-Style Black Swan",
        "Black swan event 1 month after launch, 80% liquidity drop"
    )
    s3.add_event(launch_date + timedelta(days=30), "black_swan", 0.20, "COVID-style market crash")
    scenarios.append(s3)
    
    # Scenario 4: Gradual Decline
    s4 = MarketScenario(
        "Gradual Bear Market",
        "Slow decline over 12 months, 50% total drop"
    )
    s4.add_event(launch_date + timedelta(days=90), "decline", 0.75, "Early decline")
    s4.add_event(launch_date + timedelta(days=180), "decline", 0.60, "Mid decline")
    s4.add_event(launch_date + timedelta(days=270), "decline", 0.50, "Bottom")
    scenarios.append(s4)
    
    # Scenario 5: Bull Run Then Crash
    s5 = MarketScenario(
        "Bull Run Then Crash",
        "Strong growth for 6 months, then 70% crash"
    )
    s5.add_event(launch_date + timedelta(days=60), "bull", 1.50, "Early bull run")
    s5.add_event(launch_date + timedelta(days=120), "bull", 2.00, "Peak bull")
    s5.add_event(launch_date + timedelta(days=180), "crash", 0.60, "Major crash")
    scenarios.append(s5)
    
    # Scenario 6: Volatile Market
    s6 = MarketScenario(
        "High Volatility",
        "Multiple 30-40% swings throughout first year"
    )
    s6.add_event(launch_date + timedelta(days=45), "volatility", 0.70, "First dip")
    s6.add_event(launch_date + timedelta(days=90), "volatility", 1.30, "Recovery")
    s6.add_event(launch_date + timedelta(days=135), "volatility", 0.65, "Second dip")
    s6.add_event(launch_date + timedelta(days=180), "volatility", 1.20, "Second recovery")
    scenarios.append(s6)
    
    # Scenario 7: Stable Growth
    s7 = MarketScenario(
        "Stable Growth",
        "Gradual 20% liquidity increase over 12 months"
    )
    s7.add_event(launch_date + timedelta(days=180), "growth", 1.10, "Early growth")
    s7.add_event(launch_date + timedelta(days=360), "growth", 1.20, "Sustained growth")
    scenarios.append(s7)
    
    # Scenario 8: Early Crash Recovery
    s8 = MarketScenario(
        "Early Crash with Recovery",
        "Crash at month 2, recovery by month 6"
    )
    s8.add_event(launch_date + timedelta(days=60), "crash", 0.50, "Early crash")
    s8.add_event(launch_date + timedelta(days=120), "recovery", 0.80, "Partial recovery")
    s8.add_event(launch_date + timedelta(days=180), "recovery", 1.00, "Full recovery")
    scenarios.append(s8)
    
    # Scenario 9: Late Crash
    s9 = MarketScenario(
        "Late Market Crash",
        "Crash at month 9 after strong growth"
    )
    s9.add_event(launch_date + timedelta(days=90), "growth", 1.30, "Early growth")
    s9.add_event(launch_date + timedelta(days=180), "growth", 1.50, "Peak growth")
    s9.add_event(launch_date + timedelta(days=270), "crash", 0.50, "Late crash")
    scenarios.append(s9)
    
    # Scenario 10: Worst Case - Multiple Crashes
    s10 = MarketScenario(
        "Worst Case: Multiple Crashes",
        "Multiple crashes at months 2, 6, and 12"
    )
    s10.add_event(launch_date + timedelta(days=60), "crash", 0.60, "First crash")
    s10.add_event(launch_date + timedelta(days=180), "crash", 0.40, "Second crash")
    s10.add_event(launch_date + timedelta(days=360), "crash", 0.30, "Third crash")
    scenarios.append(s10)
    
    return scenarios


def print_results(results: Dict):
    """Print formatted simulation results"""
    print(f"\n{'='*80}")
    print(f"SCENARIO: {results['scenario']}")
    print(f"{'='*80}")
    print(f"Description: {results['description']}")
    print(f"\nKey Metrics:")
    print(f"  Final Price: ${results['final_price']:.6f}")
    print(f"  Min Price: ${results['min_price']:.6f}")
    print(f"  Max Price: ${results['max_price']:.6f}")
    print(f"  Final Circulating: {results['final_circulating']:,} tokens")
    print(f"  Final Market Cap: ${results['final_market_cap']:,.0f}")
    
    if results['emergency_brake_triggered']:
        print(f"\n⚠️  EMERGENCY BRAKE TRIGGERED")
        print(f"   Reason: {results['emergency_brake_reason']}")
        print(f"   Month: {results.get('emergency_brake_month', 'N/A')}")
    else:
        print(f"\n✅ No emergency brake triggered")
    
    # Show key months
    print(f"\nMonthly Breakdown (Key Months):")
    key_months = [0, 3, 6, 12, 18, 24]
    for month_data in results['months']:
        if month_data['month'] in key_months:
            print(f"  Month {month_data['month']:2d}: "
                  f"Price=${month_data['price']:.6f}, "
                  f"Circulating={month_data['circulating']:,}, "
                  f"Market Cap=${month_data['market_cap']:,.0f}")


def generate_summary_report(all_results: List[Dict]):
    """Generate summary report comparing all scenarios"""
    print(f"\n{'='*80}")
    print("SUMMARY REPORT: All Scenarios Comparison")
    print(f"{'='*80}\n")
    
    print(f"{'Scenario':<30} {'Final Price':<15} {'Min Price':<15} {'Emergency Brake':<15}")
    print("-" * 80)
    
    for results in all_results:
        brake_status = "✅ No" if not results['emergency_brake_triggered'] else "⚠️  YES"
        print(f"{results['scenario']:<30} "
              f"${results['final_price']:.6f}      "
              f"${results['min_price']:.6f}      "
              f"{brake_status:<15}")
    
    # Statistics
    emergency_count = sum(1 for r in all_results if r['emergency_brake_triggered'])
    avg_final_price = sum(r['final_price'] for r in all_results) / len(all_results)
    avg_min_price = sum(r['min_price'] for r in all_results) / len(all_results)
    
    print(f"\nStatistics:")
    print(f"  Scenarios with Emergency Brake: {emergency_count}/{len(all_results)}")
    print(f"  Average Final Price: ${avg_final_price:.6f}")
    print(f"  Average Minimum Price: ${avg_min_price:.6f}")


def main():
    """Run all simulations"""
    print("BlockDAG Vesting Solution - Market Scenario Simulations")
    print("=" * 80)
    
    scenarios = create_scenarios()
    all_results = []
    
    for scenario in scenarios:
        results = simulate_scenario(scenario, months=24)
        print_results(results)
        all_results.append(results)
    
    generate_summary_report(all_results)
    
    # Save results to JSON
    output_file = "vesting_simulation_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n📊 Detailed results saved to: {output_file}")


if __name__ == "__main__":
    main()

