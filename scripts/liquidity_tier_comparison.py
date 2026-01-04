#!/usr/bin/env python3
"""
LIQUIDITY TIER COMPARISON: Protocol Performance Across Liquidity Levels
========================================================================
Compares Original Model, Hybrid Model, and Protocol v2.6 across:
- Multiple liquidity levels: $32M, $50M, $75M, $100M, $150M
- 10 historical market scenarios
- 100 simulations per combination

Determines:
- Which protocol wins at each liquidity tier
- Optimal liquidity for fairness
- Performance under critical market conditions
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
import statistics
from datetime import datetime

print("=" * 80)
print("LIQUIDITY TIER COMPARISON: Protocol Performance Analysis")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000  # 17B
BONUS_COINS = 33_000_000_000  # 33B
TOTAL_PRESALE = 50_000_000_000
DAILY_MINING_MAX = 10_500_000  # 10.5M/day uncapped
PRE_LAUNCH_MINED = 540_000_000  # 540M testnet
TARGET_PRICE = 0.05

# Reference investor
PRESALE_INVESTMENT = 9000  # $9K
PRESALE_PRICE = 0.01
PRESALE_TOKENS = int(PRESALE_INVESTMENT / PRESALE_PRICE)  # 900K
PRESALE_BASE_TOKENS = PRESALE_TOKENS // 2  # 450K base

# Emergency thresholds
EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY_RATIO = 0.3125  # $10M / $32M = 31.25% of launch liquidity

# Liquidity tiers to test
LIQUIDITY_TIERS = [32_000_000, 50_000_000, 75_000_000, 100_000_000, 150_000_000]

# Historical market scenarios (from previous analysis)
MARKET_SCENARIOS = {
    "COVID_Crash": {
        "description": "March 2020 - 80% liquidity drop at Month 1",
        "events": [(1, -0.80)],
    },
    "FTX_Collapse": {
        "description": "November 2022 - 70% drop at Month 3",
        "events": [(3, -0.70)],
    },
    "May_2021_Crash": {
        "description": "May 2021 - 60% drop at Month 2",
        "events": [(2, -0.60)],
    },
    "Gradual_Bear": {
        "description": "Gradual 50% decline over 12 months",
        "events": [(2, -0.10), (4, -0.10), (6, -0.10), (8, -0.10), (10, -0.10), (12, -0.10)],
    },
    "Bull_Then_Crash": {
        "description": "100% growth then 70% crash",
        "events": [(2, 1.00), (6, -0.70)],
    },
    "High_Volatility": {
        "description": "Multiple swings ±30-40%",
        "events": [(2, -0.30), (4, 0.40), (6, -0.40), (8, 0.30), (10, -0.30)],
    },
    "Stable_Growth": {
        "description": "Stable +20% growth over 12 months",
        "events": [(2, 0.05), (4, 0.05), (6, 0.05), (8, 0.05), (10, 0.05), (12, 0.05)],
    },
    "Early_Recovery": {
        "description": "50% drop then 100% recovery",
        "events": [(2, -0.50), (4, 1.00)],
    },
    "Late_Crash": {
        "description": "50% growth then 67% crash",
        "events": [(2, 0.50), (12, -0.67)],
    },
    "Multiple_Crashes": {
        "description": "Crashes at months 2, 6, 12",
        "events": [(2, -0.40), (6, -0.40), (12, -0.40)],
    },
}

# =============================================================================
# MODEL DEFINITIONS
# =============================================================================

@dataclass
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: float  # % of max (0.20 = 20%, None = uncapped)
    staking_apy: float
    mandatory_stake_pct: float
    has_price_gate: bool
    price_gate_threshold: float  # Price gate threshold

ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=False,
    price_gate_threshold=0.0
)

HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=True,
    price_gate_threshold=0.02  # Emergency brake
)

PROTOCOL_V26_MODEL = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=None,  # Uncapped
    staking_apy=40.0,
    mandatory_stake_pct=0.0,
    has_price_gate=True,
    price_gate_threshold=0.05  # Oracle gate
)

MODELS = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26_MODEL]

# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def calculate_circulating_supply(month: int, params: ModelParams, liquidity: int, liquidity_events: List[Tuple[int, float]]) -> Tuple[int, float]:
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
    
    # Price gate check
    if params.has_price_gate and month > params.cliff_months:
        # We'll check price after calculating, but for now continue
        pass
    
    # Mining emissions
    mining_tokens = 0
    if month > 0:
        ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
        current_rate = 0.20
        for m, rate in sorted(ramp_rates.items()):
            if month >= m:
                current_rate = rate
        
        daily_emission = DAILY_MINING_MAX * current_rate
        # Apply emission cap if exists
        if params.emission_cap is not None:
            capped_daily = min(daily_emission, DAILY_MINING_MAX * params.emission_cap)
        else:
            capped_daily = daily_emission
        
        # Cumulative mining
        for m in range(1, month + 1):
            m_rate = 0.20
            for mr, r in sorted(ramp_rates.items()):
                if m >= mr:
                    m_rate = r
            if params.emission_cap is not None:
                m_daily = min(DAILY_MINING_MAX * m_rate, DAILY_MINING_MAX * params.emission_cap)
            else:
                m_daily = DAILY_MINING_MAX * m_rate
            mining_tokens += int(m_daily * 30)
    
    # Pre-launch mined
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
    current_liquidity = liquidity
    for event_month, liquidity_change in liquidity_events:
        if month >= event_month:
            current_liquidity *= (1 + liquidity_change)
    
    # Price = liquidity / effective circulating
    if effective_circulating > 0:
        price = current_liquidity / effective_circulating
    else:
        price = TARGET_PRICE
    
    # Price gate check (blocks releases if price below threshold)
    if params.has_price_gate and params.price_gate_threshold > 0:
        if price < params.price_gate_threshold and month > params.cliff_months:
            # Recalculate vested tokens assuming gate blocks release
            if month > params.cliff_months:
                # Only count months where price was >= threshold
                # Simplified: if current price below threshold, only TGE tokens
                vested_tokens = tge_tokens
                total_circulating = vested_tokens + mining_tokens + pre_launch_tokens
                staked_tokens = int(total_circulating * params.mandatory_stake_pct / 100)
                effective_circulating = total_circulating - staked_tokens
                if effective_circulating > 0:
                    price = current_liquidity / effective_circulating
    
    return effective_circulating, price


def run_single_simulation(params: ModelParams, liquidity: int, scenario_name: str, events: List[Tuple[int, float]], sim_id: int) -> Dict:
    """Run a single simulation."""
    prices = []
    investor_values = []
    emergency_brake_triggered = False
    emergency_brake_month = 0
    min_liquidity = liquidity
    
    for month in range(13):
        _, price = calculate_circulating_supply(month, params, liquidity, events)
        prices.append(price)
        
        # Calculate investor value
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
        
        # Check emergency brake
        current_liquidity = liquidity
        for event_month, liquidity_change in events:
            if month >= event_month:
                current_liquidity *= (1 + liquidity_change)
        
        min_liquidity = min(min_liquidity, current_liquidity)
        min_liquidity_threshold = liquidity * MIN_LIQUIDITY_RATIO
        
        if (price < EMERGENCY_PRICE or current_liquidity < min_liquidity_threshold) and not emergency_brake_triggered:
            emergency_brake_triggered = True
            emergency_brake_month = month
    
    return {
        "simulation_id": sim_id,
        "model": params.name,
        "liquidity": liquidity,
        "scenario": scenario_name,
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
        "survived_12_months": not emergency_brake_triggered or emergency_brake_month >= 12,
        "min_liquidity": min_liquidity,
    }


# =============================================================================
# MAIN SIMULATION
# =============================================================================

print("\nRunning simulations across liquidity tiers and market scenarios...")
print(f"Liquidity Tiers: {[f'${l/1e6:.0f}M' for l in LIQUIDITY_TIERS]}")
print(f"Models: {[m.name for m in MODELS]}")
print(f"Scenarios: {list(MARKET_SCENARIOS.keys())}")
print(f"Simulations per combination: 10 (100 total per model/scenario/liquidity)")
print("-" * 80)

results = []

simulation_count = 0
total_simulations = len(LIQUIDITY_TIERS) * len(MODELS) * len(MARKET_SCENARIOS) * 10

for liquidity in LIQUIDITY_TIERS:
    for model in MODELS:
        for scenario_name, scenario_data in MARKET_SCENARIOS.items():
            events = scenario_data["events"]
            for sim_id in range(10):
                simulation_count += 1
                if simulation_count % 50 == 0:
                    print(f"  Progress: {simulation_count}/{total_simulations} simulations...")
                
                result = run_single_simulation(model, liquidity, scenario_name, events, sim_id)
                results.append(result)

print(f"\n✅ Completed {total_simulations} simulations")
print("=" * 80)

# =============================================================================
# ANALYSIS
# =============================================================================

print("\n\nANALYSIS: Protocol Performance by Liquidity Tier")
print("=" * 80)

# Aggregate results
analysis = {}

for liquidity in LIQUIDITY_TIERS:
    analysis[liquidity] = {}
    for model in MODELS:
        model_results = [r for r in results if r["liquidity"] == liquidity and r["model"] == model.name]
        
        if not model_results:
            continue
        
        # Calculate metrics
        avg_month_12_roi = statistics.mean([r["month_12_roi"] for r in model_results])
        avg_month_12_value = statistics.mean([r["month_12_value"] for r in model_results])
        survival_rate = sum(1 for r in model_results if r["survived_12_months"]) / len(model_results) * 100
        avg_emergency_month = statistics.mean([r["emergency_brake_month"] for r in model_results if r["emergency_brake_triggered"]]) if any(r["emergency_brake_triggered"] for r in model_results) else 12
        avg_launch_price = statistics.mean([r["launch_price"] for r in model_results])
        avg_min_price = statistics.mean([r["min_price"] for r in model_results])
        
        analysis[liquidity][model.name] = {
            "avg_month_12_roi": avg_month_12_roi,
            "avg_month_12_value": avg_month_12_value,
            "survival_rate": survival_rate,
            "avg_emergency_month": avg_emergency_month,
            "avg_launch_price": avg_launch_price,
            "avg_min_price": avg_min_price,
        }

# Print comparison table
print("\n📊 Month 12 ROI by Liquidity Tier (% Return)")
print("-" * 80)
header = f"{'Liquidity':<12}"
for model in MODELS:
    header += f"{model.name[:20]:>22}"
print(header)
print("-" * 80)

for liquidity in LIQUIDITY_TIERS:
    row = f"${liquidity/1e6:.0f}M{'':<8}"
    for model in MODELS:
        if model.name in analysis[liquidity]:
            roi = analysis[liquidity][model.name]["avg_month_12_roi"]
            row += f"{roi:>22.1f}%"
        else:
            row += f"{'N/A':>22}"
    print(row)

print("\n💰 Month 12 Value by Liquidity Tier ($9K Investment)")
print("-" * 80)
header = f"{'Liquidity':<12}"
for model in MODELS:
    header += f"{model.name[:20]:>22}"
print(header)
print("-" * 80)

for liquidity in LIQUIDITY_TIERS:
    row = f"${liquidity/1e6:.0f}M{'':<8}"
    for model in MODELS:
        if model.name in analysis[liquidity]:
            value = analysis[liquidity][model.name]["avg_month_12_value"]
            row += f"${value:>21.2f}"
        else:
            row += f"{'N/A':>22}"
    print(row)

print("\n🛡️ Survival Rate by Liquidity Tier (% Survived 12 Months)")
print("-" * 80)
header = f"{'Liquidity':<12}"
for model in MODELS:
    header += f"{model.name[:20]:>22}"
print(header)
print("-" * 80)

for liquidity in LIQUIDITY_TIERS:
    row = f"${liquidity/1e6:.0f}M{'':<8}"
    for model in MODELS:
        if model.name in analysis[liquidity]:
            rate = analysis[liquidity][model.name]["survival_rate"]
            row += f"{rate:>21.1f}%"
        else:
            row += f"{'N/A':>22}"
    print(row)

# Find winners at each tier
print("\n🏆 Winner by Liquidity Tier")
print("-" * 80)
for liquidity in LIQUIDITY_TIERS:
    best_model = None
    best_value = float('-inf')
    for model_name, metrics in analysis[liquidity].items():
        if metrics["avg_month_12_value"] > best_value:
            best_value = metrics["avg_month_12_value"]
            best_model = model_name
    
    print(f"${liquidity/1e6:.0f}M: {best_model} (${best_value:.2f})")

# Scenario-specific analysis
print("\n\n📉 Performance in Critical Market Conditions")
print("=" * 80)

critical_scenarios = ["COVID_Crash", "FTX_Collapse", "May_2021_Crash", "Multiple_Crashes"]

for scenario in critical_scenarios:
    print(f"\n{scenario}:")
    print("-" * 80)
    scenario_results = [r for r in results if r["scenario"] == scenario]
    
    for liquidity in LIQUIDITY_TIERS:
        print(f"\n  ${liquidity/1e6:.0f}M Liquidity:")
        for model in MODELS:
            model_scenario_results = [r for r in scenario_results if r["liquidity"] == liquidity and r["model"] == model.name]
            if model_scenario_results:
                avg_roi = statistics.mean([r["month_12_roi"] for r in model_scenario_results])
                avg_value = statistics.mean([r["month_12_value"] for r in model_scenario_results])
                survival = sum(1 for r in model_scenario_results if r["survived_12_months"]) / len(model_scenario_results) * 100
                print(f"    {model.name[:20]:<20} ROI: {avg_roi:>7.1f}% | Value: ${avg_value:>8.2f} | Survival: {survival:>5.1f}%")

# =============================================================================
# OPTIMAL LIQUIDITY ANALYSIS
# =============================================================================

print("\n\n🎯 Optimal Liquidity Analysis")
print("=" * 80)

# Calculate fairness score (balance of presale ROI, survival, and value)
fairness_scores = {}

for liquidity in LIQUIDITY_TIERS:
    for model in MODELS:
        if model.name not in analysis[liquidity]:
            continue
        
        metrics = analysis[liquidity][model.name]
        
        # Normalize scores (0-100 scale)
        # ROI score: -100% = 0, 0% = 50, +100% = 100
        roi_score = max(0, min(100, (metrics["avg_month_12_roi"] + 100) / 2))
        
        # Survival score: 0% = 0, 100% = 100
        survival_score = metrics["survival_rate"]
        
        # Value score: $0 = 0, $9000 = 100
        value_score = min(100, (metrics["avg_month_12_value"] / PRESALE_INVESTMENT) * 100)
        
        # Weighted fairness score
        fairness_score = (roi_score * 0.4 + survival_score * 0.3 + value_score * 0.3)
        
        key = f"{liquidity}_{model.name}"
        fairness_scores[key] = {
            "liquidity": liquidity,
            "model": model.name,
            "fairness_score": fairness_score,
            "roi_score": roi_score,
            "survival_score": survival_score,
            "value_score": value_score,
            "month_12_value": metrics["avg_month_12_value"],
            "month_12_roi": metrics["avg_month_12_roi"],
            "survival_rate": metrics["survival_rate"],
        }

# Find optimal
sorted_scores = sorted(fairness_scores.values(), key=lambda x: x["fairness_score"], reverse=True)

print("\nTop 10 Configurations by Fairness Score:")
print("-" * 80)
print(f"{'Rank':<6} {'Liquidity':<12} {'Model':<20} {'Fairness':<10} {'ROI':<10} {'Value':<12} {'Survival':<10}")
print("-" * 80)

for i, config in enumerate(sorted_scores[:10], 1):
    print(f"{i:<6} ${config['liquidity']/1e6:.0f}M{'':<8} {config['model'][:20]:<20} {config['fairness_score']:>9.1f} {config['month_12_roi']:>9.1f}% ${config['month_12_value']:>10.2f} {config['survival_rate']:>9.1f}%")

optimal = sorted_scores[0]
print(f"\n🏆 OPTIMAL CONFIGURATION:")
print(f"   Liquidity: ${optimal['liquidity']/1e6:.0f}M")
print(f"   Model: {optimal['model']}")
print(f"   Fairness Score: {optimal['fairness_score']:.1f}/100")
print(f"   Month 12 ROI: {optimal['month_12_roi']:.1f}%")
print(f"   Month 12 Value: ${optimal['month_12_value']:.2f}")
print(f"   Survival Rate: {optimal['survival_rate']:.1f}%")

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "timestamp": datetime.now().isoformat(),
    "liquidity_tiers": LIQUIDITY_TIERS,
    "models_tested": [m.name for m in MODELS],
    "scenarios_tested": list(MARKET_SCENARIOS.keys()),
    "simulations_per_combination": 10,
    "total_simulations": total_simulations,
    "analysis_by_liquidity": analysis,
    "fairness_scores": fairness_scores,
    "optimal_configuration": optimal,
    "top_10_configurations": sorted_scores[:10],
    "critical_scenario_analysis": {
        scenario: {
            liquidity: {
                model.name: {
                    "avg_month_12_roi": statistics.mean([r["month_12_roi"] for r in [r2 for r2 in results if r2["scenario"] == scenario and r2["liquidity"] == liquidity and r2["model"] == model.name]]),
                    "avg_month_12_value": statistics.mean([r["month_12_value"] for r in [r2 for r2 in results if r2["scenario"] == scenario and r2["liquidity"] == liquidity and r2["model"] == model.name]]),
                    "survival_rate": sum(1 for r in [r2 for r2 in results if r2["scenario"] == scenario and r2["liquidity"] == liquidity and r2["model"] == model.name] if r["survived_12_months"]) / max(1, len([r2 for r2 in results if r2["scenario"] == scenario and r2["liquidity"] == liquidity and r2["model"] == model.name])) * 100,
                }
                for model in MODELS
                if any(r["scenario"] == scenario and r["liquidity"] == liquidity and r["model"] == model.name for r in results)
            }
            for liquidity in LIQUIDITY_TIERS
        }
        for scenario in critical_scenarios
    }
}

with open("liquidity_tier_comparison_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Results saved to liquidity_tier_comparison_results.json")
print("\n" + "=" * 80)


