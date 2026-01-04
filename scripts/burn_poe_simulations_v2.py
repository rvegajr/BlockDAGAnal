#!/usr/bin/env python3
"""
BlockDAG Burn & POE Parameter Optimization v2

Key insight from v1: Burns alone don't solve the problem.
Mining emissions (~10.5M/day) overwhelm burn capacity.

V2 tests: Burns + Emission Cap Reductions

Tests combinations of:
- Burn rates (2%, 5%, 10%)
- Max emission cap (50%, 75%, 100%)
- POE auto-stake (30, 90 days)
"""

import json
from typing import Dict, List
from dataclasses import dataclass

print("=" * 80)
print("BURN + EMISSION CAP OPTIMIZATION (v2)")
print("=" * 80)
print("\nKey insight: Burns alone don't work. Testing burns + emission caps.")

# Constants
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
TOTAL_SUPPLY = 50_000_000_000
BASE_COINS = 17_000_000_000

# Real miner data
DAILY_MINING_100 = 10_500_000  # At 100% rate
PRE_LAUNCH_MINED = 540_000_000

# Emission schedule (month -> rate)
def get_capped_emission(month: int, max_cap: float) -> float:
    """Get emission rate with a maximum cap"""
    base_rates = {
        0: 0.0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
        6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75
    }
    base = base_rates.get(month, 1.0)
    return min(base, max_cap)


@dataclass
class SimParams:
    burn_rate: float
    emission_cap: float  # Max emission rate (0.5 = 50%)
    poe_stake_days: int
    name: str


@dataclass
class SimResult:
    params: SimParams
    final_price: float
    min_price: float
    total_burned: int
    emergency_month: int
    months_above_2c: int  # Months above $0.02 (emergency threshold)
    net_inflation: float
    score: float


def run_sim(params: SimParams, months: int = 24) -> SimResult:
    """Run simulation"""
    
    # Initial state
    circulating = PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)
    liquidity = LAUNCH_LIQUIDITY
    price = liquidity / circulating
    
    total_burned = 0
    prices = []
    emergency_month = -1
    months_above_2c = 0
    
    for month in range(months + 1):
        # Get CAPPED emission rate
        emission_rate = get_capped_emission(month, params.emission_cap)
        
        # Mining emissions
        mining = int(DAILY_MINING_100 * 30 * emission_rate)
        
        # POE locked portion
        poe_locked_rate = params.poe_stake_days / 90 * 0.5
        mining_liquid = int(mining * (1 - poe_locked_rate))
        
        # Vesting (simplified)
        if month == 0:
            vesting = 0
        elif month < 13:
            vesting = 0
        else:
            vesting = int(BASE_COINS * 0.015)
        
        # Burns
        tx_volume = int(circulating * 0.05)
        burned = int(tx_volume * params.burn_rate / 100)
        total_burned += burned
        
        # Update circulating
        circulating = circulating + mining_liquid + vesting - burned
        
        # Price
        if circulating > 0:
            price = liquidity / circulating
        
        prices.append(price)
        
        # Track
        if price >= 0.02:
            months_above_2c += 1
        
        if emergency_month == -1 and price < 0.02:
            emergency_month = month
    
    # Results
    initial = PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)
    net_inflation = (circulating - initial) / initial * 100
    
    # Score: prioritize staying above $0.02
    price_score = min(100, (prices[-1] / 0.02) * 30)
    stability_score = (months_above_2c / (months + 1)) * 40
    brake_score = ((emergency_month + 1) / (months + 1)) * 20 if emergency_month >= 0 else 20
    burn_score = min(10, total_burned / 100_000_000)
    
    total_score = price_score + stability_score + brake_score + burn_score
    
    return SimResult(
        params=params,
        final_price=prices[-1],
        min_price=min(prices),
        total_burned=total_burned,
        emergency_month=emergency_month,
        months_above_2c=months_above_2c,
        net_inflation=net_inflation,
        score=total_score
    )


