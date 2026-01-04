#!/usr/bin/env python3
"""
THIRD OPINION: Compressed Comparison (adds Protocol v3.1)
=========================================================

This harness is intentionally DIFFERENT from:
- primary harness: `scripts/hybrid_tokenomics_comparison.py` (AMM-style, simplistic)
- second opinion: `scripts/hybrid_tokenomics_second_opinion_compare.py` (order-book + sell pressure)

Third opinion methodology:
- Sequential month-by-month simulation (path dependent)
- Uses a *volume-limited release* mechanism for Protocol v3.1:
  - Oracle price gate: vest normally only if price >= $0.05
  - Emergency brake: if price < $0.02, vesting stops (TGE-only)
  - Volume pegging: if $0.02 <= price < $0.05, vesting delta is limited to
    2% of *daily volume* converted to tokens (proxy for 24h volume)
- Uses a *volume-capped mining* mechanism for v3.1:
  - daily mined tokens capped by 20% of daily volume (USD) converted to tokens

We include all past models we tested (plus Protocol v3.1):
- Original Model
- Hybrid Model
- Protocol v2.6
- Protocol v3.0 (existing approximation)
- Protocol v3.1 (from the provided spec page)
- Hybrid B
- Hybrid Tokenomics (Solvency-Anchored)

Runs:
- 100 sims per model across market types (bull/bear/normal/volatile)
- 100 sims per model for each of 10 choppy market scenarios

Outputs:
- third_opinion_v31_results.json
- THIRD_OPINION_V31_REPORT.md
"""

import json
import random
import statistics
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, List, Optional, Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000
DAILY_MINING_MAX = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

DEFAULT_LIQUIDITY = 32_000_000
TARGET_PRICE = 0.05

EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY = 10_000_000

PRESALE_PRICE = 0.01
INVESTMENT_REF = 9000  # report baseline

# Choppy scenarios (same 10 as prior docs/harnesses)
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

MARKET_TYPES = ["bull", "bear", "normal", "volatile"]


# =============================================================================
# MODELS
# =============================================================================


@dataclass(frozen=True)
class Model:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    mandatory_stake_pct: float  # fraction [0..1]

    # mining (base cap vs volume cap)
    emission_cap: Optional[float]  # fraction of DAILY_MINING_MAX, None = uncapped
    mining_lock_months: int
    mining_lock_ratio_early: float  # additional early lock (Hybrid Tokenomics), fraction [0..1]
    mining_lock_ratio_months: int

    # vesting gates
    gate_high: Optional[float]  # e.g. 0.05
    brake_low: Optional[float]  # e.g. 0.02

    # volume pegging (v3.1)
    use_volume_peg: bool
    vest_volume_peg_pct: float  # fraction of daily volume (USD) convertible to tokens
    mining_volume_cap_pct: float  # fraction of daily volume (USD) convertible to tokens

    # state driven (Hybrid B / Hybrid Tokenomics)
    state_driven: bool
    global_monthly_cap_pct: Optional[float]  # percent of BASE_COINS per month


ORIGINAL_MODEL = Model(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    mandatory_stake_pct=0.50,
    emission_cap=0.20,
    mining_lock_months=0,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=None,
    brake_low=None,
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=False,
    global_monthly_cap_pct=None,
)

HYBRID_MODEL = Model(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    mandatory_stake_pct=0.50,
    emission_cap=0.20,
    mining_lock_months=0,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=None,
    brake_low=0.02,
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=False,
    global_monthly_cap_pct=None,
)

PROTOCOL_V26 = Model(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    mandatory_stake_pct=0.0,
    emission_cap=None,
    mining_lock_months=0,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=0.05,
    brake_low=None,  # “hard gate” at 0.05
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=False,
    global_monthly_cap_pct=None,
)

# Protocol v3.0 (existing approximation): gate_high, brake_low, mid “drip” is modeled here as volume peg OFF.
# We keep it simple: if below 0.05 but above 0.02, allow a reduced vest delta (10% of scheduled) like prior harness.
PROTOCOL_V30 = Model(
    name="Protocol v3.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=33,
    mandatory_stake_pct=0.0,
    emission_cap=0.20,
    mining_lock_months=24,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=False,
    global_monthly_cap_pct=None,
)

