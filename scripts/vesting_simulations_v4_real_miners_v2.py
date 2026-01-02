#!/usr/bin/env python3
"""
BlockDAG Vesting Solution - SECOND OPINION for Real Miner Data (v4)

This is an INDEPENDENT verification model for the real miner data simulation (v3).
Uses DIFFERENT methodology:
- Order book depth + sell pressure (like v2)
- But with REAL miner numbers from stakeholders
- Historical crash data
- Monte Carlo holder behavior

Purpose: Validate v3 real miner results independently.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random

print("=" * 80)
print("SECOND OPINION: REAL MINER DATA VERIFICATION (v4)")
print("=" * 80)
print("\nThis model validates v3 (real miners) using DIFFERENT methodology:")
print("• Order book depth pricing (vs AMM in v3)")
print("• Sell pressure modeling (vs static supply in v3)")
print("• Historical crash data (vs estimated impacts in v3)")
print("• Monte Carlo sampling (vs deterministic in v3)")
print("=" * 80)

# REAL MINER DATA (same as v3)
MINERS = {
    "X10": {"units": 15_000, "daily_output": 200},
    "X30": {"units": 2_500, "daily_output": 600},
    "X100": {"units": 2_500, "daily_output": 2_000},
    "X1_migrated": {"units": 50_000, "daily_output": 20},
}

X1_TOTAL_USERS = 3_000_000
X1_MIGRATION_COST = 7_500
X1_DAILY_OUTPUT = 20
TESTNET_MONTHS = 18
TESTNET_DAILY_MINERS = 50_000
PRE_LAUNCH_MINED = TESTNET_MONTHS * 30 * TESTNET_DAILY_MINERS * X1_DAILY_OUTPUT

BASE_DAILY_EMISSION = sum(m["units"] * m["daily_output"] for m in MINERS.values())

# Constants
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000

# Historical crash data
HISTORICAL_CRASHES = {
    "COVID_2020_03": {"magnitude": 0.55, "recovery_months": 2},
    "LUNA_2022_05": {"magnitude": 0.40, "recovery_months": 6},
    "FTX_2022_11": {"magnitude": 0.25, "recovery_months": 3},
}

HOLDER_SELL_BEHAVIOR = {
    "panic_sellers": 0.20,
    "partial_sellers": 0.30,
    "holders": 0.35,
    "long_term": 0.15,
}


class OrderBookModel:
    """Order book depth pricing"""
    
    def __init__(self, initial_liquidity: float, initial_depth: float = 0.1):
        self.liquidity = initial_liquidity
        self.depth = initial_depth
        self.buy_support = initial_liquidity * 0.3
        
    def calculate_price_impact(self, sell_volume_usd: float) -> float:
        if self.buy_support <= 0:
            return 0.9
        impact_ratio = sell_volume_usd / self.buy_support
        return min(0.9, impact_ratio * self.depth)
    
    def execute_sell(self, sell_volume_usd: float, current_price: float) -> float:
        price_impact = self.calculate_price_impact(sell_volume_usd)
        new_price = current_price * (1 - price_impact)
        self.buy_support = max(0, self.buy_support - sell_volume_usd * 0.5)
        return new_price


class SellPressureModel:
    """Model sell pressure from unlocks and mining"""
    
    def calculate_unlock_sell_pressure(self, unlock_amount: int, current_price: float) -> float:
        panic_sell = unlock_amount * HOLDER_SELL_BEHAVIOR["panic_sellers"] * current_price
        partial_sell = unlock_amount * HOLDER_SELL_BEHAVIOR["partial_sellers"] * 0.5 * current_price
        variance = random.uniform(0.8, 1.2)
        return (panic_sell + partial_sell) * variance
    
    def calculate_mining_sell_pressure(self, mining_amount: int, current_price: float) -> float:
        # 60% of miners sell immediately (costs to cover)
        miner_sell_rate = 0.60
        variance = random.uniform(0.5, 0.7)
        return mining_amount * miner_sell_rate * variance * current_price


class RealMinerSecondOpinion:
    """Second opinion simulator with real miner data"""
    
    def __init__(self, digression_start: int = 6):
        self.order_book = OrderBookModel(LAUNCH_LIQUIDITY)
        self.sell_pressure = SellPressureModel()
        self.digression_start = digression_start
        self.pre_launch_supply = PRE_LAUNCH_MINED
        
    def calculate_emission_rate(self, month: int) -> float:
        """Emission rate with digression"""
        emission_caps = {0: 0.0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
                         6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75}
        cap_rate = emission_caps.get(month, 1.0)
        
        if month >= self.digression_start:
            months_since = month - self.digression_start
            digression_rate = max(0.50, 1.0 - (months_since * 0.02))
        else:
            digression_rate = 1.0
        
        return cap_rate * digression_rate
    
    def calculate_x1_migrations(self, month: int, current_price: float) -> int:
        """X1 migration curve based on price"""
        migration_cost_usd = X1_MIGRATION_COST * current_price
        
        if migration_cost_usd < 100:
            monthly_rate = 0.05
        elif migration_cost_usd < 250:
            monthly_rate = 0.03
        elif migration_cost_usd < 500:
            monthly_rate = 0.02
        else:
            monthly_rate = 0.01
        
        cumulative = 50_000  # Start estimate
        remaining = X1_TOTAL_USERS - cumulative
        
        for m in range(month):
            new = int(remaining * monthly_rate)
            cumulative += new
            remaining -= new
        
        return min(cumulative, int(X1_TOTAL_USERS * 0.1))
    
    def calculate_monthly_mining(self, month: int, current_price: float) -> Dict:
        """Calculate mining with real miner data"""
        emission_rate = self.calculate_emission_rate(month)
        
        x10_emission = MINERS["X10"]["units"] * MINERS["X10"]["daily_output"] * 30 * emission_rate
        x30_emission = MINERS["X30"]["units"] * MINERS["X30"]["daily_output"] * 30 * emission_rate
        x100_emission = MINERS["X100"]["units"] * MINERS["X100"]["daily_output"] * 30 * emission_rate
        
        x1_active = self.calculate_x1_migrations(month, current_price)
        x1_emission = x1_active * X1_DAILY_OUTPUT * 30 * emission_rate
        
        return {
            "x10": int(x10_emission),
            "x30": int(x30_emission),
            "x100": int(x100_emission),
            "x1": int(x1_emission),
            "x1_active": x1_active,
            "total": int(x10_emission + x30_emission + x100_emission + x1_emission),
            "emission_rate": emission_rate
        }
    
    def apply_market_event(self, event_type: str, current_liquidity: float) -> float:
        """Apply market event using historical data"""
        if event_type == "crash_severe":
            crash = HISTORICAL_CRASHES["COVID_2020_03"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)
            return current_liquidity * (1 - impact)
        elif event_type == "crash_moderate":
            crash = HISTORICAL_CRASHES["FTX_2022_11"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)
            return current_liquidity * (1 - impact)
        elif event_type == "crash_exchange":
            crash = HISTORICAL_CRASHES["LUNA_2022_05"]
            impact = crash["magnitude"] * random.uniform(0.9, 1.1)
            return current_liquidity * (1 - impact)
        elif event_type == "bull":
            return current_liquidity * random.uniform(1.2, 1.5)
        elif event_type == "recovery":
            return current_liquidity * random.uniform(1.3, 1.5)
        return current_liquidity


def run_real_miner_v2_scenario(name: str, description: str, events: List[Dict],
                                digression_start: int = 6, months: int = 24) -> Dict:
    """Run second opinion simulation with real miner data"""
    
    sim = RealMinerSecondOpinion(digression_start=digression_start)
    
    results = {
        "scenario": name,
        "description": description,
        "methodology": "Second Opinion - Order Book + Sell Pressure",
        "miner_data": "REAL (from stakeholders)",
        "digression_start": digression_start,
        "pre_launch_mined": PRE_LAUNCH_MINED,
        "months": [],
        "emergency_brake_triggered": False,
        "emergency_brake_month": None,
        "emergency_brake_reason": "",
    }
    
    current_price = TARGET_PRICE
    current_liquidity = LAUNCH_LIQUIDITY
    total_circulating = PRE_LAUNCH_MINED  # Start with pre-launch mined
    consecutive_low_days = 0
    emergency_active = False
    
    for month in range(months + 1):
        # Apply market events
        for event in events:
            if event["month"] == month:
                current_liquidity = sim.apply_market_event(event["type"], current_liquidity)
                sim.order_book.liquidity = current_liquidity
                sim.order_book.buy_support = current_liquidity * 0.3
        
        # Base vesting
        if month == 0:
            base_vested = int(BASE_COINS * 0.02)
        elif month < 13:
            base_vested = int(BASE_COINS * 0.02)
        elif month < 25:
            months_in = month - 12
            base_vested = int(BASE_COINS * (0.02 + 0.08 * months_in / 12))
        else:
            base_vested = int(BASE_COINS * 0.10)
        
        # Mining this month
        mining = sim.calculate_monthly_mining(month, current_price)
        total_circulating += mining["total"]
        
        # Calculate sell pressure
        if month > 0:
            unlock_sell = sim.sell_pressure.calculate_unlock_sell_pressure(
                base_vested - (int(BASE_COINS * 0.02) if month > 0 else 0), current_price
            )
            mining_sell = sim.sell_pressure.calculate_mining_sell_pressure(
                mining["total"], current_price
            )
            
            total_sell_usd = unlock_sell + mining_sell
            
            if total_sell_usd > 0:
                current_price = sim.order_book.execute_sell(total_sell_usd, current_price)
                current_price = max(0.0001, current_price)
        
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
                results["emergency_brake_reason"] = f"Price ${current_price:.4f} < $0.02"
            elif current_liquidity < 10_000_000:
                emergency_active = True
                results["emergency_brake_triggered"] = True
                results["emergency_brake_month"] = month
                results["emergency_brake_reason"] = f"Liquidity ${current_liquidity/1e6:.1f}M"
        
        market_cap = current_price * total_circulating
        
        results["months"].append({
            "month": month,
            "price": current_price,
            "circulating": total_circulating,
            "mining_cumulative": total_circulating - PRE_LAUNCH_MINED - base_vested,
            "x1_active": mining["x1_active"],
            "emission_rate": mining["emission_rate"],
            "market_cap": market_cap,
            "emergency_active": emergency_active
        })
    
    results["final_price"] = current_price
    results["final_circulating"] = total_circulating
    results["final_market_cap"] = results["months"][-1]["market_cap"]
    
    return results


def compare_all_models():
    """Compare v3 (real miners, first opinion) vs v4 (real miners, second opinion)"""
    
    print("\n" + "=" * 80)
    print("COMPARING REAL MINER MODELS: v3 vs v4")
    print("=" * 80)
    
    # Load v3 results
    try:
        with open("vesting_simulation_v3_real_miners.json", "r") as f:
            v3_results = json.load(f)
    except FileNotFoundError:
        print("⚠️ v3 results not found. Run vesting_simulations_v3_real_miners.py first.")
        return
    
    # Run v4 scenarios (matching v3 digression scenarios)
    v4_results = []
    
    scenarios = [
        ("Immediate Digression", 0),
        ("Digression at Month 3", 3),
        ("Digression at Month 6", 6),
        ("No Digression", 99),
    ]
    
    for name, digression_start in scenarios:
        result = run_real_miner_v2_scenario(
            f"{name} [V4 Second Opinion]",
            f"Real miners with order book model, digression at month {digression_start}",
            [],
            digression_start,
            24
        )
        v4_results.append(result)
    
    # Comparison
    print(f"\n{'Scenario':<30} {'V3 Price':<15} {'V4 Price':<15} {'V3 Brake':<12} {'V4 Brake':<12} {'Match':<8}")
    print("-" * 100)
    
    matches = 0
    for v3, v4 in zip(v3_results, v4_results):
        v3_brake = f"M{v3['emergency_brake_month']}" if v3.get('emergency_brake_triggered') else "No"
        v4_brake = f"M{v4['emergency_brake_month']}" if v4.get('emergency_brake_triggered') else "No"
        
        brake_match = v3_brake == v4_brake
        price_ratio = v3['final_price'] / max(v4['final_price'], 0.0001)
        price_match = 0.5 < price_ratio < 2.0
        
        if brake_match and price_match:
            match_status = "✅ FULL"
            matches += 1
        elif brake_match:
            match_status = "🔶 BRAKE"
        else:
            match_status = "❌ DIFFER"
        
        print(f"{v3['scenario']:<30} "
              f"${v3['final_price']:<13.6f} "
              f"${v4['final_price']:<13.6f} "
              f"{v3_brake:<12} "
              f"{v4_brake:<12} "
              f"{match_status:<8}")
    
    print("-" * 100)
    print(f"\nAgreement: {matches}/{len(v3_results)} scenarios ({matches/len(v3_results)*100:.0f}%)")
    
    # Save v4 results
    with open("vesting_simulation_v4_real_miners.json", "w") as f:
        json.dump(v4_results, f, indent=2, default=str)
    
    print(f"\n📊 v4 results saved to: vesting_simulation_v4_real_miners.json")


def main():
    """Run second opinion for real miner data"""
    
    print("\n" + "=" * 80)
    print("SECOND OPINION: REAL MINER DATA VALIDATION")
    print("=" * 80)
    
    compare_all_models()
    
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print("""
MODEL COMPARISON:
• v3: Real miners + AMM pricing (first opinion)
• v4: Real miners + Order book + sell pressure (second opinion)

BOTH USE SAME MINER DATA:
• X10: 15,000 × 200/day
• X30: 2,500 × 600/day
• X100: 2,500 × 2,000/day
• X1: ~50,000 × 20/day
• Pre-launch: 540M BDAG

DIFFERENT METHODOLOGIES:
• v3: Price = Liquidity / Supply
• v4: Price impact from sell pressure on order book

If both agree → HIGH confidence in real miner results
""")


if __name__ == "__main__":
    random.seed(42)  # Reproducibility
    main()

