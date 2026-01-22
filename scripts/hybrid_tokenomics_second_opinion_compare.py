#!/usr/bin/env python3
"""
SECOND OPINION: Hybrid Tokenomics vs Other Models (Order-Book + Sell Pressure)
=============================================================================

This is an independent verification harness that re-runs the same comparisons
using a DIFFERENT pricing methodology than `scripts/hybrid_tokenomics_comparison.py`.

Key differences vs the primary comparison script:
- Price is NOT computed purely as Liquidity / Circulating.
- We compute a baseline reference price from liquidity/circulating, then apply
  order-book depth + sell-pressure impacts from:
  - newly liquid vesting unlocks (net of mandatory staking/locks)
  - miners selling a fraction of their liquid emissions
  - pre-launch migration liquidity (assumed partially sellable)

What it produces:
- 100 Monte Carlo simulations per model across 4 market types (bull/bear/normal/volatile)
- 100 Monte Carlo runs per model per each of 10 choppy market scenarios
- ROI tables for multiple investment sizes for every model
- Focus comparison: Hybrid Tokenomics (Solvency-Anchored) vs Hybrid B (the 4th model)

Outputs:
- `data/results/second_opinion_compare_results_{N}_models.json`
- `docs/vesting/SECOND_OPINION_COMPARE_REPORT_{N}_MODELS.md`
"""

import json
import random
import statistics
import gzip
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Deque, Dict, List, Optional, Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_COINS = 17_000_000_000
BONUS_COINS = 33_000_000_000
DAILY_MINING_MAX = 10_500_000
PRE_LAUNCH_MINED = 540_000_000

TARGET_PRICE = 0.05
DEFAULT_LAUNCH_LIQUIDITY = 32_000_000

EMERGENCY_PRICE = 0.02
MIN_LIQUIDITY = 10_000_000

# “Second opinion” order book model params
BUY_SUPPORT_PCT = 0.30  # portion of liquidity available as near-price buy support
DEPTH_FACTOR = 0.12  # higher => more sensitive price to sell volume
MAX_IMPACT = 0.90  # cap single-step price impact

# Sell behavior assumptions (Monte Carlo)
# These represent fraction of newly liquid tokens sold quickly.
SELL_BEHAVIOR = {
    "panic": 0.20,      # weight
    "partial": 0.30,    # weight
    "holder": 0.35,     # weight
    "long_term": 0.15,  # weight
}

INVESTMENT_LEVELS = [1_000, 5_000, 9_000, 25_000, 50_000, 100_000]
PRESALE_PRICE = 0.01  # used only for sizing token allocations

# ROI horizons requested (months)
ROI_HORIZONS = [12, 24, 36, 48, 72]

# =============================================================================
# MODELS
# =============================================================================

@dataclass(frozen=True)
class ModelParams:
    name: str
    tge_percent: float
    cliff_months: int
    vesting_months: int
    emission_cap: float  # e.g. 0.20 = 20% of DAILY_MINING_MAX
    mandatory_stake_pct: float
    model_type: str  # "time_based" | "state_driven" | "hybrid"
    state_driven_release: bool = False
    global_monthly_cap: Optional[float] = None  # % of BASE_COINS per month across sources (soft in this harness)
    bonus_option: Optional[str] = None
    mining_lock_ratio: Optional[float] = None
    # v7.0 style mechanics (approximations)
    adaptive_trend_shield_pct: Optional[float] = None  # require price within ±X of moving average
    miner_burn_fee_pct: float = 0.0  # burn on miner claims reduces sellable emissions
    # protocol gates / special mechanics (v2.6/v3.0/v3.1)
    price_gate_high: Optional[float] = None        # e.g. 0.05
    brake_low: Optional[float] = None              # e.g. 0.02
    drip_factor_between: Optional[float] = None    # v3.0 style: reduced vesting when brake_low <= price < gate_high
    mining_lock_months: int = 0                    # v3.0: mined emissions not circulating for N months
    use_volume_peg: bool = False                   # v3.1: volume pegging in band (0.02..0.05)
    vest_volume_peg_pct: float = 0.0               # v3.1: 0.02 == 2% of daily volume
    mining_volume_cap_pct: float = 0.0             # v3.1: 0.20 == 20% of daily volume


ORIGINAL_MODEL = ModelParams(
    name="Original Model",
    tge_percent=2.0,
    cliff_months=12,
    vesting_months=60,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    model_type="time_based",
)

HYBRID_MODEL = ModelParams(
    name="Hybrid Model",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    model_type="hybrid",
)

PROTOCOL_V26_MODEL = ModelParams(
    name="Protocol v2.6",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    drip_factor_between=0.0,  # hard stop below gate
)

# Protocol v3.0 (existing approximation from our other harnesses)
PROTOCOL_V30_MODEL = ModelParams(
    name="Protocol v3.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=33,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    drip_factor_between=0.10,
    mining_lock_months=24,
)

# Protocol v3.1 (Adjusted) from the provided spec page
PROTOCOL_V31_MODEL = ModelParams(
    name="Protocol v3.1 (Adjusted)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=1.0,  # max-cap bypass; volume cap applied below
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
)

