# Ingo Projects (Source CSVs)

This directory contains source CSV files for the "Ingo Projects" workstream. These are **inputs/source material** for model definitions and variants used in the simulation harness.

## 📊 Analysis Report

**[View Full Analysis →](../../reports/INGO_MODEL_ANALYSIS.md)**

The analysis evaluates all models against stated design goals:
- Risk-reward trade-offs
- Adaptive throttling & emergency controls
- Parameter sensitivity
- TGE isolation (0% vs 3%)
- Smooth transitions vs binary failure modes

---

## Models Integrated into Backtest

| File | Model Name in Harness | Status |
|------|----------------------|--------|
| `Hybrid B.csv` | Hybrid B (Ingo Detailed) | ✅ Tested |
| `hybrid C.csv` | Hybrid C (Ingo CSV) | ✅ Tested |
| `Hybrid.csv` | Hybrid (Ingo CSV) | ✅ Tested |
| `Hybrid Lite.csv` | Hybrid Lite (Ingo CSV) | ✅ Tested |
| `Hybrid_C_Lite_Defaults.csv` | Hybrid C Lite (Defaults, Ingo CSV) | ✅ Tested |
| `Hybrid_C_Lite_Plus.csv` | Hybrid C Lite+ Base (Ingo CSV) | ✅ Tested |
| `Hybrid_C_Lite_Plus_Final.csv` | Hybrid C Lite+ (Final, Ingo CSV) | ✅ Tested |
| `Hybrid_C_Lite_Plus_Extended.csv` | Hybrid C Lite+ Extended (Ingo CSV) | ✅ Tested |
| `Hybrid_C_Lite_Plus_Bonus_Variants.csv` | Variant A & B (Ingo CSV) | ✅ Tested |
| `Hybrid_D.1.csv` | Hybrid D.1 (Ingo CSV) | ✅ Tested |
| `Hybrid_E.1.csv` | Hybrid E.1 (both TGE variants) | ✅ Tested |
| `Hybrid_E_0__TGE.csv` | Hybrid E.1 0% TGE (Ingo CSV) | ✅ Tested |
| `Hybrid_E_3__TGE.csv` | Hybrid E.1 3% TGE (Ingo CSV) | ✅ Tested |
| `Hybrid_F.csv` | Hybrid F (Ingo CSV) | ✅ Tested |
| `Hybrid_F.1.csv` | Hybrid F.1 (Ingo CSV) | ✅ Tested |
| `Model_A_ROI.csv` | Model A (Base, Ingo CSV) | ✅ Tested |
| `Model_A_ROI_Final_Test.csv` | Model A (ROI Optimized, Ingo CSV) | ✅ Tested |
| `Model_A_Roi_Final_With_Bonus.csv` | Model A (Bonus Separated, Ingo CSV) | ✅ Tested |

## Reference Files (Not Models)

| File | Purpose |
|------|---------|
| `Hybrid_C_Lite_Plus_Test_Spec.csv` | Test specification / invariants |
| `ROI_Scenarios.csv` | Scenario assumptions |

---

## Results Summary

| Model | Conservative 72mo | Ideal 72mo | Rank |
|-------|-------------------|------------|:----:|
| **Hybrid C (Ingo CSV)** | -40.9% | +756.6% | 🥇 |
| **Hybrid B (Ingo Detailed)** | -46.6% | +672.9% | 🥈 |
| Hybrid C Lite (Defaults) | -51.7% | +598.5% | 🥉 |
| Hybrid C Lite+ Variant A | -59.3% | +541.9% | 4 |
| Hybrid D.1/E.1/F/F.1 | -82% | +301% | 10+ |

See **[Full Analysis](../../reports/INGO_MODEL_ANALYSIS.md)** for detailed breakdown.

---

*Last Updated: January 10, 2026*
