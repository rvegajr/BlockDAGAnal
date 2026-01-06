# 13-Model Comprehensive Analysis

**Generated**: 2026-01-05  
**Data Source**: BTC historical prices 2015-2024 (10 years of actual crypto market cycles)  
**Investment**: $100,000 baseline  
**Simulations**: 30 runs per model × 3 scenarios × 10 crash overlays

---

## Executive Summary

We tested **13 tokenomics protocols** using real-world historical crypto market data to determine which provides the best investor outcomes. The results reveal a clear hierarchy based on how each model handles sell pressure, liquidity preservation, and market volatility.

### 🏆 Final Rankings (by Conservative Year 3 ROI)

| Rank | Model | Author | Y3 ROI | Verdict |
|:----:|-------|--------|-------:|---------|
| 1 | **Protocol v3.0** | — | **+40%** | ✅ **WINNER** - Best risk-adjusted returns |
| 2 | Protocol v5.5 | Maxime | +7% | 🥈 Strong runner-up |
| 3 | Protocol v5.8 | Maxime | +7% | 🥈 Strong runner-up |
| 4 | Protocol v5.7 | Maxime | +4% | ⚠️ Good with streaming |
| 5 | Protocol v5.3 | Maxime | +3% | ⚠️ Good baseline |
| 6 | Hybrid Model | — | -35% | Breaks even by Y6 |
| 7 | Protocol v2.6 | — | -41% | ❌ Underperforms |
| 8 | Original Model | — | -45% | Breaks even by Y6 |
| 9 | Protocol v3.1 | — | -46% | ❌ Volume peg too restrictive |
| 10 | Hybrid Tokenomics | — | -58% | ❌ Over-conservative |
| 11 | HybridC | Ingo Jeanrond | -66% | ❌ Too restrictive |
| 12 | Harris Model | Harris | -67% | ❌ TGE too high |
| 13 | Hybrid B | — | -68% | ❌ Weakest performer |

---

## Detailed Model Analysis

### 1. Protocol v3.0 — **🏆 THE WINNER**

