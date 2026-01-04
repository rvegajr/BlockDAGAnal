#!/usr/bin/env python3
"""
HYBRID TOKENOMICS COMPARISON: Solvency-Anchored, State-Driven Model
====================================================================
Compares the new Hybrid Tokenomics model against existing models:
1. Original Model (2% TGE, 12mo cliff, 60mo vest)
2. Hybrid Model (3% TGE, 3mo cliff, 36mo vest)
3. Protocol v2.6 (3% TGE, 3mo cliff, 21mo vest)
4. Hybrid B (State-Driven with Time Orientation)
5. NEW: Hybrid Tokenomics - Solvency-Anchored, State-Driven

Runs 100 simulations + 10 choppy market scenarios
Analyzes investor returns and survivability
"""

import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
import statistics
from datetime import datetime
from collections import deque

print("=" * 80)
print("HYBRID TOKENOMICS COMPARISON: Solvency-Anchored, State-Driven")
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
    has_price_gate: bool
    model_type: str  # "time_based", "state_driven", "hybrid"
    # New Hybrid Tokenomics specific params
    global_monthly_cap: Optional[float] = None  # Max % of supply per month (all sources)
    state_driven_release: bool = False  # If True, releases depend on market state
    bonus_option: Optional[str] = None  # "A", "B", "C" for bonus token options
    mining_lock_ratio: Optional[float] = None  # % of mining rewards locked

# Original Model
ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=False,
    model_type="time_based"
)

# Hybrid Model (current)
HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=True,
    model_type="hybrid"
)

# Protocol v2.6
PROTOCOL_V26_MODEL = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,
    staking_apy=40.0,
    mandatory_stake_pct=0.0,
    has_price_gate=True,
    model_type="time_based"
)

# Hybrid B (State-Driven with Time Orientation)
HYBRID_B_MODEL = ModelParams(
    name="Hybrid B",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=50.0,
    has_price_gate=True,
    model_type="hybrid",
    global_monthly_cap=1.0,  # 0.3-1.0% max per month
    state_driven_release=True
)

# NEW: Hybrid Tokenomics - Solvency-Anchored, State-Driven
HYBRID_TOKENOMICS_MODEL = ModelParams(
    name="Hybrid Tokenomics (Solvency-Anchored)",
    tge_percent=3.0,
    cliff_months=3,  # 90 days = 3 months
    vesting_months=36,  # State-driven, no fixed timeline
    emission_cap=0.20,
    staking_apy=40.0,
    mandatory_stake_pct=60.0,  # Higher staking requirement
    has_price_gate=True,
    model_type="state_driven",
    global_monthly_cap=1.0,  # 0.3-1.0% max per month (all sources)
    state_driven_release=True,
    bonus_option="B",  # State-Gated Release & Supply Control
    mining_lock_ratio=0.70  # ≥70% locked in Phase 1
)

# =============================================================================
# MARKET SCENARIOS (10 Choppy Situations)
# =============================================================================

MARKET_SCENARIOS = {
    "normal": {
        "name": "Normal Market Conditions",
        "description": "Stable market, no major crashes",
        "events": []
    },
    "may_2021_crash": {
        "name": "May 2021-Style Crash",
        "description": "60% liquidity drop at month 2",
        "events": [(2, -0.60)]  # Month 2: 60% drop
    },
    "ftx_collapse": {
        "name": "FTX Collapse",
        "description": "70% liquidity drop at month 3",
        "events": [(3, -0.70)]  # Month 3: 70% drop
    },
    "covid_black_swan": {
        "name": "COVID Black Swan",
        "description": "80% liquidity drop at month 1",
        "events": [(1, -0.80)]  # Month 1: 80% drop
    },
    "gradual_bear": {
        "name": "Gradual Bear Market",
        "description": "50% drop over 12 months",
        "events": [(i, -0.05) for i in range(2, 13)]  # -5% per month
    },
    "bull_then_crash": {
        "name": "Bull Run Then Crash",
        "description": "+100% for 6 months, then -70%",
        "events": [(i, 0.15) for i in range(2, 7)] + [(7, -0.70)]
    },
    "high_volatility": {
        "name": "High Volatility",
        "description": "Multiple 30-40% swings",
        "events": [(2, -0.30), (4, 0.40), (6, -0.40), (8, 0.30), (10, -0.30)]
    },
    "stable_growth": {
        "name": "Stable Growth",
        "description": "+20% liquidity over 12 months",
        "events": [(i, 0.02) for i in range(2, 13)]  # +2% per month
    },
    "early_crash_recovery": {
        "name": "Early Crash with Recovery",
        "description": "-50% at month 2, recovery by month 6",
        "events": [(2, -0.50), (4, 0.25), (6, 0.50)]
    },
    "multiple_crashes": {
        "name": "Multiple Crashes",
        "description": "Crashes at months 2, 6, 12",
        "events": [(2, -0.40), (6, -0.40), (12, -0.40)]
    }
}

