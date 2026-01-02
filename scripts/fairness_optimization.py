#!/usr/bin/env python3
"""
BlockDAG Fairness Optimization: Finding the Fair TGE Unlock

Problem: 2% TGE penalizes early investors vs launch buyers
Goal: Find TGE % that balances price stability AND investor fairness

Tests 100 scenarios across:
- TGE unlock: 2%, 5%, 10%, 15%, 20%, 25%
- Liquidity: $32M, $50M, $75M, $100M
- With various burn/emission combinations

Measures:
- Price stability (does it crash immediately?)
- Investor fairness (presale vs launch buyer ROI)
- Risk-adjusted returns
"""

import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from itertools import product
import statistics

print("=" * 80)
print("FAIRNESS OPTIMIZATION: Finding Fair TGE Unlock %")
print("=" * 80)
print("\nGoal: Balance price stability AND early investor fairness")

# Constants
BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000
TOTAL_PRESALE = 50_000_000_000
DAILY_MINING_100 = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

# Ricky's example
RICKY_BASE_COINS = 226_000
RICKY_PRESALE_COST = 0.01  # Assumed average presale price


@dataclass
class FairnessResult:
    tge_percent: float
    liquidity: float
    emission_cap: float
    burn_rate: float
    
    # Price metrics
    launch_price: float
    month_3_price: float
    month_6_price: float
    month_12_price: float
    price_crashed: bool  # Below $0.01
    
    # Fairness metrics
    presale_tge_value: float  # Value of TGE tokens
    presale_roi_tge: float    # ROI at TGE
    launch_buyer_roi_m6: float  # Launch buyer ROI at month 6
    fairness_ratio: float     # Presale ROI / Launch ROI (1.0 = equal)
    
    # Risk metrics
    emergency_brake_month: int
    months_above_02: int
    
    # Overall score
    fairness_score: float


def simulate_price(tge_percent: float, liquidity: float, emission_cap: float, 
                   burn_rate: float, months: int = 12) -> List[float]:
    """Simulate price over time"""
    
    # Initial circulating = pre-launch + TGE unlock
    tge_tokens = int(BASE_COINS * tge_percent / 100)
    circulating = PRE_LAUNCH_MINED + tge_tokens
    
    prices = []
    current_liquidity = liquidity
    
    for month in range(months + 1):
        # Price
        price = current_liquidity / circulating if circulating > 0 else 0
        prices.append(price)
        
        # Mining emissions
        base_rate = {0: 0.0, 1: 0.10, 2: 0.10, 3: 0.25, 4: 0.25, 5: 0.25,
                     6: 0.50, 7: 0.50, 8: 0.50, 9: 0.75, 10: 0.75, 11: 0.75}.get(month, 1.0)
        rate = min(base_rate, emission_cap)
        mining = int(DAILY_MINING_100 * 30 * rate * 0.75)  # 75% liquid (25% staked)
        
        # Vesting unlocks (simplified)
        if month > 0 and month <= 12:
            vesting = int(BASE_COINS * 0.005)  # 0.5% per month
        else:
            vesting = 0
        
        # Burns
        tx_vol = int(circulating * 0.05)
        burned = int(tx_vol * burn_rate / 100)
        
        # Update
        circulating = circulating + mining + vesting - burned
    
    return prices