# “Fourth model” in our comparison set:
HYBRID_B_MODEL = ModelParams(
    name="Hybrid B",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    model_type="hybrid",
    state_driven_release=True,
    global_monthly_cap=1.0,
    price_gate_high=0.05,
    brake_low=0.02,
)

HYBRID_TOKENOMICS_MODEL = ModelParams(
    name="Hybrid Tokenomics (Solvency-Anchored)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=60.0,
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=1.0,
    bonus_option="B",
    mining_lock_ratio=0.70,
    price_gate_high=0.05,
    brake_low=0.02,
)

# Harris vesting model (external PDF spec). Approximated here using a higher TGE and faster vesting.
HARRIS_MODEL = ModelParams(
    name="Harris Model",
    tge_percent=10.0,
    cliff_months=0,
    vesting_months=9,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    # We approximate the miner “diamond hands” incentive by reducing early liquid mining.
    mining_lock_ratio=0.75,
)

# Maxime v5.x family (spec pages). Approximated using the existing gate/brake/volume-peg mechanics.
# Sources:
# - https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/
# - https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/
# - https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/
# - https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/
PROTOCOL_V53_MODEL = ModelParams(
    name="Protocol v5.3",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
)

PROTOCOL_V55_MODEL = ModelParams(
    name="Protocol v5.5",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
)

PROTOCOL_V57_MODEL = ModelParams(
    name="Protocol v5.7",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
    # Revised “streaming” is approximated as a softer vesting drip in the band.
    drip_factor_between=0.15,
)

PROTOCOL_V58_MODEL = ModelParams(
    name="Protocol v5.8",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    use_volume_peg=True,
    vest_volume_peg_pct=0.02,
    mining_volume_cap_pct=0.20,
    drip_factor_between=0.15,
)

# HybridC (spreadsheet spec). Approximated using a hard monthly cap and heavy locks.
HYBRID_C_MODEL = ModelParams(
    name="HybridC",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=50.0,
    model_type="state_driven",
    state_driven_release=True,
    # Spreadsheet: 0.3% monthly cap (0.003) of supply.
    global_monthly_cap=0.30,
    # Spreadsheet: 15% mining liquid share (85% effectively locked).
    mining_lock_ratio=0.85,
    price_gate_high=0.05,
    brake_low=0.02,
)

# =============================================================================
# Additional Ingo CSV models (source material)
# =============================================================================
#
# Notes:
# - These CSVs describe rule-driven monetary policy with ranges (not a single
#   canonical parameter set). We map them into this harness as fixed-point
#   approximations so they can be compared consistently against the rest of the
#   suite.
# - Sources live under `docs/sources/Ingo  Projects/`.
#

# Hybrid (Ingo CSV): state-driven, wide global cap range (0.3–1.0%/mo), optional staking.
# Source: docs/sources/Ingo  Projects/Hybrid.csv
HYBRID_INGO_CSV_MODEL = ModelParams(
    name="Hybrid (Ingo CSV)",
    tge_percent=3.0,
    cliff_months=3,          # "Hard cliff, 90 days"
    vesting_months=36,       # mapped as a max-duration vesting window (releases are still state-driven here)
    emission_cap=0.20,
    mandatory_stake_pct=0.0,  # CSV states "optional" auto-staking
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=0.70,   # midpoint of 0.3–1.0% range
    mining_lock_ratio=0.70,    # "≥70% locked" in early phase
    price_gate_high=0.05,
    brake_low=0.02,
)

# Hybrid C (Ingo CSV): strict 0.30%/30d cap, deterministic states, stronger auto-stake range.
# Source: docs/sources/Ingo  Projects/hybrid C.csv
HYBRID_C_INGO_CSV_MODEL = ModelParams(
    name="Hybrid C (Ingo CSV)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=55.0,  # midpoint of 40–70% "Auto-staking"
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=0.30,
    mining_lock_ratio=0.65,    # midpoint of 30–40% liquid => 60–70% locked
    price_gate_high=0.05,
    brake_low=0.02,
)

# Hybrid C Lite Plus (Final): looser cap (0.40–0.45%/30d), lower auto-stake, higher miner liquidity.
# Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Plus_Final.csv
HYBRID_C_LITE_PLUS_FINAL_MODEL = ModelParams(
    name="Hybrid C Lite+ (Final, Ingo CSV)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    mandatory_stake_pct=30.0,  # midpoint of 20–40% auto-staking
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=0.45,   # upper bound of 0.40–0.45% range
    mining_lock_ratio=0.55,    # midpoint of 45–50% liquid => 50–55% locked
    price_gate_high=0.05,
    brake_low=0.02,
)

# Hybrid C Lite (Defaults): parameter defaults snapshot (distinct from Lite+ Final).
# Source: docs/sources/Ingo  Projects/Hybrid_C_Lite_Defaults.csv
HYBRID_C_LITE_DEFAULTS_MODEL = ModelParams(
    name="Hybrid C Lite (Defaults, Ingo CSV)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    # CSV: Auto-staking 30–60% (use midpoint)
    mandatory_stake_pct=45.0,
    model_type="state_driven",
    state_driven_release=True,
    # CSV: Max new circulation / 30d = 0.45%
    global_monthly_cap=0.45,
    # CSV: Mining liquid 40–45%, locked 35–45%, performance 10–20%.
    # We treat (locked + performance) as "effectively locked" supply in this harness.
    mining_lock_ratio=0.55,
    price_gate_high=0.05,
    brake_low=0.02,
)