# =============================================================================
# STATE-DRIVEN LOGIC
# =============================================================================

def calculate_30_day_vwap(prices: deque, month: int) -> float:
    """Calculate 30-day VWAP (simplified as average of last 30 days)."""
    if len(prices) == 0:
        return TARGET_PRICE
    # Simplified: average of last month's prices
    recent_prices = list(prices)[-min(30, len(prices)):]
    return statistics.mean(recent_prices) if recent_prices else TARGET_PRICE

def check_market_state(price: float, vwap: float, liquidity: float, 
                      price_trend: List[float]) -> Dict[str, bool]:
    """Determine market state for state-driven releases."""
    # Price trend (negative if declining)
    price_change = (price - price_trend[0]) / price_trend[0] if price_trend else 0
    
    # Liquidity trend (simplified)
    liquidity_stable = liquidity >= LAUNCH_LIQUIDITY * 0.9
    
    return {
        "price_stable": abs(price - vwap) / vwap < 0.20,  # Within 20% of VWAP
        "price_positive": price_change >= -0.10,  # Not down more than 10%
        "liquidity_stable": liquidity_stable,
        "can_release": price >= EMERGENCY_PRICE and liquidity >= MIN_LIQUIDITY
    }

def calculate_state_driven_vesting(month: int, params: ModelParams, 
                                   market_state: Dict[str, bool],
                                   current_circulating: int) -> int:
    """Calculate vesting release based on market state."""
    if month == 0:
        return int(BASE_COINS * params.tge_percent / 100)
    
    # Phase 0: TGE only (months 0-3)
    if month <= params.cliff_months:
        return int(BASE_COINS * params.tge_percent / 100)
    
    # Phase 1: Observation (months 3-6, no vesting)
    if month <= 6:
        return int(BASE_COINS * params.tge_percent / 100)
    
    # Phase 2: State-driven release (from month 6+)
    if not market_state["can_release"]:
        # No release if market conditions don't allow
        return int(BASE_COINS * params.tge_percent / 100)
    
    # Calculate max monthly release based on global cap
    max_monthly_tokens = int(BASE_COINS * params.global_monthly_cap / 100) if params.global_monthly_cap else 0
    
    # Determine release rate based on market state
    if market_state["price_stable"] and market_state["liquidity_stable"]:
        # Early/Stable state: ≤0.3% per month
        release_rate = 0.003
    elif market_state["price_positive"]:
        # Accelerated state: ≤0.7% per month
        release_rate = 0.007
    else:
        # Negative trend: 0% release
        release_rate = 0.0
    
    monthly_release = int(BASE_COINS * release_rate)
    
    # Apply global cap
    if params.global_monthly_cap:
        monthly_release = min(monthly_release, max_monthly_tokens)
    
    # Cumulative release
    cumulative_release = int(BASE_COINS * params.tge_percent / 100)
    for m in range(params.cliff_months + 1, month + 1):
        if m > 6:  # Only after Phase 1
            cumulative_release += monthly_release
    
    return min(cumulative_release, BASE_COINS)

# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def calculate_circulating_supply(month: int, params: ModelParams, 
                                liquidity_events: List[Tuple[int, float]],
                                price_history: deque = None,
                                liquidity_history: List[float] = None) -> Tuple[int, float, Dict]:
    """Calculate circulating supply and price at a given month."""
    if price_history is None:
        price_history = deque(maxlen=100)
    if liquidity_history is None:
        liquidity_history = []
    
    # Calculate current liquidity
    current_liquidity = LAUNCH_LIQUIDITY
    for event_month, liquidity_change in liquidity_events:
        if month >= event_month:
            current_liquidity *= (1 + liquidity_change)
    liquidity_history.append(current_liquidity)
    
    # TGE tokens
    tge_tokens = int(BASE_COINS * params.tge_percent / 100)
    
    # Vesting release
    if params.state_driven_release:
        # State-driven vesting
        if len(price_history) > 0:
            vwap = calculate_30_day_vwap(price_history, month)
            price_trend = list(price_history)[-min(10, len(price_history)):] if len(price_history) > 0 else [TARGET_PRICE]
            market_state = check_market_state(
                price_history[-1] if price_history else TARGET_PRICE,
                vwap,
                current_liquidity,
                price_trend
            )
        else:
            market_state = {"can_release": True, "price_stable": True, 
                          "price_positive": True, "liquidity_stable": True}
        
        vested_tokens = calculate_state_driven_vesting(month, params, market_state, 0)
    else:
        # Time-based vesting
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
        else:
            vested_tokens = tge_tokens
    
    # Price gate check
    if params.has_price_gate and params.model_type == "time_based":
        # For time-based models, check price gate after calculating
        pass
    
    # Mining emissions
    mining_tokens = 0
    if month > 0:
        # Ramp up: 20% month 1, 35% month 2, 50% month 3, 80% month 6, 100% month 12
        ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
        current_rate = 0.20
        for m, rate in sorted(ramp_rates.items()):
            if month >= m:
                current_rate = rate
        
        daily_emission = DAILY_MINING_MAX * current_rate
        capped_daily = min(daily_emission, DAILY_MINING_MAX * params.emission_cap)
        
        # Cumulative mining
        for m in range(1, month + 1):
            m_rate = 0.20
            for mr, r in sorted(ramp_rates.items()):
                if m >= mr:
                    m_rate = r
            m_daily = min(DAILY_MINING_MAX * m_rate, DAILY_MINING_MAX * params.emission_cap)
            
            # Apply mining lock ratio for Hybrid Tokenomics
            if params.mining_lock_ratio and m <= 6:  # Phase 1
                m_daily *= (1 - params.mining_lock_ratio)  # Only (1-lock_ratio) is liquid
            
            mining_tokens += int(m_daily * 30)
    
    # Pre-launch mined (migrated over time)
    pre_launch_tokens = 0
    if month > 0:
        immediate = int(PRE_LAUNCH_MINED * 0.30)
        gradual = int(PRE_LAUNCH_MINED * 0.50)
        monthly_gradual = gradual / 6
        pre_launch_tokens = immediate + int(min(month, 6) * monthly_gradual)
    
    # Bonus tokens (simplified - only for Hybrid Tokenomics)
    bonus_tokens = 0
    if params.bonus_option == "B" and month > 6:  # Option B: State-Gated Release
        # Only release if all conditions met
        if len(price_history) > 0:
            vwap = calculate_30_day_vwap(price_history, month)
            market_state = check_market_state(
                price_history[-1] if price_history else TARGET_PRICE,
                vwap,
                current_liquidity,
                list(price_history)[-min(10, len(price_history)):] if price_history else [TARGET_PRICE]
            )
            if market_state["can_release"] and market_state["price_stable"]:
                # Max 0.05-0.10% per month
                bonus_release = int(BONUS_COINS * 0.00075)  # ~0.075% per month
                bonus_tokens = min(bonus_release * (month - 6), BONUS_COINS)
    
    # Staking removes from circulating
    total_circulating = vested_tokens + mining_tokens + pre_launch_tokens + bonus_tokens
    
    # Adjust staking based on market conditions
    stake_pct = params.mandatory_stake_pct
    if current_liquidity < LAUNCH_LIQUIDITY * 0.7:
        stake_pct = min(stake_pct + 10, 70)  # Increase staking in bad markets
    
    staked_tokens = int(total_circulating * stake_pct / 100)
    effective_circulating = total_circulating - staked_tokens
    
    # Calculate price
    if effective_circulating > 0:
        price = current_liquidity / effective_circulating
    else:
        price = TARGET_PRICE
    
    price_history.append(price)
    
    # Price gate check (for time-based models)
    if params.has_price_gate and params.model_type == "time_based" and params.name == "Protocol v2.6":
        if price < 0.05 and month > params.cliff_months:
            # Recalculate without vesting
            vested_tokens = tge_tokens
            total_circulating = vested_tokens + mining_tokens + pre_launch_tokens
            staked_tokens = int(total_circulating * stake_pct / 100)
            effective_circulating = total_circulating - staked_tokens
            if effective_circulating > 0:
                price = current_liquidity / effective_circulating
            price_history[-1] = price
    
    return effective_circulating, price, {
        "vested": vested_tokens,
        "mining": mining_tokens,
        "bonus": bonus_tokens,
        "staked": staked_tokens,
        "liquidity": current_liquidity
    }