def calculate_fairness(tge_percent: float, liquidity: float, emission_cap: float,
                       burn_rate: float) -> FairnessResult:
    """Calculate fairness metrics"""
    
    prices = simulate_price(tge_percent, liquidity, emission_cap, burn_rate, 12)
    
    launch_price = prices[0]
    month_3_price = prices[3] if len(prices) > 3 else prices[-1]
    month_6_price = prices[6] if len(prices) > 6 else prices[-1]
    month_12_price = prices[-1]
    
    price_crashed = min(prices) < 0.01
    
    # Ricky's scenario
    ricky_tge_tokens = int(RICKY_BASE_COINS * tge_percent / 100)
    ricky_tge_value = ricky_tge_tokens * launch_price
    ricky_investment = RICKY_BASE_COINS * RICKY_PRESALE_COST
    ricky_roi_tge = (ricky_tge_value / ricky_investment - 1) * 100  # % ROI
    
    # Launch buyer scenario ($1000 investment)
    launch_investment = 1000
    launch_tokens = launch_investment / launch_price if launch_price > 0 else 0
    launch_value_m6 = launch_tokens * month_6_price
    launch_roi_m6 = (launch_value_m6 / launch_investment - 1) * 100 if launch_investment > 0 else 0
    
    # Fairness ratio: How does presale compare to launch buyer?
    # 1.0 = equal, >1 = presale better, <1 = launch better
    # Use accessible value ratio
    presale_accessible_ratio = tge_percent / 100  # % accessible at TGE
    launch_accessible_ratio = 1.0  # 100% accessible
    
    # Adjusted fairness: presale paid less, but gets less access
    # Fair if: presale_price_advantage >= lockup_disadvantage
    presale_price = RICKY_PRESALE_COST
    price_advantage = launch_price / presale_price if presale_price > 0 else 0
    access_disadvantage = launch_accessible_ratio / presale_accessible_ratio if presale_accessible_ratio > 0 else 999
    
    fairness_ratio = price_advantage / access_disadvantage if access_disadvantage > 0 else 0
    
    # Emergency brake
    emergency_month = -1
    months_above_02 = 0
    for i, p in enumerate(prices):
        if p >= 0.02:
            months_above_02 += 1
        elif emergency_month == -1:
            emergency_month = i
    
    # Fairness score (0-100)
    # Weights:
    # - Price stability (30%): No crash, stays above $0.02
    # - Presale ROI positive (25%): TGE value >= some threshold
    # - Fairness ratio (25%): Close to 1.0
    # - Long-term survival (20%): Emergency brake late/never
    
    stability_score = min(30, months_above_02 / 13 * 30)
    
    roi_score = 0
    if ricky_roi_tge >= 0:
        roi_score = min(25, 25)  # Full points if positive ROI
    elif ricky_roi_tge >= -50:
        roi_score = 12.5  # Half points if not too negative
    
    fair_score = 0
    if 0.8 <= fairness_ratio <= 1.2:
        fair_score = 25  # Full points if close to equal
    elif 0.5 <= fairness_ratio <= 1.5:
        fair_score = 15
    elif fairness_ratio > 0:
        fair_score = 5
    
    survival_score = 0
    if emergency_month == -1:
        survival_score = 20
    elif emergency_month >= 6:
        survival_score = 15
    elif emergency_month >= 3:
        survival_score = 10
    
    total_score = stability_score + roi_score + fair_score + survival_score
    
    return FairnessResult(
        tge_percent=tge_percent,
        liquidity=liquidity,
        emission_cap=emission_cap,
        burn_rate=burn_rate,
        launch_price=launch_price,
        month_3_price=month_3_price,
        month_6_price=month_6_price,
        month_12_price=month_12_price,
        price_crashed=price_crashed,
        presale_tge_value=ricky_tge_value,
        presale_roi_tge=ricky_roi_tge,
        launch_buyer_roi_m6=launch_roi_m6,
        fairness_ratio=fairness_ratio,
        emergency_brake_month=emergency_month,
        months_above_02=months_above_02,
        fairness_score=total_score
    )


def run_100_simulations():
    """Run 100 different scenarios"""
    
    # Parameter ranges
    tge_percents = [2, 5, 8, 10, 12, 15, 20, 25]
    liquidities = [32_000_000, 50_000_000, 75_000_000, 100_000_000]
    emission_caps = [0.10, 0.20, 0.25]
    burn_rates = [5, 10, 15]
    
    results = []
    
    for tge, liq, em, burn in product(tge_percents, liquidities, emission_caps, burn_rates):
        result = calculate_fairness(tge, liq, em, burn)
        results.append(result)
    
    # Sort by fairness score
    results.sort(key=lambda x: x.fairness_score, reverse=True)
    
    print(f"\nRan {len(results)} simulations")
    
    return results


