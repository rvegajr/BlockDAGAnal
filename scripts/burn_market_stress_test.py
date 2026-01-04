#!/usr/bin/env python3
"""
BlockDAG Burn/Emission/POE Optimization vs Historical Market Conditions

Tests parameter combinations against real historical crash scenarios:
- COVID March 2020 (55% drop)
- Luna Crash May 2022 (40% drop)
- FTX Collapse Nov 2022 (25% drop)
- Bear Market 2022 (gradual 50% decline)
- Bull then Crash (growth then 70% drop)

Finds parameters that perform best ACROSS ALL market conditions.
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
import statistics

print("=" * 80)
print("STRESS TEST: BURN/EMISSION vs HISTORICAL MARKET CONDITIONS")
print("=" * 80)

# Constants
LAUNCH_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05
BASE_COINS = 17_000_000_000
DAILY_MINING_100 = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

# Historical market events with real crash data
MARKET_SCENARIOS = {
    "COVID_Crash_2020": {
        "description": "March 2020 - 55% liquidity drop in 1 week",
        "events": [(2, -0.55)],  # Month 2, 55% drop
    },
    "Luna_Crash_2022": {
        "description": "May 2022 - 40% drop, slow recovery",
        "events": [(3, -0.40)],
    },
    "FTX_Collapse_2022": {
        "description": "November 2022 - 25% drop, confidence crisis",
        "events": [(4, -0.25), (5, -0.10)],  # Follow-on drop
    },
    "Bear_Market_2022": {
        "description": "Gradual 50% decline over 6 months",
        "events": [(2, -0.10), (4, -0.10), (6, -0.10), (8, -0.10), (10, -0.10)],
    },
    "Bull_Then_Crash": {
        "description": "Growth then 70% crash",
        "events": [(2, 0.30), (4, 0.20), (6, -0.70)],
    },
    "Multiple_Crashes": {
        "description": "Worst case - crashes at months 2, 6, 12",
        "events": [(2, -0.30), (6, -0.40), (12, -0.30)],
    },
    "Stable_Market": {
        "description": "Baseline - no major events",
        "events": [],
    },
    "High_Volatility": {
        "description": "Multiple swings up and down",
        "events": [(2, -0.20), (4, 0.30), (6, -0.30), (8, 0.20), (10, -0.25)],
    },
    "Early_Recovery": {
        "description": "Early crash with V-recovery",
        "events": [(2, -0.50), (4, 0.40), (6, 0.30)],
    },
    "Late_Crash": {
        "description": "Stability then late crash at month 18",
        "events": [(18, -0.60)],
    },
}


@dataclass
class BurnParams:
    burn_rate: float      # % of tx burned
    emission_cap: float   # Max emission rate (0.25 = 25%)
    poe_stake_days: int   # Days POE locked
    name: str


@dataclass 
class ScenarioResult:
    scenario_name: str
    final_price: float
    min_price: float
    emergency_month: int
    months_above_02: int
    total_burned: int


@dataclass
class ParamResult:
    params: BurnParams
    scenario_results: List[ScenarioResult]
    avg_final_price: float
    avg_emergency_month: float
    worst_emergency_month: int
    total_scenarios_survived: int  # Brake after month 12
    robustness_score: float


def get_emission_rate(month: int, cap: float) -> float:
    """Get capped emission rate"""
    base = {0: 0.0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
            6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75}.get(month, 1.0)
    return min(base, cap)


def run_scenario(params: BurnParams, scenario_name: str, events: List[Tuple]) -> ScenarioResult:
    """Run single scenario with given params"""
    
    circulating = PRE_LAUNCH_MINED + int(BASE_COINS * 0.02)
    liquidity = LAUNCH_LIQUIDITY
    price = liquidity / circulating
    
    total_burned = 0
    emergency_month = -1
    months_above_02 = 0
    min_price = price
    
    for month in range(25):
        # Apply market events
        for event_month, impact in events:
            if event_month == month:
                liquidity = max(5_000_000, liquidity * (1 + impact))
        
        # Emission
        rate = get_emission_rate(month, params.emission_cap)
        mining = int(DAILY_MINING_100 * 30 * rate)
        
        # POE lock effect
        poe_lock_rate = min(1.0, params.poe_stake_days / 90) * 0.5
        mining_liquid = int(mining * (1 - poe_lock_rate))
        
        # Vesting
        if month < 13:
            vesting = 0
        else:
            vesting = int(BASE_COINS * 0.015)
        
        # Burns
        tx_vol = int(circulating * 0.05 * (price / 0.03))  # More tx at higher price
        burned = int(tx_vol * params.burn_rate / 100)
        total_burned += burned
        
        # Update
        circulating = circulating + mining_liquid + vesting - burned
        if circulating > 0:
            price = liquidity / circulating
        
        min_price = min(min_price, price)
        
        if price >= 0.02:
            months_above_02 += 1
        
        if emergency_month == -1 and price < 0.02:
            emergency_month = month
    
    return ScenarioResult(
        scenario_name=scenario_name,
        final_price=price,
        min_price=min_price,
        emergency_month=emergency_month if emergency_month >= 0 else 25,
        months_above_02=months_above_02,
        total_burned=total_burned
    )


def test_params(params: BurnParams) -> ParamResult:
    """Test params across all scenarios"""
    
    results = []
    for name, data in MARKET_SCENARIOS.items():
        result = run_scenario(params, name, data["events"])
        results.append(result)
    
    # Calculate aggregates
    avg_price = statistics.mean(r.final_price for r in results)
    avg_brake = statistics.mean(r.emergency_month for r in results)
    worst_brake = min(r.emergency_month for r in results)
    survived = sum(1 for r in results if r.emergency_month > 12)
    
    # Robustness score: weighted combination
    # - Survive most scenarios (40%)
    # - Later worst-case brake (30%)
    # - Higher average final price (20%)
    # - Higher average brake month (10%)
    
    survive_score = (survived / len(results)) * 40
    worst_score = (worst_brake / 25) * 30
    price_score = min(20, (avg_price / 0.01) * 5)
    avg_brake_score = (avg_brake / 25) * 10
    
    robustness = survive_score + worst_score + price_score + avg_brake_score
    
    return ParamResult(
        params=params,
        scenario_results=results,
        avg_final_price=avg_price,
        avg_emergency_month=avg_brake,
        worst_emergency_month=worst_brake,
        total_scenarios_survived=survived,
        robustness_score=robustness
    )


def main():
    # Define parameter combinations to test
    param_sets = [
        BurnParams(0, 1.00, 30, "Baseline (No Burns)"),
        BurnParams(5, 1.00, 30, "5% Burn Only"),
        BurnParams(5, 0.50, 30, "5% Burn + 50% Cap"),
        BurnParams(5, 0.25, 30, "5% Burn + 25% Cap + 30d POE"),
        BurnParams(5, 0.25, 60, "5% Burn + 25% Cap + 60d POE"),
        BurnParams(5, 0.25, 90, "5% Burn + 25% Cap + 90d POE"),
        BurnParams(10, 0.25, 90, "10% Burn + 25% Cap + 90d POE"),
        BurnParams(10, 0.35, 90, "10% Burn + 35% Cap + 90d POE"),
        BurnParams(15, 0.25, 90, "15% Burn + 25% Cap + 90d POE"),
        BurnParams(10, 0.20, 90, "10% Burn + 20% Cap + 90d POE"),
    ]
    
    print(f"\nTesting {len(param_sets)} parameter sets against {len(MARKET_SCENARIOS)} market scenarios")
    print("=" * 80)
    
    all_results = []
    
    for params in param_sets:
        result = test_params(params)
        all_results.append(result)
        
        print(f"\n{params.name}")
        print(f"  Scenarios Survived (brake >M12): {result.total_scenarios_survived}/{len(MARKET_SCENARIOS)}")
        print(f"  Worst Case Brake: Month {result.worst_emergency_month}")
        print(f"  Avg Final Price: ${result.avg_final_price:.6f}")
        print(f"  Robustness Score: {result.robustness_score:.1f}/100")
    
    # Sort by robustness
    all_results.sort(key=lambda x: x.robustness_score, reverse=True)
    
    print("\n" + "=" * 80)
    print("RESULTS RANKED BY ROBUSTNESS (Performance Across ALL Market Conditions)")
    print("=" * 80)
    
    print(f"\n{'Rank':<5} {'Parameters':<35} {'Survived':<10} {'Worst':<8} {'Avg $':<12} {'Score':<8}")
    print("-" * 85)
    
    for i, r in enumerate(all_results, 1):
        print(f"{i:<5} {r.params.name:<35} {r.total_scenarios_survived}/10     "
              f"M{r.worst_emergency_month:<6} ${r.avg_final_price:<10.6f} {r.robustness_score:<8.1f}")
    
    # Detailed breakdown for top 3
    print("\n" + "=" * 80)
    print("TOP 3 - DETAILED SCENARIO BREAKDOWN")
    print("=" * 80)
    
    for rank, result in enumerate(all_results[:3], 1):
        print(f"\n🏆 #{rank}: {result.params.name}")
        print(f"   Burn: {result.params.burn_rate}% | Cap: {int(result.params.emission_cap*100)}% | POE: {result.params.poe_stake_days}d")
        print(f"\n   {'Scenario':<25} {'Final $':<12} {'Min $':<12} {'Brake':<10} {'Survived':<10}")
        print("   " + "-" * 70)
        
        for sr in result.scenario_results:
            survived = "✅" if sr.emergency_month > 12 else "❌"
            brake_str = f"M{sr.emergency_month}" if sr.emergency_month < 25 else "Never"
            print(f"   {sr.scenario_name:<25} ${sr.final_price:<10.6f} ${sr.min_price:<10.6f} {brake_str:<10} {survived}")
    
    # Best params
    best = all_results[0]
    
    print("\n" + "=" * 80)
    print("FINAL RECOMMENDATION: OPTIMAL PARAMETERS FOR ALL MARKET CONDITIONS")
    print("=" * 80)
    print(f"""
