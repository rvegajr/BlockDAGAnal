#!/usr/bin/env python3
"""
Real-World Backtest (Second Opinion)
===================================

Purpose
-------
Replace synthetic market generators (bull/bear/volatile/choppy) with a replay of
historical crypto market regimes from a time series (e.g., BTC or ETH).

We reuse the same "second opinion" microstructure assumptions:
- baseline price = Liquidity / EffectiveCirculating
- apply order-book impact from sell pressure (vesting/mining/migration)

What changes vs synthetic harness:
- liquidity is *path-driven* by the historical market series (monthly returns/volatility)
- optional "buy support" component derived from market volume/returns (simple proxy)

Inputs
------
CSV with at least:
- date (YYYY-MM-DD)
- close (float)
- volume (float, optional but recommended)

Outputs
-------
- backtest_second_opinion_results.json
- docs/vesting/REAL_WORLD_BACKTEST_REPORT.md
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import random

# Import core model logic by copying the model params and pricing logic from
# scripts/hybrid_tokenomics_second_opinion_compare.py (kept local for stability).

# =============================================================================
# CONSTANTS (match second-opinion harness defaults)
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

PRESALE_PRICE = 0.01
INVESTMENT_REF_USD = 9000

ROI_HORIZONS = [12, 24, 36, 48, 72]


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
    price_gate_high: Optional[float] = None
    brake_low: Optional[float] = None
    drip_factor_between: Optional[float] = None
    mining_lock_months: int = 0
    use_volume_peg: bool = False
    vest_volume_peg_pct: float = 0.0
    mining_volume_cap_pct: float = 0.0


MODELS = [
    ModelParams("Original Model", 2.0, 12, 60, 0.20, 50.0),
    ModelParams("Hybrid Model", 3.0, 3, 36, 0.20, 50.0),
    ModelParams("Protocol v2.6", 3.0, 3, 21, 1.0, 0.0, price_gate_high=0.05, drip_factor_between=0.0),
    ModelParams("Protocol v3.0", 3.0, 3, 33, 0.20, 0.0, price_gate_high=0.05, brake_low=0.02, drip_factor_between=0.10, mining_lock_months=24),
    ModelParams(
        "Protocol v3.1 (Adjusted)",
        3.0,
        3,
        21,
        1.0,
        0.0,
        price_gate_high=0.05,
        brake_low=0.02,
        use_volume_peg=True,
        vest_volume_peg_pct=0.02,
        mining_volume_cap_pct=0.20,
    ),
    ModelParams("Hybrid B", 3.0, 3, 36, 0.20, 50.0, state_driven_release=True, global_monthly_cap=1.0, price_gate_high=0.05, brake_low=0.02),
    ModelParams(
        "Hybrid Tokenomics (Solvency-Anchored)",
        3.0,
        3,
        36,
        0.20,
        60.0,
        state_driven_release=True,
        global_monthly_cap=1.0,
        mining_lock_ratio=0.70,
        price_gate_high=0.05,
        brake_low=0.02,
    ),
]


# =============================================================================
# Helpers (copied / aligned with second-opinion harness)
# =============================================================================


def investor_base_tokens(investment_usd: float) -> int:
    total_tokens = int(investment_usd / PRESALE_PRICE)
    return total_tokens // 2


def sample_sell_fraction() -> float:
    # Same distribution as the second-opinion harness
    r = random.random()
    if r < 0.20:
        return random.uniform(0.70, 1.00)  # panic
    if r < 0.50:
        return random.uniform(0.30, 0.70)  # partial
    if r < 0.85:
        return random.uniform(0.05, 0.20)  # holder
    return random.uniform(0.00, 0.05)      # long_term


def apply_order_book_impact(reference_price: float, liquidity: float, sell_volume_usd: float, extra_buy_support_usd: float = 0.0) -> float:
    # Allow a simple "real-world" proxy: extra_buy_support offsets net sell USD.
    net_sell = max(0.0, sell_volume_usd - max(0.0, extra_buy_support_usd))
    buy_support = liquidity * BUY_SUPPORT_PCT
    if buy_support <= 0:
        return reference_price * (1 - MAX_IMPACT)
    impact = min(MAX_IMPACT, (net_sell / buy_support) * DEPTH_FACTOR)
    return max(0.000001, reference_price * (1.0 - impact))


def cumulative_prelaunch_migrated(month: int) -> int:
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6.0
    return immediate + int(min(month, 6) * monthly_gradual)


def daily_volume_usd_proxy(liquidity: float) -> float:
    return liquidity * random.uniform(0.02, 0.10)


def monthly_mining_liquid(month: int, params: ModelParams, liquidity: float, last_price: float) -> int:
    if month <= 0:
        return 0
    ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    rate = 0.20
    for m, r in sorted(ramp_rates.items()):
        if month >= m:
            rate = r
    daily = DAILY_MINING_MAX * rate
    capped_daily = min(daily, DAILY_MINING_MAX * params.emission_cap)

    if params.mining_lock_months and month <= params.mining_lock_months:
        return 0

    monthly = int(capped_daily * 30)

    # v3.1 mining volume cap
    if params.mining_volume_cap_pct and params.mining_volume_cap_pct > 0:
        dv = daily_volume_usd_proxy(liquidity)
        cap_tokens_month = int(((dv * params.mining_volume_cap_pct) / max(last_price, 1e-9)) * 30)
        monthly = min(monthly, cap_tokens_month)

    # Hybrid Tokenomics early lock ratio
    if params.mining_lock_ratio is not None and month <= 6:
        monthly = int(monthly * (1.0 - params.mining_lock_ratio))

    return monthly


def scheduled_vest_delta(month: int, params: ModelParams, last_price: float, liquidity: float) -> int:
    if month <= params.cliff_months:
        return 0

    tge = int(BASE_COINS * params.tge_percent / 100.0)
    remaining = BASE_COINS - tge
    vested_delta = int(remaining / max(params.vesting_months, 1))

    # emergency brake
    if params.brake_low is not None and last_price < params.brake_low:
        vested_delta = 0

    # gate behavior
    if params.price_gate_high is not None and last_price < params.price_gate_high:
        if params.use_volume_peg and params.vest_volume_peg_pct > 0 and (params.brake_low is None or last_price >= params.brake_low):
            dv = daily_volume_usd_proxy(liquidity)
            cap_tokens_month = int(((dv * params.vest_volume_peg_pct) / max(last_price, 1e-9)) * 30)
            vested_delta = min(vested_delta, cap_tokens_month)
        elif params.drip_factor_between is not None:
            vested_delta = int(vested_delta * params.drip_factor_between)
        else:
            vested_delta = 0

    return max(0, vested_delta)


# =============================================================================
# Market data ingestion + monthly regime conversion
# =============================================================================


@dataclass(frozen=True)
class DailyBar:
    date: str
    close: float
    volume: Optional[float]


def read_csv_bars(path: Path) -> List[DailyBar]:
    rows: List[DailyBar] = []
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            date = (r.get("date") or r.get("Date") or "").strip()
            close_s = (r.get("close") or r.get("Close") or "").strip()
            vol_s = (r.get("volume") or r.get("Volume") or "").strip()
            if not date or not close_s:
                continue
            close = float(close_s)
            vol = float(vol_s) if vol_s else None
            rows.append(DailyBar(date=date, close=close, volume=vol))
    # assume already sorted; sort defensively
    rows.sort(key=lambda x: x.date)
    return rows


def to_monthly(bars: List[DailyBar]) -> List[Dict]:
    """
    Build monthly series:
    - month (YYYY-MM)
    - close (month-end close)
    - volume (sum, if available)
    - return (pct change vs prior month close)
    - vol30 (proxy: stdev of daily log returns within month; falls back to |return|)
    """
    if not bars:
        return []

    # group by YYYY-MM
    by_m: Dict[str, List[DailyBar]] = {}
    for b in bars:
        m = b.date[:7]
        by_m.setdefault(m, []).append(b)

    months = sorted(by_m.keys())
    out: List[Dict] = []
    prev_close: Optional[float] = None
    for m in months:
        chunk = by_m[m]
        close = chunk[-1].close
        vol_sum = None
        vols = [c.volume for c in chunk if c.volume is not None]
        if vols:
            vol_sum = float(sum(vols))

        # daily log returns for volatility proxy
        rets = []
        for i in range(1, len(chunk)):
            a = chunk[i - 1].close
            b = chunk[i].close
            if a > 0 and b > 0:
                rets.append(math.log(b / a))
        vol30 = statistics.pstdev(rets) if len(rets) >= 2 else 0.0

        r_m = (close / prev_close - 1.0) if prev_close else 0.0
        if vol30 == 0.0:
            vol30 = abs(r_m)  # fallback

        out.append({"month": m, "close": close, "volume": vol_sum, "ret": r_m, "vol": vol30})
        prev_close = close

    return out


# =============================================================================
# Backtest mapping: monthly market -> liquidity path + buy support proxy
# =============================================================================


@dataclass(frozen=True)
class ReplayConfig:
    launch_liquidity: float
    liquidity_beta: float
    liquidity_vol_penalty: float
    buy_support_beta: float
    use_volume: bool
    # “Ideal / adoption overlay”: structural liquidity growth independent of market returns
    liquidity_cagr_annual: float  # e.g. 0.50 => +50% per year
    net_inflow_monthly_pct: float  # e.g. 0.01 => +1% additive monthly inflow


def replay_months(
    monthly: List[Dict],
    start_idx: int,
    months: int,
    cfg: ReplayConfig,
) -> Tuple[List[float], List[float], List[str]]:
    """
    Returns (liquidity_path[0..months], buy_support_path[0..months], labels[0..months])
    Month 0 uses start month level; following months apply market-derived multipliers.
    """
    liq = cfg.launch_liquidity
    liquidity_path = []
    buy_support_path = []
    labels = []

    # Convert overlays to monthly multipliers
    cagr_monthly = (1.0 + cfg.liquidity_cagr_annual) ** (1.0 / 12.0) - 1.0 if cfg.liquidity_cagr_annual else 0.0

    for t in range(0, months + 1):
        row = monthly[start_idx + t]
        r = float(row["ret"])
        v = float(row["vol"])

        # liquidity moves with market return but is penalized by volatility
        liq *= max(0.05, (1.0 + cfg.liquidity_beta * r) * (1.0 - cfg.liquidity_vol_penalty * v))
        # adoption overlay: compound growth + additive inflow
        if cagr_monthly:
            liq *= (1.0 + cagr_monthly)
        if cfg.net_inflow_monthly_pct:
            liq += cfg.launch_liquidity * cfg.net_inflow_monthly_pct
        liq = max(MIN_LIQUIDITY * 0.5, liq)  # allow some degradation but keep numeric stability

        # extra buy support proxy:
        # - increases with positive returns (risk-on)
        # - optionally scales with market volume (normalized later by beta)
        vol_factor = 1.0
        if cfg.use_volume and row.get("volume"):
            # normalize with log to avoid crazy magnitudes; treat as relative within window
            vol_factor = 1.0 + math.log(1.0 + float(row["volume"])) / 100.0

        buy_support = max(0.0, cfg.buy_support_beta * cfg.launch_liquidity * max(0.0, r) * vol_factor)

        liquidity_path.append(liq)
        buy_support_path.append(buy_support)
        labels.append(row["month"])

    return liquidity_path, buy_support_path, labels


# =============================================================================
# Backtest simulation (token mechanics + price impact), horizon ROI
# =============================================================================


def investor_vested_pct(month: int, params: ModelParams, emergency_brake_month: int) -> float:
    # aligned to our second-opinion harness: schedule-based for time-based; simple proxy for state-driven
    if month == 0:
        return params.tge_percent / 100.0
    if month <= params.cliff_months:
        return params.tge_percent / 100.0

    if not params.state_driven_release:
        months_vesting = month - params.cliff_months
        remaining_pct = (100.0 - params.tge_percent) / 100.0
        monthly_vest_rate = remaining_pct / params.vesting_months
        vested_pct = params.tge_percent / 100.0 + months_vesting * monthly_vest_rate
        return min(vested_pct, 1.0)

    if month <= 6:
        return params.tge_percent / 100.0
    if emergency_brake_month and emergency_brake_month <= month:
        return params.tge_percent / 100.0
    months_releasing = month - 6
    vested = (params.tge_percent / 100.0) + (0.003 * months_releasing)
    return min(vested, 1.0)


def simulate_replay_path(
    params: ModelParams,
    liquidity_path: List[float],
    buy_support_path: List[float],
    months: int,
) -> Dict:
    vested_cum = int(BASE_COINS * params.tge_percent / 100.0)
    mining_cum = 0
    prelaunch_prev = 0
    emergency_brake_month = 0

    prices: List[float] = []

    for month in range(0, months + 1):
        liq = float(liquidity_path[month])
        last_price = prices[-1] if prices else TARGET_PRICE

        # vesting delta
        if params.state_driven_release:
            # keep consistent with second-opinion: no vesting until month 6, then small rate if not braked
            if month <= 6 or (emergency_brake_month and emergency_brake_month <= month):
                vested_delta = 0
            else:
                rate = 0.003
                if params.global_monthly_cap is not None:
                    rate = min(rate, params.global_monthly_cap / 100.0)
                vested_delta = int(BASE_COINS * rate)
        else:
            vested_delta = scheduled_vest_delta(month, params, last_price, liq)

        vested_cum = min(BASE_COINS, vested_cum + vested_delta)

        # mining
        mined = monthly_mining_liquid(month, params, liq, last_price)
        mining_cum += mined

        # prelaunch migration
        prelaunch_cum = cumulative_prelaunch_migrated(month)
        prelaunch_delta = max(0, prelaunch_cum - prelaunch_prev)
        prelaunch_prev = prelaunch_cum

        total_liquidish = vested_cum + mining_cum + prelaunch_cum
        staked = int(total_liquidish * (params.mandatory_stake_pct / 100.0))
        effective_circ = max(1, total_liquidish - staked)
        reference_price = liq / effective_circ

        # sell pressure
        vest_sell_usd = vested_delta * sample_sell_fraction() * reference_price
        miner_sell_usd = mined * random.uniform(0.50, 0.70) * reference_price
        pre_sell_usd = prelaunch_delta * random.uniform(0.10, 0.40) * reference_price
        sell_usd = vest_sell_usd + miner_sell_usd + pre_sell_usd

        price = apply_order_book_impact(reference_price, liq, sell_usd, extra_buy_support_usd=buy_support_path[month])
        prices.append(price)

        if emergency_brake_month == 0 and (price < EMERGENCY_PRICE or liq < MIN_LIQUIDITY):
            emergency_brake_month = month

    return {"prices": prices, "emergency_brake_month": emergency_brake_month}


def roi_pct(value: float, investment: float) -> float:
    return (value / investment - 1.0) * 100.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to daily CSV with date,close,(volume)")
    ap.add_argument("--launch-liquidity", type=float, default=32_000_000, help="Launch liquidity in USD")
    ap.add_argument("--seed", type=int, default=2026, help="Random seed for sell-behavior Monte Carlo")
    ap.add_argument("--runs", type=int, default=50, help="Monte Carlo runs per window per model (sell behavior)")
    ap.add_argument("--window-months", type=int, default=72, help="Window length in months (must cover horizons)")
    ap.add_argument("--step-months", type=int, default=1, help="Rolling window step in months")
    ap.add_argument("--liquidity-beta", type=float, default=1.25, help="How strongly liquidity follows market returns")
    ap.add_argument("--liquidity-vol-penalty", type=float, default=0.75, help="How strongly volatility reduces liquidity")
    ap.add_argument("--buy-support-beta", type=float, default=0.40, help="Extra buy-support USD proxy from positive returns")
    ap.add_argument(
        "--liquidity-cagr-annual",
        type=float,
        default=0.0,
        help="Adoption overlay: structural annual liquidity CAGR (e.g. 0.5 = +50 pct/yr)",
    )
    ap.add_argument(
        "--net-inflow-monthly-pct",
        type=float,
        default=0.0,
        help="Adoption overlay: additive monthly inflow as pct of launch liquidity (e.g. 0.01 = +1 pct/mo)",
    )
    ap.add_argument("--use-volume", action="store_true", help="Use volume column (if present) to scale buy support")
    args = ap.parse_args()

    random.seed(args.seed)
    csv_path = Path(args.csv)
    bars = read_csv_bars(csv_path)
    monthly = to_monthly(bars)

    if len(monthly) < args.window_months + 1:
        raise SystemExit(f"Not enough monthly data ({len(monthly)}) for window {args.window_months} months")

    cfg = ReplayConfig(
        launch_liquidity=args.launch_liquidity,
        liquidity_beta=args.liquidity_beta,
        liquidity_vol_penalty=args.liquidity_vol_penalty,
        buy_support_beta=args.buy_support_beta,
        use_volume=args.use_volume,
        liquidity_cagr_annual=args.liquidity_cagr_annual,
        net_inflow_monthly_pct=args.net_inflow_monthly_pct,
    )

    base_tokens = investor_base_tokens(INVESTMENT_REF_USD)
    horizons = [h for h in ROI_HORIZONS if h <= args.window_months]

    windows = []
    for start in range(0, len(monthly) - args.window_months, args.step_months):
        liq_path, buy_path, labels = replay_months(monthly, start, args.window_months, cfg)
        windows.append({"start_month": labels[0], "end_month": labels[-1], "liq_path": liq_path, "buy_path": buy_path, "labels": labels})

    out = {
        "timestamp": datetime.now().isoformat(),
        "input_csv": str(csv_path),
        "methodology": "Second opinion replay (historical monthly regimes → liquidity path + optional buy-support proxy).",
        "config": cfg.__dict__,
        "investment_ref_usd": INVESTMENT_REF_USD,
        "roi_horizons_months": horizons,
        "window_months": args.window_months,
        "step_months": args.step_months,
        "runs_per_window": args.runs,
        "models": [m.__dict__ for m in MODELS],
        "results": [],
    }

    for w in windows:
        wres = {"start_month": w["start_month"], "end_month": w["end_month"], "by_model": {}}
        for model in MODELS:
            runs = []
            for _ in range(args.runs):
                sim = simulate_replay_path(model, w["liq_path"], w["buy_path"], months=args.window_months)
                em = int(sim["emergency_brake_month"])
                rec = {"emergency_brake_month": em, "by_horizon": {}}
                for h in horizons:
                    price = sim["prices"][h]
                    pct = investor_vested_pct(h, model, em)
                    vested = int(base_tokens * pct)
                    value = vested * price
                    rec["by_horizon"][str(h)] = {"price": price, "value": value, "roi_pct": roi_pct(value, INVESTMENT_REF_USD)}
                runs.append(rec)
            # summarize
            summary = {}
            for h in horizons:
                hs = str(h)
                rois = [r["by_horizon"][hs]["roi_pct"] for r in runs]
                values = [r["by_horizon"][hs]["value"] for r in runs]
                brakes = sum(1 for r in runs if r["emergency_brake_month"] and r["emergency_brake_month"] <= h)
                summary[hs] = {
                    "roi_avg": statistics.mean(rois),
                    "roi_median": statistics.median(rois),
                    "roi_p10": statistics.quantiles(rois, n=10)[0],
                    "roi_p90": statistics.quantiles(rois, n=10)[-1],
                    "value_avg": statistics.mean(values),
                    "brake_rate_pct": brakes / len(runs) * 100.0,
                    "positive_rate_pct": sum(1 for x in rois if x > 0) / len(rois) * 100.0,
                }
            wres["by_model"][model.name] = {"summary": summary}
        out["results"].append(wres)

    Path("backtest_second_opinion_results.json").write_text(json.dumps(out, indent=2))

    # Markdown report: winners by horizon across all windows (avg ROI) + positive-hit rate
    lines: List[str] = []
    lines.append("# Real-World Backtest Report (Second Opinion Replay)\n\n")
    lines.append(f"**Generated**: {out['timestamp']}\n\n")
    lines.append(f"**Input**: `{out['input_csv']}`\n\n")
    lines.append(f"**Windows**: {len(out['results'])} rolling windows, {args.window_months} months each (step {args.step_months})\n\n")
    lines.append(f"**Runs/window/model**: {args.runs}\n\n")
    lines.append(f"**Investment reference**: ${INVESTMENT_REF_USD:,}\n\n")

    lines.append("## Winner by horizon (avg ROI across all rolling windows)\n\n")
    lines.append("| Horizon | Winner | Avg ROI | Avg positive rate |\n")
    lines.append("|---:|---|---:|---:|\n")
    for h in horizons:
        hs = str(h)
        avg_by_model = {}
        pos_by_model = {}
        for model in MODELS:
            rois = [w['by_model'][model.name]['summary'][hs]['roi_avg'] for w in out['results']]
            poss = [w['by_model'][model.name]['summary'][hs]['positive_rate_pct'] for w in out['results']]
            avg_by_model[model.name] = sum(rois) / len(rois)
            pos_by_model[model.name] = sum(poss) / len(poss)
        win = max(avg_by_model.items(), key=lambda kv: kv[1])
        lines.append(f"| Month {h} | **{win[0]}** | {win[1]:+.1f}% | {pos_by_model[win[0]]:.1f}% |\n")

    lines.append("\n## Notes\n")
    lines.append("- This is still a *tokenomics stress test* (it includes sell pressure + order-book impact). It becomes more “real-world” by replaying historical market regimes into liquidity/buy-support.\n")
    lines.append("- For true realism you’d also want: project-specific demand modeling (users, fees, incentives), exchange listings, and actual DEX liquidity growth curves.\n")

    out_md = Path("docs/vesting/REAL_WORLD_BACKTEST_REPORT.md")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(lines))

    print("✅ wrote backtest_second_opinion_results.json")
    print("✅ wrote docs/vesting/REAL_WORLD_BACKTEST_REPORT.md")


if __name__ == "__main__":
    main()