# Protocol v3.1 (from the provided page):
# - 3% TGE, 3mo cliff
# - Linear vesting Month 4-24 => 21 months
# - Oracle price gate: vest only if price >= 0.05
# - Emergency brake: if price < 0.02 stop vesting
# - Volume pegging: if 0.02 <= price < 0.05, vest delta limited to 2% of 24h volume
# - Mining emission cap: 20% of daily volume
PROTOCOL_V31 = Model(
    name="Protocol v3.1 (Adjusted)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    mandatory_stake_pct=0.0,
    emission_cap=None,  # governed by volume cap here
    mining_lock_months=0,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
    state_driven=False,
    global_monthly_cap_pct=None,
)

HYBRID_B = Model(
    name="Hybrid B",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    mandatory_stake_pct=0.50,
    emission_cap=0.20,
    mining_lock_months=0,
    mining_lock_ratio_early=0.0,
    mining_lock_ratio_months=0,
    gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=True,
    global_monthly_cap_pct=1.0,
)

HYBRID_TOKENOMICS = Model(
    name="Hybrid Tokenomics (Solvency-Anchored)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    mandatory_stake_pct=0.60,
    emission_cap=0.20,
    mining_lock_months=0,
    mining_lock_ratio_early=0.70,
    mining_lock_ratio_months=6,
    gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=False,
    vest_volume_peg_pct=0.0,
    mining_volume_cap_pct=0.0,
    state_driven=True,
    global_monthly_cap_pct=1.0,
)

MODELS: List[Model] = [
    ORIGINAL_MODEL,
    HYBRID_MODEL,
    PROTOCOL_V26,
    PROTOCOL_V30,
    PROTOCOL_V31,
    HYBRID_B,
    HYBRID_TOKENOMICS,
]


# =============================================================================
# HELPERS
# =============================================================================


def apply_liquidity_events(base_liquidity: float, month: int, events: List[Tuple[int, float]], noise: List[Tuple[int, float]]) -> float:
    liq = base_liquidity
    for m, pct in events:
        if month >= m:
            liq *= (1.0 + pct)
    for m, pct in noise:
        if month >= m:
            liq *= (1.0 + pct)
    return liq


def gen_noise() -> List[Tuple[int, float]]:
    # mild noise (±2%) per month
    return [(m, random.uniform(-0.02, 0.02)) for m in range(1, 13)]


def prelaunch_circulating(month: int) -> int:
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6.0
    return immediate + int(min(month, 6) * monthly_gradual)


def ramp_rate(month: int) -> float:
    ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    r = 0.20
    for m, v in sorted(ramp_rates.items()):
        if month >= m:
            r = v
    return r


def daily_volume_usd_proxy(liquidity: float) -> float:
    """
    Proxy for 24h DEX volume.
    We use a stochastic turnover fraction of liquidity (2%..10% daily).
    """
    return liquidity * random.uniform(0.02, 0.10)


def tge_tokens(model: Model) -> int:
    return int(BASE_COINS * model.tge_percent / 100.0)


def scheduled_vested_cumulative(month: int, model: Model) -> int:
    if month <= 0:
        return tge_tokens(model)
    if month <= model.cliff_months:
        return tge_tokens(model)
    months_vesting = month - model.cliff_months
    remaining = (100.0 - model.tge_percent) / 100.0
    monthly_rate = remaining / model.vesting_months
    vested_pct = (model.tge_percent / 100.0) + months_vesting * monthly_rate
    return int(BASE_COINS * min(vested_pct, 1.0))


def vwap_30(prices: Deque[float]) -> float:
    if not prices:
        return TARGET_PRICE
    recent = list(prices)[-min(30, len(prices)):]
    return statistics.mean(recent) if recent else TARGET_PRICE