def run_single_simulation(params: ModelParams, market_type: str, 
                          scenario_events: List[Tuple[int, float]] = None,
                          simulation_id: int = 0) -> Dict:
    """Run a single simulation with given parameters."""
    if scenario_events is None:
        scenario_events = []
    
    price_history = deque(maxlen=100)
    liquidity_history = []
    
    prices = []
    investor_values = []
    emergency_brake_triggered = False
    emergency_brake_month = 0
    monthly_details = []
    
    for month in range(13):
        _, price, details = calculate_circulating_supply(
            month, params, scenario_events, price_history, liquidity_history
        )
        prices.append(price)
        
        # Calculate investor value at this month
        if params.state_driven_release:
            # For state-driven, calculate vested percentage
            if month == 0:
                vested_pct = params.tge_percent / 100
            elif month <= params.cliff_months:
                vested_pct = params.tge_percent / 100
            elif month <= 6:
                vested_pct = params.tge_percent / 100  # Phase 1: no vesting
            else:
                # Phase 2: state-driven
                cumulative_vested = details["vested"]
                vested_pct = cumulative_vested / BASE_COINS
        else:
            # Time-based
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
        
        monthly_details.append({
            "month": month,
            "price": price,
            "circulating": details["vested"] + details["mining"] + details["bonus"],
            "investor_value": investor_value,
            "vested_pct": vested_pct * 100
        })
        
        # Check emergency brake
        if params.has_price_gate:
            current_liquidity = liquidity_history[-1] if liquidity_history else LAUNCH_LIQUIDITY
            
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
        "monthly_details": monthly_details
    }

# =============================================================================
# LIQUIDITY LEVELS TO TEST
# =============================================================================

LIQUIDITY_LEVELS = [20_000_000, 32_000_000, 50_000_000, 75_000_000, 100_000_000]

# =============================================================================
# MAIN SIMULATION
# =============================================================================

print("\nPhase 1: Running 100 Simulations per Model...")
print("=" * 80)

models = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26_MODEL, HYBRID_B_MODEL, HYBRID_TOKENOMICS_MODEL]
market_types = ["bull", "bear", "normal", "volatile"]
simulations_per_market = 25  # 25 × 4 = 100 total per model

results = {}
liquidity_results = {}  # Store results by liquidity level

for model in models:
    print(f"\nTesting {model.name}...")
    model_results = []
    
    for market_type in market_types:
        for sim_id in range(simulations_per_market):
            # Generate random market events for this simulation
            if market_type == "bull":
                events = [(i, random.uniform(0.05, 0.10)) for i in [2, 4, 6, 8, 10, 12]]
            elif market_type == "bear":
                events = [(i, random.uniform(-0.10, -0.05)) for i in [2, 4, 6, 8, 10, 12]]
            elif market_type == "volatile":
                events = [(i, random.choice([-1, 1]) * random.uniform(0.15, 0.30)) 
                         for i in [2, 4, 6, 8, 10, 12]]
            else:  # normal
                events = [(i, random.uniform(-0.03, 0.03)) for i in [2, 4, 6, 8, 10, 12]]
            
            result = run_single_simulation(model, market_type, events, sim_id)
            result["model"] = model.name
            model_results.append(result)
    
    results[model.name] = model_results

# =============================================================================
# PHASE 1B: Test Across Different Liquidity Levels
# =============================================================================

