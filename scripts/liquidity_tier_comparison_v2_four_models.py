#!/usr/bin/env python3
"""
LIQUIDITY TIER COMPARISON (v2): 4 Models × Liquidity Tiers × 10 Historical Scenarios × 100 Runs
==============================================================================================

Adds Protocol v3.0 to the prior liquidity-tier harness and makes the "100 simulations"
real by introducing small stochastic noise around liquidity each month, while preserving
the 10 historical event shocks.

Methodology note:
- We use a one-pass gating approach (consistent with earlier scripts):
  compute price with time-based vesting, then apply gates (oracle/brake/drip) once and recompute.

Models:
- Original Model
- Hybrid Model
- Protocol v2.6
- Protocol v3.0 (Hybrid Optimized)

Liquidity tiers:
- $32M, $50M, $75M, $100M, $150M

Historical scenarios (10):
- COVID_Crash, FTX_Collapse, May_2021_Crash, Gradual_Bear, Bull_Then_Crash,
  High_Volatility, Stable_Growth, Early_Recovery, Late_Crash, Multiple_Crashes

Output:
- liquidity_tier_comparison_v2_results.json
"""

import json
import random
import statistics
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Optional

print("=" * 80)
print("LIQUIDITY TIER COMPARISON v2: 4 Models + 100 Monte Carlo Runs")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000
DAILY_MINING_MAX = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

PRESALE_INVESTMENT = 9000
PRESALE_PRICE = 0.01
PRESALE_TOKENS = int(PRESALE_INVESTMENT / PRESALE_PRICE)
PRESALE_BASE_TOKENS = PRESALE_TOKENS // 2

SURVIVAL_PRICE = 0.02

LIQUIDITY_TIERS = [32_000_000, 50_000_000, 75_000_000, 100_000_000, 150_000_000]

MARKET_SCENARIOS = {
    "COVID_Crash": {"events": [(1, -0.80)]},
    "FTX_Collapse": {"events": [(3, -0.70)]},
    "May_2021_Crash": {"events": [(2, -0.60)]},
    "Gradual_Bear": {"events": [(2, -0.10), (4, -0.10), (6, -0.10), (8, -0.10), (10, -0.10), (12, -0.10)]},
    "Bull_Then_Crash": {"events": [(2, 1.00), (6, -0.70)]},
    "High_Volatility": {"events": [(2, -0.30), (4, 0.40), (6, -0.40), (8, 0.30), (10, -0.30)]},
    "Stable_Growth": {"events": [(2, 0.05), (4, 0.05), (6, 0.05), (8, 0.05), (10, 0.05), (12, 0.05)]},
    "Early_Recovery": {"events": [(2, -0.50), (4, 1.00)]},
    "Late_Crash": {"events": [(2, 0.50), (12, -0.67)]},
    "Multiple_Crashes": {"events": [(2, -0.40), (6, -0.40), (12, -0.40)]},
}


# =============================================================================
# MODELS
# =============================================================================


@dataclass(frozen=True)
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: Optional[float]  # fraction of DAILY_MINING_MAX
    mandatory_stake_pct: float
    vest_gate_high: Optional[float]
    vest_gate_low: Optional[float]
    vest_mid_factor: float
    mining_lock_months: int


ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    mandatory_stake_pct=0.50,
    vest_gate_high=None,
    vest_gate_low=None,
    vest_mid_factor=1.0,
    mining_lock_months=0,
)

HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=0.50,
    vest_gate_high=None,
    vest_gate_low=0.02,
    vest_mid_factor=1.0,
    mining_lock_months=0,
)

PROTOCOL_V26 = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=None,
    mandatory_stake_pct=0.0,
    vest_gate_high=0.05,
    vest_gate_low=None,
    vest_mid_factor=0.0,
    mining_lock_months=0,
)

PROTOCOL_V30 = ModelParams(
    name="Protocol v3.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=33,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    vest_gate_high=0.05,
    vest_gate_low=0.02,
    vest_mid_factor=0.10,
    mining_lock_months=24,
)

MODELS = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26, PROTOCOL_V30]


# =============================================================================
# HELPERS
# =============================================================================


def apply_events(liquidity: float, month: int, base_events: List[Tuple[int, float]], noise_events: List[Tuple[int, float]]) -> float:
    liq = liquidity
    for m, pct in base_events:
        if month >= m:
            liq *= (1.0 + pct)
    for m, pct in noise_events:
        if month >= m:
            liq *= (1.0 + pct)
    return liq


