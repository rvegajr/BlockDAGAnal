#!/usr/bin/env python3
"""
THREE MODEL COMPARISON: Investor Returns Analysis
==================================================
Compares investor returns across 100 simulations for:
1. Original Model (2% TGE, 12mo cliff, 60mo vest)
2. Hybrid Model (3% TGE, 3mo cliff, 36mo vest)
3. Protocol v2.6 (3% TGE, 3mo cliff, 21mo vest)

Tests across varying market conditions:
- Bull Market (+50% liquidity growth)
- Bear Market (-50% liquidity decline)
- Normal Market (stable)
- Volatile Market (±30% swings)
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import statistics
from datetime import datetime

print("=" * 80)
print("THREE MODEL COMPARISON: Investor Returns Analysis")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000  # 17B
BONUS_COINS = 33_000_000_000  # 33B
TOTAL_PRESALE = 50_000_000_000
DAILY_MINING_MAX = 10_500_000  # 10.5M/day uncapped
PRE_LAUNCH_MINED = 540_000_000  # 540M testnet
LAUNCH_LIQUIDITY = 32_000_000  # $32M
TARGET_PRICE = 0.05

# Reference investor
PRESALE_INVESTMENT = 9000  # $9K
PRESALE_PRICE = 0.01
PRESALE_TOKENS = int(PRESALE_INVESTMENT / PRESALE_PRICE)  # 900K
PRESALE_BASE_TOKENS = PRESALE_TOKENS // 2  # 450K base

# Emergency thresholds
EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY = 10_000_000

# =============================================================================
# MODEL DEFINITIONS
# =============================================================================

@dataclass
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: float  # % of max (0.20 = 20%)
    staking_apy: float
    mandatory_stake_pct: float
    has_price_gate: bool  # Protocol v2.6 has oracle gate at $0.05

# Original Model (before hybrid)
ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,  # 20%
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=False
)

# Hybrid Model (current)
HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,  # 20%
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=True  # Emergency brake at $0.02
)

# Protocol v2.6
PROTOCOL_V26_MODEL = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,  # No cap mentioned (assume uncapped)
    staking_apy=40.0,
    mandatory_stake_pct=0.0,  # No mandatory staking mentioned
    has_price_gate=True  # Oracle gate at $0.05
)

# =============================================================================
# MARKET CONDITIONS
# =============================================================================

def generate_market_conditions(scenario_type: str, months: int = 12) -> List[Tuple[int, float]]:
    """Generate liquidity events based on market condition type."""
    events = []
    
    if scenario_type == "bull":
        # Bull market: gradual growth
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(0.05, 0.10)))  # +5-10% per period
    
    elif scenario_type == "bear":
        # Bear market: gradual decline
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(-0.10, -0.05)))  # -5-10% per period
    
    elif scenario_type == "volatile":
        # Volatile: swings up and down
        for month in [2, 4, 6, 8, 10, 12]:
            swing = random.choice([-1, 1]) * random.uniform(0.15, 0.30)
            events.append((month, swing))
    
    elif scenario_type == "normal":
        # Normal: small fluctuations
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(-0.03, 0.03)))  # ±3%
    
    return events

# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def calculate_circulating_supply(month: int, params: ModelParams, liquidity_events: List[Tuple[int, float]]) -> Tuple[int, float]:
    """Calculate circulating supply and price at a given month."""
    # TGE tokens
    tge_tokens = int(BASE_COINS * params.tge_percent / 100)
    
    # Vesting release
    vested_tokens = 0
    if month == 0:
        vested_tokens = tge_tokens
    elif month > params.cliff_months:
        months_vesting = month - params.cliff_months
        if months_vesting > 0:
            remaining_pct = (100 - params.tge_percent) / 100
            monthly_vest_rate = remaining_pct / params.vesting_months
            vested_pct = params.tge_percent / 100 + (months_vesting * monthly_vest_rate)
            vested_tokens = int(BASE_COINS * min(vested_pct, 1.0))
    
    # Price gate check (Protocol v2.6)
    if params.has_price_gate:
        # Check if we can calculate price yet
        if month > 0:
            # We'll check price after calculating, but for now continue
            pass
    
    # Mining emissions (ramp up then cap)
    mining_tokens = 0
    if month > 0:
        # Ramp up: 20% month 1, 35% month 2, 50% month 3, 80% month 6, 100% month 12
        ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
        current_rate = 0.0
        for m, rate in sorted(ramp_rates.items()):
            if month >= m:
                current_rate = rate
        
        if current_rate == 0:
            current_rate = 0.20
        
        daily_emission = DAILY_MINING_MAX * current_rate
        # Apply emission cap
        capped_daily = min(daily_emission, DAILY_MINING_MAX * params.emission_cap)
        
        # Cumulative mining
        for m in range(1, month + 1):
            m_rate = 0.20
            for mr, r in sorted(ramp_rates.items()):
                if m >= mr:
                    m_rate = r
            m_daily = min(DAILY_MINING_MAX * m_rate, DAILY_MINING_MAX * params.emission_cap)
            mining_tokens += int(m_daily * 30)
    
    # Pre-launch mined (migrated over time)
    pre_launch_tokens = 0
    if month > 0:
        immediate = int(PRE_LAUNCH_MINED * 0.30)
        gradual = int(PRE_LAUNCH_MINED * 0.50)
        monthly_gradual = gradual / 6
        pre_launch_tokens = immediate + int(min(month, 6) * monthly_gradual)
    
    # Staking removes from circulating
    total_circulating = vested_tokens + mining_tokens + pre_launch_tokens
    staked_tokens = int(total_circulating * params.mandatory_stake_pct / 100)
    effective_circulating = total_circulating - staked_tokens
    
    # Calculate liquidity (affected by events)
    current_liquidity = LAUNCH_LIQUIDITY
    for event_month, liquidity_change in liquidity_events:
        if month >= event_month:
            current_liquidity *= (1 + liquidity_change)
    
    # Price = liquidity / effective circulating
    if effective_circulating > 0:
        price = current_liquidity / effective_circulating
    else:
        price = TARGET_PRICE
    
    # Price gate check (Protocol v2.6: only vest if price >= $0.05)
    if params.has_price_gate and params.name == "Protocol v2.6":
        if price < 0.05 and month > params.cliff_months:
            # Recalculate vested tokens assuming gate blocks release
            if month > params.cliff_months:
                months_vesting = month - params.cliff_months
                remaining_pct = (100 - params.tge_percent) / 100
                monthly_vest_rate = remaining_pct / params.vesting_months
                # Only count months where price was >= $0.05
                # Simplified: assume gate blocks all releases below $0.05
                if price < 0.05:
                    vested_tokens = tge_tokens  # Only TGE tokens
                    # Recalculate total
                    total_circulating = vested_tokens + mining_tokens + pre_launch_tokens
                    staked_tokens = int(total_circulating * params.mandatory_stake_pct / 100)
                    effective_circulating = total_circulating - staked_tokens
                    if effective_circulating > 0:
                        price = current_liquidity / effective_circulating
    
    return effective_circulating, price


def run_single_simulation(params: ModelParams, market_type: str, simulation_id: int) -> Dict:
    """Run a single simulation with given parameters."""
    liquidity_events = generate_market_conditions(market_type)
    
    # Track prices and investor value over time
    prices = []
    investor_values = []
    emergency_brake_triggered = False
    emergency_brake_month = 0
    
    for month in range(13):
        _, price = calculate_circulating_supply(month, params, liquidity_events)
        prices.append(price)
        
        # Calculate investor value at this month
        tge_tokens = int(PRESALE_BASE_TOKENS * params.tge_percent / 100)
        
        if month == 0:
            vested_pct = params.tge_percent / 100
        elif month > params.cliff_months:
            months_vesting = month - params.cliff_months
            remaining_pct = (100 - params.tge_percent) / 100
            monthly_vest_rate = remaining_pct / params.vesting_months
            vested_pct = params.tge_percent / 100 + (months_vesting * monthly_vest_rate)
            vested_pct = min(vested_pct, 1.0)
        else:
            vested_pct = params.tge_percent / 100
        
        vested_tokens = int(PRESALE_BASE_TOKENS * vested_pct)
        investor_value = vested_tokens * price
        investor_values.append(investor_value)
        
        # Check emergency brake (for Hybrid Model)
        if params.has_price_gate and params.name == "Hybrid Model":
            current_liquidity = LAUNCH_LIQUIDITY
            for event_month, liquidity_change in liquidity_events:
                if month >= event_month:
                    current_liquidity *= (1 + liquidity_change)
            
            if (price < EMERGENCY_PRICE or current_liquidity < MIN_LIQUIDITY) and not emergency_brake_triggered:
                emergency_brake_triggered = True
                emergency_brake_month = month
    
    return {
        "simulation_id": simulation_id,
        "market_type": market_type,
        "launch_price": prices[0],
        "month_3_price": prices[3],
        "month_6_price": prices[6],
        "month_12_price": prices[12],
        "min_price": min(prices),
        "max_price": max(prices),
        "tge_value": investor_values[0],
        "month_3_value": investor_values[3],
        "month_6_value": investor_values[6],
        "month_12_value": investor_values[12],
        "tge_roi": (investor_values[0] / PRESALE_INVESTMENT - 1) * 100,
        "month_3_roi": (investor_values[3] / PRESALE_INVESTMENT - 1) * 100,
        "month_6_roi": (investor_values[6] / PRESALE_INVESTMENT - 1) * 100,
        "month_12_roi": (investor_values[12] / PRESALE_INVESTMENT - 1) * 100,
        "emergency_brake_triggered": emergency_brake_triggered,
        "emergency_brake_month": emergency_brake_month,
    }


# =============================================================================
# MAIN SIMULATION
# =============================================================================

print("\nRunning 100 simulations per model across 4 market conditions...")
print("=" * 80)

models = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26_MODEL]
market_types = ["bull", "bear", "normal", "volatile"]
simulations_per_market = 25  # 25 × 4 = 100 total per model

results = {}

for model in models:
    print(f"\nTesting {model.name}...")
    model_results = []
    
    for market_type in market_types:
        for sim_id in range(simulations_per_market):
            result = run_single_simulation(model, market_type, sim_id)
            result["model"] = model.name
            model_results.append(result)
    
    results[model.name] = model_results

print("\n✅ All simulations complete!")
print("=" * 80)

# =============================================================================
# ANALYSIS
# =============================================================================

print("\n\nINVESTOR RETURNS COMPARISON")
print("=" * 80)

comparison = {}

for model_name in [m.name for m in models]:
    model_results = results[model_name]
    
    # Aggregate by market type
    by_market = {}
    for market_type in market_types:
        market_results = [r for r in model_results if r["market_type"] == market_type]
        
        by_market[market_type] = {
            "tge_roi_avg": statistics.mean([r["tge_roi"] for r in market_results]),
            "tge_roi_median": statistics.median([r["tge_roi"] for r in market_results]),
            "month_3_roi_avg": statistics.mean([r["month_3_roi"] for r in market_results]),
            "month_6_roi_avg": statistics.mean([r["month_6_roi"] for r in market_results]),
            "month_12_roi_avg": statistics.mean([r["month_12_roi"] for r in market_results]),
            "month_12_value_avg": statistics.mean([r["month_12_value"] for r in market_results]),
            "min_price_avg": statistics.mean([r["min_price"] for r in market_results]),
            "max_price_avg": statistics.mean([r["max_price"] for r in market_results]),
            "emergency_brake_rate": sum(1 for r in market_results if r["emergency_brake_triggered"]) / len(market_results) * 100,
        }
    
    # Overall averages
    comparison[model_name] = {
        "by_market": by_market,
        "overall_tge_roi": statistics.mean([r["tge_roi"] for r in model_results]),
        "overall_month_12_roi": statistics.mean([r["month_12_roi"] for r in model_results]),
        "overall_month_12_value": statistics.mean([r["month_12_value"] for r in model_results]),
        "overall_emergency_brake_rate": sum(1 for r in model_results if r["emergency_brake_triggered"]) / len(model_results) * 100,
    }

# Print comparison table
print("\n📊 TGE ROI Comparison (% Return)")
print("-" * 80)
print(f"{'Model':<20} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<20}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        roi = comparison[model_name]["by_market"][market_type]["tge_roi_avg"]
        row += f"{roi:>12.1f}%"
    overall = comparison[model_name]["overall_tge_roi"]
    row += f"{overall:>12.1f}%"
    print(row)

print("\n📊 Month 12 ROI Comparison (% Return)")
print("-" * 80)
print(f"{'Model':<20} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<20}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        roi = comparison[model_name]["by_market"][market_type]["month_12_roi_avg"]
        row += f"{roi:>12.1f}%"
    overall = comparison[model_name]["overall_month_12_roi"]
    row += f"{overall:>12.1f}%"
    print(row)

print("\n💰 Month 12 Value Comparison ($9K Investment)")
print("-" * 80)
print(f"{'Model':<20} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<20}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        value = comparison[model_name]["by_market"][market_type]["month_12_value_avg"]
        row += f"${value:>11.2f}"
    overall = comparison[model_name]["overall_month_12_value"]
    row += f"${overall:>11.2f}"
    print(row)

print("\n🛡️ Emergency Brake Activation Rate")
print("-" * 80)
print(f"{'Model':<20} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<20}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        rate = comparison[model_name]["by_market"][market_type]["emergency_brake_rate"]
        row += f"{rate:>11.1f}%"
    overall = comparison[model_name]["overall_emergency_brake_rate"]
    row += f"{overall:>11.1f}%"
    print(row)

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "timestamp": datetime.now().isoformat(),
    "models_tested": [m.name for m in models],
    "simulations_per_model": 100,
    "market_conditions": market_types,
    "comparison": comparison,
    "raw_results": results
}

with open("three_model_comparison_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Results saved to three_model_comparison_results.json")
print("\n" + "=" * 80)