print("\n\nPhase 1B: Testing Hybrid Tokenomics Across Liquidity Levels...")
print("=" * 80)

for liquidity_level in LIQUIDITY_LEVELS:
    print(f"\nTesting at ${liquidity_level/1e6:.0f}M liquidity...")
    
    # Temporarily override launch liquidity
    original_liquidity = LAUNCH_LIQUIDITY
    globals()['LAUNCH_LIQUIDITY'] = liquidity_level
    
    # Test Hybrid Tokenomics model at this liquidity level
    model_results = []
    for market_type in market_types:
        for sim_id in range(simulations_per_market):
            if market_type == "bull":
                events = [(i, random.uniform(0.05, 0.10)) for i in [2, 4, 6, 8, 10, 12]]
            elif market_type == "bear":
                events = [(i, random.uniform(-0.10, -0.05)) for i in [2, 4, 6, 8, 10, 12]]
            elif market_type == "volatile":
                events = [(i, random.choice([-1, 1]) * random.uniform(0.15, 0.30)) 
                         for i in [2, 4, 6, 8, 10, 12]]
            else:
                events = [(i, random.uniform(-0.03, 0.03)) for i in [2, 4, 6, 8, 10, 12]]
            
            result = run_single_simulation(HYBRID_TOKENOMICS_MODEL, market_type, events, sim_id)
            result["liquidity_level"] = liquidity_level
            model_results.append(result)
    
    # Test against choppy scenarios at this liquidity level
    scenario_results_at_liquidity = {}
    for scenario_key, scenario_data in MARKET_SCENARIOS.items():
        events = scenario_data.get("events", [])
        result = run_single_simulation(HYBRID_TOKENOMICS_MODEL, scenario_key, events, 0)
        result["liquidity_level"] = liquidity_level
        scenario_results_at_liquidity[scenario_key] = result
    
    liquidity_results[liquidity_level] = {
        "simulations": model_results,
        "scenarios": scenario_results_at_liquidity
    }
    
    # Restore original liquidity
    globals()['LAUNCH_LIQUIDITY'] = original_liquidity
    
    # Print summary
    avg_roi = statistics.mean([r["month_12_roi"] for r in model_results])
    avg_value = statistics.mean([r["month_12_value"] for r in model_results])
    brake_rate = sum(1 for r in model_results if r["emergency_brake_triggered"]) / len(model_results) * 100
    survived_scenarios = sum(1 for s in scenario_results_at_liquidity.values() 
                            if not s["emergency_brake_triggered"])
    
    print(f"  Avg ROI: {avg_roi:.1f}% | Avg Value: ${avg_value:.2f} | "
          f"Brake Rate: {brake_rate:.1f}% | Scenarios Survived: {survived_scenarios}/10")

print("\n✅ Phase 1 Complete: 100 simulations per model")
print("=" * 80)

# =============================================================================
# PHASE 2: Test Against 10 Choppy Market Scenarios
# =============================================================================

print("\n\nPhase 2: Testing Against 10 Choppy Market Scenarios...")
print("=" * 80)

scenario_results = {}

for model in models:
    model_name = model.name
    scenario_results[model_name] = {}
    
    print(f"\nTesting {model_name}...")
    print("-" * 80)
    
    for scenario_key, scenario_data in MARKET_SCENARIOS.items():
        events = scenario_data.get("events", [])
        result = run_single_simulation(model, scenario_key, events, 0)
        
        scenario_results[model_name][scenario_key] = result
        
        status = "✅ Survived" if not result['emergency_brake_triggered'] else f"🔴 Brake Month {result['emergency_brake_month']}"
        print(f"  {scenario_data['name']:30s} | Final: ${result['month_12_price']:.4f} | "
              f"ROI: {result['month_12_roi']:+.1f}% | {status}")

# =============================================================================
# ANALYSIS
# =============================================================================