def gen_noise_events() -> List[Tuple[int, float]]:
    # Small monthly noise to make 100 runs non-identical (±2%)
    return [(m, random.uniform(-0.02, 0.02)) for m in range(1, 13)]


def mining_emissions_cumulative(month: int, emission_cap: Optional[float], mining_lock_months: int) -> int:
    if month <= 0 or month <= mining_lock_months:
        return 0
    ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    total = 0
    for m in range(1, month + 1):
        if m <= mining_lock_months:
            continue
        m_rate = 0.20
        for mr, r in sorted(ramp_rates.items()):
            if m >= mr:
                m_rate = r
        daily = DAILY_MINING_MAX * m_rate
        if emission_cap is not None:
            daily = min(daily, DAILY_MINING_MAX * emission_cap)
        total += int(daily * 30)
    return total


def vested_base_tokens_time_only(month: int, model: ModelParams) -> int:
    """Time-based vesting schedule ignoring gates."""
    tge_tokens = int(BASE_COINS * model.tge_percent / 100)
    if month <= 0:
        return tge_tokens
    if month <= model.cliff_months:
        return tge_tokens
    months_vesting = month - model.cliff_months
    remaining_pct = (100.0 - model.tge_percent) / 100.0
    monthly_rate = remaining_pct / model.vesting_months
    vested_pct = (model.tge_percent / 100.0) + (months_vesting * monthly_rate)
    vested_pct = min(vested_pct, 1.0)
    return int(BASE_COINS * vested_pct)


def prelaunch_mined_circulating(month: int) -> int:
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6
    return immediate + int(min(month, 6) * monthly_gradual)


def vested_base_tokens(month: int, model: ModelParams, price: float) -> int:
    tge_tokens = int(BASE_COINS * model.tge_percent / 100)
    if month <= 0:
        return tge_tokens
    if month <= model.cliff_months:
        return tge_tokens

    months_vesting = month - model.cliff_months
    remaining_pct = (100.0 - model.tge_percent) / 100.0
    monthly_rate = remaining_pct / model.vesting_months

    if model.vest_gate_low is not None and price < model.vest_gate_low:
        return tge_tokens

    if model.vest_gate_high is not None:
        if price >= model.vest_gate_high:
            factor = 1.0
        else:
            factor = model.vest_mid_factor
    else:
        factor = 1.0

    vested_pct = (model.tge_percent / 100.0) + (months_vesting * monthly_rate * factor)
    vested_pct = min(vested_pct, 1.0)
    return int(BASE_COINS * vested_pct)


def simulate_month(model: ModelParams, month: int, launch_liquidity: int, base_events: List[Tuple[int, float]], noise_events: List[Tuple[int, float]]) -> Tuple[int, float, float]:
    liquidity = apply_events(float(launch_liquidity), month, base_events, noise_events)

    mined = mining_emissions_cumulative(month, model.emission_cap, model.mining_lock_months)
    pre = prelaunch_mined_circulating(month)

    # 1) nominal price with time-only vesting
    vested_nominal = vested_base_tokens_time_only(month, model)
    circulating = vested_nominal + mined + pre
    staked = int(circulating * model.mandatory_stake_pct)
    effective = max(1, circulating - staked)
    price_nominal = liquidity / effective

    # 2) apply gates based on nominal price, recompute once
    vested_gated = vested_base_tokens(month, model, price_nominal)
    circulating2 = vested_gated + mined + pre
    staked2 = int(circulating2 * model.mandatory_stake_pct)
    effective2 = max(1, circulating2 - staked2)
    price_final = liquidity / effective2

    return effective2, price_final, liquidity


def run_one(model: ModelParams, launch_liquidity: int, scenario: str, base_events: List[Tuple[int, float]], sim_id: int) -> Dict:
    noise_events = gen_noise_events()
    prices: List[float] = []
    values: List[float] = []
    breach_month = 0

    for month in range(13):
        _, price, liq = simulate_month(model, month, launch_liquidity, base_events, noise_events)
        prices.append(price)
        vested = vested_base_tokens(month, model, price)
        inv_tokens = int(PRESALE_BASE_TOKENS * (vested / BASE_COINS))
        values.append(inv_tokens * price)

        if breach_month == 0 and price < SURVIVAL_PRICE:
            breach_month = month

    return {
        "simulation_id": sim_id,
        "model": model.name,
        "liquidity": launch_liquidity,
        "scenario": scenario,
        "launch_price": prices[0],
        "month_12_price": prices[12],
        "min_price": min(prices),
        "month_12_value": values[12],
        "month_12_roi": (values[12] / PRESALE_INVESTMENT - 1) * 100.0,
        "breach_month": breach_month,  # 0 = never breached $0.02 price floor
    }


