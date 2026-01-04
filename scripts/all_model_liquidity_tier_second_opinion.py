#!/usr/bin/env python3
"""
ALL-MODEL LIQUIDITY TIER ANALYSIS (Second Opinion)
=================================================

Goal:
- Provide a liquidity-tier winner analysis that tests *every* model in our current set.
- Uses the same "second opinion" methodology as `scripts/hybrid_tokenomics_second_opinion_compare.py`:
  baseline (Liquidity/Circulating) + order-book depth + sell-pressure impacts.

Models (7):
- Original Model
- Hybrid Model
- Protocol v2.6
- Protocol v3.0
- Protocol v3.1 (Adjusted)
- Hybrid B
- Hybrid Tokenomics (Solvency-Anchored)

What we run:
- For each liquidity tier and each of the 10 choppy scenarios:
  - 100 Monte Carlo runs per model

Outputs:
- all_model_liquidity_tier_second_opinion_results.json
- docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md
"""

import json
import random
import statistics
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Deque, Dict, List, Optional, Tuple

# =============================================================================
# CONSTANTS / CONFIG
# =============================================================================

BASE_COINS = 17_000_000_000
DAILY_MINING_MAX = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

TARGET_PRICE = 0.05
EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY = 10_000_000

BUY_SUPPORT_PCT = 0.30
DEPTH_FACTOR = 0.12
MAX_IMPACT = 0.90

INVESTMENT_USD = 9000
PRESALE_PRICE = 0.01
INVESTMENT_LEVEL_KEY = "9000"

RUNS_PER_MODEL = 100

LIQUIDITY_TIERS = [20_000_000, 32_000_000, 50_000_000, 75_000_000, 100_000_000, 150_000_000]

CHOPPY_SCENARIOS: Dict[str, Dict] = {
    "normal": {"name": "Normal Market Conditions", "events": []},
    "may_2021_crash": {"name": "May 2021-Style Crash", "events": [(2, -0.60)]},
    "ftx_collapse": {"name": "FTX Collapse", "events": [(3, -0.70)]},
    "covid_black_swan": {"name": "COVID Black Swan", "events": [(1, -0.80)]},
    "gradual_bear": {"name": "Gradual Bear Market", "events": [(i, -0.05) for i in range(2, 13)]},
    "bull_then_crash": {"name": "Bull Run Then Crash", "events": [(i, 0.15) for i in range(2, 7)] + [(7, -0.70)]},
    "high_volatility": {"name": "High Volatility", "events": [(2, -0.30), (4, 0.40), (6, -0.40), (8, 0.30), (10, -0.30)]},
    "stable_growth": {"name": "Stable Growth", "events": [(i, 0.02) for i in range(2, 13)]},
    "early_crash_recovery": {"name": "Early Crash with Recovery", "events": [(2, -0.50), (4, 0.25), (6, 0.50)]},
    "multiple_crashes": {"name": "Multiple Crashes", "events": [(2, -0.40), (6, -0.40), (12, -0.40)]},
}

# Sell behavior (fraction of newly-liquid vesting sold quickly)
SELL_BEHAVIOR_WEIGHTS = {
    "panic": 0.20,
    "partial": 0.30,
    "holder": 0.35,
    "long_term": 0.15,
}


@dataclass(frozen=True)
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: float
    mandatory_stake_pct: float
    state_driven_release: bool = False
    global_monthly_cap: Optional[float] = None
    mining_lock_ratio: Optional[float] = None
    # gates / protocol mechanics
    price_gate_high: Optional[float] = None
    brake_low: Optional[float] = None
    drip_factor_between: Optional[float] = None
    mining_lock_months: int = 0
    use_volume_peg: bool = False
    vest_volume_peg_pct: float = 0.0
    mining_volume_cap_pct: float = 0.0


ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
)

HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    brake_low=0.02,
)

PROTOCOL_V26 = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,
    mandatory_stake_pct=0.0,
    price_gate_high=0.05,
    drip_factor_between=0.0,
)

PROTOCOL_V30 = ModelParams(
    name="Protocol v3.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=33,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    price_gate_high=0.05,
    brake_low=0.02,
    drip_factor_between=0.10,
    mining_lock_months=24,
)

PROTOCOL_V31 = ModelParams(
    name="Protocol v3.1 (Adjusted)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,
    mandatory_stake_pct=0.0,
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
)

