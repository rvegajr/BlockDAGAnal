#!/usr/bin/env python3
"""
FOUR MODEL COMPARISON: Investor Returns (Moderate Market Conditions)
===================================================================
This extends the original `three_model_comparison.py` methodology (so results
stay comparable) and adds Protocol v3.0.

Models:
1) Original Model (2% TGE, 12mo cliff, 60mo vest, 20% emission cap, 50% mandatory stake)
2) Hybrid Model (3% TGE, 3mo cliff, 36mo vest, 20% emission cap, 50% mandatory stake)
3) Protocol v2.6 (3% TGE, 3mo cliff, 21mo vest, oracle gate @ $0.05)
4) Protocol v3.0 (3% TGE, 3mo cliff, 33mo vest, oracle gate @ $0.05, emergency brake @ $0.02,
                  emission cap 20%, miners locked 24mo, volume-pegged drip approximated)

Important:
- We keep the same “one-pass gate” style as earlier scripts:
  compute price assuming schedule, then apply gates and recompute once.

Output:
- four_model_comparison_results.json
"""

import json
import random
import statistics
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple, Optional

print("=" * 80)
print("FOUR MODEL COMPARISON: Investor Returns (Moderate Markets)")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000  # 17B
DAILY_MINING_MAX = 10_500_000  # 10.5M/day uncapped
PRE_LAUNCH_MINED = 540_000_000  # assumed testnet/prelaunch mined
LAUNCH_LIQUIDITY = 32_000_000  # $32M

# Reference investor
PRESALE_INVESTMENT = 9000  # $9K
PRESALE_PRICE = 0.01
PRESALE_TOKENS = int(PRESALE_INVESTMENT / PRESALE_PRICE)  # 900K tokens
PRESALE_BASE_TOKENS = PRESALE_TOKENS // 2  # 450K base tokens

# Price threshold used for breach metric
SURVIVAL_PRICE = 0.02

# =============================================================================
# MODEL DEFINITIONS
# =============================================================================


@dataclass(frozen=True)
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: Optional[float]  # fraction of DAILY_MINING_MAX (0.20 = 20%), None = uncapped
    mandatory_stake_pct: float  # fraction of circulating removed

    # gating + special mechanics
    price_gate_high: Optional[float]  # oracle gate (e.g., 0.05). If price below, vesting may pause or drip.
    brake_low: Optional[float]        # emergency brake (e.g., 0.02). If price below, vesting pauses.
    drip_factor_between: float        # if brake_low <= price < price_gate_high, vest at reduced factor (Protocol v3.0)

    mining_lock_months: int           # mined emissions excluded from circulating for this many months


ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    mandatory_stake_pct=0.50,
    price_gate_high=None,
    brake_low=None,
    drip_factor_between=1.0,
    mining_lock_months=0,
)

HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=0.50,
    price_gate_high=None,
    brake_low=None,  # keep comparable to prior harness (hybrid didn't hard-stop vesting in v1 script)
    drip_factor_between=1.0,
    mining_lock_months=0,
)

PROTOCOL_V26 = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=None,    # uncapped in their writeup
    mandatory_stake_pct=0.0,
    price_gate_high=0.05,  # oracle gate at listing price
    brake_low=None,
    drip_factor_between=0.0,  # hard stop when below 0.05
    mining_lock_months=0,
)

PROTOCOL_V30 = ModelParams(
    name="Protocol v3.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=33,    # Month 4 → 36 = 33 months for remaining 97%
    emission_cap=0.20,    # explicitly mentions cap
    mandatory_stake_pct=0.0,  # staking is offered but not mandatory in text
    price_gate_high=0.05,  # oracle gate
    brake_low=0.02,        # emergency brake
    drip_factor_between=0.10,  # approximation of “2% of 24h volume drip” when 0.02–0.05
    mining_lock_months=24,     # miners locked 2 years (per v3.0 page)
)

MODELS = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26, PROTOCOL_V30]


