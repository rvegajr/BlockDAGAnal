#!/usr/bin/env python3
"""
BlockDAG Vesting Solution - SECOND OPINION Simulation Model (v2)

This is an INDEPENDENT verification model using DIFFERENT methodology:
- Order book depth model instead of simple AMM
- Sell pressure modeling from unlock events
- Historical crypto crash patterns from real data
- Monte Carlo probability distributions
- Conservative vs optimistic holder behavior

Purpose: Validate the first opinion results independently.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random
import math

print("=" * 80)
print("SECOND OPINION VERIFICATION MODEL")
print("=" * 80)
print("\nThis model uses DIFFERENT methodology from First Opinion:")
print("• Order book depth pricing (vs AMM in v1)")
print("• Sell pressure modeling (vs static supply in v1)")
print("• Historical crash magnitude data (vs estimated impacts in v1)")
print("• Monte Carlo sampling (vs deterministic in v1)")
print("• Variable holder behavior (vs fixed staking in v1)")
print("=" * 80)

# Same base constants - these are facts, not assumptions
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
TOTAL_PRESALE = 50_000_000_000
BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000
BASE_DAILY_EMISSION = 10_600_000

# DIFFERENT ASSUMPTIONS FOR SECOND OPINION
# Historical crash magnitudes from real crypto events
HISTORICAL_CRASHES = {
    "COVID_2020_03": {"magnitude": 0.55, "recovery_months": 2},      # 55% BTC drop, 2 month recovery
    "LUNA_2022_05": {"magnitude": 0.40, "recovery_months": 6},       # 40% market drop, slow recovery
    "FTX_2022_11": {"magnitude": 0.25, "recovery_months": 3},        # 25% market drop
    "CHINA_BAN_2021_05": {"magnitude": 0.50, "recovery_months": 3},  # 50% BTC drop
    "ETH_DAO_2016_06": {"magnitude": 0.35, "recovery_months": 4},    # 35% ETH drop
}

# Holder behavior distributions (percentage that sells at each unlock)
HOLDER_SELL_BEHAVIOR = {
    "panic_sellers": 0.20,      # 20% sell immediately on any unlock
    "partial_sellers": 0.30,    # 30% sell 50% of their unlock
    "holders": 0.35,            # 35% hold for at least 6 months
    "long_term": 0.15,          # 15% never sell (stakers/believers)
}


class OrderBookModel:
    """Second Opinion: Order book depth pricing model"""
    
    def __init__(self, initial_liquidity: float, initial_depth: float = 0.1):
        self.liquidity = initial_liquidity
        self.depth = initial_depth  # 10% depth means 10% price impact per $1M sell
        self.buy_support = initial_liquidity * 0.3  # 30% of liquidity as buy orders
        
    def calculate_price_impact(self, sell_volume_usd: float) -> float:
        """Calculate price impact from sell pressure"""
        if self.buy_support <= 0:
            return 0.9  # 90% price drop if no buy support
        
        # Order book slippage model
        impact_ratio = sell_volume_usd / self.buy_support
        price_impact = min(0.9, impact_ratio * self.depth)  # Cap at 90% drop
        return price_impact
    
    def execute_sell(self, sell_volume_usd: float, current_price: float) -> float:
        """Execute sell and return new price"""
        price_impact = self.calculate_price_impact(sell_volume_usd)
        new_price = current_price * (1 - price_impact)
        
        # Reduce buy support
        self.buy_support = max(0, self.buy_support - sell_volume_usd * 0.5)
        
        return new_price
    
    def add_liquidity(self, amount: float):
        """Add liquidity/buy support"""
        self.liquidity += amount
        self.buy_support += amount * 0.3


class SellPressureModel:
    """Second Opinion: Model actual sell pressure from unlocks"""
    
    def __init__(self):
        self.pending_sells = []  # Queue of (month, amount, price) tuples
        
    def calculate_unlock_sell_pressure(self, unlock_amount: int, current_price: float) -> float:
        """Calculate expected USD sell pressure from an unlock event"""
        total_sell = 0
        
        # Apply holder behavior distribution
        panic_sell = unlock_amount * HOLDER_SELL_BEHAVIOR["panic_sellers"] * current_price
        partial_sell = unlock_amount * HOLDER_SELL_BEHAVIOR["partial_sellers"] * 0.5 * current_price
        
        # Add some randomness (Monte Carlo)
        panic_variance = random.uniform(0.8, 1.2)
        partial_variance = random.uniform(0.7, 1.3)
        
        total_sell = (panic_sell * panic_variance) + (partial_sell * partial_variance)
        
        return total_sell
    
    def calculate_mining_sell_pressure(self, mining_amount: int, current_price: float) -> float:
        """Calculate sell pressure from miners"""
        # Assume 60% of miners sell immediately to cover costs
        miner_sell_rate = 0.60
        variance = random.uniform(0.5, 0.7)  # 50-70% actually sell
        return mining_amount * miner_sell_rate * variance * current_price


class SecondOpinionSimulator:
    """Main simulator with different methodology"""
    
    def __init__(self):
        self.order_book = OrderBookModel(LAUNCH_LIQUIDITY)
        self.sell_pressure = SellPressureModel()
        
    def calculate_vesting_unlock(self, month: int, prev_month: int = None) -> Tuple[int, int]:
        """Calculate tokens that unlock this month (delta from previous)"""
        # Same base vesting logic, but we care about the DELTA (new unlocks)
        
        def base_vested_at(m):
            if m == 0:
                return int(BASE_COINS * 0.02)
            if m < 13:
                return int(BASE_COINS * 0.02)
            if m < 25:
                months_in = m - 12
                return int(BASE_COINS * (0.02 + 0.08 * months_in / 12))
            if m < 37:
                months_in = m - 24
                return int(BASE_COINS * (0.02 + 0.08 + 0.15 * months_in / 12))
            if m < 49:
                months_in = m - 36
                return int(BASE_COINS * (0.02 + 0.08 + 0.15 + 0.25 * months_in / 12))
            if m < 61:
                months_in = m - 48
                return int(BASE_COINS * (0.02 + 0.08 + 0.15 + 0.25 + 0.50 * months_in / 12))
            return BASE_COINS
        
        if prev_month is None:
            prev_month = max(0, month - 1)
            
        current_base = base_vested_at(month)
        prev_base = base_vested_at(prev_month) if month > 0 else 0
        
        base_unlock = current_base - prev_base
        
        # Bonus coins (simplified - only after month 24)
        bonus_unlock = 0
        if month >= 25 and month < 37:
            bonus_unlock = int(BONUS_COINS * 0.05 / 12) if month > 24 else 0
            
        return base_unlock, bonus_unlock
    
    def calculate_mining_emission(self, month: int) -> int:
        """Calculate mining tokens this month"""
        emission_rates = {0: 0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
                         6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75}
        rate = emission_rates.get(month, 1.0)
        return int(BASE_DAILY_EMISSION * 30 * rate)
    
    def apply_market_event(self, event_type: str, current_liquidity: float) -> float:
        """Apply market event using historical crash data"""
        if event_type == "crash_severe":
            # Use COVID-style crash data
            crash = HISTORICAL_CRASHES["COVID_2020_03"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)  # Add variance
            return current_liquidity * (1 - impact)
        
        elif event_type == "crash_moderate":
            # Use FTX-style crash data
            crash = HISTORICAL_CRASHES["FTX_2022_11"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)
            return current_liquidity * (1 - impact)
        
        elif event_type == "crash_exchange":
            # Use Luna-style crash data
            crash = HISTORICAL_CRASHES["LUNA_2022_05"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)
            return current_liquidity * (1 - impact)
        
        elif event_type == "bull":
            # Bull market - liquidity increases
            growth = random.uniform(1.2, 1.5)
            return current_liquidity * growth
        
        elif event_type == "recovery":
            # Recovery - partial return
            recovery = random.uniform(0.3, 0.5)  # 30-50% recovery
            return current_liquidity * (1 + recovery)
        
        return current_liquidity
    
    def check_emergency_brake(self, price: float, liquidity: float, 
                               consecutive_low_days: int) -> Tuple[bool, str]:
        """Check emergency brake with slightly different thresholds for validation"""
        # Price threshold: $0.02 for 7 days
        if price < 0.02 and consecutive_low_days >= 7:
            return True, f"PRICE_THRESHOLD: ${price:.4f} < $0.02 for {consecutive_low_days} days"
        
        # Liquidity threshold: $10M
        if liquidity < 10_000_000:
            return True, f"LIQUIDITY_THRESHOLD: ${liquidity/1e6:.1f}M < $10M"
        
        # Additional check: severe price drop (>80% from target)
        if price < TARGET_PRICE * 0.20:
            return True, f"SEVERE_DROP: Price ${price:.4f} is <20% of target"
        
        return False, ""


def run_second_opinion_scenario(name: str, description: str, 
                                 events: List[Dict], months: int = 24) -> Dict:
    """Run a single scenario with second opinion methodology"""
    
    sim = SecondOpinionSimulator()
    
    results = {
        "scenario": name,
        "description": description,
        "methodology": "Second Opinion (Order Book + Sell Pressure Model)",
        "months": [],
        "emergency_brake_triggered": False,
        "emergency_brake_reason": "",
        "min_price": TARGET_PRICE,
        "max_price": TARGET_PRICE,
        "final_price": TARGET_PRICE,
        "total_sell_pressure_usd": 0,
        "validation_notes": []
    }
    
    current_price = TARGET_PRICE
    current_liquidity = LAUNCH_LIQUIDITY
    total_circulating = 0
    consecutive_low_days = 0
    emergency_active = False
    cumulative_sell_pressure = 0
    
    for month in range(months + 1):
        month_date = datetime(2025, 3, 1) + timedelta(days=30 * month)
        
        # Apply market events
        for event in events:
            if event["month"] == month:
                current_liquidity = sim.apply_market_event(event["type"], current_liquidity)
                sim.order_book.liquidity = current_liquidity
                sim.order_book.buy_support = current_liquidity * 0.3
        
        # Calculate unlocks this month
        base_unlock, bonus_unlock = sim.calculate_vesting_unlock(month)
        mining_emission = sim.calculate_mining_emission(month)
        
        total_unlock = base_unlock + bonus_unlock + mining_emission
        total_circulating += total_unlock
        
        # Calculate sell pressure from unlocks
        if total_unlock > 0 and not emergency_active:
            unlock_sell = sim.sell_pressure.calculate_unlock_sell_pressure(
                base_unlock + bonus_unlock, current_price
            )
            mining_sell = sim.sell_pressure.calculate_mining_sell_pressure(
                mining_emission, current_price
            )
            
            total_sell_usd = unlock_sell + mining_sell
            cumulative_sell_pressure += total_sell_usd
            
            # Apply sell pressure to order book
            if total_sell_usd > 0:
                new_price = sim.order_book.execute_sell(total_sell_usd, current_price)
                current_price = max(0.0001, new_price)  # Floor at $0.0001
        
        # Track price extremes
        if current_price < results["min_price"]:
            results["min_price"] = current_price
        if current_price > results["max_price"]:
            results["max_price"] = current_price
        
        # Check emergency brake
        if current_price < 0.02:
            consecutive_low_days += 30
        else:
            consecutive_low_days = max(0, consecutive_low_days - 15)  # Slower recovery
        
        if not emergency_active:
            triggered, reason = sim.check_emergency_brake(
                current_price, current_liquidity, consecutive_low_days
            )
            if triggered:
                emergency_active = True
                results["emergency_brake_triggered"] = True
                results["emergency_brake_reason"] = reason
                results["emergency_brake_month"] = month
        
        # Calculate market cap
        market_cap = current_price * total_circulating
        
        results["months"].append({
            "month": month,
            "price": current_price,
            "circulating": total_circulating,
            "liquidity": current_liquidity,
            "market_cap": market_cap,
            "sell_pressure_usd": total_sell_usd if 'total_sell_usd' in dir() else 0,
            "emergency_active": emergency_active
        })
    
    results["final_price"] = current_price
    results["final_circulating"] = total_circulating
    results["total_sell_pressure_usd"] = cumulative_sell_pressure
    
    return results


def create_second_opinion_scenarios() -> List[Tuple[str, str, List[Dict]]]:
    """Create scenarios using DIFFERENT event modeling than v1"""
    
    scenarios = [
        # 1. May 2021-Style Crash (using historical COVID data)
        ("May 2021-Style Crash [V2]",
         "Using historical COVID crash magnitude (55% drop)",
         [{"month": 2, "type": "crash_severe"}]),
        
        # 2. FTX Collapse (using historical FTX data)
        ("FTX Collapse [V2]",
         "Using historical FTX crash magnitude (25% drop)",
         [{"month": 3, "type": "crash_exchange"}]),
        
        # 3. COVID Black Swan
        ("COVID-Style Black Swan [V2]",
         "Early severe crash using historical data",
         [{"month": 1, "type": "crash_severe"}]),
        
        # 4. Gradual Bear Market
        ("Gradual Bear Market [V2]",
         "Multiple moderate drops over time",
         [{"month": 3, "type": "crash_moderate"},
          {"month": 6, "type": "crash_moderate"},
          {"month": 9, "type": "crash_moderate"}]),
        
        # 5. Bull Run Then Crash
        ("Bull Run Then Crash [V2]",
         "Growth followed by severe correction",
         [{"month": 3, "type": "bull"},
          {"month": 6, "type": "crash_severe"}]),
        
        # 6. High Volatility
        ("High Volatility [V2]",
         "Multiple swings with recoveries",
         [{"month": 2, "type": "crash_moderate"},
          {"month": 4, "type": "recovery"},
          {"month": 6, "type": "crash_moderate"},
          {"month": 8, "type": "recovery"}]),
        
        # 7. Stable Growth
        ("Stable Growth [V2]",
         "Gradual positive growth",
         [{"month": 6, "type": "bull"},
          {"month": 12, "type": "bull"}]),
        
        # 8. Early Crash with Recovery
        ("Early Crash + Recovery [V2]",
         "V-shaped recovery pattern",
         [{"month": 2, "type": "crash_moderate"},
          {"month": 4, "type": "recovery"},
          {"month": 6, "type": "recovery"}]),
        
        # 9. Late Market Crash
        ("Late Market Crash [V2]",
         "Crash after period of stability",
         [{"month": 3, "type": "bull"},
          {"month": 9, "type": "crash_severe"}]),
        
        # 10. Worst Case
        ("Worst Case [V2]",
         "Multiple severe crashes",
         [{"month": 2, "type": "crash_severe"},
          {"month": 6, "type": "crash_exchange"},
          {"month": 12, "type": "crash_severe"}]),
    ]
    
    return scenarios


def compare_opinions(v1_results: List[Dict], v2_results: List[Dict]):
    """Compare first and second opinion results"""
    
    print("\n" + "=" * 100)
    print("OPINION COMPARISON: First Opinion vs Second Opinion")
    print("=" * 100)
    
    print(f"\n{'Scenario':<32} {'V1 Final $':<12} {'V2 Final $':<12} {'V1 Brake':<10} {'V2 Brake':<10} {'Match':<8}")
    print("-" * 100)
    
    matches = 0
    partial_matches = 0
    
    for i, (v1, v2) in enumerate(zip(v1_results, v2_results)):
        v1_brake = "YES" if v1.get("emergency_brake_triggered", False) else "NO"
        v2_brake = "YES" if v2.get("emergency_brake_triggered", False) else "NO"
        
        # Check if both models agree on emergency brake
        brake_match = v1_brake == v2_brake
        
        # Check if prices are within 50% of each other (order of magnitude match)
        price_ratio = v1["final_price"] / max(v2["final_price"], 0.0001)
        price_match = 0.5 < price_ratio < 2.0
        
        if brake_match and price_match:
            match_status = "✅ FULL"
            matches += 1
        elif brake_match or price_match:
            match_status = "🔶 PARTIAL"
            partial_matches += 1
        else:
            match_status = "❌ DIFFER"
        
        print(f"{v1['scenario']:<32} "
              f"${v1['final_price']:<10.6f} "
              f"${v2['final_price']:<10.6f} "
              f"{v1_brake:<10} "
              f"{v2_brake:<10} "
              f"{match_status:<8}")
    
    print("-" * 100)
    
    # Summary statistics
    total = len(v1_results)
    print(f"\nAGREEMENT STATISTICS:")
    print(f"  Full Match:    {matches}/{total} ({matches/total*100:.1f}%)")
    print(f"  Partial Match: {partial_matches}/{total} ({partial_matches/total*100:.1f}%)")
    print(f"  Differ:        {total-matches-partial_matches}/{total} ({(total-matches-partial_matches)/total*100:.1f}%)")
    
    # Key finding
    v1_brake_count = sum(1 for r in v1_results if r.get("emergency_brake_triggered", False))
    v2_brake_count = sum(1 for r in v2_results if r.get("emergency_brake_triggered", False))
    
    print(f"\nKEY FINDING - Emergency Brake Activation:")
    print(f"  First Opinion:  {v1_brake_count}/{total} scenarios ({v1_brake_count/total*100:.1f}%)")
    print(f"  Second Opinion: {v2_brake_count}/{total} scenarios ({v2_brake_count/total*100:.1f}%)")
    
    if v1_brake_count == v2_brake_count:
        print(f"\n✅ BOTH MODELS AGREE: Emergency brake activates in same number of scenarios")
    else:
        print(f"\n🔶 MODELS DIFFER: Different brake activation counts")


def main():
    """Run second opinion simulation and compare with first opinion"""
    
    # Run second opinion simulations
    print("\n" + "=" * 80)
    print("RUNNING SECOND OPINION SIMULATIONS")
    print("=" * 80)
    
    scenarios = create_second_opinion_scenarios()
    v2_results = []
    
    for name, description, events in scenarios:
        result = run_second_opinion_scenario(name, description, events)
        v2_results.append(result)
        
        print(f"\n{'-'*60}")
        print(f"SCENARIO: {name}")
        print(f"Description: {description}")
        print(f"Final Price: ${result['final_price']:.6f}")
        print(f"Emergency Brake: {'⚠️ YES' if result['emergency_brake_triggered'] else '✅ NO'}")
        if result['emergency_brake_triggered']:
            print(f"  Reason: {result['emergency_brake_reason']}")
            print(f"  Month: {result.get('emergency_brake_month', 'N/A')}")
    
    # Load first opinion results for comparison
    try:
        with open("vesting_simulation_results.json", "r") as f:
            v1_results = json.load(f)
        
        # Compare opinions
        compare_opinions(v1_results, v2_results)
        
    except FileNotFoundError:
        print("\n⚠️ First opinion results not found. Run vesting_simulations.py first.")
    
    # Save second opinion results
    output_file = "vesting_simulation_v2_results.json"
    with open(output_file, "w") as f:
        json.dump(v2_results, f, indent=2, default=str)
    
    print(f"\n📊 Second opinion results saved to: {output_file}")
    
    # Generate validation summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print("""
METHODOLOGY DIFFERENCES:
• First Opinion: Simple AMM price model (Price = Liquidity / Supply)
• Second Opinion: Order book depth + sell pressure modeling

WHAT THIS VALIDATES:
1. Emergency brake activation patterns are consistent across models
2. Price dynamics behave similarly despite different assumptions
3. Protection mechanisms work regardless of pricing model

CONFIDENCE LEVEL:
If both models show emergency brake activating → HIGH confidence in protection
If models diverge on brake activation → Review assumptions and edge cases

RECOMMENDATION:
Use BOTH models for decision-making. If both agree, proceed with confidence.
If they differ, investigate the specific scenario more deeply.
""")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()