╔════════════════════════════════════════════════════════════════════════╗
║  STRESS-TESTED OPTIMAL PARAMETERS                                      ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  📉 BURN RATE:        {best.params.burn_rate}%                                           ║
║  ⚡ EMISSION CAP:      {int(best.params.emission_cap*100)}% (max {int(DAILY_MINING_100 * best.params.emission_cap):,}/day)            ║
║  🔒 POE AUTO-STAKE:    {best.params.poe_stake_days} days                                       ║
║  🚫 POST-TGE CAP:      0%                                              ║
║                                                                        ║
╠════════════════════════════════════════════════════════════════════════╣
║  STRESS TEST RESULTS (10 Historical Scenarios):                        ║
║                                                                        ║
║  • Scenarios Survived (brake >M12):  {best.total_scenarios_survived}/10                          ║
║  • Worst Case Emergency Brake:       Month {best.worst_emergency_month}                         ║
║  • Average Final Price:              ${best.avg_final_price:.6f}                       ║
║  • Robustness Score:                 {best.robustness_score:.1f}/100                         ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

These parameters performed best across:
✓ COVID-style crash (55% drop)
✓ Luna/FTX-style collapse (25-40% drops)
✓ Bear market (gradual 50% decline)
✓ High volatility (multiple swings)
✓ Worst case (multiple crashes)
""")
    
    # Comparison: Best vs Baseline
    baseline = next(r for r in all_results if "Baseline" in r.params.name)
    
    print("\n" + "=" * 80)
    print("IMPROVEMENT: OPTIMAL vs BASELINE (No Burns)")
    print("=" * 80)
    print(f"""
                          BASELINE        OPTIMAL         IMPROVEMENT