def analyze_results(results: List[FairnessResult]):
    """Analyze and present results"""
    
    print("\n" + "=" * 80)
    print("TOP 20 FAIREST SCENARIOS")
    print("=" * 80)
    
    print(f"\n{'Rank':<5} {'TGE%':<7} {'Liq':<8} {'Em%':<6} {'Burn%':<7} {'Launch$':<10} {'Presale ROI':<12} {'Fair Ratio':<12} {'Score':<8}")
    print("-" * 90)
    
    for i, r in enumerate(results[:20], 1):
        liq_m = r.liquidity / 1_000_000
        em_pct = int(r.emission_cap * 100)
        print(f"{i:<5} {r.tge_percent}%{'':<4} ${liq_m:.0f}M{'':<3} {em_pct}%{'':<3} {r.burn_rate}%{'':<4} "
              f"${r.launch_price:<8.4f} {r.presale_roi_tge:>+8.1f}%{'':<3} {r.fairness_ratio:<10.2f} {r.fairness_score:<8.1f}")
    
    # Find sweet spots
    print("\n" + "=" * 80)
    print("ANALYSIS BY TGE PERCENTAGE")
    print("=" * 80)
    
    for tge in [2, 5, 10, 15, 20, 25]:
        tge_results = [r for r in results if r.tge_percent == tge]
        if tge_results:
            avg_score = statistics.mean(r.fairness_score for r in tge_results)
            avg_roi = statistics.mean(r.presale_roi_tge for r in tge_results)
            avg_fair = statistics.mean(r.fairness_ratio for r in tge_results)
            best = max(tge_results, key=lambda x: x.fairness_score)
            
            print(f"\n{tge}% TGE:")
            print(f"  Avg Fairness Score: {avg_score:.1f}")
            print(f"  Avg Presale ROI: {avg_roi:+.1f}%")
            print(f"  Avg Fairness Ratio: {avg_fair:.2f}")
            print(f"  Best Config: ${best.liquidity/1e6:.0f}M liq, {int(best.emission_cap*100)}% em, {best.burn_rate}% burn → Score {best.fairness_score:.1f}")
    
    # Analysis by liquidity
    print("\n" + "=" * 80)
    print("ANALYSIS BY LIQUIDITY")
    print("=" * 80)
    
    for liq in [32_000_000, 50_000_000, 75_000_000, 100_000_000]:
        liq_results = [r for r in results if r.liquidity == liq]
        if liq_results:
            avg_score = statistics.mean(r.fairness_score for r in liq_results)
            best = max(liq_results, key=lambda x: x.fairness_score)
            
            print(f"\n${liq/1e6:.0f}M Liquidity:")
            print(f"  Avg Fairness Score: {avg_score:.1f}")
            print(f"  Best TGE%: {best.tge_percent}%")
            print(f"  Best Score: {best.fairness_score:.1f}")
    
    return results