HYBRID_B = ModelParams(
    name="Hybrid B",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    state_driven_release=True,
    global_monthly_cap=1.0,
    price_gate_high=0.05,
    brake_low=0.02,
)

HYBRID_TOKENOMICS = ModelParams(
    name="Hybrid Tokenomics (Solvency-Anchored)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=60.0,
    state_driven_release=True,
    global_monthly_cap=1.0,
    mining_lock_ratio=0.70,
    price_gate_high=0.05,
    brake_low=0.02,
)

MODELS = [ORIGINAL_MODEL, HYBRID_MODEL, PROTOCOL_V26, PROTOCOL_V30, PROTOCOL_V31, HYBRID_B, HYBRID_TOKENOMICS]


def investor_base_tokens(investment_usd: float) -> int:
    return int(investment_usd / PRESALE_PRICE) // 2


def sample_sell_fraction() -> float:
    r = random.random()
    if r < SELL_BEHAVIOR_WEIGHTS["panic"]:
        return random.uniform(0.70, 1.00)
    if r < SELL_BEHAVIOR_WEIGHTS["panic"] + SELL_BEHAVIOR_WEIGHTS["partial"]:
        return random.uniform(0.30, 0.70)
    if r < SELL_BEHAVIOR_WEIGHTS["panic"] + SELL_BEHAVIOR_WEIGHTS["partial"] + SELL_BEHAVIOR_WEIGHTS["holder"]:
        return random.uniform(0.05, 0.20)
    return random.uniform(0.00, 0.05)


def apply_order_book_impact(reference_price: float, liquidity: float, sell_volume_usd: float) -> float:
    buy_support = liquidity * BUY_SUPPORT_PCT
    if buy_support <= 0:
        return reference_price * (1 - MAX_IMPACT)
    impact = min(MAX_IMPACT, (sell_volume_usd / buy_support) * DEPTH_FACTOR)
    return max(0.000001, reference_price * (1.0 - impact))


def cumulative_prelaunch_migrated(month: int) -> int:
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6.0
    return immediate + int(min(month, 6) * monthly_gradual)


def vwap_30(prices: Deque[float]) -> float:
    if not prices:
        return TARGET_PRICE
    recent = list(prices)[-min(30, len(prices)):]
    return statistics.mean(recent) if recent else TARGET_PRICE


def market_allows_release(price: float, vwap: float, liquidity: float, trend: List[float]) -> bool:
    if liquidity < MIN_LIQUIDITY:
        return False
    if price < EMERGENCY_PRICE:
        return False
    if trend and (price - trend[0]) / trend[0] < -0.10:
        return False
    if vwap > 0 and abs(price - vwap) / vwap > 0.25:
        return False
    return True


def daily_volume_usd_proxy(liquidity: float) -> float:
    return liquidity * random.uniform(0.02, 0.10)


def monthly_mining_liquid(month: int, model: ModelParams, liquidity: float, last_price: float) -> int:
    if month <= 0:
        return 0

    ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    rate = 0.20
    for m, r in sorted(ramp_rates.items()):
        if month >= m:
            rate = r

    daily = DAILY_MINING_MAX * rate
    daily = min(daily, DAILY_MINING_MAX * model.emission_cap)

    # v3.0 lock
    if model.mining_lock_months and month <= model.mining_lock_months:
        return 0

    monthly = int(daily * 30)

    # v3.1 volume cap
    if model.mining_volume_cap_pct and model.mining_volume_cap_pct > 0:
        dv = daily_volume_usd_proxy(liquidity)
        cap_tokens_month = int(((dv * model.mining_volume_cap_pct) / max(last_price, 1e-9)) * 30)
        monthly = min(monthly, cap_tokens_month)

    # Hybrid Tokenomics extra early lock
    if model.mining_lock_ratio is not None and month <= 6:
        monthly = int(monthly * (1.0 - model.mining_lock_ratio))

    return monthly


def scheduled_vest_delta(month: int, model: ModelParams) -> int:
    if month <= model.cliff_months:
        return 0
    tge = int(BASE_COINS * model.tge_percent / 100.0)
    remaining = BASE_COINS - tge
    return int(remaining / max(model.vesting_months, 1))


