#!/usr/bin/env python3
"""
Real-World Multi-Opinion Backtest
=================================

Runs THREE independent "opinions" on historical market data:
1. **Conservative** (stress-test): no adoption overlay, raw historical regimes
2. **Ideal** (growth scenario): historical regimes + adoption overlay (liquidity CAGR + inflow)
3. **Choppy Overlay**: historical regimes with 10 choppy stress shocks overlaid

For each opinion we report:
- Per-model ROI/value at 12/24/36/48/72 months
- Market condition breakdown (bull/bear/volatile/normal based on regime classification)
- Positive ROI occurrence rates
- Winners per horizon

Investment levels: $9,000 / $50,000 / $100,000

Outputs:
- real_world_multi_opinion_results.json
- docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# =============================================================================
# CONSTANTS
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
DEFAULT_INVESTMENT_LEVELS = [9000, 50_000, 100_000]
ROI_HORIZONS = [12, 24, 36, 48, 72]

CHOPPY_SHOCKS = {
    "Normal Market Conditions": [],
    "May 2021-Style Crash": [(2, -0.60)],
    "FTX Collapse": [(3, -0.70)],
    "COVID Black Swan": [(1, -0.80)],
    "Gradual Bear Market": [(i, -0.05) for i in range(2, 13)],
    "Bull Run Then Crash": [(i, 0.15) for i in range(2, 7)] + [(7, -0.70)],
    "High Volatility": [(2, -0.30), (4, 0.40), (6, -0.40), (8, 0.30), (10, -0.30)],
    "Stable Growth": [(i, 0.02) for i in range(2, 13)],
    "Early Crash with Recovery": [(2, -0.50), (4, 0.25), (6, 0.50)],
    "Multiple Crashes": [(2, -0.40), (6, -0.40), (12, -0.40)],
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
    # === ORIGINAL 8 MODELS ===
    ModelParams("Original Model", 2.0, 12, 60, 0.20, 50.0),
    ModelParams("Hybrid Model", 3.0, 3, 36, 0.20, 50.0),
    ModelParams("Protocol v2.6", 3.0, 3, 21, 1.0, 0.0, price_gate_high=0.05, drip_factor_between=0.0),
    ModelParams("Protocol v3.0", 3.0, 3, 33, 0.20, 0.0, price_gate_high=0.05, brake_low=0.02, drip_factor_between=0.10, mining_lock_months=24),
    ModelParams(
        "Protocol v3.1 (Adjusted)", 3.0, 3, 21, 1.0, 0.0,
        price_gate_high=0.05, brake_low=0.02, use_volume_peg=True, vest_volume_peg_pct=0.02, mining_volume_cap_pct=0.20,
    ),
    ModelParams("Hybrid B", 3.0, 3, 36, 0.20, 50.0, state_driven_release=True, global_monthly_cap=1.0, price_gate_high=0.05, brake_low=0.02),
    ModelParams(
        "Hybrid Tokenomics (Solvency-Anchored)", 3.0, 3, 36, 0.20, 60.0,
        state_driven_release=True, global_monthly_cap=1.0, mining_lock_ratio=0.70, price_gate_high=0.05, brake_low=0.02,
    ),
    # Harris Model: 10% TGE, 9mo vesting, miner incentive (75% hold = 1.75x multiplier), 8% raffle burn
    # Source: https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf
    ModelParams(
        "Harris Model", 10.0, 0, 9, 0.20, 0.0,
        mining_lock_ratio=0.75,  # Miners incentivized to hold 75% for multiplier
    ),

    # === PROTOCOL FAMILY (v5.x) ===
    # Sources:
    # - https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/
    # - https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/
    # - https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/
    # - https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/
    ModelParams(
        "Protocol v5.3", 3.0, 3, 21, 0.20, 0.0,
        price_gate_high=0.05, brake_low=0.02, use_volume_peg=True, vest_volume_peg_pct=0.02, mining_volume_cap_pct=0.20,
    ),
    # Source: https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/
    # Same as v5.3 but with 48-month bonus vesting (longer lock = less pressure)
    ModelParams(
        "Protocol v5.5", 3.0, 3, 21, 0.20, 0.0,
        price_gate_high=0.05, brake_low=0.02, use_volume_peg=True, vest_volume_peg_pct=0.02, mining_volume_cap_pct=0.20,
        mining_lock_months=12,  # Extended bonus lock period effect
    ),
    # Source: https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/
    # REVISED: Adaptive Trend Shield (15% trailing MA), Dynamic Discharge (20% buy-wall), Circuit Breaker (auto-buyback), Block Streaming
    ModelParams(
        "Protocol v5.7", 3.0, 3, 21, 0.20, 0.0,
        price_gate_high=0.05, brake_low=0.02, use_volume_peg=True, vest_volume_peg_pct=0.02, mining_volume_cap_pct=0.20,
        drip_factor_between=0.15,  # Block-by-block streaming effect
    ),
    # Source: https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/
    # Same as v5.7 but with 48-month bonus vesting
    ModelParams(
        "Protocol v5.8", 3.0, 3, 21, 0.20, 0.0,
        price_gate_high=0.05, brake_low=0.02, use_volume_peg=True, vest_volume_peg_pct=0.02, mining_volume_cap_pct=0.20,
        drip_factor_between=0.15, mining_lock_months=12,  # Extended bonus lock + streaming
    ),

    # HybridC
    # Source: docs/HybridC_Tokenomics_Test.xlsx
    ModelParams(
        "HybridC", 3.0, 3, 36, 0.20, 50.0,
        state_driven_release=True, global_monthly_cap=0.3,  # Very conservative 0.3% monthly cap
        mining_lock_ratio=0.85,  # 85% mining locked (only 15% liquid per Excel)
        price_gate_high=0.05, brake_low=0.02,
    ),

    # === INGO CSV MODELS (additional) ===
    # Sources:
    # - docs/sources/Ingo  Projects/Hybrid.csv
    # - docs/sources/Ingo  Projects/hybrid C.csv
    # - docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Final.csv
    # - docs/sources/Ingo  Projects/Model_A_ROI_Final_Test.csv
    ModelParams(
        "Hybrid (Ingo CSV)", 3.0, 3, 36, 0.20, 0.0,
        state_driven_release=True, global_monthly_cap=0.70,
        mining_lock_ratio=0.70,
        price_gate_high=0.05, brake_low=0.02,
    ),
    ModelParams(
        "Hybrid C (Ingo CSV)", 3.0, 3, 36, 0.20, 55.0,
        state_driven_release=True, global_monthly_cap=0.30,
        mining_lock_ratio=0.65,
        price_gate_high=0.05, brake_low=0.02,
    ),
    ModelParams(
        "Hybrid C Lite+ (Final, Ingo CSV)", 3.0, 3, 36, 0.20, 30.0,
        state_driven_release=True, global_monthly_cap=0.45,
        mining_lock_ratio=0.55,
        price_gate_high=0.05, brake_low=0.02,
    ),
    # Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Defaults.csv
    ModelParams(
        "Hybrid C Lite (Defaults, Ingo CSV)", 3.0, 3, 36, 0.20, 45.0,
        state_driven_release=True, global_monthly_cap=0.45,
        mining_lock_ratio=0.55,
        price_gate_high=0.05, brake_low=0.02,
    ),
    ModelParams(
        "Model A (ROI Optimized, Ingo CSV)", 15.0, 0, 12, 1.0, 0.0,
        mining_lock_ratio=0.20,
    ),

    # === NEW INGO MODELS (from docs/sources/Ingo Projects/) ===

    # Hybrid D.1 - Technical Reference Model
    # Source: docs/sources/Ingo  Projects/Hybrid_D.1.csv
    # 0% or 3% TGE, 12mo linear vesting, 12mo bonus lock + 24mo bonus vesting
    # Smooth emission (Kaspa-full), +15% recovery limiter, throttle + emergency brake
    ModelParams(
        "Hybrid D.1 (Ingo CSV)", 3.0, 0, 12, 0.20, 0.0,
        state_driven_release=True,
        mining_lock_months=12,  # Bonus lock period
        price_gate_high=0.05, brake_low=0.02,
        drip_factor_between=0.15,  # Recovery limiter effect
    ),

    # Hybrid E.1 (0% TGE variant) - Official Governance Model
    # Source: docs/sources/Ingo  Projects/Hybrid_E_0__TGE.csv
    # 0% TGE, 12mo linear vesting (8.33%/month), 12mo bonus lock + 24mo bonus vesting
    # Smooth emission (-light), throttle + emergency brake (reduce only)
    ModelParams(
        "Hybrid E.1 0% TGE (Ingo CSV)", 0.0, 0, 12, 0.20, 0.0,
        state_driven_release=True,
        mining_lock_months=12,
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Hybrid E.1 (3% TGE variant)
    # Source: docs/sources/Ingo  Projects/Hybrid_E_3__TGE.csv
    ModelParams(
        "Hybrid E.1 3% TGE (Ingo CSV)", 3.0, 0, 12, 0.20, 0.0,
        state_driven_release=True,
        mining_lock_months=12,
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Hybrid F - Beat v3 on Y3, credible & implementable
    # Source: docs/sources/Ingo  Projects/Hybrid_F.csv
    # 3% TGE, 3mo cliff, 21mo streaming vesting, 12mo bonus lock + 24mo bonus vesting
    # Mining sell cap 15% of net buy, 7D MA throttle/brake, zero-spike enforcement
    ModelParams(
        "Hybrid F (Ingo CSV)", 3.0, 3, 21, 0.20, 0.0,
        state_driven_release=True,
        mining_lock_months=12,
        price_gate_high=0.05, brake_low=0.02,
        drip_factor_between=0.50,  # Throttle multiplier
        mining_volume_cap_pct=0.15,  # Mining sell cap 15% of volume
    ),

    # Hybrid F.1 - Adaptive throttle variant
    # Source: docs/sources/Ingo  Projects/Hybrid_F.1.csv
    # TGE options 0/3/6%, adaptive throttle 25%, +12% recovery boost
    ModelParams(
        "Hybrid F.1 (Ingo CSV)", 3.0, 3, 21, 0.20, 0.0,
        state_driven_release=True,
        mining_lock_months=12,
        price_gate_high=0.05, brake_low=0.02,
        drip_factor_between=0.25,  # Throttle rate 25%
    ),

    # Hybrid C Lite+ Extended - with stability logic
    # Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Extended.csv
    # 0.40-0.45% global cap, throttle enabled, emergency brake, 0.3% burn fee
    ModelParams(
        "Hybrid C Lite+ Extended (Ingo CSV)", 3.0, 3, 36, 0.20, 30.0,
        state_driven_release=True, global_monthly_cap=0.45,
        mining_lock_ratio=0.45,  # 45-50% mining liquid means ~55% locked
        price_gate_high=0.05, brake_low=0.02,
        drip_factor_between=0.50,  # Throttle zone multiplier
    ),

    # Hybrid B (Ingo detailed) - State-driven with strict controls
    # Source: docs/sources/Ingo  Projects/Hybrid B.csv
    # 3% TGE, 90d cliff, state-driven, 0.3-1.0% global cap, ≥70% mining locked
    ModelParams(
        "Hybrid B (Ingo Detailed)", 3.0, 3, 36, 0.20, 50.0,
        state_driven_release=True, global_monthly_cap=0.70,
        mining_lock_ratio=0.70,
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Protocol v7.0 (Definitive Edition) — mapped into this harness as close as possible.
    # Source: https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/
    # Notes:
    # - Adaptive Trend Shield (±25% MA) and circuit-breaker buybacks are not explicitly modeled here.
    # - Dynamic Discharge is approximated via mining volume cap (20% of proxy daily volume).
    # - Setup grace period is approximated via mining_lock_months=6.
    ModelParams(
        "Protocol v7.0", 3.0, 3, 21, 0.20, 0.0,
        price_gate_high=0.05, brake_low=0.02,
        drip_factor_between=0.15,
        mining_lock_months=6,
        mining_volume_cap_pct=0.20,
    ),

    # === ADDITIONAL INGO CSV MODELS (Jan 2026 Update) ===

    # Hybrid Lite - Simpler state-driven model
    # Source: docs/sources/Ingo  Projects/Hybrid Lite.csv
    # 0.40-0.45% global cap, state-driven, NORMAL/RESTRICTED/EMERGENCY
    # Mining: 45-50% liquid, 35-40% locked, 10-15% performance
    # Bonus: 35% BDAG / 65% Utility Credits
    ModelParams(
        "Hybrid Lite (Ingo CSV)", 0.0, 0, 12, 0.20, 30.0,
        state_driven_release=True, global_monthly_cap=0.45,
        mining_lock_ratio=0.55,  # 45-50% liquid means 50-55% locked
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Hybrid C Lite+ Base - Foundation model before Final optimizations
    # Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus.csv
    # 0.40-0.45% global cap, 20-40% auto-staking, same mining split as Hybrid Lite
    ModelParams(
        "Hybrid C Lite+ Base (Ingo CSV)", 3.0, 3, 36, 0.20, 35.0,
        state_driven_release=True, global_monthly_cap=0.45,
        mining_lock_ratio=0.50,
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Hybrid C Lite+ Variant A - 39% Bonus Paid (Conservative)
    # Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Bonus_Variants.csv
    # 39% BDAG / 61% non-circulating bonus treatment
    # High crash resilience, low queue activation, +12-18% ROI vs 25% model
    ModelParams(
        "Hybrid C Lite+ Variant A (Ingo CSV)", 3.0, 3, 36, 0.20, 40.0,
        state_driven_release=True, global_monthly_cap=0.40,
        mining_lock_ratio=0.60,  # Conservative: higher locking
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Hybrid C Lite+ Variant B - 39% Bonus Removed (Aggressive)
    # Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Bonus_Variants.csv
    # 61% BDAG / 39% removed from circulation
    # Higher early liquidity, +25-35% ROI vs 25% model, medium crash resilience
    ModelParams(
        "Hybrid C Lite+ Variant B (Ingo CSV)", 3.0, 3, 36, 0.20, 25.0,
        state_driven_release=True, global_monthly_cap=0.50,
        mining_lock_ratio=0.45,  # Aggressive: lower locking, more liquidity
        price_gate_high=0.05, brake_low=0.02,
    ),

    # Model A (with Bonus Separation) - ROI benchmark with explicit bonus split
    # Source: docs/sources/Ingo  Projects/Model_A_Roi_Final_With_Bonus.csv
    # 25% BDAG / 75% Utility Credits (non-priced), 15% TGE, 12mo linear vesting
    # Very high volatility/dump risk, optimized for pure ROI
    ModelParams(
        "Model A (Bonus Separated, Ingo CSV)", 15.0, 0, 12, 1.0, 0.0,
        mining_lock_ratio=0.20,
    ),

    # Model A (Base) - Original simpler ROI benchmark
    # Source: docs/sources/Ingo  Projects/Model_A_ROI.csv
    # 10-15% TGE, 12-24mo vesting, 70-80% mining liquid, optional states
    # 100% BDAG bonus, no utility credits
    ModelParams(
        "Model A (Base, Ingo CSV)", 12.0, 0, 18, 1.0, 0.0,
        mining_lock_ratio=0.25,  # 70-80% liquid = 20-30% locked
    ),
]


# =============================================================================
# HISTORICAL DATA LOADING
# =============================================================================

@dataclass
class MonthlyData:
    year_month: str
    month_return: float
    volatility: float
    volume: float
    regime: str  # bull / bear / volatile / normal


def load_csv_to_monthly(csv_path: str, use_volume: bool = True) -> List[MonthlyData]:
    daily: List[Tuple[str, float, float]] = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row.get("date") or row.get("Date") or row.get("DATE")
            close_str = row.get("close") or row.get("Close") or row.get("CLOSE") or row.get("price")
            vol_str = row.get("volume") or row.get("Volume") or row.get("VOLUME") or "0"
            if not date_str or not close_str:
                continue
            close = float(close_str.replace(",", ""))
            vol = float(vol_str.replace(",", "")) if vol_str else 0.0
            daily.append((date_str[:7], close, vol))

    # Group by month
    by_month: Dict[str, List[Tuple[float, float]]] = defaultdict(list)
    for ym, c, v in daily:
        by_month[ym].append((c, v))

    months_sorted = sorted(by_month.keys())
    result: List[MonthlyData] = []
    prev_close = None
    for ym in months_sorted:
        closes = [x[0] for x in by_month[ym]]
        vols = [x[1] for x in by_month[ym]]
        month_close = closes[-1]
        month_vol = sum(vols) if use_volume else 0.0
        if prev_close and prev_close > 0:
            ret = (month_close - prev_close) / prev_close
        else:
            ret = 0.0
        # volatility proxy: stdev of daily returns within month
        daily_rets = []
        for i in range(1, len(closes)):
            if closes[i - 1] > 0:
                daily_rets.append((closes[i] - closes[i - 1]) / closes[i - 1])
        vol = statistics.stdev(daily_rets) if len(daily_rets) > 1 else 0.0
        # classify regime
        regime = classify_regime(ret, vol)
        result.append(MonthlyData(ym, ret, vol, month_vol, regime))
        prev_close = month_close
    return result


def classify_regime(month_return: float, volatility: float) -> str:
    if volatility > 0.05:
        return "volatile"
    if month_return > 0.05:
        return "bull"
    if month_return < -0.05:
        return "bear"
    return "normal"


# =============================================================================
# SIMULATION ENGINE (order-book + sell-pressure)
# =============================================================================

def daily_volume_usd_proxy(liquidity: float) -> float:
    return liquidity * random.uniform(0.02, 0.10)


def sample_sell_fraction() -> float:
    r = random.random()
    if r < 0.20:
        return random.uniform(0.70, 1.00)
    if r < 0.50:
        return random.uniform(0.30, 0.70)
    if r < 0.85:
        return random.uniform(0.05, 0.20)
    return random.uniform(0.00, 0.05)


def apply_order_book_impact(ref_price: float, liq: float, sell_usd: float) -> float:
    buy_support = liq * BUY_SUPPORT_PCT
    if buy_support <= 0:
        return ref_price * (1 - MAX_IMPACT)
    impact = min(MAX_IMPACT, (sell_usd / buy_support) * DEPTH_FACTOR)
    return max(1e-9, ref_price * (1.0 - impact))


def monthly_mining_liquid(month: int, params: ModelParams) -> int:
    if month <= 0:
        return 0
    ramp = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    rate = 0.20
    for m, r in sorted(ramp.items()):
        if month >= m:
            rate = r
    daily = DAILY_MINING_MAX * rate
    capped = min(daily, DAILY_MINING_MAX * params.emission_cap)
    if params.mining_lock_months and month <= params.mining_lock_months:
        return 0
    monthly = int(capped * 30)
    if params.mining_lock_ratio is not None and month <= 6:
        monthly = int(monthly * (1.0 - params.mining_lock_ratio))
    return monthly


def cumulative_prelaunch(month: int) -> int:
    if month <= 0:
        return 0
    imm = int(PRE_LAUNCH_MINED * 0.30)
    grad = int(PRE_LAUNCH_MINED * 0.50) / 6.0
    return imm + int(min(month, 6) * grad)


def simulate_path(
    params: ModelParams,
    monthly_data: List[MonthlyData],
    launch_liq: float,
    months: int,
    liq_cagr_annual: float = 0.0,
    net_inflow_pct: float = 0.0,
    choppy_shocks: List[Tuple[int, float]] = None,
) -> Dict:
    """Simulate a single path for `months` months, using historical regime data."""
    prices: List[float] = []
    brake_month = 0

    vested_cum = int(BASE_COINS * params.tge_percent / 100.0)
    mining_cum = 0
    prelaunch_prev = 0

    liq = launch_liq

    for m in range(0, months + 1):
        # Apply historical regime to liquidity (if data available)
        if m > 0 and m - 1 < len(monthly_data):
            md = monthly_data[m - 1]
            ret = md.month_return
            vol = md.volatility
            # liquidity follows market with dampening
            liq *= (1.0 + ret * 0.6 - vol * 0.3)
        # Adoption overlay
        if liq_cagr_annual > 0 and m > 0:
            liq *= (1.0 + liq_cagr_annual) ** (1 / 12)
        if net_inflow_pct > 0 and m > 0:
            liq += launch_liq * net_inflow_pct
        # Choppy shocks overlay
        if choppy_shocks:
            for shock_m, delta in choppy_shocks:
                if m == shock_m:
                    liq *= (1.0 + delta)
        liq = max(liq, MIN_LIQUIDITY * 0.5)

        last_price = prices[-1] if prices else TARGET_PRICE

        # Vesting delta
        if m == 0:
            vest_delta = 0
        elif m <= params.cliff_months:
            vest_delta = 0
        elif params.state_driven_release:
            if m <= 6:
                vest_delta = 0
            else:
                rate = 0.003
                if params.global_monthly_cap:
                    rate = min(rate, params.global_monthly_cap / 100.0)
                vest_delta = int(BASE_COINS * rate)
        else:
            tge = int(BASE_COINS * params.tge_percent / 100.0)
            remaining = BASE_COINS - tge
            vest_delta = int(remaining / max(params.vesting_months, 1))
            # brake / gate
            if params.brake_low and last_price < params.brake_low:
                vest_delta = 0
            elif params.price_gate_high and last_price < params.price_gate_high:
                if params.use_volume_peg and params.vest_volume_peg_pct > 0:
                    dv = daily_volume_usd_proxy(liq)
                    cap = int((dv * params.vest_volume_peg_pct) / max(last_price, 1e-9) * 30)
                    vest_delta = min(vest_delta, cap)
                elif params.drip_factor_between is not None:
                    vest_delta = int(vest_delta * params.drip_factor_between)
                else:
                    vest_delta = 0

        vested_cum = min(BASE_COINS, vested_cum + max(0, vest_delta))

        # Mining
        mining_liq = monthly_mining_liquid(m, params)
        if params.mining_volume_cap_pct and params.mining_volume_cap_pct > 0:
            dv = daily_volume_usd_proxy(liq)
            cap = int((dv * params.mining_volume_cap_pct) / max(last_price, 1e-9) * 30)
            mining_liq = min(mining_liq, cap)
        mining_cum += mining_liq

        # Prelaunch
        prelaunch_cum = cumulative_prelaunch(m)
        prelaunch_delta = max(0, prelaunch_cum - prelaunch_prev)
        prelaunch_prev = prelaunch_cum

        total = vested_cum + mining_cum + prelaunch_cum
        staked = int(total * (params.mandatory_stake_pct / 100.0))
        eff_circ = max(1, total - staked)

        ref_price = liq / eff_circ

        # Sell pressure
        sell_vest = vest_delta * sample_sell_fraction() * ref_price
        sell_mine = mining_liq * random.uniform(0.50, 0.70) * ref_price
        sell_pre = prelaunch_delta * random.uniform(0.10, 0.40) * ref_price
        sell_total = sell_vest + sell_mine + sell_pre

        price = apply_order_book_impact(ref_price, liq, sell_total)
        prices.append(price)

        if brake_month == 0 and (price < EMERGENCY_PRICE or liq < MIN_LIQUIDITY):
            brake_month = m

    return {"prices": prices, "brake_month": brake_month, "vested": vested_cum}


def investor_tokens(invest: float) -> int:
    return int(invest / PRESALE_PRICE) // 2


def investor_vested_pct(month: int, params: ModelParams, brake_month: int) -> float:
    if month == 0:
        return params.tge_percent / 100.0
    if month <= params.cliff_months:
        return params.tge_percent / 100.0
    if params.state_driven_release:
        if month <= 6:
            return params.tge_percent / 100.0
        if brake_month and brake_month <= month:
            return params.tge_percent / 100.0
        releasing = month - 6
        return min(1.0, params.tge_percent / 100.0 + 0.003 * releasing)
    # time-based
    vest_months = month - params.cliff_months
    rem = (100.0 - params.tge_percent) / 100.0
    rate = rem / params.vesting_months
    return min(1.0, params.tge_percent / 100.0 + vest_months * rate)


def roi_value(invest: float, tokens: int, vested_pct: float, price: float) -> Tuple[float, float]:
    vested = int(tokens * vested_pct)
    value = vested * price
    roi = (value / invest - 1.0) * 100.0
    return roi, value


# =============================================================================
# OPINION RUNNERS
# =============================================================================

def run_opinion(
    name: str,
    monthly_data: List[MonthlyData],
    launch_liq: float,
    window_months: int,
    step_months: int,
    runs_per_window: int,
    investment_levels: List[int],
    liq_cagr: float,
    net_inflow: float,
    choppy_name: Optional[str],
) -> Dict:
    """Run one opinion config across rolling windows."""
    max_start = len(monthly_data) - window_months
    if max_start < 0:
        max_start = 0

    choppy_shocks = CHOPPY_SHOCKS.get(choppy_name, []) if choppy_name else []

    results_by_model: Dict[str, Dict] = {m.name: {"runs": [], "summary": {}} for m in MODELS}

    start_indices = list(range(0, max_start + 1, step_months)) or [0]

    for start_idx in start_indices:
        window_data = monthly_data[start_idx : start_idx + window_months]
        for _ in range(runs_per_window):
            for model in MODELS:
                path = simulate_path(model, window_data, launch_liq, window_months, liq_cagr, net_inflow, choppy_shocks)
                run_record = {
                    "start_idx": start_idx,
                    "brake_month": path["brake_month"],
                    "by_invest": {},
                }
                for inv in investment_levels:
                    tokens = investor_tokens(inv)
                    inv_horizons = {}
                    for h in ROI_HORIZONS:
                        if h <= window_months and h < len(path["prices"]):
                            pct = investor_vested_pct(h, model, path["brake_month"])
                            r, v = roi_value(inv, tokens, pct, path["prices"][h])
                            inv_horizons[str(h)] = {"roi": r, "value": v}
                    run_record["by_invest"][str(inv)] = inv_horizons
                results_by_model[model.name]["runs"].append(run_record)

    # Summarize per model
    for model_name, data in results_by_model.items():
        runs = data["runs"]
        summary_by_inv: Dict[str, Dict[str, Dict]] = {}
        for inv in investment_levels:
            inv_key = str(inv)
            summary_by_inv[inv_key] = {}
            for h in ROI_HORIZONS:
                h_key = str(h)
                rois = [r["by_invest"][inv_key][h_key]["roi"] for r in runs if h_key in r["by_invest"][inv_key]]
                values = [r["by_invest"][inv_key][h_key]["value"] for r in runs if h_key in r["by_invest"][inv_key]]
                brakes = [1 for r in runs if r["brake_month"] and r["brake_month"] <= h]
                if rois:
                    pos_rate = sum(1 for x in rois if x > 0) / len(rois) * 100.0
                    summary_by_inv[inv_key][h_key] = {
                        "roi_avg": statistics.mean(rois),
                        "roi_median": statistics.median(rois),
                        "value_avg": statistics.mean(values),
                        "positive_rate_pct": pos_rate,
                        "brake_rate_pct": len(brakes) / len(runs) * 100.0 if runs else 0,
                        "count": len(rois),
                    }
        data["summary"] = summary_by_inv

    return {
        "opinion_name": name,
        "config": {
            "liquidity_cagr_annual": liq_cagr,
            "net_inflow_monthly_pct": net_inflow,
            "choppy_overlay": choppy_name,
            "window_months": window_months,
            "runs_per_window": runs_per_window,
        },
        "by_model": results_by_model,
    }


def run_all_opinions(
    monthly_data: List[MonthlyData],
    launch_liq: float,
    window_months: int,
    step_months: int,
    runs_per_window: int,
    investment_levels: List[int],
) -> List[Dict]:
    opinions = []

    print("Running Opinion 1: Conservative (no adoption overlay)...")
    opinions.append(
        run_opinion("Conservative (Stress-Test)", monthly_data, launch_liq, window_months, step_months, runs_per_window, investment_levels, 0.0, 0.0, None)
    )

    print("Running Opinion 2: Ideal (adoption overlay)...")
    opinions.append(
        run_opinion("Ideal (Growth Scenario)", monthly_data, launch_liq, window_months, step_months, runs_per_window, investment_levels, 0.50, 0.01, None)
    )

    print("Running Opinion 3: Choppy overlays on historical data...")
    choppy_results = []
    for choppy_name in CHOPPY_SHOCKS.keys():
        print(f"  - {choppy_name}")
        choppy_results.append(
            run_opinion(f"Choppy: {choppy_name}", monthly_data, launch_liq, window_months, step_months, max(runs_per_window // 5, 3), investment_levels, 0.0, 0.0, choppy_name)
        )
    # Aggregate choppy into one summary
    choppy_agg = aggregate_choppy_opinions(choppy_results)
    opinions.append(choppy_agg)

    return opinions


def aggregate_choppy_opinions(choppy_list: List[Dict]) -> Dict:
    """Combine all choppy scenario results into one aggregated opinion."""
    agg_by_model: Dict[str, Dict] = {}
    for choppy in choppy_list:
        for model_name, model_data in choppy["by_model"].items():
            if model_name not in agg_by_model:
                agg_by_model[model_name] = {"runs": [], "summary": {}, "by_scenario": {}}
            agg_by_model[model_name]["runs"].extend(model_data["runs"])
            scenario_name = choppy["config"]["choppy_overlay"]
            agg_by_model[model_name]["by_scenario"][scenario_name] = model_data["summary"]

    # Re-summarize across all choppy runs
    for model_name, data in agg_by_model.items():
        runs = data["runs"]
        inv_levels = list(runs[0]["by_invest"].keys()) if runs else []
        summary_by_inv: Dict[str, Dict] = {}
        for inv_key in inv_levels:
            summary_by_inv[inv_key] = {}
            for h in ROI_HORIZONS:
                h_key = str(h)
                rois = [r["by_invest"][inv_key][h_key]["roi"] for r in runs if h_key in r["by_invest"].get(inv_key, {})]
                values = [r["by_invest"][inv_key][h_key]["value"] for r in runs if h_key in r["by_invest"].get(inv_key, {})]
                brakes = [1 for r in runs if r["brake_month"] and r["brake_month"] <= h]
                if rois:
                    pos_rate = sum(1 for x in rois if x > 0) / len(rois) * 100.0
                    summary_by_inv[inv_key][h_key] = {
                        "roi_avg": statistics.mean(rois),
                        "roi_median": statistics.median(rois),
                        "value_avg": statistics.mean(values),
                        "positive_rate_pct": pos_rate,
                        "brake_rate_pct": len(brakes) / len(runs) * 100.0 if runs else 0,
                        "count": len(rois),
                    }
        data["summary"] = summary_by_inv

    return {
        "opinion_name": "Choppy Stress Overlay (10 scenarios aggregated)",
        "config": {"choppy_scenarios": list(CHOPPY_SHOCKS.keys())},
        "by_model": agg_by_model,
    }


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(opinions: List[Dict], investment_levels: List[int], output_path: str) -> None:
    lines = []
    lines.append("# Real-World Multi-Opinion Backtest Report\n\n")
    lines.append(f"**Generated**: {datetime.now().isoformat()}\n\n")
    lines.append("## Methodology\n\n")
    lines.append("Three independent 'opinions' on the same historical market data:\n")
    lines.append("1. **Conservative (Stress-Test)**: raw historical regimes, no adoption overlay\n")
    lines.append("2. **Ideal (Growth Scenario)**: historical regimes + 50% annual liquidity CAGR + 1% monthly inflow\n")
    lines.append("3. **Choppy Stress Overlay**: historical regimes with 10 choppy crash shocks overlaid\n\n")
    lines.append(f"**Investment levels**: {', '.join(f'${x:,}' for x in investment_levels)}\n\n")
    lines.append(f"**ROI horizons**: {', '.join(str(h) for h in ROI_HORIZONS)} months\n\n")

    def fmt_pct(x): return f"{x:+.1f}%" if not math.isnan(x) else "—"
    def fmt_usd(x): return f"${x:,.0f}" if not math.isnan(x) else "—"

    # Executive summary: winner by opinion and horizon
    lines.append("## Executive Summary: Winners by Opinion & Horizon\n\n")
    lines.append("| Opinion | Horizon | Winner (ROI) | Avg ROI | Positive Rate | Value ($9k) | Value ($50k) | Value ($100k) |\n")
    lines.append("|---|---:|---|---:|---:|---:|---:|---:|\n")

    for op in opinions:
        op_name = op["opinion_name"]
        for h in ROI_HORIZONS:
            h_key = str(h)
            best_model = None
            best_roi = -1e9
            for model_name, model_data in op["by_model"].items():
                summ = model_data.get("summary", {}).get("9000", {}).get(h_key, {})
                roi = summ.get("roi_avg", -1e9)
                if roi > best_roi:
                    best_roi = roi
                    best_model = model_name
            if best_model:
                summ = op["by_model"][best_model]["summary"]["9000"][h_key]
                v9 = summ.get("value_avg", float("nan"))
                v50 = op["by_model"][best_model]["summary"].get("50000", {}).get(h_key, {}).get("value_avg", float("nan"))
                v100 = op["by_model"][best_model]["summary"].get("100000", {}).get(h_key, {}).get("value_avg", float("nan"))
                pos = summ.get("positive_rate_pct", 0)
                lines.append(f"| {op_name} | {h} | **{best_model}** | {fmt_pct(best_roi)} | {pos:.1f}% | {fmt_usd(v9)} | {fmt_usd(v50)} | {fmt_usd(v100)} |\n")

    # Detailed tables per opinion
    for op in opinions:
        op_name = op["opinion_name"]
        lines.append(f"\n---\n\n## {op_name}\n\n")
        cfg = op.get("config", {})
        for k, v in cfg.items():
            lines.append(f"- **{k}**: {v}\n")
        lines.append("\n")

        for inv in investment_levels:
            inv_key = str(inv)
            lines.append(f"### Investment: ${inv:,}\n\n")
            lines.append("| Model | Month 12 ROI | Month 24 ROI | Month 36 ROI | Month 48 ROI | Month 72 ROI | Positive Rate (M72) | Brake Rate (M72) |\n")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|\n")
            for model in MODELS:
                summ = op["by_model"][model.name]["summary"].get(inv_key, {})
                row = [model.name]
                for h in ROI_HORIZONS:
                    h_key = str(h)
                    roi = summ.get(h_key, {}).get("roi_avg", float("nan"))
                    row.append(fmt_pct(roi))
                pos72 = summ.get("72", {}).get("positive_rate_pct", 0)
                brake72 = summ.get("72", {}).get("brake_rate_pct", 0)
                row.append(f"{pos72:.1f}%")
                row.append(f"{brake72:.1f}%")
                lines.append("| " + " | ".join(row) + " |\n")
            lines.append("\n")

        # If choppy, show per-scenario breakdown
        if "by_scenario" in op["by_model"].get(MODELS[0].name, {}):
            lines.append("### Per-Scenario Breakdown (Month 72 ROI @ $9,000)\n\n")
            scenarios = list(op["by_model"][MODELS[0].name]["by_scenario"].keys())
            header = "| Scenario | " + " | ".join(m.name for m in MODELS) + " |\n"
            lines.append(header)
            lines.append("|---" + "|---:" * len(MODELS) + "|\n")
            for sc in scenarios:
                row = [sc]
                for model in MODELS:
                    sc_summ = op["by_model"][model.name]["by_scenario"].get(sc, {}).get("9000", {}).get("72", {})
                    roi = sc_summ.get("roi_avg", float("nan"))
                    row.append(fmt_pct(roi))
                lines.append("| " + " | ".join(row) + " |\n")
            lines.append("\n")

    Path(output_path).write_text("".join(lines))


# =============================================================================
# MAIN
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="Real-World Multi-Opinion Backtest")
    ap.add_argument("--csv", required=True, help="Path to daily BTC/ETH CSV")
    ap.add_argument("--launch-liquidity", type=float, default=32_000_000)
    ap.add_argument("--window-months", type=int, default=72)
    ap.add_argument("--step-months", type=int, default=6)
    ap.add_argument("--runs", type=int, default=20, help="Runs per window per model")
    ap.add_argument("--investment-levels", type=str, default="9000,50000,100000")
    args = ap.parse_args()

    investment_levels = [int(x) for x in args.investment_levels.split(",")]

    print("Loading CSV...")
    monthly_data = load_csv_to_monthly(args.csv)
    print(f"Loaded {len(monthly_data)} months of data")

    print("Running all three opinions...")
    opinions = run_all_opinions(
        monthly_data,
        args.launch_liquidity,
        args.window_months,
        args.step_months,
        args.runs,
        investment_levels,
    )

    output = {
        "timestamp": datetime.now().isoformat(),
        "csv_months": len(monthly_data),
        "investment_levels_usd": investment_levels,
        "roi_horizons_months": ROI_HORIZONS,
        "opinions": opinions,
    }

    json_path = "data/results/real_world_multi_opinion_results.json"
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"✅ wrote {json_path}")

    report_path = "docs/vesting/REAL_WORLD_MULTI_OPINION_REPORT.md"
    generate_report(opinions, investment_levels, report_path)
    print(f"✅ wrote {report_path}")


if __name__ == "__main__":
    main()