def state_driven_monthly_release_rate(model: Model, price: float, vwap: float, liquidity: float, trend: List[float]) -> float:
    # negative trend => 0
    if liquidity < MIN_LIQUIDITY or price < EMERGENCY_PRICE:
        return 0.0
    if trend and (price - trend[0]) / trend[0] < -0.10:
        return 0.0
    stable = vwap > 0 and abs(price - vwap) / vwap < 0.20
    rate = 0.003 if stable else 0.007
    if model.global_monthly_cap_pct is not None:
        rate = min(rate, model.global_monthly_cap_pct / 100.0)
    return rate


# =============================================================================
# CORE SIMULATION (month-by-month)
# =============================================================================


def simulate_path(model: Model, base_liquidity: float, events: List[Tuple[int, float]], months: int = 12) -> Dict:
    noise = gen_noise()
    prices: Deque[float] = deque(maxlen=120)

    vested_cum = tge_tokens(model)
    mining_cum = 0
    emergency_month = 0

    month_prices: List[float] = []
    month_liq: List[float] = []
    month_vested: List[int] = []
    month_mined: List[int] = []

    for month in range(0, months + 1):
        liq = apply_liquidity_events(base_liquidity, month, events, noise)
        month_liq.append(liq)

        # --- mining: compute monthly mined entering circulating
        if month == 0:
            mined_this_month = 0
        else:
            # base emission ramp
            daily = DAILY_MINING_MAX * ramp_rate(month)
            if model.emission_cap is not None:
                daily = min(daily, DAILY_MINING_MAX * model.emission_cap)

            # volume-capped mining (v3.1)
            if model.mining_volume_cap_pct > 0:
                # if no price yet, approximate with target
                price_for_cap = prices[-1] if prices else TARGET_PRICE
                dv = daily_volume_usd_proxy(liq)
                cap_tokens = (dv * model.mining_volume_cap_pct) / max(price_for_cap, 1e-9)
                daily = min(daily, cap_tokens)

            mined_this_month = int(daily * 30)

            # extra early lock ratio (Hybrid Tokenomics)
            if model.mining_lock_ratio_early > 0 and month <= model.mining_lock_ratio_months:
                mined_this_month = int(mined_this_month * (1.0 - model.mining_lock_ratio_early))

            # long mining lock (Protocol v3.0)
            if model.mining_lock_months > 0 and month <= model.mining_lock_months:
                mined_this_month = 0

        mining_cum += mined_this_month

        # --- vesting: compute monthly delta and apply gates/caps
        if month == 0:
            vested_cum = tge_tokens(model)
        else:
            # default scheduled delta
            scheduled = scheduled_vested_cumulative(month, model)
            scheduled_prev = scheduled_vested_cumulative(month - 1, model)
            scheduled_delta = max(0, scheduled - scheduled_prev)

            # start with scheduled delta; adjust per model mechanics
            delta = scheduled_delta

            # compute nominal price from last price if available, else rough estimate
            pre = prelaunch_circulating(month)
            total_nominal = vested_cum + mining_cum + pre
            staked_nominal = int(total_nominal * model.mandatory_stake_pct)
            effective_nominal = max(1, total_nominal - staked_nominal)
            price_nominal = liq / effective_nominal

            # update emergency/brake tracking
            if emergency_month == 0 and (price_nominal < EMERGENCY_PRICE or liq < MIN_LIQUIDITY):
                emergency_month = month

            # emergency brake (v3.0, v3.1, hybrid-type)
            if model.brake_low is not None and price_nominal < model.brake_low:
                delta = 0

            # price gate (v2.6 hard stop, v3.1 uses volume peg in-band)
            if model.gate_high is not None and price_nominal < model.gate_high:
                if model.use_volume_peg and (model.brake_low is None or price_nominal >= model.brake_low):
                    # cap delta by 2% of daily volume converted to tokens
                    dv = daily_volume_usd_proxy(liq)
                    max_tokens = (dv * model.vest_volume_peg_pct) / max(price_nominal, 1e-9)
                    delta = min(delta, int(max_tokens * 30))  # approximate monthly cap from daily cap
                else:
                    # Protocol v2.6: stop; Protocol v3.0: reduced drip (10% of scheduled)
                    if model.name == "Protocol v3.0":
                        delta = int(delta * 0.10)
                    else:
                        delta = 0

            # state-driven overrides schedule after month 6
            if model.state_driven:
                if month <= model.cliff_months:
                    delta = 0
                elif month <= 6:
                    delta = 0
                else:
                    v = vwap_30(prices)
                    trend = list(prices)[-min(10, len(prices)):] if prices else []
                    rate = state_driven_monthly_release_rate(model, price_nominal, v, liq, trend)
                    delta = int(BASE_COINS * rate)

            vested_cum = min(BASE_COINS, vested_cum + delta)

        # compute final price with updated components
        pre = prelaunch_circulating(month)
        total = vested_cum + mining_cum + pre
        staked = int(total * model.mandatory_stake_pct)
        effective = max(1, total - staked)
        price = liq / effective
        prices.append(price)

        month_prices.append(price)
        month_vested.append(vested_cum)
        month_mined.append(mining_cum)

    return {
        "prices": month_prices,
        "liquidity": month_liq,
        "vested_cum": month_vested,
        "mined_cum": month_mined,
        "emergency_month": emergency_month,
    }