# =============================================================================
# MARKET GENERATORS
# =============================================================================


def generate_market_conditions(scenario_type: str) -> List[Tuple[int, float]]:
    events: List[Tuple[int, float]] = []
    if scenario_type == "bull":
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(0.05, 0.10)))
    elif scenario_type == "bear":
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(-0.10, -0.05)))
    elif scenario_type == "volatile":
        for month in [2, 4, 6, 8, 10, 12]:
            swing = random.choice([-1, 1]) * random.uniform(0.15, 0.30)
            events.append((month, swing))
    elif scenario_type == "normal":
        for month in [2, 4, 6, 8, 10, 12]:
            events.append((month, random.uniform(-0.03, 0.03)))
    else:
        raise ValueError(f"unknown scenario_type: {scenario_type}")
    return events


# =============================================================================
# CORE SIMULATION
# =============================================================================


def apply_liquidity_events(base_liquidity: float, month: int, events: List[Tuple[int, float]]) -> float:
    liq = base_liquidity
    for m, pct in events:
        if month >= m:
            liq *= (1.0 + pct)
    return liq


def mining_emissions_cumulative(month: int, emission_cap: Optional[float], mining_lock_months: int) -> int:
    """Cumulative mined tokens that are *circulating* by `month`."""
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


def prelaunch_mined_circulating(month: int) -> int:
    """Simple migration curve for prelaunch mined (circulating)."""
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6
    return immediate + int(min(month, 6) * monthly_gradual)


def vested_base_tokens(month: int, model: ModelParams, factor: float = 1.0) -> int:
    """How many base tokens are vested (claimable) at `month` (time-based, optionally scaled)."""
    tge_tokens = int(BASE_COINS * model.tge_percent / 100)
    if month <= 0:
        return tge_tokens
    if month <= model.cliff_months:
        return tge_tokens

    months_vesting = month - model.cliff_months
    remaining_pct = (100.0 - model.tge_percent) / 100.0
    monthly_rate = remaining_pct / model.vesting_months
    vested_pct = (model.tge_percent / 100.0) + (months_vesting * monthly_rate * factor)
    vested_pct = min(vested_pct, 1.0)
    return int(BASE_COINS * vested_pct)


def simulate_month(model: ModelParams, month: int, events: List[Tuple[int, float]]) -> Tuple[int, float, float]:
    """Returns (effective_circulating, price, liquidity) using the older one-pass gate approach."""
    liquidity = apply_liquidity_events(LAUNCH_LIQUIDITY, month, events)

    # start with full scheduled vesting (time-based)
    vested = vested_base_tokens(month, model, factor=1.0)
    mined = mining_emissions_cumulative(month, model.emission_cap, model.mining_lock_months)
    pre = prelaunch_mined_circulating(month)
    circulating = vested + mined + pre
    staked = int(circulating * model.mandatory_stake_pct)
    effective = max(1, circulating - staked)
    price = liquidity / effective

    # apply gates (one pass), then recompute price once
    if month > model.cliff_months:
        # emergency brake
        if model.brake_low is not None and price < model.brake_low:
            vested = int(BASE_COINS * model.tge_percent / 100)
        # oracle gate / drip
        elif model.price_gate_high is not None and price < model.price_gate_high:
            factor = model.drip_factor_between
            vested = vested_base_tokens(month, model, factor=factor)

        circulating = vested + mined + pre
        staked = int(circulating * model.mandatory_stake_pct)
        effective = max(1, circulating - staked)
        price = liquidity / effective

    return effective, price, liquidity