**Source**: [Protocol 3.0 Spec](https://a-changer-plus-tard.github.io/Protocol-3.0/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -58% | -43% | -70% |
| Year 3 | **+40%** | +209% | **+6%** |
| Year 6 | +27% | +646% | -7% |

**Why It Wins:**
- **Oracle price gate at $0.05**: Prevents vesting when price is below listing price
- **Emergency brake at $0.02**: Completely halts all releases during crashes
- **Drip throttling at 10%**: Between $0.02-$0.05, releases are reduced to 10%
- **24-month mining lock**: Prevents miner dumping in first 2 years

**Key Insight**: The combination of price gate + emergency brake + drip throttling creates a "pressure valve" that adapts to market conditions. When price falls, supply slows down. This is why it's the **only model with positive ROI by Year 3** in the conservative scenario.

---

### 2. Protocol v5.5 (Maxime) — **🥈 STRONG RUNNER-UP**

**Source**: [Protocol v5.5](https://a-changer-plus-tard.github.io/Protocol-v5.5-Original-Protocol-Bonus-48-Months-/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -37% | -20% | -56% |
| Year 3 | **+7%** | +130% | -15% |
| Year 6 | -14% | +596% | -31% |

**Why It Performs Well:**
- **48-month bonus vesting**: Extremely long lock on bonus tokens reduces sell pressure
- **Volume pegging at 2%**: Limits daily sell volume to 2% of 24h trading volume
- **Mining cap at 20%**: Prevents miner inflation overwhelming the market
- **12-month extended lock effect**: Additional mining lock period

**Key Insight**: The 48-month bonus vesting (vs 36 months in v5.3) makes a meaningful difference. By keeping bonus tokens locked longer, sell pressure is distributed over a longer period, leading to better price stability.

---

### 3. Protocol v5.8 (Maxime) — **🥈 STRONG RUNNER-UP**

**Source**: [Protocol v5.8](https://a-changer-plus-tard.github.io/Protocol-v5.8-Revised-Protocol-Bonus-48-Months/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -38% | -20% | -56% |
| Year 3 | **+7%** | +128% | -15% |
| Year 6 | -14% | +596% | -31% |

**Why It Performs Well:**
- **Block-by-block streaming**: Tokens unlock every ~12 seconds, making sell pressure invisible
- **Adaptive Trend Shield**: 15% trailing MA instead of static price gate
- **Dynamic Discharge**: Buy-wall refill at 20% ratio
- **Liquidity Circuit Breaker**: Auto-buyback on price floor

**Key Insight**: The revised mechanisms (streaming + adaptive shield) provide marginally better performance than the original v5.5. The continuous release pattern distributes sell pressure more evenly.

---

### 4. Protocol v5.7 (Maxime) — **⚠️ GOOD**

**Source**: [Protocol v5.7](https://a-changer-plus-tard.github.io/Protocol-v5.7-Revised-Protocol-Bonus-36-Months-3/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -50% | -36% | -67% |
| Year 3 | **+4%** | +124% | -22% |
| Year 6 | -15% | +573% | -33% |

**Why It's Good But Not Best:**
- Same revised mechanisms as v5.8 (streaming, adaptive shield, etc.)
- **36-month bonus vesting** (shorter than v5.5/v5.8)

**Key Insight**: The 36-month bonus period releases tokens earlier than v5.5/v5.8, creating slightly more sell pressure. This shows that **bonus vesting duration matters**.

---

### 5. Protocol v5.3 (Maxime) — **⚠️ GOOD**

**Source**: [Protocol v5.3](https://a-changer-plus-tard.github.io/Protocol-v5.3-Original-Protocol-Bonus-36-Months-/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -50% | -36% | -67% |
| Year 3 | **+3%** | +125% | -21% |
| Year 6 | -15% | +573% | -33% |

**Why It's Good:**
- **6 Pillars**: Oracle Gate, Mining Cap, Emergency Brake, Volume Peg, DAO Consensus, Ultimatum Burn
- Solid foundation with all key protective mechanisms

**Key Insight**: v5.3 is the "baseline" of Maxime's protocol family. The 6-pillar approach works well, but the 36-month bonus period and lack of streaming mechanisms put it slightly behind v5.5/v5.8.

---

### 6. Hybrid Model — **BREAKS EVEN BY Y6**

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -72% | -55% | -83% |
| Year 3 | -35% | +153% | -61% |
| Year 6 | **+3%** | **+1240%** | -38% |

**Why It Breaks Even Eventually:**
- **50% mandatory staking**: Half of released tokens are locked in staking
- **3-month cliff + 36-month vesting**: Moderate release schedule
- No price gate or emergency brake

**Key Insight**: The staking mechanism helps long-term, but the lack of price-adaptive mechanisms means it suffers more during downturns. It eventually breaks even by Year 6, but requires patience.

---

### 7. Protocol v2.6 — **❌ UNDERPERFORMS**

**Source**: [Protocol v2.6](https://a-changer-plus-tard.github.io/BlockDag-Launch-Protocol-v2.6/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -65% | -51% | -78% |
| Year 3 | -41% | +86% | -65% |
| Year 6 | **-49%** | +306% | **-70%** |

**Why It Underperforms:**
- **Price gate at $0.05 but NO emergency brake**
- **NO drip throttling** between $0.02-$0.05
- Tokens either fully release or fully stop—no middle ground

**Key Insight**: The binary nature of v2.6 (all-or-nothing gate) hurts it. When price is between $0.02-$0.05, there's no throttling, so sell pressure continues at full force.

---

### 8. Original Model — **BREAKS EVEN BY Y6**

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -92% | -87% | -95% |
| Year 3 | -45% | +113% | -67% |
| Year 6 | **+3%** | **+1245%** | -38% |

**Why It Eventually Works:**
- **12-month cliff**: Long initial lock
- **60-month vesting**: Very slow release
- **50% mandatory staking**

**Key Insight**: The extremely long vesting (60 months) and 12-month cliff eventually pay off in ideal conditions. However, the lack of any price-adaptive mechanisms means severe losses in Year 1.

---

### 9. Protocol v3.1 (Adjusted) — **❌ VOLUME PEG TOO RESTRICTIVE**

**Source**: [Protocol v3.1](https://a-changer-plus-tard.github.io/Protocol-3.1-Ajusted-/)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -66% | -54% | -79% |
| Year 3 | -46% | +44% | -66% |
| Year 6 | **-54%** | +287% | **-71%** |

**Why It Underperforms:**
- **Volume pegging at 2%**: Good idea, but...
- **Mining capped at 20% of volume**: Also good, but...
- **21-month vesting**: Too fast, creates front-loaded pressure

**Key Insight**: The volume pegging is well-intentioned but the 21-month vesting period is too short. By the time protective mechanisms kick in, too much supply has already been released.

---

### 10. Hybrid Tokenomics (Solvency-Anchored) — **❌ OVER-CONSERVATIVE**

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -80% | -67% | -88% |
| Year 3 | -58% | +68% | -78% |
| Year 6 | -27% | +880% | -64% |

**Why It Underperforms:**
- **60% mandatory staking**: Very high lock
- **70% mining lock**: Most mining rewards are locked
- **1% global monthly cap**: Very restrictive

**Key Insight**: This model is *too* conservative. By restricting releases so heavily, it paradoxically creates more price pressure because the tokens that *do* release face a thinner liquidity environment.

---

### 11. HybridC (Ingo Jeanrond) — **❌ TOO RESTRICTIVE**

**Source**: docs/HybridC_Tokenomics_Test.xlsx

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -83% | -72% | -90% |
| Year 3 | -66% | +37% | -84% |
| Year 6 | -41% | +690% | -75% |

**Why It Underperforms:**
- **0.3% monthly cap**: Extremely conservative—only 0.3% of supply can release per month
- **50% auto-stake**: Additional locking
- **85% mining lock**: Only 15% of mining rewards are liquid

**Key Insight**: The 0.3% monthly cap is far too restrictive. While it protects against dumping, it also means legitimate liquidity demand can't be met, leading to price suppression. The ultra-conservative approach backfires.

---

### 12. Harris Model — **❌ TGE TOO HIGH**

**Source**: [Harris Vesting PDF](https://github.com/harrisjustinhagen-oss/Vesting-Economy_Harris/blob/main/BDAG%20VESTING%20HARRIS.pdf)

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -83% | -73% | -90% |
| Year 3 | -67% | +29% | -80% |
| Year 6 | -48% | +577% | -69% |

**Why It Underperforms:**
- **10% TGE**: Highest of all models—huge day-1 sell pressure
- **9-month vesting**: Fastest vesting period—all tokens unlocked by month 9
- **75% miner hold incentive**: Good idea, but can't offset the TGE problem

**Key Insight**: The 10% TGE is the killer. Even with the clever miner incentive (1.75x multiplier for holding), the massive initial unlock creates too much sell pressure. Compare to v3.0's 3% TGE—the difference is dramatic.

---

### 13. Hybrid B — **❌ WEAKEST PERFORMER**

| Metric | Conservative | Ideal | Choppy |
|--------|-------------|-------|--------|
| Year 1 | -86% | -77% | -92% |
| Year 3 | -68% | +28% | -86% |
| Year 6 | -44% | +662% | -77% |

**Why It's Weakest:**
- **State-gated issuance**: Releases depend on market state
- **1% global monthly cap**: Restrictive
- **50% mandatory staking**: Heavy lock
- **36-month vesting**: Moderate

**Key Insight**: Hybrid B combines state-driven release with staking, but the combination doesn't work well. The state-gating often triggers during volatility, causing tokens to "bunch up" and release in clusters, creating price spikes.

---

## Why Protocol v3.0 Wins

The winning formula is **adaptive supply management**:

| Feature | v3.0 | Others |
|---------|------|--------|
| Price gate | ✅ $0.05 | Some have, some don't |
| Emergency brake | ✅ $0.02 | Few have this |
| Drip throttling | ✅ 10% between gate/brake | **Unique to v3.0** |
| Mining lock | ✅ 24 months | Varies widely |
| TGE | 3% | 2-10% |
| Vesting | 33 months | 9-60 months |

The **drip throttling** is the key differentiator. When price falls below $0.05 but stays above $0.02, v3.0 doesn't stop releases entirely—it throttles them to 10%. This:
1. Prevents the "supply shock" when brakes fully release
2. Maintains some liquidity for legitimate trading
3. Creates a gradual recovery path

---

## Investment Decision Matrix

| If You Want... | Choose | Why |
|----------------|--------|-----|
| **Best short-term (Y1-Y3)** | Protocol v3.0 | Only one with positive Y3 ROI |
| **Best long-term (Y6)** | Original or Hybrid Model | +1245% in ideal scenario |
| **Best crash protection** | Protocol v3.0 | +6% ROI even in choppy markets |
| **Maxime's best** | v5.5 or v5.8 | 48-month bonus lock is key |
| **Most conservative** | HybridC (Ingo) | 0.3% cap (but underperforms) |
| **Avoid** | Harris Model | 10% TGE is too high |

---

## Methodology Notes

### Simulation Parameters
- **Historical data**: BTC prices 2015-2024 (10 years)
- **Rolling windows**: 72-month forward projections
- **Investment levels**: $9,000 / $50,000 / $100,000
- **Launch liquidity**: $32,000,000
- **Scenarios**: Conservative (no growth), Ideal (50% CAGR), Choppy (10 crash overlays)

### Model Assumptions
- Price = f(Liquidity, Circulating Supply, Sell Pressure)
- Sell pressure = f(Vesting releases, Mining emissions, Market sentiment)
- Order book depth simulated with 20% ratio of 24h volume
- Emergency brakes fully halt releases when triggered

### Attribution
- **Maxime**: Protocol v5.3, v5.5, v5.7, v5.8
- **Ingo Jeanrond**: HybridC
- **Harris**: Harris Model

---

## Appendix: Full Data Tables

### Conservative Scenario (All 13 Models)

| Model | Y1 | Y2 | Y3 | Y6 | $100k→Y3 | $100k→Y6 |
|-------|---:|---:|---:|---:|---------:|---------:|
| Protocol v3.0 | -58% | -1% | +40% | +27% | $140,094 | $126,470 |
| Protocol v5.5 (Maxime) | -37% | -9% | +7% | -14% | $107,400 | $86,000 |
| Protocol v5.8 (Maxime) | -38% | -10% | +7% | -14% | $106,900 | $85,600 |
| Protocol v5.7 (Maxime) | -50% | -16% | +4% | -15% | $103,800 | $84,700 |
| Protocol v5.3 (Maxime) | -50% | -17% | +3% | -15% | $103,400 | $84,800 |
| Hybrid Model | -72% | -51% | -35% | +3% | $65,500 | $102,800 |
| Protocol v2.6 | -65% | -32% | -41% | -49% | $59,000 | $50,600 |
| Original Model | -92% | -62% | -45% | +3% | $55,200 | $103,100 |
| Protocol v3.1 (Adjusted) | -66% | -40% | -46% | -54% | $54,000 | $46,000 |
| Hybrid Tokenomics | -80% | -68% | -58% | -27% | $42,000 | $73,000 |
| HybridC (Ingo) | -83% | -74% | -66% | -41% | $34,000 | $59,000 |
| Harris Model | -83% | -74% | -67% | -48% | $33,000 | $52,000 |
| Hybrid B | -86% | -76% | -68% | -44% | $32,000 | $56,000 |

---

*Report generated by BlockDAG Tokenomics Simulation Framework*