# =============================================================================
# ROI
# =============================================================================


def investor_base_tokens(investment_usd: float) -> int:
    total = int(investment_usd / PRESALE_PRICE)
    return total // 2


def investor_value_at_month(model: Model, path: Dict, month: int, investment_usd: float) -> float:
    base = investor_base_tokens(investment_usd)
    vested_pct = path["vested_cum"][month] / BASE_COINS
    vested_tokens = int(base * vested_pct)
    return vested_tokens * path["prices"][month]


def roi_pct(value: float, investment: float) -> float:
    return (value / investment - 1.0) * 100.0


# =============================================================================
# RUNS
# =============================================================================


def gen_market_events(market_type: str) -> List[Tuple[int, float]]:
    if market_type == "bull":
        return [(m, random.uniform(0.05, 0.10)) for m in [2, 4, 6, 8, 10, 12]]
    if market_type == "bear":
        return [(m, random.uniform(-0.10, -0.05)) for m in [2, 4, 6, 8, 10, 12]]
    if market_type == "volatile":
        return [(m, random.choice([-1, 1]) * random.uniform(0.15, 0.30)) for m in [2, 4, 6, 8, 10, 12]]
    return [(m, random.uniform(-0.03, 0.03)) for m in [2, 4, 6, 8, 10, 12]]


def run_100_market_type_sims(seed: int = 3131) -> Dict[str, List[Dict]]:
    random.seed(seed)
    sims_per_market = 25
    out: Dict[str, List[Dict]] = {}
    for model in MODELS:
        rows: List[Dict] = []
        for mt in MARKET_TYPES:
            for i in range(sims_per_market):
                events = gen_market_events(mt)
                path = simulate_path(model, DEFAULT_LIQUIDITY, events, months=12)
                v12 = investor_value_at_month(model, path, 12, INVESTMENT_REF)
                rows.append(
                    {
                        "market_type": mt,
                        "sim_id": i,
                        "month_12_price": path["prices"][12],
                        "min_price": min(path["prices"]),
                        "emergency_month": path["emergency_month"],
                        "month_12_value": v12,
                        "month_12_roi": roi_pct(v12, INVESTMENT_REF),
                    }
                )
        out[model.name] = rows
    return out


def run_100_choppy_sims(seed: int = 3132) -> Dict[str, Dict[str, List[Dict]]]:
    random.seed(seed)
    out: Dict[str, Dict[str, List[Dict]]] = {}
    for model in MODELS:
        out[model.name] = {}
        for key, sc in CHOPPY_SCENARIOS.items():
            rows: List[Dict] = []
            for i in range(100):
                path = simulate_path(model, DEFAULT_LIQUIDITY, sc["events"], months=12)
                v12 = investor_value_at_month(model, path, 12, INVESTMENT_REF)
                rows.append(
                    {
                        "run_id": i,
                        "month_12_price": path["prices"][12],
                        "min_price": min(path["prices"]),
                        "emergency_month": path["emergency_month"],
                        "month_12_value": v12,
                        "month_12_roi": roi_pct(v12, INVESTMENT_REF),
                    }
                )
            out[model.name][key] = rows
    return out