def simulate_path(model: ModelParams, liquidity_base: float, events: List[Tuple[int, float]], months: int = 12) -> Dict:
    prices: Deque[float] = deque(maxlen=120)
    vested_cum = int(BASE_COINS * model.tge_percent / 100.0)
    mining_cum = 0
    prelaunch_prev = 0
    emergency_brake_month = 0

    for month in range(0, months + 1):
        # apply liquidity events (and mild noise to make runs non-identical)
        liq = liquidity_base
        for em, delta in events:
            if month >= em:
                liq *= (1.0 + delta)
        liq *= (1.0 + random.uniform(-0.02, 0.02))

        last_price = prices[-1] if prices else TARGET_PRICE

        # vesting delta
        if month == 0:
            vest_delta = 0
        elif month <= model.cliff_months:
            vest_delta = 0
        elif model.state_driven_release:
            if month <= 6:
                vest_delta = 0
            else:
                v = vwap_30(prices)
                trend = list(prices)[-min(10, len(prices)):] if prices else []
                if not market_allows_release(last_price, v, liq, trend):
                    vest_delta = 0
                else:
                    stable = abs(last_price - v) / v < 0.20 if v > 0 else True
                    rate = 0.003 if stable else 0.007
                    if model.global_monthly_cap is not None:
                        rate = min(rate, model.global_monthly_cap / 100.0)
                    vest_delta = int(BASE_COINS * rate)
        else:
            vest_delta = scheduled_vest_delta(month, model)

            # brake
            if model.brake_low is not None and last_price < model.brake_low:
                vest_delta = 0

            # gate behavior below 0.05
            if model.price_gate_high is not None and last_price < model.price_gate_high:
                if model.use_volume_peg and model.vest_volume_peg_pct > 0 and (model.brake_low is None or last_price >= model.brake_low):
                    dv = daily_volume_usd_proxy(liq)
                    cap_tokens_month = int(((dv * model.vest_volume_peg_pct) / max(last_price, 1e-9)) * 30)
                    vest_delta = min(vest_delta, cap_tokens_month)
                elif model.drip_factor_between is not None:
                    vest_delta = int(vest_delta * model.drip_factor_between)
                else:
                    vest_delta = 0

        vested_cum = min(BASE_COINS, vested_cum + max(0, vest_delta))

        # mining
        mined_this_month = monthly_mining_liquid(month, model, liq, last_price)
        mining_cum += mined_this_month

        # prelaunch migration
        prelaunch_cum = cumulative_prelaunch_migrated(month)
        prelaunch_delta = max(0, prelaunch_cum - prelaunch_prev)
        prelaunch_prev = prelaunch_cum

        # circulating & price
        total_liquidish = vested_cum + mining_cum + prelaunch_cum
        staked = int(total_liquidish * (model.mandatory_stake_pct / 100.0))
        effective = max(1, total_liquidish - staked)
        reference_price = liq / effective

        # sell pressure
        vest_sell_usd = vest_delta * sample_sell_fraction() * reference_price
        miner_sell_usd = mined_this_month * random.uniform(0.50, 0.70) * reference_price
        pre_sell_usd = prelaunch_delta * random.uniform(0.10, 0.40) * reference_price
        price = apply_order_book_impact(reference_price, liq, vest_sell_usd + miner_sell_usd + pre_sell_usd)

        prices.append(price)

        if emergency_brake_month == 0 and (price < EMERGENCY_PRICE or liq < MIN_LIQUIDITY):
            emergency_brake_month = month

    return {
        "month_12_price": prices[-1],
        "min_price": min(prices),
        "emergency_brake_month": emergency_brake_month,
        "vested_cumulative": vested_cum,
    }


