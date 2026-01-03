#!/usr/bin/env python3
"""
HYBRID MODEL VALIDATION
=======================
Tests 100 parameter combinations to find the optimal hybrid model,
then validates against 10 historical market scenarios.

Parameters tested:
- TGE %: 2%, 3%, 5%, 10%
- Cliff: 0, 3, 6, 12 months
- Vesting: 24, 36, 48, 60 months
- Emission Cap: 10%, 15%, 20%, 25%
- Staking APY: 25%, 30%, 35%, 40%
- Mandatory Staking: 30%, 40%, 50%, 60%

Then tests top performers against 10 historical market crashes.
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from itertools import product
import statistics
from datetime import datetime

print("=" * 80)
print("HYBRID MODEL VALIDATION - 100 Simulations + 10 Market Scenarios")
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

# Historical market scenarios
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
# DATA CLASSES
# =============================================================================

@dataclass
class HybridParams:
    tge_percent: float      # 2-10%
    cliff_months: int       # 0-12
    vesting_months: int     # 24-60
    emission_cap: float     # 10-25%
    staking_apy: float      # 25-40%
    mandatory_stake_pct: float  # 30-60%
    
    def __str__(self):
        return f"TGE:{self.tge_percent}% Cliff:{self.cliff_months}mo Vest:{self.vesting_months}mo Cap:{self.emission_cap}% APY:{self.staking_apy}% Mand:{self.mandatory_stake_pct}%"


@dataclass
class SimulationResult:
    params: HybridParams
    launch_price: float
    month_3_price: float
    month_6_price: float
    month_12_price: float
    min_price: float
    max_price: float
    emergency_brake_month: int  # 0 = never
    months_above_target: int
    presale_tge_value: float
    presale_tge_roi: float
    presale_year1_roi: float
    total_score: float


@dataclass
class MarketScenarioResult:
    scenario_name: str
    final_price: float
    min_price: float
    emergency_brake_month: int
    months_survived: int
    presale_year1_value: float


# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def calculate_circulating_supply(month: int, params: HybridParams, liquidity_events: List[Tuple[int, float]]) -> Tuple[int, float]:
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
    
    # Mining emissions (ramp up then cap)
    mining_tokens = 0
    if month > 0:
        # Ramp up: 20% month 1, 35% month 2, 50% month 3, 80% month 6, 100% month 12
        ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
        current_rate = 0.0
        for m, rate in sorted(ramp_rates.items()):
            if month >= m:
                current_rate = rate
        
        # If no exact match, interpolate
        if current_rate == 0:
            current_rate = 0.20  # Month 1 default
        
        daily_emission = DAILY_MINING_MAX * current_rate
        # Apply emission cap
        capped_daily = min(daily_emission, DAILY_MINING_MAX * params.emission_cap / 100)
        
        # Cumulative mining
        for m in range(1, month + 1):
            m_rate = 0.20
            for mr, r in sorted(ramp_rates.items()):
                if m >= mr:
                    m_rate = r
            m_daily = min(DAILY_MINING_MAX * m_rate, DAILY_MINING_MAX * params.emission_cap / 100)
            mining_tokens += int(m_daily * 30)  # Monthly
    
    # Pre-launch mined (migrated over time)
    pre_launch_tokens = 0
    if month > 0:
        # 30% migrate immediately, 50% over 6 months, 20% never
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
    
    return effective_circulating, price


def run_single_simulation(params: HybridParams, liquidity_events: List[Tuple[int, float]] = None) -> SimulationResult:
    """Run a single simulation with given parameters."""
    if liquidity_events is None:
        liquidity_events = []
    
    # Calculate prices at key milestones
    _, launch_price = calculate_circulating_supply(0, params, liquidity_events)
    _, month_3_price = calculate_circulating_supply(3, params, liquidity_events)
    _, month_6_price = calculate_circulating_supply(6, params, liquidity_events)
    _, month_12_price = calculate_circulating_supply(12, params, liquidity_events)
    
    # Find min/max over 12 months
    min_price = launch_price
    max_price = launch_price
    months_above_target = 0
    emergency_brake_month = 0
    
    for month in range(13):
        _, price = calculate_circulating_supply(month, params, liquidity_events)
        min_price = min(min_price, price)
        max_price = max(max_price, price)
        
        if price >= EMERGENCY_PRICE:
            months_above_target += 1
        
        # Check emergency brake
        current_liquidity = LAUNCH_LIQUIDITY
        for event_month, liquidity_change in liquidity_events:
            if month >= event_month:
                current_liquidity *= (1 + liquidity_change)
        
        if (price < EMERGENCY_PRICE or current_liquidity < MIN_LIQUIDITY) and emergency_brake_month == 0:
            emergency_brake_month = month
    
    # Calculate investor metrics
    tge_tokens = int(PRESALE_BASE_TOKENS * params.tge_percent / 100)
    presale_tge_value = tge_tokens * launch_price
    presale_tge_roi = (presale_tge_value / PRESALE_INVESTMENT - 1) * 100
    
    # Year 1 value (assuming 35% vested by month 12)
    year1_vested_pct = params.tge_percent / 100
    if 12 > params.cliff_months:
        months_vesting = 12 - params.cliff_months
        remaining_pct = (100 - params.tge_percent) / 100
        monthly_vest_rate = remaining_pct / params.vesting_months
        year1_vested_pct += months_vesting * monthly_vest_rate
    
    year1_tokens = int(PRESALE_BASE_TOKENS * min(year1_vested_pct, 1.0))
    presale_year1_value = year1_tokens * month_12_price
    presale_year1_roi = (presale_year1_value / PRESALE_INVESTMENT - 1) * 100
    
    # Scoring: balance price stability, investor fairness, project viability
    # Higher is better
    price_stability_score = (months_above_target / 12) * 30  # Max 30 points
    investor_score = min(presale_year1_roi / 20, 1.0) * 30  # Max 30 points (20% ROI = full score)
    emergency_score = max(0, (12 - emergency_brake_month) / 12) * 40  # Max 40 points (later brake = better)
    
    total_score = price_stability_score + investor_score + emergency_score
    
    return SimulationResult(
        params=params,
        launch_price=launch_price,
        month_3_price=month_3_price,
        month_6_price=month_6_price,
        month_12_price=month_12_price,
        min_price=min_price,
        max_price=max_price,
        emergency_brake_month=emergency_brake_month,
        months_above_target=months_above_target,
        presale_tge_value=presale_tge_value,
        presale_tge_roi=presale_tge_roi,
        presale_year1_roi=presale_year1_roi,
        total_score=total_score
    )


def run_market_scenario(params: HybridParams, scenario_name: str, events: List[Tuple[int, float]]) -> MarketScenarioResult:
    """Test parameters against a specific market scenario."""
    # Run 12-month simulation with market events
    final_price = 0
    min_price = float('inf')
    emergency_brake_month = 0
    months_survived = 12
    
    for month in range(13):
        _, price = calculate_circulating_supply(month, params, events)
        final_price = price
        
        if price < min_price:
            min_price = price
        
        # Check emergency brake
        current_liquidity = LAUNCH_LIQUIDITY
        for event_month, liquidity_change in events:
            if month >= event_month:
                current_liquidity *= (1 + liquidity_change)
        
        if (price < EMERGENCY_PRICE or current_liquidity < MIN_LIQUIDITY) and emergency_brake_month == 0:
            emergency_brake_month = month
            months_survived = month
    
    # Calculate year 1 investor value
    year1_vested_pct = params.tge_percent / 100
    if 12 > params.cliff_months:
        months_vesting = 12 - params.cliff_months
        remaining_pct = (100 - params.tge_percent) / 100
        monthly_vest_rate = remaining_pct / params.vesting_months
        year1_vested_pct += months_vesting * monthly_vest_rate
    
    year1_tokens = int(PRESALE_BASE_TOKENS * min(year1_vested_pct, 1.0))
    presale_year1_value = year1_tokens * final_price
    
    return MarketScenarioResult(
        scenario_name=scenario_name,
        final_price=final_price,
        min_price=min_price,
        emergency_brake_month=emergency_brake_month,
        months_survived=months_survived,
        presale_year1_value=presale_year1_value
    )


# =============================================================================
# MAIN SIMULATION
# =============================================================================

print("\nPhase 1: Testing 100 Parameter Combinations...")
print("-" * 80)

# Generate 100 random parameter combinations
param_combinations = []
for _ in range(100):
    params = HybridParams(
        tge_percent=random.choice([2, 3, 5, 10]),
        cliff_months=random.choice([0, 3, 6, 12]),
        vesting_months=random.choice([24, 36, 48, 60]),
        emission_cap=random.choice([10, 15, 20, 25]),
        staking_apy=random.choice([25, 30, 35, 40]),
        mandatory_stake_pct=random.choice([30, 40, 50, 60])
    )
    param_combinations.append(params)

# Also include our "hybrid model" parameters
hybrid_model_params = HybridParams(
    tge_percent=3,
    cliff_months=3,
    vesting_months=36,
    emission_cap=20,
    staking_apy=40,
    mandatory_stake_pct=50
)
param_combinations.append(hybrid_model_params)

# Run simulations
results = []
for i, params in enumerate(param_combinations):
    if (i + 1) % 20 == 0:
        print(f"  Progress: {i + 1}/101 simulations...")
    result = run_single_simulation(params)
    results.append(result)

# Sort by total score
results.sort(key=lambda x: x.total_score, reverse=True)

print(f"\n✅ Completed 101 simulations")
print(f"\nTop 5 Parameter Combinations:")
print("=" * 80)

for i, result in enumerate(results[:5], 1):
    print(f"\n{i}. Score: {result.total_score:.2f}/100")
    print(f"   {result.params}")
    print(f"   Launch: ${result.launch_price:.4f} | Month 12: ${result.month_12_price:.4f}")
    print(f"   Emergency Brake: Month {result.emergency_brake_month if result.emergency_brake_month > 0 else 'Never'}")
    print(f"   Presale Year 1 ROI: {result.presale_year1_roi:.1f}%")

# Find our hybrid model ranking
hybrid_rank = None
for i, result in enumerate(results, 1):
    if result.params == hybrid_model_params:
        hybrid_rank = i
        break

print(f"\n{'=' * 80}")
print(f"Hybrid Model (3% TGE, 3mo cliff, 36mo vest, 20% cap) Rank: #{hybrid_rank}")
print(f"{'=' * 80}")

# =============================================================================
# PHASE 2: Test Top Performers Against Market Scenarios
# =============================================================================

print("\n\nPhase 2: Testing Top 3 Against 10 Historical Market Scenarios...")
print("=" * 80)

top_3_params = [r.params for r in results[:3]]
if hybrid_model_params not in top_3_params:
    top_3_params.append(hybrid_model_params)

scenario_results = {}

for params in top_3_params:
    param_name = str(params)
    scenario_results[param_name] = []
    
    print(f"\nTesting: {params}")
    print("-" * 80)
    
    for scenario_name, scenario_data in MARKET_SCENARIOS.items():
        events = scenario_data["events"]
        result = run_market_scenario(params, scenario_name, events)
        scenario_results[param_name].append(result)
        
        status = "✅ Survived" if result.emergency_brake_month == 0 else f"🔴 Brake Month {result.emergency_brake_month}"
        print(f"  {scenario_name:20s} | Final: ${result.final_price:.4f} | Min: ${result.min_price:.4f} | {status}")

# =============================================================================
# SUMMARY ANALYSIS
# =============================================================================

print("\n\n" + "=" * 80)
print("FINAL ANALYSIS")
print("=" * 80)

for params in top_3_params:
    param_name = str(params)
    results_list = scenario_results[param_name]
    
    survived_count = sum(1 for r in results_list if r.emergency_brake_month == 0)
    avg_final_price = statistics.mean([r.final_price for r in results_list])
    avg_min_price = statistics.mean([r.min_price for r in results_list])
    avg_brake_month = statistics.mean([r.emergency_brake_month for r in results_list if r.emergency_brake_month > 0] or [12])
    avg_year1_value = statistics.mean([r.presale_year1_value for r in results_list])
    
    print(f"\n{param_name}")
    print(f"  Scenarios Survived: {survived_count}/10")
    print(f"  Avg Final Price: ${avg_final_price:.4f}")
    print(f"  Avg Min Price: ${avg_min_price:.4f}")
    print(f"  Avg Emergency Brake Month: {avg_brake_month:.1f}")
    print(f"  Avg Presale Year 1 Value: ${avg_year1_value:.2f}")

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "timestamp": datetime.now().isoformat(),
    "total_simulations": 101,
    "market_scenarios": 10,
    "top_5_combinations": [
        {
            "rank": i + 1,
            "params": {
                "tge_percent": r.params.tge_percent,
                "cliff_months": r.params.cliff_months,
                "vesting_months": r.params.vesting_months,
                "emission_cap": r.params.emission_cap,
                "staking_apy": r.params.staking_apy,
                "mandatory_stake_pct": r.params.mandatory_stake_pct,
            },
            "score": r.total_score,
            "launch_price": r.launch_price,
            "month_12_price": r.month_12_price,
            "emergency_brake_month": r.emergency_brake_month,
            "presale_year1_roi": r.presale_year1_roi,
        }
        for i, r in enumerate(results[:5])
    ],
    "hybrid_model_rank": hybrid_rank,
    "market_scenario_results": {
        param_name: [
            {
                "scenario": r.scenario_name,
                "final_price": r.final_price,
                "min_price": r.min_price,
                "emergency_brake_month": r.emergency_brake_month,
                "months_survived": r.months_survived,
                "presale_year1_value": r.presale_year1_value,
            }
            for r in results_list
        ]
        for param_name, results_list in scenario_results.items()
    }
}

with open("hybrid_model_validation_results.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Results saved to hybrid_model_validation_results.json")
print("\n" + "=" * 80)

