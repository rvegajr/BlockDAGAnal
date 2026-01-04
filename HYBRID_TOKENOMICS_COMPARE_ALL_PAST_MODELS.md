# Hybrid Tokenomics vs All Previously-Tested Models (Compare + Contrast)

**Generated**: 2026-01-03  
**Purpose**: Compare **Hybrid Tokenomics (Solvency‑Anchored, State‑Driven)** against **every model we’ve previously simulated** in this repo, across:
- **Design mechanics** (how supply is controlled)
- **Investor outcomes** (Month‑12 ROI/value in our harnesses)
- **Choppy market behavior** (10 historical/choppy scenarios)
- **Liquidity sensitivity** (tier testing where available)

---

## Models included (all previously tested)

From our prior simulation harnesses and results files, the “past models” set is:
- **Original Model** (2% TGE, 12mo cliff, 60mo vest)
- **Hybrid Model** (3% TGE, 3mo cliff, 36mo vest)
- **Protocol v2.6** (3% TGE, 3mo cliff, 21mo vest, price gate)
- **Protocol v3.0** (3% TGE, 3mo cliff, 33mo vest, price gate + brake + drip + mining locks)
- **Protocol v3.1 (Adjusted)** (3% TGE, 3mo cliff, 21mo linear vest, price gate @ $0.05, emergency brake @ $0.02, volume pegging, volume-capped mining) — from `https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/`[^v31]
- **Hybrid B** (state‑driven + time‑oriented review window; implemented as state‑driven release in our harness)
- **Hybrid Tokenomics (Solvency‑Anchored)** (3% TGE, 90‑day cliff, observation window, state‑driven issuance + global caps, heavy staking/locks)

**Primary sources (results):**
- `hybrid_tokenomics_comparison_results.json` (5 models incl. Hybrid B + Hybrid Tokenomics + liquidity sweep)
- `three_model_comparison_results.json` (Original / Hybrid / v2.6)
- `four_model_comparison_results.json` (adds Protocol v3.0)
- `liquidity_tier_comparison_v2_results.json` (liquidity tiers for Original / Hybrid / v2.6 / v3.0)
- `second_opinion_compare_results.json` + `SECOND_OPINION_COMPARE_REPORT.md` (2nd‑opinion pricing, 5 models; does **not** include v3.0)
- `third_opinion_v31_results.json` + `THIRD_OPINION_V31_REPORT.md` (3rd‑opinion, path‑dependent sim including Protocol v3.1)

---

## Design / mechanism differences (why these models behave differently)

### Hybrid Tokenomics (Solvency‑Anchored, State‑Driven)
- **Supply control primitive**: **market‑state gating + global circulating cap** (issuance throttles to what liquidity/price trend can absorb)
- **Launch survivability**: 3% TGE, then **hard 90‑day cliff**
- **Observation window**: no vesting releases early; mining continues but **heavily locked**
- **Locks/staking**: higher mandatory staking (modeled at **60%**) + mining lock ratio (modeled **70%** early)
- **Bonus token policy**: modeled using Option **B** style (state‑gated, counted in cap)
- **Failure mode**: in extreme shocks, issuance pauses; survivability becomes liquidity‑bounded rather than schedule‑bounded

### Hybrid B (State‑Driven + Time Orientation)
- **Supply control primitive**: primarily **state‑driven**, with limited time‑window reviews (in docs); in our harness this behaves like **state‑gated release** without the annual “review tranche”
- **Locks/staking**: lower than Hybrid Tokenomics (modeled at **50%**)
- **Failure mode**: more circulation under stress vs Hybrid Tokenomics → worse in choppy markets

### Protocol v3.0 (Hybrid Optimized)
- **Supply control primitive**: **oracle gates + drip factor + explicit mining lock months**
- **Designed for**: strong performance when liquidity is high enough that gates rarely bind; constrains issuance in down markets
- **Failure mode**: at low liquidity, gates bind often; results become very sensitive to liquidity tier

### Protocol v2.6
- **Supply control primitive**: **price gate at $0.05** (strong gating)
- **Failure mode**: in most realistic low‑liquidity stress, vesting is effectively frozen (high “brake/gate binding” rate)

### Hybrid Model (earlier “realistic hybrid”)
- **Supply control primitive**: time‑based vesting + emergency brake logic
- **Failure mode**: frequent brake activation in stress; more schedule‑dependent than state‑dependent

### Original Model
- **Supply control primitive**: long cliff + slow vesting (time‑based)
- **Failure mode**: lowest returns, but very steady (few explicit brakes)

---

## Performance snapshot @ $32M liquidity (Primary harness, AMM‑style)

These are **Month‑12 investor outcomes** from `hybrid_tokenomics_comparison_results.json` (our newest “primary” harness):

| Model | Month‑12 ROI (avg) | Month‑12 Value (avg) | Brake rate |
|---|---:|---:|---:|
| **Protocol v2.6** | **-77.2%** | **$2,049** | **98.0%** |
| Hybrid Model | -83.2% | $1,510 | 98.0% |
| **Hybrid Tokenomics (Solvency‑Anchored)** | -90.6% | $845 | **2.0%** |
| Hybrid B | -93.6% | $578 | 3.0% |
| Original Model | -95.3% | $421 | 0.0% |

**How to read this correctly:** Protocol v2.6 and the earlier Hybrid Model show “better ROI”, but they also show **very high brake/gate binding** in this harness. Hybrid Tokenomics is designed to keep issuance adaptive (low brake rate) even if raw ROI is lower at $32M.

---

## Second‑opinion performance @ $32M (Order‑book + sell‑pressure pricing)

Second‑opinion results (different methodology) from `SECOND_OPINION_COMPARE_REPORT.md`:

### Hybrid Tokenomics vs Hybrid B (the “4th model”)

| Model | Avg Month‑12 ROI | P10..P90 ROI | Brake rate |
|---|---:|---:|---:|
| **Hybrid Tokenomics (Solvency‑Anchored)** | **-86.8%** | -92.4%..-79.8% | **2.0%** |
| Hybrid B | -90.8% | -94.7%..-85.9% | 7.0% |

### All models (second opinion, Month‑12 ROI avg @ $32M)

| Model | Avg Month‑12 ROI | Brake rate |
|---|---:|---:|
| Hybrid Model | -85.4% | 100.0% |
| **Hybrid Tokenomics (Solvency‑Anchored)** | **-86.8%** | **2.0%** |
| Hybrid B | -90.8% | 7.0% |
| Protocol v2.6 | -93.1% | 100.0% |
| Original Model | -95.6% | 1.0% |

**Key takeaway from the second opinion:** Hybrid Tokenomics consistently beats Hybrid B in both **ROI distribution** and **brake rate** under a more realistic “sell pressure” price model.

> Note: the second‑opinion harness currently covers the same 5 models as `hybrid_tokenomics_comparison_results.json` and does **not** include Protocol v3.0 (because v3.0’s drip/gate/lock mechanics need explicit modeling in the second‑opinion engine).

---

## Choppy market comparison (10 scenarios)

### Second‑opinion “choppy market” (100 runs per scenario)

From `SECOND_OPINION_COMPARE_REPORT.md` (Avg ROI @ $9,000):

Hybrid Tokenomics beats Hybrid B in **every** choppy scenario in the second‑opinion model:
- Normal: **-87.0% vs -91.1%**
- May crash: **-94.8% vs -97.8%**
- High volatility: **-93.0% vs -97.0%**
- Stable growth: **-83.8% vs -89.0%**
- Worst cases (COVID / Multiple crashes): still better, though both are very negative

**Interpretation:** Under sell‑pressure pricing, Hybrid Tokenomics’ heavier staking/locks + state gating meaningfully reduces sell pressure relative to Hybrid B.

---

## Liquidity sensitivity (tier tests)

### Hybrid Tokenomics (our harness)

From `hybrid_tokenomics_comparison_results.json` liquidity sweep:

| Liquidity | Avg ROI (Month‑12) | Brake rate | Choppy survival (out of 10) |
|---:|---:|---:|---:|
| $20M | -94.2% | 7.0% | 6/10 |
| $32M | -90.3% | 2.0% | 7/10 |
| $50M | -84.8% | 0.0% | 9/10 |
| $75M | -76.9% | 0.0% | 10/10 |
| $100M | -71.0% | 0.0% | 10/10 |

**Practical threshold:** Hybrid Tokenomics becomes “very robust” around **$50M+**, and effectively “bulletproof” in our choppy set at **$75M+**.

### Older 4‑model liquidity tier harness (includes Protocol v3.0)

From `liquidity_tier_comparison_v2_results.json` (different harness + metrics):

**At $32M:** v3.0 and v2.6 are heavily constrained; survivability is low.  
**At $100M–$150M:** v3.0 becomes extremely strong (high survivability, much better ROI).

Selected highlights (Avg Month‑12 ROI / survival rate):
- **$32M**:
  - v3.0: ROI **-95.9%**, survival **17.9%**
  - v2.6: ROI **-99.2%**, survival **0.0%**
- **$100M**:
  - v3.0: ROI **-33.7%**, survival **98.3%**
- **$150M**:
  - v3.0: ROI **+0.8%**, survival **100%**

**What this means:** Protocol v3.0 appears to be a **high‑liquidity winner** (when gates rarely bind and liquidity absorbs sell flow), while Hybrid Tokenomics is designed to be a **low‑to‑mid liquidity survivability winner** via hard issuance caps + heavy locks.

---

## Compare/contrast summary (plain English)

### Where Hybrid Tokenomics is clearly stronger
- **Choppy markets at modest liquidity**: consistently better than Hybrid B (and typically more “accessible” than v2.6/v2.6‑style gating).
- **Brake/gate dependence**: much lower brake rates in both primary + second‑opinion harnesses.
- **Launch‑day survivability logic**: 3% TGE + strict early lock regimes aligns with “don’t die on day 1” constraint.

### Where other models can outperform Hybrid Tokenomics
- **High‑liquidity environments**: Protocol v3.0 (per the older tier harness) can outperform strongly when liquidity is very high (e.g., $100M–$150M).
- **Paper ROI under heavy gating**: Protocol v2.6 / Hybrid Model can show better ROI numbers in some harnesses, but are often paired with **near‑certain gating/brake activation** (low accessibility).

### Where Protocol v3.1 sits (based on third-opinion implementation)
- **Intent** (per v3.1 page): 3% solvency + oracle gate + emergency brake + volume pegging + volume-capped mining.[^v31]
- **Observed in our 3rd opinion @ $32M** (`THIRD_OPINION_V31_REPORT.md`): it behaves very similarly to a heavily-gated system under stress:
  - **High brake rate** and **very low ROI** in choppy scenarios
  - The volume peg + volume-capped mining help limit emissions/vesting when price is below target, but do not by themselves “create” price support in low-liquidity crash regimes.

---

## Immediate next step (optional, if you want absolute completeness)

If you want Hybrid Tokenomics compared to Protocol v3.0 under the **same second‑opinion pricing model**, I can extend `scripts/hybrid_tokenomics_second_opinion_compare.py` to implement v3.0’s:
- vest price gate (high/low thresholds),
- drip factor between bands,
- mining lock months,
and then rerun the same **100 sims + 10 choppy scenarios**.

---

[^v31]: Protocol v3.1 (Adjusted) spec page: `https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/`