# Super Ultra Mega Sphincer best-of-breed model
SUPER_ULTRA_MEGA_SPHINCER_MODEL = ModelParams(
    name="Super Ultra Mega Sphincer",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=30,
    emission_cap=0.20,
    mandatory_stake_pct=40.0,
    model_type="state_driven",
    state_driven_release=True,
    global_monthly_cap=0.55,
    adaptive_trend_shield_pct=0.20,
    drip_factor_between=0.07,
    price_gate_high=0.05,
    brake_low=0.02,
    mining_lock_ratio=0.65,
    mining_volume_cap_pct=0.20,
    mining_lock_months=2,
)
    name="Hybrid C Lite (Defaults, Ingo CSV)",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=36,
    emission_cap=0.20,
    # CSV: Auto-staking 30–60% (use midpoint)
    mandatory_stake_pct=45.0,
    model_type="state_driven",
    state_driven_release=True,
    # CSV: Max new circulation / 30d = 0.45%
    global_monthly_cap=0.45,
    # CSV: Mining liquid 40–45%, locked 35–45%, performance 10–20%.
    # We treat (locked + performance) as "effectively locked" supply in this harness.
    mining_lock_ratio=0.55,
    price_gate_high=0.05,
    brake_low=0.02,
)

# Model A (ROI Optimized): deliberately aggressive benchmark model.
# Source: docs/sources/Ingo  Projects/Model_A_ROI_Final_Test.csv
MODEL_A_ROI_OPTIMIZED_MODEL = ModelParams(
    name="Model A (ROI Optimized, Ingo CSV)",
    tge_percent=15.0,
    cliff_months=0,
    vesting_months=12,        # "Linear, 12 months"
    emission_cap=1.0,         # "High, volume-scaled" mining output (mapped to uncapped in this harness)
    mandatory_stake_pct=0.0,
    model_type="time_based",
    mining_lock_ratio=0.20,   # 80% liquid mining rewards
    price_gate_high=None,
    brake_low=None,
)

# Protocol v7.0 (Definitive Edition) — approximated into this harness.
# Source: https://a-changer-plus-tard.github.io/BlockDAG-Protocol-v7.0-Definitive-Edition/
#
# Key mechanics mapped:
# - Adaptive Trend Shield: vesting halts if price deviates >±25% from moving average.
# - Dynamic Discharge: miner sell allowance capped at 20% of retail buy volume (mapped to mining volume cap 20%).
# - Setup Grace Period: X-tier miners hard-locked 6 months (mapped to mining_lock_months=6).
# - Ecosystem Burn Guard: 2.5% burn on high-tier claims (mapped to miner_burn_fee_pct=2.5%).
PROTOCOL_V70_MODEL = ModelParams(
    name="Protocol v7.0",
    tge_percent=3.0,
    cliff_months=3,
    vesting_months=21,
    emission_cap=0.20,
    mandatory_stake_pct=0.0,
    model_type="time_based",
    price_gate_high=0.05,
    brake_low=0.02,
    adaptive_trend_shield_pct=0.25,
    mining_lock_months=6,
    mining_volume_cap_pct=0.20,
    miner_burn_fee_pct=0.025,
)

MODELS = [
    ORIGINAL_MODEL,
    HYBRID_MODEL,
    PROTOCOL_V26_MODEL,
    PROTOCOL_V30_MODEL,
    PROTOCOL_V31_MODEL,
    HYBRID_B_MODEL,
    HYBRID_TOKENOMICS_MODEL,
    HARRIS_MODEL,
    PROTOCOL_V53_MODEL,
    PROTOCOL_V55_MODEL,
    PROTOCOL_V57_MODEL,
    PROTOCOL_V58_MODEL,
    HYBRID_C_MODEL,
    HYBRID_INGO_CSV_MODEL,
    HYBRID_C_INGO_CSV_MODEL,
    HYBRID_C_LITE_PLUS_FINAL_MODEL,
    HYBRID_C_LITE_DEFAULTS_MODEL,
MODEL_A_ROI_OPTIMIZED_MODEL,
    SUPER_ULTRA_MEGA_SPHINCER_MODEL,
    PROTOCOL_V70_MODEL,
]

# =============================================================================
# CHOPPY MARKET SCENARIOS (same shape as primary script)
# =============================================================================