def summarize(rows: List[Dict]) -> Dict:
    rois = [r["month_12_roi"] for r in rows]
    return {
        "roi_avg": statistics.mean(rois),
        "roi_median": statistics.median(rois),
        "roi_p10": statistics.quantiles(rois, n=10)[0],
        "roi_p90": statistics.quantiles(rois, n=10)[-1],
        "brake_rate": sum(1 for r in rows if r["emergency_month"] != 0) / len(rows) * 100.0,
        "avg_price_12": statistics.mean([r["month_12_price"] for r in rows]),
    }


def main() -> None:
    print("=" * 80)
    print("THIRD OPINION (v3.1): 100 sims + choppy scenarios")
    print("=" * 80)
    print(f"Models: {[m.name for m in MODELS]}")

    print("\nPhase 1: 100 sims/model across market types...")
    primary = run_100_market_type_sims()

    print("Phase 2: 100 sims/model for each choppy scenario...")
    choppy = run_100_choppy_sims()

    primary_summary = {m: summarize(rows) for m, rows in primary.items()}
    choppy_summary = {m: {k: summarize(rows) for k, rows in scenarios.items()} for m, scenarios in choppy.items()}

    out = {
        "timestamp": datetime.now().isoformat(),
        "methodology": "Third opinion: path-dependent sequential sim with volume-limited vesting/mining (v3.1), stochastic volume proxy, and monthly liquidity noise.",
        "models": [m.__dict__ for m in MODELS],
        "liquidity": DEFAULT_LIQUIDITY,
        "investment_ref": INVESTMENT_REF,
        "primary_100": primary,
        "choppy_100": choppy,
        "summaries": {
            "primary": primary_summary,
            "choppy": choppy_summary,
        },
    }

    with open("third_opinion_v31_results.json", "w") as f:
        json.dump(out, f, indent=2)

    # markdown report
    def pct(x: float) -> str:
        return f"{x:+.1f}%"

    lines: List[str] = []
    lines.append("# Third Opinion Report (adds Protocol v3.1)\n\n")
    lines.append(f"**Generated**: {out['timestamp']}\n\n")
    lines.append(f"**Liquidity**: ${DEFAULT_LIQUIDITY/1e6:.0f}M, **Investment ref**: ${INVESTMENT_REF:,}\n\n")
    lines.append("## Primary (100 sims across bull/bear/normal/volatile)\n\n")
    lines.append("| Model | Avg ROI | P10..P90 ROI | Brake rate |\n")
    lines.append("|---|---:|---:|---:|\n")
    for m in MODELS:
        s = primary_summary[m.name]
        lines.append(f"| {m.name} | {pct(s['roi_avg'])} | {pct(s['roi_p10'])}..{pct(s['roi_p90'])} | {s['brake_rate']:.1f}% |\n")

    lines.append("\n## Choppy markets (10 scenarios, 100 runs each) — Avg ROI\n\n")
    lines.append("| Scenario | " + " | ".join([m.name for m in MODELS]) + " |\n")
    lines.append("|---|" + "|".join(["---:" for _ in MODELS]) + "|\n")
    for key, sc in CHOPPY_SCENARIOS.items():
        row = [sc["name"]]
        for m in MODELS:
            row.append(pct(choppy_summary[m.name][key]["roi_avg"]))
        lines.append("| " + " | ".join(row) + " |\n")

    with open("THIRD_OPINION_V31_REPORT.md", "w") as f:
        f.write("".join(lines))

    print("\n✅ Wrote third_opinion_v31_results.json and THIRD_OPINION_V31_REPORT.md")


if __name__ == "__main__":
    main()


