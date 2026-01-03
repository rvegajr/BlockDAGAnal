#!/usr/bin/env python3
"""
OPTIMAL LIQUIDITY ANALYSIS
==========================
Finding the best liquidity level for BlockDAG launch.

Parameters tested:
- Liquidity: $10M, $20M, $32M, $50M, $75M, $100M
- Exchanges: 3, 5, 10 (affects liquidity distribution and slippage)
- TGE %: 2%, 5%, 10%, 15%, 20%
- Market conditions: Normal, Bear, Bull, Volatile

Metrics:
- Price stability
- Presale investor fairness (ROI)
- New buyer opportunity
- Project sustainability
- Exchange depth quality
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict
from itertools import product
import statistics
from datetime import datetime

print("=" * 80)
print("OPTIMAL LIQUIDITY ANALYSIS - Finding the Sweet Spot")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000  # 17B
BONUS_COINS = 33_000_000_000  # 33B (but may be utility)
TOTAL_PRESALE = 50_000_000_000
DAILY_MINING = 10_500_000  # 10.5M/day
PRE_LAUNCH_MINED = 540_000_000  # 540M testnet

# Reference investor
PRESALE_INVESTMENT = 9000  # $9K invested
PRESALE_PRICE = 0.01  # Average presale price
PRESALE_TOKENS = int(PRESALE_INVESTMENT / PRESALE_PRICE)  # 900K tokens
PRESALE_BASE_TOKENS = PRESALE_TOKENS // 2  # 450K base

# Thresholds
EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY = 10_000_000

# =============================================================================
# PARAMETERS TO TEST
# =============================================================================

LIQUIDITY_LEVELS = [10_000_000, 20_000_000, 32_000_000, 50_000_000, 75_000_000, 100_000_000]
EXCHANGE_COUNTS = [3, 5, 10]
TGE_PERCENTAGES = [2, 5, 10, 15, 20]
MARKET_CONDITIONS = ["normal", "bear", "bull", "volatile"]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SimulationResult:
    # Input parameters
    liquidity: int
    exchanges: int
    tge_percent: int
    market_condition: str
    
    # Calculated values
    per_exchange_liquidity: float
    tge_tokens: int
    launch_price: float
    
    # Price trajectory
    month_1_price: float
    month_3_price: float
    month_6_price: float
    month_12_price: float
    min_price: float
    max_price: float
    
    # Stability metrics
    emergency_brake_month: int  # 0 = never triggered
    price_volatility: float
    months_above_target: int  # Months above $0.02
    
    # Fairness metrics
    presale_tge_value: float
    presale_tge_roi: float  # % return at TGE
    presale_year1_roi: float  # % return after 1 year
    new_buyer_month6_roi: float  # New buyer ROI after 6 months
    fairness_ratio: float  # Presale ROI / New buyer ROI
    
    # Exchange quality
    slippage_1k: float  # Slippage for $1K trade
    slippage_10k: float  # Slippage for $10K trade
    slippage_100k: float  # Slippage for $100K trade
    depth_score: float  # 0-100
    
    # Overall scores
    presale_score: float  # 0-100
    new_buyer_score: float  # 0-100
    project_score: float  # 0-100
    overall_score: float  # Weighted average


def calculate_slippage(trade_size: float, pool_liquidity: float) -> float:
    """Calculate price slippage for AMM trade (x*y=k model)"""
    if pool_liquidity <= 0:
        return 100.0
    # Simplified constant product formula
    impact = (trade_size / pool_liquidity) * 100
    return min(impact * 2, 100)  # Double for both sides of trade


def simulate_scenario(liquidity: int, exchanges: int, tge_percent: int, 
                      market_condition: str) -> SimulationResult:
    """Run a single simulation scenario"""
    
    # Calculate initial values
    per_exchange = liquidity / exchanges
    tge_tokens = int(BASE_COINS * tge_percent / 100)
    initial_circulating = PRE_LAUNCH_MINED + tge_tokens
    launch_price = liquidity / initial_circulating
    
    # Market condition multipliers
    market_mults = {
        "normal": {"m1": 1.0, "m3": 0.95, "m6": 0.85, "m12": 0.70},
        "bear": {"m1": 0.8, "m3": 0.5, "m6": 0.4, "m12": 0.3},
        "bull": {"m1": 1.2, "m3": 1.5, "m6": 1.3, "m12": 1.0},
        "volatile": {"m1": 0.7, "m3": 1.2, "m6": 0.6, "m12": 0.8}
    }
    mults = market_mults[market_condition]
    
    # Simulate price trajectory
    prices = [launch_price]
    circulating = initial_circulating
    current_liq = liquidity
    emergency_month = 0
    
    for month in range(1, 13):
        # Add mining emissions (50% staked)
        monthly_mining = DAILY_MINING * 30 * 0.5
        circulating += monthly_mining
        
        # Add vesting if past cliff (simplified)
        if month > 6 and tge_percent < 100:
            monthly_vest = BASE_COINS * 0.02  # 2% per month
            circulating += monthly_vest
        
        # Apply market condition
        if month == 1:
            current_liq = liquidity * mults["m1"]
        elif month == 3:
            current_liq = liquidity * mults["m3"]
        elif month == 6:
            current_liq = liquidity * mults["m6"]
        elif month == 12:
            current_liq = liquidity * mults["m12"]
        
        # Calculate price
        price = current_liq / circulating if circulating > 0 else 0
        prices.append(price)
        
        # Check emergency brake
        if emergency_month == 0 and (price < EMERGENCY_PRICE or current_liq < MIN_LIQUIDITY):
            emergency_month = month
    
    # Extract key prices
    month_1 = prices[1] if len(prices) > 1 else launch_price
    month_3 = prices[3] if len(prices) > 3 else launch_price
    month_6 = prices[6] if len(prices) > 6 else launch_price
    month_12 = prices[12] if len(prices) > 12 else launch_price
    
    # Calculate metrics
    min_price = min(prices)
    max_price = max(prices)
    volatility = statistics.stdev(prices) / statistics.mean(prices) if len(prices) > 1 else 0
    months_above = sum(1 for p in prices if p >= 0.02)
    
    # Presale investor metrics
    presale_tge_tokens = int(PRESALE_BASE_TOKENS * tge_percent / 100)
    presale_tge_value = presale_tge_tokens * launch_price
    presale_tge_roi = ((presale_tge_value / PRESALE_INVESTMENT) - 1) * 100
    presale_year1_value = PRESALE_BASE_TOKENS * month_12 * 0.3  # ~30% vested by year 1
    presale_year1_roi = ((presale_year1_value / PRESALE_INVESTMENT) - 1) * 100
    
    # New buyer metrics (buys $9K at launch)
    new_buyer_tokens = PRESALE_INVESTMENT / launch_price if launch_price > 0 else 0
    new_buyer_m6_value = new_buyer_tokens * month_6
    new_buyer_m6_roi = ((new_buyer_m6_value / PRESALE_INVESTMENT) - 1) * 100 if PRESALE_INVESTMENT > 0 else 0
    
    # Fairness ratio (1.0 = equal treatment)
    if new_buyer_m6_roi != 0:
        fairness = presale_year1_roi / new_buyer_m6_roi if new_buyer_m6_roi > 0 else 0
    else:
        fairness = 0
    fairness = max(0, min(2, fairness))  # Cap at 0-2 range
    
    # Exchange depth metrics
    slippage_1k = calculate_slippage(1000, per_exchange)
    slippage_10k = calculate_slippage(10000, per_exchange)
    slippage_100k = calculate_slippage(100000, per_exchange)
    
    # Depth score (lower slippage = higher score)
    depth_score = max(0, 100 - (slippage_1k + slippage_10k / 2 + slippage_100k / 4))
    
    # Calculate component scores
    
    # Presale score: TGE value + long-term potential + fairness
    presale_score = 0
    if presale_tge_value > 0:
        presale_score += min(30, (presale_tge_value / 1000) * 10)  # TGE value (max 30)
    if presale_year1_roi > -90:
        presale_score += min(40, (presale_year1_roi + 100) / 5)  # Year 1 ROI (max 40)
    if emergency_month == 0 or emergency_month > 6:
        presale_score += 30  # No early brake (30 points)
    
    # New buyer score: Entry price + growth potential
    new_buyer_score = 0
    if launch_price < 0.10:
        new_buyer_score += 30  # Accessible entry price
    if new_buyer_m6_roi > -50:
        new_buyer_score += min(40, (new_buyer_m6_roi + 50))  # 6-month potential
    if months_above > 6:
        new_buyer_score += 30  # Price stability
    
    # Project score: Sustainability + depth + stability
    project_score = 0
    project_score += depth_score * 0.3  # Exchange depth (max 30)
    project_score += min(30, months_above * 2.5)  # Price above threshold (max 30)
    if emergency_month == 0:
        project_score += 40  # No emergency brake
    elif emergency_month > 6:
        project_score += 20  # Late brake
    
    # Overall score (weighted)
    overall = (presale_score * 0.35 + new_buyer_score * 0.30 + project_score * 0.35)
    
    return SimulationResult(
        liquidity=liquidity,
        exchanges=exchanges,
        tge_percent=tge_percent,
        market_condition=market_condition,
        per_exchange_liquidity=per_exchange,
        tge_tokens=tge_tokens,
        launch_price=launch_price,
        month_1_price=month_1,
        month_3_price=month_3,
        month_6_price=month_6,
        month_12_price=month_12,
        min_price=min_price,
        max_price=max_price,
        emergency_brake_month=emergency_month,
        price_volatility=volatility,
        months_above_target=months_above,
        presale_tge_value=presale_tge_value,
        presale_tge_roi=presale_tge_roi,
        presale_year1_roi=presale_year1_roi,
        new_buyer_month6_roi=new_buyer_m6_roi,
        fairness_ratio=fairness,
        slippage_1k=slippage_1k,
        slippage_10k=slippage_10k,
        slippage_100k=slippage_100k,
        depth_score=depth_score,
        presale_score=presale_score,
        new_buyer_score=new_buyer_score,
        project_score=project_score,
        overall_score=overall
    )


# =============================================================================
# RUN ALL SIMULATIONS
# =============================================================================

print(f"\nRunning simulations across:")
print(f"  Liquidity levels: {[f'${l/1e6:.0f}M' for l in LIQUIDITY_LEVELS]}")
print(f"  Exchange counts:  {EXCHANGE_COUNTS}")
print(f"  TGE percentages:  {TGE_PERCENTAGES}")
print(f"  Market conditions: {MARKET_CONDITIONS}")

total_combinations = len(LIQUIDITY_LEVELS) * len(EXCHANGE_COUNTS) * len(TGE_PERCENTAGES) * len(MARKET_CONDITIONS)
print(f"\nTotal simulations: {total_combinations}")

all_results: List[SimulationResult] = []

for liquidity, exchanges, tge, market in product(LIQUIDITY_LEVELS, EXCHANGE_COUNTS, 
                                                   TGE_PERCENTAGES, MARKET_CONDITIONS):
    result = simulate_scenario(liquidity, exchanges, tge, market)
    all_results.append(result)

print(f"\n✅ Completed {len(all_results)} simulations")

# =============================================================================
# ANALYSIS BY LIQUIDITY LEVEL
# =============================================================================

print("\n" + "=" * 80)
print("ANALYSIS BY LIQUIDITY LEVEL")
print("=" * 80)

liquidity_summary = {}

for liq in LIQUIDITY_LEVELS:
    liq_results = [r for r in all_results if r.liquidity == liq]
    
    avg_overall = statistics.mean([r.overall_score for r in liq_results])
    avg_presale = statistics.mean([r.presale_score for r in liq_results])
    avg_newbuyer = statistics.mean([r.new_buyer_score for r in liq_results])
    avg_project = statistics.mean([r.project_score for r in liq_results])
    
    best = max(liq_results, key=lambda x: x.overall_score)
    worst = min(liq_results, key=lambda x: x.overall_score)
    
    no_brake = sum(1 for r in liq_results if r.emergency_brake_month == 0)
    
    liquidity_summary[liq] = {
        "avg_overall": avg_overall,
        "avg_presale": avg_presale,
        "avg_newbuyer": avg_newbuyer,
        "avg_project": avg_project,
        "best_scenario": asdict(best),
        "worst_scenario": asdict(worst),
        "no_brake_count": no_brake,
        "no_brake_pct": (no_brake / len(liq_results)) * 100
    }
    
    print(f"\n${liq/1e6:.0f}M LIQUIDITY:")
    print(f"  Average Overall Score: {avg_overall:.1f}/100")
    print(f"  Presale Score:         {avg_presale:.1f}/100")
    print(f"  New Buyer Score:       {avg_newbuyer:.1f}/100")
    print(f"  Project Score:         {avg_project:.1f}/100")
    print(f"  No Emergency Brake:    {no_brake}/{len(liq_results)} ({no_brake/len(liq_results)*100:.0f}%)")
    print(f"  Best Config:           {best.tge_percent}% TGE, {best.exchanges} exchanges, {best.market_condition}")
    print(f"  Best Score:            {best.overall_score:.1f}")

# =============================================================================
# EXCHANGE COUNT IMPACT
# =============================================================================

print("\n" + "=" * 80)
print("EXCHANGE COUNT IMPACT")
print("=" * 80)

for ex in EXCHANGE_COUNTS:
    ex_results = [r for r in all_results if r.exchanges == ex]
    avg_depth = statistics.mean([r.depth_score for r in ex_results])
    avg_slippage = statistics.mean([r.slippage_10k for r in ex_results])
    avg_overall = statistics.mean([r.overall_score for r in ex_results])
    
    print(f"\n{ex} EXCHANGES:")
    print(f"  Avg Depth Score:    {avg_depth:.1f}/100")
    print(f"  Avg Slippage ($10K): {avg_slippage:.2f}%")
    print(f"  Avg Overall Score:  {avg_overall:.1f}/100")

# =============================================================================
# TOP 20 BEST SCENARIOS
# =============================================================================

print("\n" + "=" * 80)
print("TOP 20 BEST SCENARIOS (Across All Conditions)")
print("=" * 80)

# Sort by overall score
sorted_results = sorted(all_results, key=lambda x: x.overall_score, reverse=True)

print(f"\n{'Rank':<5} {'Liquidity':<12} {'Ex':<4} {'TGE%':<6} {'Market':<10} {'Price':<10} {'Overall':<8} {'Presale':<8} {'NewBuy':<8}")
print("-" * 85)

for i, r in enumerate(sorted_results[:20], 1):
    print(f"{i:<5} ${r.liquidity/1e6:.0f}M{'':<6} {r.exchanges:<4} {r.tge_percent}%{'':<4} {r.market_condition:<10} ${r.launch_price:.4f}{'':<2} {r.overall_score:.1f}{'':<4} {r.presale_score:.1f}{'':<4} {r.new_buyer_score:.1f}")

# =============================================================================
# BEST FOR EACH STAKEHOLDER
# =============================================================================

print("\n" + "=" * 80)
print("BEST SCENARIO FOR EACH STAKEHOLDER")
print("=" * 80)

best_presale = max(all_results, key=lambda x: x.presale_score)
best_newbuyer = max(all_results, key=lambda x: x.new_buyer_score)
best_project = max(all_results, key=lambda x: x.project_score)
best_overall = max(all_results, key=lambda x: x.overall_score)

print(f"\nBEST FOR PRESALE HOLDERS:")
print(f"  Config: ${best_presale.liquidity/1e6:.0f}M, {best_presale.exchanges} exchanges, {best_presale.tge_percent}% TGE, {best_presale.market_condition}")
print(f"  Launch Price: ${best_presale.launch_price:.4f}")
print(f"  TGE Value ($9K investor): ${best_presale.presale_tge_value:.0f}")
print(f"  Score: {best_presale.presale_score:.1f}/100")

print(f"\nBEST FOR NEW BUYERS:")
print(f"  Config: ${best_newbuyer.liquidity/1e6:.0f}M, {best_newbuyer.exchanges} exchanges, {best_newbuyer.tge_percent}% TGE, {best_newbuyer.market_condition}")
print(f"  Launch Price: ${best_newbuyer.launch_price:.4f}")
print(f"  6-Month ROI: {best_newbuyer.new_buyer_month6_roi:.1f}%")
print(f"  Score: {best_newbuyer.new_buyer_score:.1f}/100")

print(f"\nBEST FOR PROJECT:")
print(f"  Config: ${best_project.liquidity/1e6:.0f}M, {best_project.exchanges} exchanges, {best_project.tge_percent}% TGE, {best_project.market_condition}")
print(f"  Emergency Brake: {'Never' if best_project.emergency_brake_month == 0 else f'Month {best_project.emergency_brake_month}'}")
print(f"  Depth Score: {best_project.depth_score:.1f}/100")
print(f"  Score: {best_project.project_score:.1f}/100")

print(f"\n🏆 BEST OVERALL (BALANCED):")
print(f"  Config: ${best_overall.liquidity/1e6:.0f}M, {best_overall.exchanges} exchanges, {best_overall.tge_percent}% TGE, {best_overall.market_condition}")
print(f"  Launch Price: ${best_overall.launch_price:.4f}")
print(f"  Overall Score: {best_overall.overall_score:.1f}/100")
print(f"  Presale Score: {best_overall.presale_score:.1f} | New Buyer: {best_overall.new_buyer_score:.1f} | Project: {best_overall.project_score:.1f}")

# =============================================================================
# OPTIMAL LIQUIDITY RECOMMENDATION
# =============================================================================

print("\n" + "=" * 80)
print("OPTIMAL LIQUIDITY RECOMMENDATION")
print("=" * 80)

# Find the liquidity level with best average score
best_liq = max(liquidity_summary.keys(), key=lambda x: liquidity_summary[x]["avg_overall"])
best_liq_data = liquidity_summary[best_liq]

# Find second best for comparison
sorted_liq = sorted(liquidity_summary.items(), key=lambda x: x[1]["avg_overall"], reverse=True)

print(f"\n🎯 RECOMMENDED LIQUIDITY: ${best_liq/1e6:.0f}M")
print(f"\nRanking by Average Overall Score:")
for i, (liq, data) in enumerate(sorted_liq, 1):
    marker = "👑" if i == 1 else "  "
    print(f"  {marker} #{i}: ${liq/1e6:.0f}M - Score: {data['avg_overall']:.1f} (No brake: {data['no_brake_pct']:.0f}%)")

# =============================================================================
# DETAILED COMPARISON TABLE
# =============================================================================

print("\n" + "=" * 80)
print("DETAILED LIQUIDITY COMPARISON")
print("=" * 80)

print(f"\n{'Liquidity':<12} {'Presale':<10} {'NewBuyer':<10} {'Project':<10} {'Overall':<10} {'No Brake%':<10}")
print("-" * 62)

for liq in LIQUIDITY_LEVELS:
    data = liquidity_summary[liq]
    print(f"${liq/1e6:.0f}M{'':<7} {data['avg_presale']:.1f}{'':<6} {data['avg_newbuyer']:.1f}{'':<6} {data['avg_project']:.1f}{'':<6} {data['avg_overall']:.1f}{'':<6} {data['no_brake_pct']:.0f}%")

# =============================================================================
# SAVE RESULTS
# =============================================================================

output = {
    "simulation_date": datetime.now().isoformat(),
    "total_simulations": len(all_results),
    "parameters": {
        "liquidity_levels": LIQUIDITY_LEVELS,
        "exchange_counts": EXCHANGE_COUNTS,
        "tge_percentages": TGE_PERCENTAGES,
        "market_conditions": MARKET_CONDITIONS
    },
    "recommended_liquidity": best_liq,
    "liquidity_summary": liquidity_summary,
    "top_20_scenarios": [asdict(r) for r in sorted_results[:20]],
    "best_for_presale": asdict(best_presale),
    "best_for_new_buyers": asdict(best_newbuyer),
    "best_for_project": asdict(best_project),
    "best_overall": asdict(best_overall),
    "all_results": [asdict(r) for r in all_results]
}

with open("optimal_liquidity_results.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n" + "=" * 80)
print("✅ Results saved to optimal_liquidity_results.json")
print("=" * 80)

# =============================================================================
# FINAL RECOMMENDATION
# =============================================================================

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        OPTIMAL LIQUIDITY ANALYSIS                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🎯 RECOMMENDED: ${best_liq/1e6:.0f}M LIQUIDITY                                           ║
║                                                                              ║
║  Best Configuration:                                                         ║
║  • Liquidity: ${best_overall.liquidity/1e6:.0f}M                                                       ║
║  • Exchanges: {best_overall.exchanges}                                                           ║
║  • TGE:       {best_overall.tge_percent}%                                                          ║
║  • Market:    {best_overall.market_condition:<10}                                                   ║
║                                                                              ║
║  Expected Outcomes:                                                          ║
║  • Launch Price:   ${best_overall.launch_price:.4f}                                              ║
║  • Presale TGE:    ${best_overall.presale_tge_value:.0f} (for $9K investor)                           ║
║  • Emergency Brake: {'Never' if best_overall.emergency_brake_month == 0 else f'Month {best_overall.emergency_brake_month}':<10}                                            ║
║                                                                              ║
║  Scores:                                                                     ║
║  • Presale:    {best_overall.presale_score:.1f}/100                                                  ║
║  • New Buyers: {best_overall.new_buyer_score:.1f}/100                                                  ║
║  • Project:    {best_overall.project_score:.1f}/100                                                  ║
║  • OVERALL:    {best_overall.overall_score:.1f}/100                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