def run_one(model: ModelParams, market_type: str, sim_id: int) -> Dict:
    events = generate_market_conditions(market_type)

    prices: List[float] = []
    values: List[float] = []
    brake_month = 0

    for month in range(13):
        _, price, liquidity = simulate_month(model, month, events)
        prices.append(price)

        # investor value: value of vested base tokens (assume claimable)
        # use the same vesting gate behavior: vesting amount is embedded in simulate_month’s logic,
        # but we approximate investor vested% from time schedule (this matches older harness).
        if month <= model.cliff_months:
            inv_pct = model.tge_percent / 100.0
        else:
            months_vesting = month - model.cliff_months
            remaining_pct = (100.0 - model.tge_percent) / 100.0
            monthly_rate = remaining_pct / model.vesting_months
            inv_pct = min(model.tge_percent / 100.0 + months_vesting * monthly_rate, 1.0)
        inv_tokens = int(PRESALE_BASE_TOKENS * inv_pct)
        values.append(inv_tokens * price)

        if brake_month == 0 and price < SURVIVAL_PRICE:
            brake_month = month

    return {
        "simulation_id": sim_id,
        "model": model.name,
        "market_type": market_type,
        "launch_price": prices[0],
        "month_3_price": prices[3],
        "month_6_price": prices[6],
        "month_12_price": prices[12],
        "min_price": min(prices),
        "max_price": max(prices),
        "tge_value": values[0],
        "month_12_value": values[12],
        "tge_roi": (values[0] / PRESALE_INVESTMENT - 1) * 100.0,
        "month_12_roi": (values[12] / PRESALE_INVESTMENT - 1) * 100.0,
        "breach_month": brake_month,  # 0 = never breached $0.02 / $10M
    }


def summarize(rows: List[Dict]) -> Dict:
    return {
        "tge_roi_avg": statistics.mean([r["tge_roi"] for r in rows]),
        "month_12_roi_avg": statistics.mean([r["month_12_roi"] for r in rows]),
        "month_12_value_avg": statistics.mean([r["month_12_value"] for r in rows]),
        "breach_rate": sum(1 for r in rows if r["breach_month"] != 0) / len(rows) * 100.0,
    }


def main() -> None:
    market_types = ["bull", "bear", "normal", "volatile"]
    sims_per_market = 25  # 25 * 4 = 100 per model

    all_results: List[Dict] = []
    for model in MODELS:
        print(f"\nRunning {model.name} ...")
        for market in market_types:
            for sid in range(sims_per_market):
                all_results.append(run_one(model, market, sid))

    # aggregate
    comparison: Dict[str, Dict] = {}
    for model in MODELS:
        mr = [r for r in all_results if r["model"] == model.name]
        comparison[model.name] = {
            "overall": summarize(mr),
            "by_market": {m: summarize([r for r in mr if r["market_type"] == m]) for m in market_types},
        }

    # print quick table
    print("\nMonth 12 ROI (avg) by Market")
    print("-" * 80)
    header = f"{'Model':<16}" + "".join([f"{m:>12}" for m in market_types]) + f"{'Overall':>12}"
    print(header)
    print("-" * 80)
    for model in MODELS:
        row = f"{model.name:<16}"
        for m in market_types:
            row += f"{comparison[model.name]['by_market'][m]['month_12_roi_avg']:>11.1f}%"
        row += f"{comparison[model.name]['overall']['month_12_roi_avg']:>11.1f}%"
        print(row)

    output = {
        "timestamp": datetime.now().isoformat(),
        "simulations_per_model": 100,
        "market_types": market_types,
        "models": [m.__dict__ for m in MODELS],
        "comparison": comparison,
        "raw_results": all_results,
        "notes": {
            "methodology": "Consistent with prior three-model harness: time-based vesting + one-pass price gate adjustments.",
            "protocol_v3_mid_factor": "Protocol v3.0 'volume pegging' approximated as 10% of scheduled vesting when 0.02 <= price < 0.05.",
            "protocol_v3_mining_lock": "Protocol v3.0 'miners locked 2 years' modeled as 24-month lock on mined emissions entering circulating supply (no impact within 12 months, but included for correctness).",
        },
    }

    with open("four_model_comparison_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n✅ Saved: four_model_comparison_results.json")


if __name__ == "__main__":
    main()