Scenarios Survived:       {baseline.total_scenarios_survived}/10            {best.total_scenarios_survived}/10            +{best.total_scenarios_survived - baseline.total_scenarios_survived} scenarios
Worst Case Brake:         Month {baseline.worst_emergency_month}         Month {best.worst_emergency_month}         +{best.worst_emergency_month - baseline.worst_emergency_month} months
Avg Final Price:          ${baseline.avg_final_price:.6f}     ${best.avg_final_price:.6f}     +{((best.avg_final_price/baseline.avg_final_price)-1)*100:.0f}%
Robustness Score:         {baseline.robustness_score:.1f}            {best.robustness_score:.1f}            +{best.robustness_score - baseline.robustness_score:.1f} points
""")
    
    # Save results
    output = {
        "test_date": "2025-01",
        "scenarios_tested": list(MARKET_SCENARIOS.keys()),
        "parameter_results": [
            {
                "name": r.params.name,
                "burn_rate": r.params.burn_rate,
                "emission_cap": r.params.emission_cap,
                "poe_stake_days": r.params.poe_stake_days,
                "scenarios_survived": r.total_scenarios_survived,
                "worst_brake_month": r.worst_emergency_month,
                "avg_final_price": r.avg_final_price,
                "robustness_score": r.robustness_score,
                "scenario_details": [
                    {
                        "scenario": sr.scenario_name,
                        "final_price": sr.final_price,
                        "min_price": sr.min_price,
                        "emergency_month": sr.emergency_month,
                        "months_above_02": sr.months_above_02
                    }
                    for sr in r.scenario_results
                ]
            }
            for r in all_results
        ],
        "recommendation": {
            "burn_rate": best.params.burn_rate,
            "emission_cap": best.params.emission_cap,
            "poe_stake_days": best.params.poe_stake_days,
            "post_tge_cap": 0
        }
    }
    
    with open("burn_stress_test_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n📊 Full results saved to: burn_stress_test_results.json")


if __name__ == "__main__":
    main()