MARKET_SCENARIOS: Dict[str, Dict] = {
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

# =============================================================================
# MARKET GENERATORS (Monte Carlo)
# =============================================================================


def generate_market_events(market_type: str) -> List[Tuple[int, float]]:
    if market_type == "bull":
        return [(m, random.uniform(0.05, 0.10)) for m in [2, 4, 6, 8, 10, 12]]
    if market_type == "bear":
        return [(m, random.uniform(-0.10, -0.05)) for m in [2, 4, 6, 8, 10, 12]]
    if market_type == "volatile":
        return [(m, random.choice([-1, 1]) * random.uniform(0.15, 0.30)) for m in [2, 4, 6, 8, 10, 12]]
    # normal
    return [(m, random.uniform(-0.03, 0.03)) for m in [2, 4, 6, 8, 10, 12]]


# =============================================================================
# STATE-DRIVEN VESTING (simplified, consistent with primary harness intent)
# =============================================================================


def vwap_30(prices: Deque[float]) -> float:
    if not prices:
        return TARGET_PRICE
    recent = list(prices)[-min(30, len(prices)):]
    return statistics.mean(recent) if recent else TARGET_PRICE


def market_allows_release(price: float, vwap: float, liquidity: float, price_trend: List[float]) -> bool:
    if liquidity < MIN_LIQUIDITY:
        return False
    if price < EMERGENCY_PRICE:
        return False
    # negative trend heuristic
    if price_trend and (price - price_trend[0]) / price_trend[0] < -0.10:
        return False
    # stability heuristic
    if vwap > 0 and abs(price - vwap) / vwap > 0.25:
        return False
    return True


def daily_volume_usd_proxy(liquidity: float) -> float:
    """
    Proxy for 24h DEX volume.
    We use a stochastic turnover fraction of liquidity (2%..10% daily).
    """
    return liquidity * random.uniform(0.02, 0.10)


# =============================================================================
# SUPPLY COMPONENTS
# =============================================================================


def monthly_mining_liquid(month: int, params: ModelParams) -> int:
    if month <= 0:
        return 0

    # ramp profile (same as primary harness)
    ramp_rates = {1: 0.20, 2: 0.35, 3: 0.50, 6: 0.80, 12: 1.0}
    rate = 0.20
    for m, r in sorted(ramp_rates.items()):
        if month >= m:
            rate = r

    daily = DAILY_MINING_MAX * rate
    capped_daily = min(daily, DAILY_MINING_MAX * params.emission_cap)

    # Protocol v3.0 mining lock: mined emissions do not enter circulating for 24 months
    if params.mining_lock_months and month <= params.mining_lock_months:
        return 0

    monthly = int(capped_daily * 30)

    # Hybrid Tokenomics phase 1 lock ratio: only (1-lock) is liquid up to month 6
    if params.mining_lock_ratio is not None and month <= 6:
        monthly = int(monthly * (1.0 - params.mining_lock_ratio))

    # miners sell only a fraction of liquid emissions; handled in sell-pressure section
    return monthly


def cumulative_prelaunch_migrated(month: int) -> int:
    if month <= 0:
        return 0
    immediate = int(PRE_LAUNCH_MINED * 0.30)
    gradual = int(PRE_LAUNCH_MINED * 0.50)
    monthly_gradual = gradual / 6.0
    return immediate + int(min(month, 6) * monthly_gradual)


# =============================================================================
# SECOND OPINION PRICE MODEL
# =============================================================================


def sample_sell_fraction() -> float:
    """
    Sample a sell fraction of newly liquid tokens using behavior weights.
    """
    r = random.random()
    if r < SELL_BEHAVIOR["panic"]:
        return random.uniform(0.70, 1.00)
    if r < SELL_BEHAVIOR["panic"] + SELL_BEHAVIOR["partial"]:
        return random.uniform(0.30, 0.70)
    if r < SELL_BEHAVIOR["panic"] + SELL_BEHAVIOR["partial"] + SELL_BEHAVIOR["holder"]:
        return random.uniform(0.05, 0.20)
    return random.uniform(0.00, 0.05)


def apply_order_book_impact(reference_price: float, liquidity: float, sell_volume_usd: float) -> float:
    buy_support = liquidity * BUY_SUPPORT_PCT
    if buy_support <= 0:
        return reference_price * (1 - MAX_IMPACT)
    impact = min(MAX_IMPACT, (sell_volume_usd / buy_support) * DEPTH_FACTOR)
    return max(0.000001, reference_price * (1.0 - impact))


def simulate_month_path(
    params: ModelParams,
    liquidity_base: float,
    events: List[Tuple[int, float]],
    months: int = 12,
) -> Dict:
    """
    Returns month-by-month dict:
    - prices[0..months]
    - liquidity[0..months]
    - effective_circulating[0..months]  (post mandatory staking)
    - emergency_brake_month (0 means none)
    """
    prices: Deque[float] = deque(maxlen=120)
    monthly_prices: List[float] = []
    monthly_liquidity: List[float] = []
    monthly_effective_circ: List[int] = []

    # cumulative state (path-dependent)
    vested_cum = int(BASE_COINS * params.tge_percent / 100.0)
    mining_cum = 0
    vested_prev = vested_cum
    prelaunch_prev = 0

    emergency_brake_month = 0

    for month in range(0, months + 1):
        # liquidity events
        liq = liquidity_base
        for event_month, delta in events:
            if month >= event_month:
                liq *= (1.0 + delta)
        monthly_liquidity.append(liq)

        # baseline reference price uses last observed price as market price for gating decisions
        last_price = prices[-1] if prices else TARGET_PRICE
        current_vwap = vwap_30(prices)

        # --- vesting delta (path dependent)
        if month == 0:
            vested_delta = 0
        elif month <= params.cliff_months:
            vested_delta = 0
        elif params.state_driven_release:
            # additional observation window until month 6 inclusive: no vesting
            if month <= 6:
                vested_delta = 0
            else:
                current_vwap = vwap_30(prices)
                trend = list(prices)[-min(10, len(prices)):] if prices else []
                if not market_allows_release(last_price, current_vwap, liq, trend):
                    vested_delta = 0
                else:
                    stable = abs(last_price - current_vwap) / current_vwap < 0.20 if current_vwap > 0 else True
                    rate = 0.003 if stable else 0.007
                    if params.global_monthly_cap is not None:
                        rate = min(rate, params.global_monthly_cap / 100.0)
                    vested_delta = int(BASE_COINS * rate)
        else:
            # time-based linear delta for the remaining (100%-TGE) tokens
            tge = int(BASE_COINS * params.tge_percent / 100.0)
            remaining = BASE_COINS - tge
            monthly_sched = remaining / max(params.vesting_months, 1)
            vested_delta = int(monthly_sched)

            # emergency brake (if defined)
            if params.brake_low is not None and last_price < params.brake_low:
                vested_delta = 0

            # Adaptive Trend Shield (v7.0): halt vesting if price deviates too far from moving average.
            if params.adaptive_trend_shield_pct is not None and current_vwap > 0:
                if abs(last_price - current_vwap) / current_vwap > params.adaptive_trend_shield_pct:
                    vested_delta = 0

            # price gate behaviors
            if params.price_gate_high is not None and last_price < params.price_gate_high:
                if params.use_volume_peg and params.vest_volume_peg_pct > 0 and (params.brake_low is None or last_price >= params.brake_low):
                    dv = daily_volume_usd_proxy(liq)
                    cap_tokens_daily = (dv * params.vest_volume_peg_pct) / max(last_price, 1e-9)
                    cap_tokens_month = int(cap_tokens_daily * 30)
                    vested_delta = min(vested_delta, cap_tokens_month)
                elif params.drip_factor_between is not None:
                    vested_delta = int(vested_delta * params.drip_factor_between)
                else:
                    vested_delta = 0

        vested_cum = min(BASE_COINS, vested_cum + max(0, vested_delta))

        # --- mining liquid this month and cumulative (path dependent for v3.1 volume cap)
        mining_liquid_this_month = monthly_mining_liquid(month, params)
        if params.mining_volume_cap_pct and params.mining_volume_cap_pct > 0:
            dv = daily_volume_usd_proxy(liq)
            cap_tokens_daily = (dv * params.mining_volume_cap_pct) / max(last_price, 1e-9)
            cap_tokens_month = int(cap_tokens_daily * 30)
            mining_liquid_this_month = min(mining_liquid_this_month, cap_tokens_month)
        mining_cum += mining_liquid_this_month

        # prelaunch migration cumulative and delta
        prelaunch_cum = cumulative_prelaunch_migrated(month)
        prelaunch_delta = max(0, prelaunch_cum - prelaunch_prev)
        prelaunch_prev = prelaunch_cum

        # total liquid-ish supply (before mandatory staking)
        total_liquidish = vested_cum + mining_cum + prelaunch_cum

        # mandatory staking reduces circulating
        staked = int(total_liquidish * (params.mandatory_stake_pct / 100.0))
        effective_circ = max(1, total_liquidish - staked)
        monthly_effective_circ.append(effective_circ)

        # baseline reference price
        reference_price = liq / effective_circ

        # sell pressure components (USD)
        sell_frac_vesting = sample_sell_fraction()
        vesting_sell_usd = vested_delta * sell_frac_vesting * reference_price

        # miners: sell 50-70% of their liquid emissions to cover costs (stochastic)
        miner_sell_frac = random.uniform(0.50, 0.70)
        miner_sellable_tokens = mining_liquid_this_month * (1.0 - max(0.0, min(1.0, params.miner_burn_fee_pct)))
        mining_sell_usd = miner_sellable_tokens * miner_sell_frac * reference_price

        # prelaunch migration: assume 10-40% sells quickly (stochastic)
        prelaunch_sell_frac = random.uniform(0.10, 0.40)
        prelaunch_sell_usd = prelaunch_delta * prelaunch_sell_frac * reference_price

        total_sell_usd = vesting_sell_usd + mining_sell_usd + prelaunch_sell_usd

        # order-book impact
        price = apply_order_book_impact(reference_price, liq, total_sell_usd)
        monthly_prices.append(price)
        prices.append(price)

        # emergency brake (second opinion uses same thresholds)
        if emergency_brake_month == 0 and (price < EMERGENCY_PRICE or liq < MIN_LIQUIDITY):
            emergency_brake_month = month

    return {
        "prices": monthly_prices,
        "liquidity": monthly_liquidity,
        "effective_circulating": monthly_effective_circ,
        "emergency_brake_month": emergency_brake_month,
        "vested_cumulative": vested_cum,
    }


# =============================================================================
# INVESTOR VALUE / ROI
# =============================================================================


def investor_base_tokens(investment_usd: float) -> int:
    total_tokens = int(investment_usd / PRESALE_PRICE)
    return total_tokens // 2  # base half (consistent with earlier harness)


def investor_vested_pct(month: int, params: ModelParams, price_path: Dict) -> float:
    if month == 0:
        return params.tge_percent / 100.0
    if month <= params.cliff_months:
        return params.tge_percent / 100.0

    if not params.state_driven_release:
        # approximate from schedule only; note that gated models can differ.
        months_vesting = month - params.cliff_months
        remaining_pct = (100.0 - params.tge_percent) / 100.0
        monthly_vest_rate = remaining_pct / params.vesting_months
        vested_pct = params.tge_percent / 100.0 + months_vesting * monthly_vest_rate
        return min(vested_pct, 1.0)

    # state-driven: approximate using effective base vesting from our engine
    # we can back it out from effective circulating path using our vesting function logic
    # for simplicity, assume base vesting follows the same cumulative function with the path's prices
    # (we recompute with the final month's liquidity and historical prices is messy; use proxy)
    # Proxy: after month 6, allow a small state-driven release if no emergency brake yet.
    if month <= 6:
        return params.tge_percent / 100.0
    if price_path["emergency_brake_month"] and price_path["emergency_brake_month"] <= month:
        return params.tge_percent / 100.0
    # approximate 0.3% monthly base release after month 6
    months_releasing = month - 6
    vested = (params.tge_percent / 100.0) + (0.003 * months_releasing)
    return min(vested, 1.0)


def roi_for_investment(investment_usd: float, vested_tokens: int, price: float) -> float:
    value = vested_tokens * price
    return (value / investment_usd - 1.0) * 100.0


# =============================================================================
# RUNNERS
# =============================================================================


def run_100_sims_per_model_market_types(seed: int = 1337) -> Dict[str, List[Dict]]:
    random.seed(seed)
    market_types = ["bull", "bear", "normal", "volatile"]
    sims_per_market = 25

    out: Dict[str, List[Dict]] = {}
    for model in MODELS:
        model_runs: List[Dict] = []
        for market in market_types:
            for i in range(sims_per_market):
                events = generate_market_events(market)
                months_max = max(ROI_HORIZONS)
                path = simulate_month_path(model, DEFAULT_LAUNCH_LIQUIDITY, events, months=months_max)
                month_12_price = path["prices"][12]
                # ROI table across investment levels
                roi_by_invest = {}
                for inv in INVESTMENT_LEVELS:
                    base = investor_base_tokens(inv)
                    by_month = {}
                    for h in ROI_HORIZONS:
                        px = path["prices"][h]
                        pct = investor_vested_pct(h, model, path)
                        vested = int(base * pct)
                        by_month[str(h)] = {
                            "vested_tokens": vested,
                            "value": vested * px,
                            "roi_pct": roi_for_investment(inv, vested, px),
                            "price": px,
                        }
                    roi_by_invest[str(inv)] = {"by_month": by_month}
                model_runs.append(
                    {
                        "market_type": market,
                        "sim_id": i,
                        "month_12_price": month_12_price,
                        "min_price": min(path["prices"]),
                        "max_price": max(path["prices"]),
                        "emergency_brake_month": path["emergency_brake_month"],
                        "prices_by_horizon": {str(h): path["prices"][h] for h in ROI_HORIZONS},
                        "roi_by_investment": roi_by_invest,
                    }
                )
        out[model.name] = model_runs
    return out


def run_100_per_model_per_choppy_scenario(seed: int = 2026) -> Dict[str, Dict[str, List[Dict]]]:
    random.seed(seed)
    results: Dict[str, Dict[str, List[Dict]]] = {}
    for model in MODELS:
        results[model.name] = {}
        for scenario_key, scenario in MARKET_SCENARIOS.items():
            scenario_runs: List[Dict] = []
            events = scenario["events"]
            for run_id in range(100):
                # note: keep base liquidity constant, events apply deltas
                months_max = max(ROI_HORIZONS)
                path = simulate_month_path(model, DEFAULT_LAUNCH_LIQUIDITY, events, months=months_max)
                month_12_price = path["prices"][12]
                roi_by_invest = {}
                for inv in INVESTMENT_LEVELS:
                    base = investor_base_tokens(inv)
                    by_month = {}
                    for h in ROI_HORIZONS:
                        px = path["prices"][h]
                        pct = investor_vested_pct(h, model, path)
                        vested = int(base * pct)
                        by_month[str(h)] = {
                            "vested_tokens": vested,
                            "value": vested * px,
                            "roi_pct": roi_for_investment(inv, vested, px),
                            "price": px,
                        }
                    roi_by_invest[str(inv)] = {"by_month": by_month}
                scenario_runs.append(
                    {
                        "run_id": run_id,
                        "month_12_price": month_12_price,
                        "min_price": min(path["prices"]),
                        "max_price": max(path["prices"]),
                        "emergency_brake_month": path["emergency_brake_month"],
                        "prices_by_horizon": {str(h): path["prices"][h] for h in ROI_HORIZONS},
                        "roi_by_investment": roi_by_invest,
                    }
                )
            results[model.name][scenario_key] = scenario_runs
    return results


def summarize_roi_by_horizon(model_runs: List[Dict], investment: int) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    for h in ROI_HORIZONS:
        hs = str(h)
        rois = [r["roi_by_investment"][str(investment)]["by_month"][hs]["roi_pct"] for r in model_runs]
        values = [r["roi_by_investment"][str(investment)]["by_month"][hs]["value"] for r in model_runs]
        prices = [r["roi_by_investment"][str(investment)]["by_month"][hs]["price"] for r in model_runs]
        brake_rate = (
            sum(1 for r in model_runs if r["emergency_brake_month"] != 0 and r["emergency_brake_month"] <= h)
            / len(model_runs)
            * 100.0
        )
        out[hs] = {
            "roi_avg": statistics.mean(rois),
            "roi_median": statistics.median(rois),
            "roi_p10": statistics.quantiles(rois, n=10)[0],
            "roi_p90": statistics.quantiles(rois, n=10)[-1],
            "value_avg": statistics.mean(values),
            "price_avg": statistics.mean(prices),
            "brake_rate_pct": brake_rate,
        }
    return out


def summarize_roi_by_market_type(model_runs: List[Dict], investment: int) -> Dict[str, Dict[str, Dict]]:
    """
    Summarize ROI by market type (bull/bear/normal/volatile) for each horizon.
    Output shape: market_type -> horizon(str) -> stats
    """
    out: Dict[str, Dict[str, Dict]] = {}
    by_mt: Dict[str, List[Dict]] = {}
    for r in model_runs:
        by_mt.setdefault(r["market_type"], []).append(r)
    for mt, runs in by_mt.items():
        out[mt] = summarize_roi_by_horizon(runs, investment)
    return out


def main() -> None:
    print("=" * 80)
    print("SECOND OPINION: 100 sims compare + investment-level ROI + choppy market")
    print("=" * 80)
    print(f"Models: {[m.name for m in MODELS]}")
    print(f"Investment levels: {INVESTMENT_LEVELS}")
    print(f"Choppy scenarios: {len(MARKET_SCENARIOS)}")

    print("\nPhase A: 100 simulations per model across 4 market types...")
    primary = run_100_sims_per_model_market_types(seed=1337)

    print("Phase B: 100 Monte Carlo runs per model per choppy scenario...")
    choppy = run_100_per_model_per_choppy_scenario(seed=2026)

    print("Phase C: Aggregating summaries...")
    investment_summaries = {}
    for model_name, runs in primary.items():
        investment_summaries[model_name] = {str(inv): summarize_roi_by_horizon(runs, inv) for inv in INVESTMENT_LEVELS}

    choppy_summaries = {}
    for model_name, scenarios in choppy.items():
        choppy_summaries[model_name] = {}
        for scenario_key, runs in scenarios.items():
            choppy_summaries[model_name][scenario_key] = {str(inv): summarize_roi_by_horizon(runs, inv) for inv in INVESTMENT_LEVELS}

    # Compact, analysis-ready output (keeps summaries; omits raw run cubes to stay under repo limits).
    output = {
        "timestamp": datetime.now().isoformat(),
        "methodology": {
            "pricing": "baseline liquidity/circulating + order-book depth + sell-pressure impacts",
            "buy_support_pct": BUY_SUPPORT_PCT,
            "depth_factor": DEPTH_FACTOR,
            "notes": "Second opinion. Results will differ numerically from primary AMM-only script.",
        },
        "models": [m.__dict__ for m in MODELS],
        "investment_levels": INVESTMENT_LEVELS,
        "roi_horizons_months": ROI_HORIZONS,
        "liquidity_base": DEFAULT_LAUNCH_LIQUIDITY,
        "market_scenarios": {k: v["name"] for k, v in MARKET_SCENARIOS.items()},
        "summaries": {
            "primary_by_investment": investment_summaries,
            "primary_by_market_type_and_investment": {
                model_name: {str(inv): summarize_roi_by_market_type(runs, inv) for inv in INVESTMENT_LEVELS}
                for model_name, runs in primary.items()
            },
            "choppy_by_scenario_and_investment": choppy_summaries,
        },
    }

    model_count = len(MODELS)
    out_json = Path(f"data/results/second_opinion_compare_results_{model_count}_models.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(output, indent=2))

    # Optional: store the full raw cube as gzip for offline triage (kept out of markdown generator).
    raw_out_gz = Path(f"data/results/second_opinion_compare_results_{model_count}_models_raw.json.gz")
    raw_payload = {
        "timestamp": output["timestamp"],
        "models": [m.__dict__ for m in MODELS],
        "investment_levels": INVESTMENT_LEVELS,
        "roi_horizons_months": ROI_HORIZONS,
        "liquidity_base": DEFAULT_LAUNCH_LIQUIDITY,
        "market_scenarios": {k: v["name"] for k, v in MARKET_SCENARIOS.items()},
        "primary_100_sims": primary,
        "choppy_100_runs": choppy,
    }
    with gzip.open(raw_out_gz, "wt", encoding="utf-8") as f:
        json.dump(raw_payload, f)

    # Produce a short markdown report
    def fmt_pct(x: float) -> str:
        return f"{x:+.1f}%"

    def fmt_usd(x: float) -> str:
        return f"${x:,.0f}"

    lines: List[str] = []
    lines.append(f"# Second Opinion Report ({len(MODELS)} Models): 100 Sims Comparison + Investment-Level ROI\n")
    lines.append(f"**Generated**: {output['timestamp']}\n")
    lines.append("## Methodology\n")
    lines.append("- **Pricing**: baseline (Liquidity / Circulating) + order-book depth + sell-pressure impacts\n")
    lines.append(f"- **Buy-support fraction**: {BUY_SUPPORT_PCT:.0%}\n")
    lines.append(f"- **Depth factor**: {DEPTH_FACTOR:.2f}\n")
    lines.append(f"- **Runs**: 100 per model (market-type Monte Carlo) + 100 per model per choppy scenario\n")
    lines.append(f"- **Liquidity base**: {fmt_usd(DEFAULT_LAUNCH_LIQUIDITY)}\n")
    lines.append("- **Note**: Some newer protocol mechanics are approximated to fit this harness (e.g., adaptive gates/streaming/buyback logic).\n")

    lines.append("\n## Focus Comparison (Hybrid Tokenomics vs Hybrid B)\n")
    lines.append(f"**ROI horizons**: {', '.join(str(h) for h in ROI_HORIZONS)} months\n\n")
    for inv in INVESTMENT_LEVELS:
        lines.append(f"### Investment: {fmt_usd(inv)}\n")
        for h in ROI_HORIZONS:
            hs = str(h)
            a = investment_summaries[HYBRID_TOKENOMICS_MODEL.name][str(inv)][hs]
            b = investment_summaries[HYBRID_B_MODEL.name][str(inv)][hs]
            lines.append(f"#### Month {h}\n")
            lines.append("| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake Rate |\n")
            lines.append("|---|---:|---:|---:|---:|---:|\n")
            lines.append(
                f"| {HYBRID_TOKENOMICS_MODEL.name} | {fmt_pct(a['roi_avg'])} | {fmt_usd(a['value_avg'])} | {fmt_pct(a['roi_median'])} | {fmt_pct(a['roi_p10'])}..{fmt_pct(a['roi_p90'])} | {a['brake_rate_pct']:.1f}% |\n"
            )
            lines.append(
                f"| {HYBRID_B_MODEL.name} | {fmt_pct(b['roi_avg'])} | {fmt_usd(b['value_avg'])} | {fmt_pct(b['roi_median'])} | {fmt_pct(b['roi_p10'])}..{fmt_pct(b['roi_p90'])} | {b['brake_rate_pct']:.1f}% |\n"
            )

    lines.append("\n## ROI by Investment Level (All Models)\n")
    lines.append("_Note: In a linear model with no investor-size slippage, ROI will be very similar across investment sizes; we still list all levels as requested._\n\n")
    for inv in INVESTMENT_LEVELS:
        lines.append(f"### Investment: {fmt_usd(inv)}\n")
        for h in ROI_HORIZONS:
            hs = str(h)
            lines.append(f"#### Month {h}\n")
            lines.append("| Model | Avg ROI | Avg Value | Median ROI | Brake Rate |\n")
            lines.append("|---|---:|---:|---:|---:|\n")
            for m in MODELS:
                s = investment_summaries[m.name][str(inv)][hs]
                lines.append(f"| {m.name} | {fmt_pct(s['roi_avg'])} | {fmt_usd(s['value_avg'])} | {fmt_pct(s['roi_median'])} | {s['brake_rate_pct']:.1f}% |\n")

    lines.append("\n## Choppy Market Performance (10 scenarios) — Avg ROI @ $9,000\n")
    inv = 9000
    for h in ROI_HORIZONS:
        hs = str(h)
        lines.append(f"### Month {h}\n")
        lines.append("| Scenario | Hybrid Tokenomics Avg ROI | Hybrid B Avg ROI | Notes |\n")
        lines.append("|---|---:|---:|---|\n")
        for scenario_key, scenario in MARKET_SCENARIOS.items():
            a = choppy_summaries[HYBRID_TOKENOMICS_MODEL.name][scenario_key][str(inv)][hs]
            b = choppy_summaries[HYBRID_B_MODEL.name][scenario_key][str(inv)][hs]
            notes = ""
            if "Crash" in scenario["name"] or "Collapse" in scenario["name"] or "Black Swan" in scenario["name"]:
                notes = "stress"
            lines.append(f"| {scenario['name']} | {fmt_pct(a['roi_avg'])} | {fmt_pct(b['roi_avg'])} | {notes} |\n")

    out_md = Path(f"docs/vesting/SECOND_OPINION_COMPARE_REPORT_{model_count}_MODELS.md")
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("".join(lines))

    print("\n✅ Wrote:")
    print(f"- {out_json}")
    print(f"- {out_md}")
    print(f"- {raw_out_gz} (gzipped raw runs for offline triage)")


if __name__ == "__main__":
    main()


