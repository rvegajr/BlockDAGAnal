#!/usr/bin/env python3
"""
BlockDAG Burn & POE Parameter Optimization Simulations

Tests combinations of:
- Burn rates (1%, 2%, 3%, 5%)
- POE auto-stake duration (30, 60, 90 days)
- Post-TGE annual allocation cap (0%, 1%, 2%)

Measures:
- Price stability (variance)
- Final price at month 24
- Net inflation rate
- Emergency brake timing
- Effective circulating supply
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
import math

print("=" * 80)
print("BURN & POE PARAMETER OPTIMIZATION")
print("=" * 80)

# Constants
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
TOTAL_SUPPLY = 50_000_000_000
BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000

# Real miner data
DAILY_MINING_EMISSION_100 = 10_500_000  # At 100% rate
PRE_LAUNCH_MINED = 540_000_000

# POE (X1 mobile) data
X1_ACTIVE_USERS = 50_000  # Migrated users
X1_DAILY_OUTPUT = 20
POE_DAILY_BASE = X1_ACTIVE_USERS * X1_DAILY_OUTPUT  # 1M/day at 100%

# Emission schedule (month -> rate)
EMISSION_RATES = {
    0: 0.0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
    6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75, 12: 1.0
}


@dataclass
class SimulationParams:
    """Parameters to test"""
    burn_rate: float  # % of transactions burned
    poe_autostake_days: int  # Days POE rewards are locked
    post_tge_annual_cap: float  # % of supply that can be minted post-TGE
    name: str


@dataclass
class SimulationResult:
    """Results from simulation"""
    params: SimulationParams
    final_price: float
    min_price: float
    max_price: float
    price_variance: float
    final_circulating: int
    total_burned: int
    net_inflation_rate: float
    emergency_brake_month: int  # -1 if never triggered
    months_above_target: int
    score: float  # Overall score (higher = better)


def get_emission_rate(month: int) -> float:
    """Get emission rate for a given month"""
    return EMISSION_RATES.get(month, 1.0)


def calculate_monthly_transactions(circulating: int, price: float) -> int:
    """Estimate monthly transaction volume (tokens)"""
    # Assume 5% of circulating supply transacts monthly
    # Higher price = more activity
    activity_multiplier = min(2.0, price / 0.03)  # More activity above $0.03
    return int(circulating * 0.05 * activity_multiplier)


def run_simulation(params: SimulationParams, months: int = 24) -> SimulationResult:
    """Run simulation with given parameters"""
    
    # Initial state
    circulating = PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)  # Pre-launch + 2% TGE
    liquidity = LAUNCH_LIQUIDITY
    price = liquidity / circulating
    
    total_burned = 0
    total_poe_staked = 0
    poe_unlock_queue = []  # (unlock_month, amount)
    
    prices = []
    emergency_brake_month = -1
    months_above_target = 0
    
    for month in range(months + 1):
        # Get emission rate
        emission_rate = get_emission_rate(month)
        
        # Mining emissions (hardware)
        hardware_mining = int((DAILY_MINING_EMISSION_100 - POE_DAILY_BASE) * 30 * emission_rate)
        
        # POE emissions (X1 mobile)
        poe_mining = int(POE_DAILY_BASE * 30 * emission_rate)
        
        # POE auto-stake: portion locked based on autostake duration
        poe_stake_rate = min(1.0, params.poe_autostake_days / 90)  # More days = more staked
        poe_staked = int(poe_mining * poe_stake_rate * 0.5)  # 50% of POE auto-staked
        poe_liquid = poe_mining - poe_staked
        
        # Queue POE unlock
        unlock_month = month + (params.poe_autostake_days // 30)
        poe_unlock_queue.append((unlock_month, poe_staked))
        
        # Process POE unlocks
        poe_unlocked = sum(amt for m, amt in poe_unlock_queue if m == month)
        
        # Base coin vesting (simplified)
        if month == 0:
            vesting_unlock = 0  # Already counted in initial
        elif month < 13:
            vesting_unlock = 0  # Cliff
        else:
            # Linear release after cliff
            vesting_unlock = int(BASE_COINS * 0.02)  # ~2% per month after cliff
        
        # Post-TGE allocations (ecosystem, marketing, etc.)
        if params.post_tge_annual_cap > 0 and month > 0:
            annual_allocation = int(TOTAL_SUPPLY * params.post_tge_annual_cap / 100)
            monthly_allocation = annual_allocation // 12
        else:
            monthly_allocation = 0
        
        # Calculate transactions and burns
        transactions = calculate_monthly_transactions(circulating, price)
        burned = int(transactions * params.burn_rate / 100)
        total_burned += burned
        
        # Net supply change
        inflow = hardware_mining + poe_liquid + poe_unlocked + vesting_unlock + monthly_allocation
        outflow = burned
        
        # Update circulating
        circulating = circulating + inflow - outflow
        
        # Calculate price (simple AMM)
        if circulating > 0:
            price = liquidity / circulating
        
        prices.append(price)
        
        # Track metrics
        if price >= TARGET_PRICE:
            months_above_target += 1
        
        # Emergency brake check
        if emergency_brake_month == -1 and price < 0.02:
            emergency_brake_month = month
    
    # Calculate results
    final_price = prices[-1]
    min_price = min(prices)
    max_price = max(prices)
    
    # Price variance (lower = more stable)
    mean_price = sum(prices) / len(prices)
    variance = sum((p - mean_price) ** 2 for p in prices) / len(prices)
    
    # Net inflation rate
    initial_supply = PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)
    net_inflation = (circulating - initial_supply) / initial_supply * 100
    
    # Calculate score (weighted)
    # Higher final price = better (weight: 30)
    # Lower variance = better (weight: 20)
    # Later emergency brake = better (weight: 25)
    # More months above target = better (weight: 15)
    # More burned = better (weight: 10)
    
    price_score = min(100, (final_price / TARGET_PRICE) * 50)
    stability_score = max(0, 100 - variance * 10000)
    brake_score = (emergency_brake_month + 1) / (months + 1) * 100 if emergency_brake_month >= 0 else 100
    target_score = (months_above_target / (months + 1)) * 100
    burn_score = min(100, (total_burned / 1_000_000_000) * 10)  # 10B burned = 100
    
    total_score = (
        price_score * 0.30 +
        stability_score * 0.20 +
        brake_score * 0.25 +
        target_score * 0.15 +
        burn_score * 0.10
    )
    
    return SimulationResult(
        params=params,
        final_price=final_price,
        min_price=min_price,
        max_price=max_price,
        price_variance=variance,
        final_circulating=circulating,
        total_burned=total_burned,
        net_inflation_rate=net_inflation,
        emergency_brake_month=emergency_brake_month,
        months_above_target=months_above_target,
        score=total_score
    )


def main():
    """Run 10 simulations with different parameter combinations"""
    
    # Define 10 test scenarios
    scenarios = [
        SimulationParams(0, 30, 0, "Baseline (No Burns)"),
        SimulationParams(1, 30, 0, "1% Burn, 30d POE"),
        SimulationParams(2, 30, 0, "2% Burn, 30d POE"),
        SimulationParams(3, 30, 0, "3% Burn, 30d POE"),
        SimulationParams(5, 30, 0, "5% Burn, 30d POE"),
        SimulationParams(2, 60, 0, "2% Burn, 60d POE"),
        SimulationParams(2, 90, 0, "2% Burn, 90d POE"),
        SimulationParams(2, 90, 1, "2% Burn, 90d POE, 1% TGE Cap"),
        SimulationParams(3, 90, 0, "3% Burn, 90d POE"),
        SimulationParams(5, 90, 0, "5% Burn, 90d POE (Aggressive)"),
    ]
    
    results = []
    
    print("\n" + "=" * 80)
    print("RUNNING 10 SIMULATIONS")
    print("=" * 80)
    
    for i, params in enumerate(scenarios, 1):
        result = run_simulation(params)
        results.append(result)
        
        brake_str = f"Month {result.emergency_brake_month}" if result.emergency_brake_month >= 0 else "Never"
        
        print(f"\n{i}. {params.name}")
        print(f"   Final Price: ${result.final_price:.6f}")
        print(f"   Total Burned: {result.total_burned:,}")
        print(f"   Emergency Brake: {brake_str}")
        print(f"   Score: {result.score:.1f}/100")
    
    # Sort by score
    results.sort(key=lambda x: x.score, reverse=True)
    
    print("\n" + "=" * 80)
    print("RESULTS RANKED BY SCORE")
    print("=" * 80)
    
    print(f"\n{'Rank':<5} {'Scenario':<35} {'Final $':<12} {'Burned':<15} {'Brake':<10} {'Score':<8}")
    print("-" * 90)
    
    for i, r in enumerate(results, 1):
        brake_str = f"M{r.emergency_brake_month}" if r.emergency_brake_month >= 0 else "Never"
        print(f"{i:<5} {r.params.name:<35} ${r.final_price:<10.6f} {r.total_burned:>12,} {brake_str:<10} {r.score:<8.1f}")
    
    # Top 3 analysis
    print("\n" + "=" * 80)
    print("TOP 3 RECOMMENDATIONS")
    print("=" * 80)
    
    for i, r in enumerate(results[:3], 1):
        print(f"\n🏆 #{i}: {r.params.name}")
        print(f"   Parameters:")
        print(f"   • Burn Rate: {r.params.burn_rate}%")
        print(f"   • POE Auto-Stake: {r.params.poe_autostake_days} days")
        print(f"   • Post-TGE Cap: {r.params.post_tge_annual_cap}%")
        print(f"   Results:")
        print(f"   • Final Price: ${r.final_price:.6f}")
        print(f"   • Price Range: ${r.min_price:.6f} - ${r.max_price:.6f}")
        print(f"   • Total Burned: {r.total_burned:,} BDAG")
        print(f"   • Net Inflation: {r.net_inflation_rate:.1f}%")
        print(f"   • Emergency Brake: {'Month ' + str(r.emergency_brake_month) if r.emergency_brake_month >= 0 else 'Never triggered'}")
        print(f"   • Score: {r.score:.1f}/100")
    
    # Best parameters
    best = results[0]
    print("\n" + "=" * 80)
    print("RECOMMENDED PARAMETERS")
    print("=" * 80)
    print(f"""
