#!/usr/bin/env python3
"""
Generate docs/vesting/ALL_MODEL_COMPARISON.md from second_opinion_compare_results_v31.json
including ROI/value at multiple horizons (12/24/36/48/72 months).
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Dict, List, Tuple


IN_JSON = Path("second_opinion_compare_results_v31.json")
OUT_MD = Path("docs/vesting/ALL_MODEL_COMPARISON.md")

INVESTMENT_REF = "9000"


def fmt_pct(x: float) -> str:
    return f"{x:+.1f}%"


def fmt_usd(x: float) -> str:
    return f"${x:,.0f}"


def verdict_for(model: str, roi: float, brake: float, best_roi: float) -> str:
    # Keep this intentionally simple and consistent with the doc’s tone.
    if abs(roi - best_roi) < 1e-9:
        return "Best ROI (raw), but check brake risk"
    if brake <= 5.0 and roi >= (best_roi - 25.0):
        return "Best balance (ROI + access)"
    if brake >= 95.0:
        return "High gate/brake risk (often “stuck”)"
    if brake <= 5.0 and roi < (best_roi - 25.0):
        return "Stable/accessible, weaker ROI"
    return "Trade-off: ROI vs access"


def group_by_market_type(primary_runs: List[Dict]) -> Dict[str, List[Dict]]:
    out: Dict[str, List[Dict]] = {}
    for r in primary_runs:
        out.setdefault(r["market_type"], []).append(r)
    return out


def summarize_runs_by_horizon(runs: List[Dict], investment: str, horizons: List[int]) -> Dict[str, Dict]:
    out: Dict[str, Dict] = {}
    for h in horizons:
        hs = str(h)
        rois = [r["roi_by_investment"][investment]["by_month"][hs]["roi_pct"] for r in runs]
        values = [r["roi_by_investment"][investment]["by_month"][hs]["value"] for r in runs]
        brake = sum(1 for r in runs if r["emergency_brake_month"] and r["emergency_brake_month"] <= h) / len(runs) * 100.0
        out[hs] = {
            "roi_avg": statistics.mean(rois),
            "roi_median": statistics.median(rois),
            "roi_p10": statistics.quantiles(rois, n=10)[0],
            "roi_p90": statistics.quantiles(rois, n=10)[-1],
            "value_avg": statistics.mean(values),
            "brake_rate_pct": brake,
        }
    return out


def main() -> None:
    data = json.loads(IN_JSON.read_text())
    horizons: List[int] = data.get("roi_horizons_months") or [12]
    liquidity = data.get("liquidity_base")
    ts = data.get("timestamp")
    scenario_name_map: Dict[str, str] = data.get("market_scenarios", {})

    models = [m["name"] for m in data["models"]]
    primary = data["primary_100_sims"]  # model -> list[runs]
    choppy = data["choppy_100_runs"]    # model -> scenario -> list[runs]

    # Precompute overall per-horizon stats for reference investment
    overall: Dict[str, Dict[str, Dict]] = {}
    for model in models:
        overall[model] = summarize_runs_by_horizon(primary[model], INVESTMENT_REF, horizons)

    # Winner per horizon (raw ROI)
    winner_by_h: Dict[str, Tuple[str, float]] = {}
    for h in horizons:
        hs = str(h)
        best = max(((m, overall[m][hs]["roi_avg"]) for m in models), key=lambda kv: kv[1])
        winner_by_h[hs] = best

    # Choppy avg ROI per horizon (avg across 10 scenarios)
    choppy_avg_by_h: Dict[str, Dict[str, float]] = {str(h): {} for h in horizons}
    scenario_keys = list(next(iter(choppy.values())).keys())
    for h in horizons:
        hs = str(h)
        for model in models:
            scenario_rois = []
            for sc in scenario_keys:
                runs = choppy[model][sc]
                rois = [r["roi_by_investment"][INVESTMENT_REF]["by_month"][hs]["roi_pct"] for r in runs]
                scenario_rois.append(statistics.mean(rois))
            choppy_avg_by_h[hs][model] = sum(scenario_rois) / len(scenario_rois)

    # Market-type breakdown per horizon
    market_types = ["bull", "bear", "normal", "volatile"]
    by_market: Dict[str, Dict[str, Dict[str, Dict]]] = {str(h): {} for h in horizons}  # h -> model -> market -> stats
    for model in models:
        grouped = group_by_market_type(primary[model])
        for h in horizons:
            hs = str(h)
            by_market[hs].setdefault(model, {})
            for mt in market_types:
                runs = grouped.get(mt, [])
                if not runs:
                    continue
                s = summarize_runs_by_horizon(runs, INVESTMENT_REF, [h])[hs]
                by_market[hs][model][mt] = {"roi_avg": s["roi_avg"], "brake_rate_pct": s["brake_rate_pct"]}

    lines: List[str] = []
    lines.append("# All Model Comparison: Investor Returns (Second Opinion, Order-Book + Sell Pressure)\n\n")
    lines.append(f"**Generated**: {ts}\n\n")
    lines.append("This document mirrors the *format/style* of `docs/vesting/THREE_MODEL_COMPARISON.md`, but covers **all models** currently tested.\n\n")

    lines.append("## Methodology (Second Opinion)\n")
    lines.append("- **Pricing**: baseline (Liquidity / Circulating) + order-book depth + sell-pressure impacts\n")
    if liquidity is not None:
        lines.append(f"- **Liquidity base**: {fmt_usd(liquidity)}\n")
    lines.append(f"- **Investment reference**: {fmt_usd(int(INVESTMENT_REF))}\n")
    lines.append(f"- **ROI horizons**: {', '.join(str(h) for h in horizons)} months\n")
    lines.append("- **Runs**: 100 sims/model across bull/bear/normal/volatile + 100 runs/model per each of 10 choppy scenarios\n\n")

    lines.append("## Executive Summary (multi-horizon)\n")
    lines.append("### Overall winner (raw ROI) by horizon\n\n")
    lines.append("| Horizon | Winner | Avg ROI |\n")
    lines.append("|---:|---|---:|\n")
    for h in horizons:
        hs = str(h)
        w, v = winner_by_h[hs]
        lines.append(f"| Month {h} | **{w}** | **{fmt_pct(v)}** |\n")
    lines.append("\n")

    # “Best balance” heuristic per horizon: lowest brake rate among top-3 ROI
    lines.append("### Best balance (ROI + access) by horizon\n\n")
    lines.append("| Horizon | Best balance | Avg ROI | Brake rate |\n")
    lines.append("|---:|---|---:|---:|\n")
    for h in horizons:
        hs = str(h)
        # Definition: among models with "low brake" (<=10%), pick the highest ROI.
        # If none qualify, fall back to the lowest brake within the top-3 ROI models.
        low_brake = [m for m in models if overall[m][hs]["brake_rate_pct"] <= 10.0]
        if low_brake:
            best_bal = max(low_brake, key=lambda m: overall[m][hs]["roi_avg"])
        else:
            ranked = sorted(((m, overall[m][hs]["roi_avg"]) for m in models), key=lambda kv: kv[1], reverse=True)
            top3 = [m for m, _ in ranked[:3]]
            best_bal = min(top3, key=lambda m: overall[m][hs]["brake_rate_pct"])
        lines.append(
            f"| Month {h} | **{best_bal}** | {fmt_pct(overall[best_bal][hs]['roi_avg'])} | {overall[best_bal][hs]['brake_rate_pct']:.1f}% |\n"
        )
    lines.append("\n")

    lines.append("### Avg choppy-market ROI (10 scenarios) by horizon\n\n")
    lines.append("| Horizon | Winner | Avg choppy ROI |\n")
    lines.append("|---:|---|---:|\n")
    for h in horizons:
        hs = str(h)
        w = max(((m, choppy_avg_by_h[hs][m]) for m in models), key=lambda kv: kv[1])
        lines.append(f"| Month {h} | **{w[0]}** | **{fmt_pct(w[1])}** |\n")
    lines.append("\n")

    lines.append("## Model Parameters (high level)\n")
    lines.append("For full model mechanics and definitions see:\n")
    lines.append("- `scripts/hybrid_tokenomics_second_opinion_compare.py`\n")
    lines.append("- `HYBRID_TOKENOMICS_COMPARE_ALL_PAST_MODELS.md`\n")
    lines.append("- Protocol v3.1 reference: `https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/`\n\n")

    # Main tables per horizon
    for h in horizons:
        hs = str(h)
        lines.append(f"## Month-{h} Results (All Models) — {fmt_usd(int(INVESTMENT_REF))} Reference\n\n")

        # compute best ROI for verdicts
        best_roi = max(overall[m][hs]["roi_avg"] for m in models)

        lines.append("| Model | Avg ROI | Avg Value | Median ROI | P10..P90 ROI | Brake rate | Verdict |\n")
        lines.append("|---|---:|---:|---:|---:|---:|---|\n")
        ranked_models = sorted(models, key=lambda m: overall[m][hs]["roi_avg"], reverse=True)
        for m in ranked_models:
            s = overall[m][hs]
            v = verdict_for(m, s["roi_avg"], s["brake_rate_pct"], best_roi)
            lines.append(
                f"| {m} | {fmt_pct(s['roi_avg'])} | {fmt_usd(s['value_avg'])} | {fmt_pct(s['roi_median'])} | "
                f"{fmt_pct(s['roi_p10'])}..{fmt_pct(s['roi_p90'])} | {s['brake_rate_pct']:.1f}% | {v} |\n"
            )
        lines.append("\n")

        lines.append(f"### Month-{h} ROI by Market Type (All Models) — Avg ROI / Brake rate\n")
        lines.append("| Model | Bull | Bear | Normal | Volatile |\n")
        lines.append("|---|---:|---:|---:|---:|\n")
        for m in ranked_models:
            row = []
            for mt in market_types:
                s = by_market[hs].get(m, {}).get(mt)
                if not s:
                    row.append("—")
                else:
                    row.append(f"{fmt_pct(s['roi_avg'])} ({s['brake_rate_pct']:.0f}%)")
            lines.append(f"| {m} | {row[0]} | {row[1]} | {row[2]} | {row[3]} |\n")
        lines.append("\n")

        lines.append(f"### Month-{h} Choppy Market Performance (10 scenarios) — Avg ROI @ {fmt_usd(int(INVESTMENT_REF))}\n")
        lines.append("| Scenario | " + " | ".join(models) + " |\n")
        lines.append("|---|"+ "|".join(["---:"] * len(models)) + "|\n")
        for sc in scenario_keys:
            # scenario name from MARKET_SCENARIOS isn't stored in JSON; use key as label
            # (we keep the key readable and consistent with scripts)
            scenario_rois = []
            for m in models:
                runs = choppy[m][sc]
                rois = [r["roi_by_investment"][INVESTMENT_REF]["by_month"][hs]["roi_pct"] for r in runs]
                scenario_rois.append(fmt_pct(statistics.mean(rois)))
            label = scenario_name_map.get(sc, sc)
            lines.append(f"| {label} | " + " | ".join(scenario_rois) + " |\n")
        lines.append("\n")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("".join(lines))
    print(f"✅ wrote {OUT_MD}")


if __name__ == "__main__":
    main()