def main():
    # 10 scenarios testing burns + emission caps
    scenarios = [
        SimParams(0, 1.0, 30, "Baseline (No Burns, 100% Emission)"),
        SimParams(5, 1.0, 90, "5% Burn, 100% Emission"),
        SimParams(5, 0.75, 90, "5% Burn, 75% Emission Cap"),
        SimParams(5, 0.50, 90, "5% Burn, 50% Emission Cap"),
        SimParams(10, 0.50, 90, "10% Burn, 50% Emission Cap"),
        SimParams(5, 0.35, 90, "5% Burn, 35% Emission Cap"),
        SimParams(10, 0.35, 90, "10% Burn, 35% Emission Cap"),
        SimParams(5, 0.25, 90, "5% Burn, 25% Emission Cap"),
        SimParams(10, 0.25, 90, "10% Burn, 25% Emission Cap"),
        SimParams(15, 0.25, 90, "15% Burn, 25% Emission Cap (Aggressive)"),
    ]
    
    results = []
    
    print("\n" + "=" * 80)
    print("RUNNING 10 SIMULATIONS")
    print("=" * 80)
    
    for i, params in enumerate(scenarios, 1):
        result = run_sim(params)
        results.append(result)
        
        brake_str = f"Month {result.emergency_month}" if result.emergency_month >= 0 else "Never"
        cap_pct = int(params.emission_cap * 100)
        
        print(f"\n{i}. {params.name}")
        print(f"   Emission Cap: {cap_pct}% | Burn: {params.burn_rate}%")
        print(f"   Final Price: ${result.final_price:.6f}")
        print(f"   Months Above $0.02: {result.months_above_2c}/25")
        print(f"   Emergency Brake: {brake_str}")
        print(f"   Score: {result.score:.1f}/100")
    
    # Sort by score
    results.sort(key=lambda x: x.score, reverse=True)
    
    print("\n" + "=" * 80)
    print("RESULTS RANKED BY SCORE")
    print("=" * 80)
    
    print(f"\n{'Rank':<5} {'Scenario':<40} {'Final $':<12} {'>$0.02':<8} {'Brake':<10} {'Score':<8}")
    print("-" * 95)
    
    for i, r in enumerate(results, 1):
        brake_str = f"M{r.emergency_month}" if r.emergency_month >= 0 else "Never"
        print(f"{i:<5} {r.params.name:<40} ${r.final_price:<10.6f} {r.months_above_2c:<8} {brake_str:<10} {r.score:<8.1f}")
    
    # Top 3
    print("\n" + "=" * 80)
    print("TOP 3 RECOMMENDATIONS")
    print("=" * 80)
    
    for i, r in enumerate(results[:3], 1):
        cap_pct = int(r.params.emission_cap * 100)
        print(f"\n🏆 #{i}: {r.params.name}")
        print(f"   ┌────────────────────────────────────────┐")
        print(f"   │  Burn Rate:     {r.params.burn_rate}%                      │")
        print(f"   │  Emission Cap:  {cap_pct}%                     │")
        print(f"   │  POE Stake:     {r.params.poe_stake_days} days                   │")
        print(f"   └────────────────────────────────────────┘")
        print(f"   Results:")
        print(f"   • Final Price: ${r.final_price:.6f}")
        print(f"   • Min Price: ${r.min_price:.6f}")
        print(f"   • Months Above $0.02: {r.months_above_2c}/25")
        print(f"   • Total Burned: {r.total_burned:,} BDAG")
        print(f"   • Net Inflation: {r.net_inflation:.1f}%")
        print(f"   • Emergency Brake: {'Month ' + str(r.emergency_month) if r.emergency_month >= 0 else 'NEVER'}")
    
    # Best
    best = results[0]
    cap_pct = int(best.params.emission_cap * 100)
    
    print("\n" + "=" * 80)
    print("FINAL RECOMMENDATION")
    print("=" * 80)
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  OPTIMAL PARAMETERS FOR BURN + EMISSION CONTROL              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📉 BURN RATE:           {best.params.burn_rate}%                                  ║
║  ⚡ EMISSION CAP:         {cap_pct}% (max {int(DAILY_MINING_100 * best.params.emission_cap):,}/day)       ║
║  🔒 POE AUTO-STAKE:       {best.params.poe_stake_days} days                              ║
║  🚫 POST-TGE ALLOCATION:  0%                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  EXPECTED OUTCOMES:                                          ║
║  • Final Price (M24):     ${best.final_price:.6f}                         ║
║  • Months Above $0.02:    {best.months_above_2c}/25                              ║
║  • Total Burned:          {best.total_burned:,} BDAG                      ║
║  • Emergency Brake:       {'Month ' + str(best.emergency_month) if best.emergency_month >= 0 else 'NEVER triggered'}               ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    print("""
KEY INSIGHT:
═══════════════════════════════════════════════════════════════
Burns ALONE cannot fix the problem.

At 100% emission rate: 10.5M tokens/day = 315M/month
At 5% burn rate: ~3-5M tokens burned/month

NET RESULT: Still +310M tokens/month → Price drops

SOLUTION: Burns + Emission Caps work together:
• Reduce inflow (emission cap)
• Increase outflow (burns)
• Lock supply (POE stake)
═══════════════════════════════════════════════════════════════
""")
    
    # Save
    output = {
        "simulations": [
            {
                "name": r.params.name,
                "burn_rate": r.params.burn_rate,
                "emission_cap": r.params.emission_cap,
                "poe_stake_days": r.params.poe_stake_days,
                "final_price": r.final_price,
                "min_price": r.min_price,
                "total_burned": r.total_burned,
                "months_above_2c": r.months_above_2c,
                "emergency_month": r.emergency_month,
                "score": r.score
            }
            for r in results
        ],
        "recommendation": {
            "burn_rate": best.params.burn_rate,
            "emission_cap": best.params.emission_cap,
            "poe_stake_days": best.params.poe_stake_days,
            "post_tge_cap": 0
        }
    }
    
    with open("burn_emission_optimization_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("📊 Results saved to: burn_emission_optimization_results.json")


if __name__ == "__main__":
    main()