print("\n\n" + "=" * 80)
print("INVESTOR RETURNS ANALYSIS")
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
            "month_12_roi_avg": statistics.mean([r["month_12_roi"] for r in market_results]),
            "month_12_roi_median": statistics.median([r["month_12_roi"] for r in market_results]),
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
    
    # Scenario analysis
    scenario_performance = {}
    for scenario_key in MARKET_SCENARIOS.keys():
        if scenario_key in scenario_results[model_name]:
            scenario_result = scenario_results[model_name][scenario_key]
            scenario_performance[scenario_key] = {
                "month_12_roi": scenario_result["month_12_roi"],
                "month_12_value": scenario_result["month_12_value"],
                "emergency_brake": scenario_result["emergency_brake_triggered"],
                "final_price": scenario_result["month_12_price"]
            }
    
    comparison[model_name]["scenario_performance"] = scenario_performance

# Print comparison tables
print("\n📊 TGE ROI Comparison (% Return)")
print("-" * 80)
print(f"{'Model':<35} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<35}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        roi = comparison[model_name]["by_market"][market_type]["tge_roi_avg"]
        row += f"{roi:>12.1f}%"
    overall = comparison[model_name]["overall_tge_roi"]
    row += f"{overall:>12.1f}%"
    print(row)

print("\n📊 Month 12 ROI Comparison (% Return)")
print("-" * 80)
print(f"{'Model':<35} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<35}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        roi = comparison[model_name]["by_market"][market_type]["month_12_roi_avg"]
        row += f"{roi:>12.1f}%"
    overall = comparison[model_name]["overall_month_12_roi"]
    row += f"{overall:>12.1f}%"
    print(row)

print("\n💰 Month 12 Value Comparison ($9K Investment)")
print("-" * 80)
print(f"{'Model':<35} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<35}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        value = comparison[model_name]["by_market"][market_type]["month_12_value_avg"]
        row += f"${value:>11.2f}"
    overall = comparison[model_name]["overall_month_12_value"]
    row += f"${overall:>11.2f}"
    print(row)

print("\n🛡️ Emergency Brake Activation Rate")
print("-" * 80)
print(f"{'Model':<35} {'Bull':>12} {'Bear':>12} {'Normal':>12} {'Volatile':>12} {'Overall':>12}")
print("-" * 80)
for model_name in [m.name for m in models]:
    row = f"{model_name:<35}"
    for market_type in ["bull", "bear", "normal", "volatile"]:
        rate = comparison[model_name]["by_market"][market_type]["emergency_brake_rate"]
        row += f"{rate:>11.1f}%"
    overall = comparison[model_name]["overall_emergency_brake_rate"]
    row += f"{overall:>11.1f}%"
    print(row)

# =============================================================================
# SCENARIO ANALYSIS
# =============================================================================

print("\n\n" + "=" * 80)
print("10 CHOPPY MARKET SCENARIOS ANALYSIS")
print("=" * 80)

for scenario_key, scenario_data in MARKET_SCENARIOS.items():
    print(f"\n{scenario_data['name']}:")
    print("-" * 80)
    print(f"{'Model':<35} {'Final Price':>15} {'Month 12 ROI':>15} {'Month 12 Value':>15} {'Brake':>10}")
    print("-" * 80)
    
    scenario_rois = []
    for model_name in [m.name for m in models]:
        if scenario_key in comparison[model_name]["scenario_performance"]:
            perf = comparison[model_name]["scenario_performance"][scenario_key]
            brake = "Yes" if perf["emergency_brake"] else "No"
            print(f"{model_name:<35} ${perf['final_price']:>14.4f} "
                  f"{perf['month_12_roi']:>14.1f}% ${perf['month_12_value']:>14.2f} "
                  f"{brake:>10}")
            scenario_rois.append((model_name, perf["month_12_roi"]))
    
    # Find best performer
    if scenario_rois:
        best_model = max(scenario_rois, key=lambda x: x[1])
        print(f"\n  🏆 Best Performer: {best_model[0]} ({best_model[1]:+.1f}% ROI)")

# =============================================================================
# OVERALL WINNER ANALYSIS
# =============================================================================

print("\n\n" + "=" * 80)
print("OVERALL WINNER: Best Model for Investors")
print("=" * 80)

# Score each model
model_scores = {}
for model_name in [m.name for m in models]:
    score = 0
    
    # ROI score (higher is better)
    roi_score = comparison[model_name]["overall_month_12_roi"]
    score += roi_score * 0.4  # 40% weight
    
    # Value score (higher is better)
    value_score = comparison[model_name]["overall_month_12_value"] / 1000  # Normalize
    score += value_score * 0.3  # 30% weight
    
    # Survival score (lower brake rate is better)
    brake_rate = comparison[model_name]["overall_emergency_brake_rate"]
    survival_score = (100 - brake_rate) * 10  # Convert to score
    score += survival_score * 0.3  # 30% weight
    
    # Scenario performance
    scenario_avg_roi = statistics.mean([
        comparison[model_name]["scenario_performance"][s]["month_12_roi"]
        for s in MARKET_SCENARIOS.keys()
        if s in comparison[model_name]["scenario_performance"]
    ])
    score += scenario_avg_roi * 0.1  # 10% weight
    
    model_scores[model_name] = score

# Sort by score
sorted_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)

print("\nModel Rankings (Higher Score = Better for Investors):")
print("-" * 80)
for i, (model_name, score) in enumerate(sorted_models, 1):
    print(f"{i}. {model_name:<35} Score: {score:.2f}")
    print(f"   Month 12 ROI: {comparison[model_name]['overall_month_12_roi']:+.1f}%")
    print(f"   Month 12 Value: ${comparison[model_name]['overall_month_12_value']:.2f}")
    print(f"   Emergency Brake Rate: {comparison[model_name]['overall_emergency_brake_rate']:.1f}%")
    print()

# =============================================================================
# SAVE RESULTS
# =============================================================================

# =============================================================================
# LIQUIDITY LEVEL ANALYSIS
# =============================================================================

print("\n\n" + "=" * 80)
print("LIQUIDITY LEVEL ANALYSIS: Hybrid Tokenomics Performance")
print("=" * 80)

liquidity_analysis = {}
for liquidity_level in LIQUIDITY_LEVELS:
    model_results = liquidity_results[liquidity_level]["simulations"]
    scenario_results_at_liquidity = liquidity_results[liquidity_level]["scenarios"]
    
    avg_roi = statistics.mean([r["month_12_roi"] for r in model_results])
    avg_value = statistics.mean([r["month_12_value"] for r in model_results])
    brake_rate = sum(1 for r in model_results if r["emergency_brake_triggered"]) / len(model_results) * 100
    survived_scenarios = sum(1 for s in scenario_results_at_liquidity.values() 
                            if not s["emergency_brake_triggered"])
    avg_final_price = statistics.mean([r["month_12_price"] for r in model_results])
    
    liquidity_analysis[liquidity_level] = {
        "avg_roi": avg_roi,
        "avg_value": avg_value,
        "brake_rate": brake_rate,
        "survived_scenarios": survived_scenarios,
        "avg_final_price": avg_final_price,
        "scenario_performance": {
            k: {
                "month_12_roi": v["month_12_roi"],
                "month_12_value": v["month_12_value"],
                "emergency_brake": v["emergency_brake_triggered"],
                "final_price": v["month_12_price"]
            }
            for k, v in scenario_results_at_liquidity.items()
        }
    }
    
    print(f"\n${liquidity_level/1e6:.0f}M Liquidity:")
    print(f"  Avg ROI: {avg_roi:.1f}%")
    print(f"  Avg Value: ${avg_value:.2f}")
    print(f"  Brake Rate: {brake_rate:.1f}%")
    print(f"  Scenarios Survived: {survived_scenarios}/10")
    print(f"  Avg Final Price: ${avg_final_price:.4f}")

output = {
    "timestamp": datetime.now().isoformat(),
    "models_tested": [m.name for m in models],
    "simulations_per_model": 100,
    "market_conditions": market_types,
    "scenarios_tested": list(MARKET_SCENARIOS.keys()),
    "liquidity_levels_tested": LIQUIDITY_LEVELS,
    "comparison": comparison,
    "model_scores": model_scores,
    "rankings": sorted_models,
    "liquidity_analysis": liquidity_analysis,
    "raw_results": {k: v[:10] for k, v in results.items()},  # Sample of raw results
    "scenario_results": scenario_results
}

with open("hybrid_tokenomics_comparison_results.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print(f"\n✅ Results saved to hybrid_tokenomics_comparison_results.json")
print("\n" + "=" * 80)