Based on 10 simulations, the OPTIMAL parameters are:

┌─────────────────────────────────────────────────────┐
│  BURN RATE:           {best.params.burn_rate}%                          │
│  POE AUTO-STAKE:      {best.params.poe_autostake_days} days                        │
│  POST-TGE CAP:        {best.params.post_tge_annual_cap}%                          │
└─────────────────────────────────────────────────────┘

Why this combination works:
1. Burn rate of {best.params.burn_rate}% removes {best.total_burned:,} tokens over 24 months
2. {best.params.poe_autostake_days}-day POE stake reduces immediate sell pressure from mobile miners
3. {best.params.post_tge_annual_cap}% post-TGE cap limits dilution

Expected outcomes:
• Final price at month 24: ${best.final_price:.6f}
• Total supply burned: {best.total_burned:,} BDAG
• Net inflation: {best.net_inflation_rate:.1f}%
• Emergency brake: {'Month ' + str(best.emergency_brake_month) if best.emergency_brake_month >= 0 else 'Never triggered'}
""")
    
    # Save results
    output = {
        "simulations": [
            {
                "name": r.params.name,
                "burn_rate": r.params.burn_rate,
                "poe_autostake_days": r.params.poe_autostake_days,
                "post_tge_cap": r.params.post_tge_annual_cap,
                "final_price": r.final_price,
                "min_price": r.min_price,
                "max_price": r.max_price,
                "total_burned": r.total_burned,
                "net_inflation": r.net_inflation_rate,
                "emergency_brake_month": r.emergency_brake_month,
                "score": r.score
            }
            for r in results
        ],
        "recommendation": {
            "burn_rate": best.params.burn_rate,
            "poe_autostake_days": best.params.poe_autostake_days,
            "post_tge_cap": best.params.post_tge_annual_cap
        }
    }
    
    with open("burn_poe_simulation_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("📊 Results saved to: burn_poe_simulation_results.json")


if __name__ == "__main__":
    main()

