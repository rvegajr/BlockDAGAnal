#!/usr/bin/env python3
"""
Generate docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md from the latest
real-world multi-opinion backtest JSON (data/results/real_world_multi_opinion_results.json).

This keeps the investor-facing doc aligned with the current model set (e.g. 14 models).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


IN_JSON = Path("data/results/real_world_multi_opinion_results.json")
OUT_MD = Path("docs/vesting/INVESTOR_COMPARISON_REAL_WORLD.md")


def fmt_pct(x: float) -> str:
    return f"{x:+.0f}%"


def fmt_usd(x: float) -> str:
    return f"${x:,.0f}"


def value_from_roi(inv: int, roi_pct: float) -> float:
    return inv * (1.0 + roi_pct / 100.0)


def extract_table(data: Dict, opinion_idx: int, inv: int, horizons: List[int]) -> List[Dict]:
    rows = []
    by_model = data["opinions"][opinion_idx]["by_model"]
    for model_name in sorted(by_model.keys()):
        summ = by_model[model_name]["summary"][str(inv)]
        row = {"model": model_name}
        for h in horizons:
            roi = summ[str(h)]["roi_avg"]
            row[str(h)] = roi
        rows.append(row)
    return rows


def main() -> None:
    data = json.loads(IN_JSON.read_text())
    generated = datetime.now().strftime("%Y-%m-%d")

    models = sorted(data["opinions"][0]["by_model"].keys())
    model_count = len(models)

    horizons = [12, 36, 72]
    inv = 100_000

    cons = extract_table(data, 0, inv, horizons)
    ideal = extract_table(data, 1, inv, horizons)
    choppy = extract_table(data, 2, inv, horizons)

    def render_section(title: str, rows: List[Dict]) -> List[str]:
        lines: List[str] = []
        lines.append(f"### {fmt_usd(inv)} Investment — {title}\n\n")
        lines.append("| Model | Year 1 | Year 3 | Year 6 | $100k → Y3 | $100k → Y6 |\n")
        lines.append("|-------|-------:|-------:|-------:|----------:|----------:|\n")
        for r in rows:
            y1 = r["12"]
            y3 = r["36"]
            y6 = r["72"]
            v3 = value_from_roi(inv, y3)
            v6 = value_from_roi(inv, y6)
            lines.append(
                f"| {r['model']} | {fmt_pct(y1)} | {fmt_pct(y3)} | {fmt_pct(y6)} | {fmt_usd(v3)} | {fmt_usd(v6)} |\n"
            )
        lines.append("\n")
        return lines

    out: List[str] = []
    out.append("# Real-World Investor Comparison\n\n")
    out.append(f"**Generated**: {generated}  \n")
    out.append("**Data source**: BTC historical prices 2015-2024 (10 years of actual crypto market cycles)\n\n")
    out.append("## If You Invest Today, What Happens?\n\n")
    out.append(
        "This comparison uses **real historical crypto market data** (BTC 2015-2024) to show realistic outcomes across **three scenarios**:\n\n"
    )
    out.append("| Scenario | Assumption | Best for |\n")
    out.append("|----------|------------|----------|\n")
    out.append("| **Conservative** | No adoption growth (stress-test) | Worst-case planning |\n")
    out.append("| **Ideal** | 50% annual liquidity growth + steady inflows | Successful launch |\n")
    out.append("| **Choppy + Crashes** | Historical + 10 crash scenarios overlaid | Stress-test with shocks |\n")
    out.append("\n---\n\n")
    out.append(f"## 💰 Investment Comparison: What You Get Back (All {model_count} Models)\n\n")

    out.extend(render_section("Conservative (Stress-Test)", cons))
    out.extend(render_section("Ideal (Growth Scenario)", ideal))
    out.extend(render_section("With Crash Overlays (10 Scenarios)", choppy))

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("".join(out))
    print(f"✅ wrote {OUT_MD} ({model_count} models)")


if __name__ == "__main__":
    main()