def summarize(rows: List[Dict]) -> Dict:
    return {
        "avg_month_12_roi": statistics.mean([r["month_12_roi"] for r in rows]),
        "avg_month_12_value": statistics.mean([r["month_12_value"] for r in rows]),
        "avg_min_price": statistics.mean([r["min_price"] for r in rows]),
        "breach_rate": sum(1 for r in rows if r["breach_month"] != 0) / len(rows) * 100.0,
        "survival_rate": sum(1 for r in rows if r["breach_month"] == 0) / len(rows) * 100.0,
    }


def main() -> None:
    runs_per_combo = 100
    results: List[Dict] = []

    total = len(LIQUIDITY_TIERS) * len(MODELS) * len(MARKET_SCENARIOS) * runs_per_combo
    done = 0

    for liq in LIQUIDITY_TIERS:
        for model in MODELS:
            for scenario, data in MARKET_SCENARIOS.items():
                base_events = data["events"]
                for sid in range(runs_per_combo):
                    done += 1
                    if done % 1000 == 0:
                        print(f"  Progress: {done}/{total} ...")
                    results.append(run_one(model, liq, scenario, base_events, sid))

    # Aggregate by liquidity x model
    analysis: Dict[int, Dict[str, Dict]] = {}
    for liq in LIQUIDITY_TIERS:
        analysis[liq] = {}
        for model in MODELS:
            rows = [r for r in results if r["liquidity"] == liq and r["model"] == model.name]
            analysis[liq][model.name] = summarize(rows)

    # winners by tier (value)
    winners = {}
    for liq in LIQUIDITY_TIERS:
        best = max(
            ((m.name, analysis[liq][m.name]["avg_month_12_value"]) for m in MODELS),
            key=lambda x: x[1],
        )
        winners[liq] = {"winner": best[0], "avg_month_12_value": best[1]}

    # fairness score (same weights as before)
    fairness_scores = []
    for liq in LIQUIDITY_TIERS:
        for model in MODELS:
            met = analysis[liq][model.name]
            roi_score = max(0, min(100, (met["avg_month_12_roi"] + 100) / 2))
            survival_score = met["survival_rate"]
            value_score = min(100, (met["avg_month_12_value"] / PRESALE_INVESTMENT) * 100)
            fairness = roi_score * 0.4 + survival_score * 0.3 + value_score * 0.3
            fairness_scores.append({
                "liquidity": liq,
                "model": model.name,
                "fairness_score": fairness,
                "avg_month_12_roi": met["avg_month_12_roi"],
                "avg_month_12_value": met["avg_month_12_value"],
                "survival_rate": met["survival_rate"],
            })

    fairness_scores.sort(key=lambda x: x["fairness_score"], reverse=True)
    optimal = fairness_scores[0]

    out = {
        "timestamp": datetime.now().isoformat(),
        "runs_per_combo": runs_per_combo,
        "liquidity_tiers": LIQUIDITY_TIERS,
        "models": [m.__dict__ for m in MODELS],
        "scenarios": list(MARKET_SCENARIOS.keys()),
        "analysis_by_liquidity": analysis,
        "winners_by_liquidity": winners,
        "top_10_fairness": fairness_scores[:10],
        "optimal_fairness": optimal,
        "raw_results": results,
        "notes": {
            "protocol_v3_mid_factor": "Protocol v3.0 volume-peg modeled as 10% vesting rate when 0.02 <= price < 0.05.",
            "protocol_v3_mining_lock": "Protocol v3.0 miners locked 24 months (mined emissions excluded from circulating first 24 months).",
            "monte_carlo_noise": "Each run adds monthly liquidity noise ±2% in addition to historical event shocks.",
        },
    }

    with open("liquidity_tier_comparison_v2_results.json", "w") as f:
        json.dump(out, f, indent=2)

    print("\n✅ Saved: liquidity_tier_comparison_v2_results.json")
    print(f"🏆 Optimal fairness: ${optimal['liquidity']/1e6:.0f}M + {optimal['model']} (score {optimal['fairness_score']:.1f})")


if __name__ == "__main__":
    main()