def main() -> None:
    print("=" * 80)
    print("ALL-MODEL LIQUIDITY TIER ANALYSIS (Second Opinion)")
    print("=" * 80)
    print(f"Models: {[m.name for m in MODELS]}")
    print(f"Tiers: {[f'${x/1e6:.0f}M' for x in LIQUIDITY_TIERS]}")
    print(f"Runs/model/scenario: {RUNS_PER_MODEL}")

    base_tokens = investor_base_tokens(INVESTMENT_USD)

    results: Dict = {
        "timestamp": datetime.now().isoformat(),
        "methodology": "Second opinion (order-book + sell-pressure), extended across liquidity tiers for all models.",
        "liquidity_tiers": LIQUIDITY_TIERS,
        "runs_per_model": RUNS_PER_MODEL,
        "investment_usd": INVESTMENT_USD,
        "models": [m.__dict__ for m in MODELS],
        "scenarios": {k: v["name"] for k, v in CHOPPY_SCENARIOS.items()},
        "analysis": {},
    }

    for tier in LIQUIDITY_TIERS:
        tier_key = str(tier)
        results["analysis"][tier_key] = {}
        for scenario_key, scenario in CHOPPY_SCENARIOS.items():
            results["analysis"][tier_key][scenario_key] = {}
            for model in MODELS:
                rows = []
                for run_id in range(RUNS_PER_MODEL):
                    path = simulate_path(model, float(tier), scenario["events"], months=12)
                    vested_pct = path["vested_cumulative"] / BASE_COINS
                    investor_tokens = int(base_tokens * vested_pct)
                    value = investor_tokens * path["month_12_price"]
                    roi = (value / INVESTMENT_USD - 1.0) * 100.0
                    rows.append(
                        {
                            "run_id": run_id,
                            "month_12_price": path["month_12_price"],
                            "min_price": path["min_price"],
                            "emergency_brake_month": path["emergency_brake_month"],
                            "month_12_value": value,
                            "month_12_roi": roi,
                        }
                    )
                rois = [r["month_12_roi"] for r in rows]
                values = [r["month_12_value"] for r in rows]
                brakes = [r["emergency_brake_month"] != 0 for r in rows]
                results["analysis"][tier_key][scenario_key][model.name] = {
                    "roi_avg": statistics.mean(rois),
                    "roi_median": statistics.median(rois),
                    "value_avg": statistics.mean(values),
                    "brake_rate_pct": sum(brakes) / len(brakes) * 100.0,
                }

    # Write JSON
    out_json = Path("all_model_liquidity_tier_second_opinion_results.json")
    out_json.write_text(json.dumps(results, indent=2))

    # Build Markdown summary
    def pct(x: float) -> str:
        return f"{x:+.1f}%"

    def usd(x: float) -> str:
        return f"${x:,.0f}"

    md = []
    md.append("# All-Model Liquidity Tier Analysis (Second Opinion)\n\n")
    md.append(f"**Generated**: {results['timestamp']}\n\n")
    md.append(f"**Runs**: {RUNS_PER_MODEL} per model per scenario\n\n")
    md.append(f"**Investment reference**: ${INVESTMENT_USD:,}\n\n")
    md.append("## Winner by liquidity tier (avg ROI across 10 scenarios)\n\n")

    for tier in LIQUIDITY_TIERS:
        tier_key = str(tier)
        avg_by_model = {}
        brake_by_model = {}
        for model in MODELS:
            mname = model.name
            rois = [results['analysis'][tier_key][sc][mname]['roi_avg'] for sc in CHOPPY_SCENARIOS.keys()]
            brakes = [results['analysis'][tier_key][sc][mname]['brake_rate_pct'] for sc in CHOPPY_SCENARIOS.keys()]
            avg_by_model[mname] = sum(rois) / len(rois)
            brake_by_model[mname] = sum(brakes) / len(brakes)
        winner = max(avg_by_model.items(), key=lambda kv: kv[1])
        md.append(f"### Tier: ${tier/1e6:.0f}M\n")
        md.append(f"- **Winner (avg choppy ROI)**: **{winner[0]}** ({pct(winner[1])})\n")
        md.append("| Model | Avg choppy ROI | Avg brake rate |\n")
        md.append("|---|---:|---:|\n")
        for mname, v in sorted(avg_by_model.items(), key=lambda kv: kv[1], reverse=True):
            md.append(f"| {mname} | {pct(v)} | {brake_by_model[mname]:.1f}% |\n")
        md.append("\n")

    md.append("## Full per-scenario tables\n\n")
    md.append("See `all_model_liquidity_tier_second_opinion_results.json` for the complete cube: tier × scenario × model.\n")

    out_md = Path("docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(md))

    print("✅ wrote all_model_liquidity_tier_second_opinion_results.json")
    print("✅ wrote docs/vesting/ALL_MODEL_LIQUIDITY_TIER_ANALYSIS.md")


if __name__ == "__main__":
    main()