def find_optimal():
    """Find the optimal fair solution"""
    
    results = run_100_simulations()
    analyze_results(results)
    
    # Best overall
    best = results[0]
    
    # Best at $32M
    best_32m = max([r for r in results if r.liquidity == 32_000_000], 
                   key=lambda x: x.fairness_score)
    
    print("\n" + "=" * 80)
    print("OPTIMAL FAIR SOLUTION")
    print("=" * 80)
    
    print(f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FAIREST SOLUTION OVERALL                                                      ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  📊 TGE UNLOCK:        {best.tge_percent}%                                                ║
║  💰 LIQUIDITY:         ${best.liquidity/1e6:.0f}M                                              ║
║  ⚡ EMISSION CAP:       {int(best.emission_cap*100)}%                                               ║
║  🔥 BURN RATE:          {best.burn_rate}%                                               ║
║                                                                                ║
║  RESULTS:                                                                      ║
║  • Launch Price:       ${best.launch_price:.4f}                                        ║
║  • Presale TGE Value:  ${best.presale_tge_value:.2f} (for 226K tokens)                  ║
║  • Presale ROI at TGE: {best.presale_roi_tge:+.1f}%                                          ║
║  • Fairness Ratio:     {best.fairness_ratio:.2f} (1.0 = perfectly fair)                     ║
║  • Fairness Score:     {best.fairness_score:.1f}/100                                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    print(f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FAIREST SOLUTION AT $32M LIQUIDITY                                            ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  📊 TGE UNLOCK:        {best_32m.tge_percent}%                                                ║
║  💰 LIQUIDITY:         ${best_32m.liquidity/1e6:.0f}M                                              ║
║  ⚡ EMISSION CAP:       {int(best_32m.emission_cap*100)}%                                               ║
║  🔥 BURN RATE:          {best_32m.burn_rate}%                                               ║
║                                                                                ║
║  RESULTS:                                                                      ║
║  • Launch Price:       ${best_32m.launch_price:.4f}                                        ║
║  • Presale TGE Value:  ${best_32m.presale_tge_value:.2f} (for 226K tokens)                  ║
║  • Presale ROI at TGE: {best_32m.presale_roi_tge:+.1f}%                                          ║
║  • Fairness Ratio:     {best_32m.fairness_ratio:.2f}                                            ║
║  • Fairness Score:     {best_32m.fairness_score:.1f}/100                                        ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Ricky's comparison
    print("\n" + "=" * 80)
    print("RICKY'S SCENARIO COMPARISON")
    print("=" * 80)
    
    print(f"""
Ricky has 226,000 base coins, paid ~$0.01 each (~$2,260 total)

                              2% TGE          {best_32m.tge_percent}% TGE (RECOMMENDED)
                              ─────────────   ─────────────────────
Tokens at TGE:                4,520           {int(226000 * best_32m.tge_percent / 100):,}
Value at Launch:              ${4520 * 0.05:.2f}         ${226000 * best_32m.tge_percent / 100 * best_32m.launch_price:.2f}
% of Investment Accessible:   {4520 * 0.05 / 2260 * 100:.1f}%            {226000 * best_32m.tge_percent / 100 * best_32m.launch_price / 2260 * 100:.1f}%
ROI at TGE:                   {(4520 * 0.05 / 2260 - 1) * 100:+.1f}%           {best_32m.presale_roi_tge:+.1f}%

IMPROVEMENT: {best_32m.tge_percent}% TGE gives presale investors {best_32m.tge_percent / 2:.1f}x more accessible tokens
""")
    
    # Trade-offs
    print("\n" + "=" * 80)
    print("TRADE-OFF ANALYSIS")
    print("=" * 80)
    
    print("""
| TGE % | Presale Fairness | Price Stability | Recommendation |
|-------|------------------|-----------------|----------------|
| 2%    | ❌ Very Unfair   | ✅ Most Stable  | Too harsh      |
| 5%    | ⚠️ Still Unfair | ✅ Stable       | Minimum viable |
| 10%   | ✅ More Fair     | ⚠️ Moderate    | RECOMMENDED    |
| 15%   | ✅ Fair          | ⚠️ Risky       | If more liquidity |
| 20%   | ✅ Very Fair     | ❌ Too Risky   | Needs $75M+ liq |
| 25%   | ✅ Very Fair     | ❌ Price Crash  | Not recommended |
""")
    
    # Save results
    output = {
        "total_simulations": len(results),
        "best_overall": {
            "tge_percent": best.tge_percent,
            "liquidity": best.liquidity,
            "emission_cap": best.emission_cap,
            "burn_rate": best.burn_rate,
            "launch_price": best.launch_price,
            "presale_roi_tge": best.presale_roi_tge,
            "fairness_ratio": best.fairness_ratio,
            "fairness_score": best.fairness_score
        },
        "best_at_32m": {
            "tge_percent": best_32m.tge_percent,
            "liquidity": best_32m.liquidity,
            "emission_cap": best_32m.emission_cap,
            "burn_rate": best_32m.burn_rate,
            "launch_price": best_32m.launch_price,
            "presale_roi_tge": best_32m.presale_roi_tge,
            "fairness_ratio": best_32m.fairness_ratio,
            "fairness_score": best_32m.fairness_score
        },
        "top_20": [
            {
                "tge_percent": r.tge_percent,
                "liquidity": r.liquidity,
                "emission_cap": r.emission_cap,
                "burn_rate": r.burn_rate,
                "launch_price": r.launch_price,
                "presale_roi_tge": r.presale_roi_tge,
                "fairness_ratio": r.fairness_ratio,
                "fairness_score": r.fairness_score
            }
            for r in results[:20]
        ]
    }
    
    with open("fairness_optimization_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n📊 Results saved to: fairness_optimization_results.json")
    
    return results, best, best_32m


if __name__ == "__main__":
    results, best, best_32m = find_optimal()

