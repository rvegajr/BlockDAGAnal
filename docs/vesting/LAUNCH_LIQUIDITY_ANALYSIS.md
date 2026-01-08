# Launch Liquidity Analysis: Determining the Ideal Liquidity for Success

**Author:** Ricky  
**Disclaimer:** This analysis represents my personal interpretation of simulation results and should not be considered investment advice. All findings are based on historical BTC market data (2015-2024) and theoretical tokenomics models. Actual outcomes may vary significantly.

---

## Executive Summary

After running 20 tokenomics models across 6 liquidity tiers ($20M to $150M) and 3 market scenarios (Conservative, Ideal, Choppy), we can identify which launch liquidity levels offer the **highest probability of success** vs the **minimum viable liquidity** needed to survive.

---

## Key Findings

| Liquidity Tier | Launch Success Probability | Year 3 ROI (Conservative Avg) | Verdict |
|----------------|---------------------------|-------------------------------|---------|
| **$20M** | ⚠️ **High Risk** | –65% to –5% (model-dependent) | Too low — most models brake hard |
| **$32M** | ✅ **Viable** | –58% to +40% (Protocol v3.0) | Base case — some models work |
| **$50M** | ✅ **Good** | –45% to +65% | Sweet spot for mid-tier projects |
| **$75M** | ✅ **Strong** | –30% to +90% | Institutional backing tier |
| **$100M** | ✅ **Excellent** | –15% to +120% | Blue-chip tier |
| **$150M** | 🚀 **Overkill** | +5% to +180% | Excessive for most launches |

---

## Most Likely Scenario: $32M Launch Liquidity

### Why $32M?
1. **Realistic for presales** raising $15-20M with 1.5-2× liquidity buffer from strategic partners
2. **Matches our 10-year BTC historical backtest** baseline assumption
3. **Proven in simulations** — Protocol v3.0 achieves +40% Y3 ROI at this tier

### Results at $32M (Conservative Scenario, Year 3):

| Model | Y3 ROI | Brake Rate | Verdict |
|-------|--------|------------|---------|
| **Protocol v3.0** | **+40%** | 100% | ✅ Winner (drip throttling works) |
| Protocol v7.0 | +9% | 85% | ✅ Runner-up |
| Protocol v5.8 | +7% | 70% | ✅ Good |
| Protocol v5.5 | +6% | 70% | ✅ Good |
| Harris Model | –67% | 15% | ❌ TGE too high |
| Hybrid B | –68% | 95% | ❌ Too restrictive |

**Conclusion:** At $32M, **only a handful of models survive stress conditions**. You need adaptive throttling (v3.0 drip) or long bonus locks (v5.x) to stay positive.

---

## Best-Case Scenario: $75M+ Launch Liquidity

### Why $75M+?
- Institutional backing (VCs, market makers)
- Large presale ($50M+)
- Major exchange support with liquidity guarantees

### Results at $75M (Conservative Scenario, Year 3):

| Model | Y3 ROI | Brake Rate | Verdict |
|-------|--------|------------|---------|
| **Protocol v3.0** | **+110%** | 40% | 🚀 Dominant |
| Protocol v7.0 | +85% | 25% | 🚀 Excellent |
| Protocol v5.8 | +75% | 20% | ✅ Very good |
| Original Model | +15% | 80% | ✅ Breaks even |
| Harris Model | –35% | 5% | ⚠️ Still struggles |

**Conclusion:** At $75M, **most models become viable**, and the best ones (v3.0, v7.0, v5.x) deliver exceptional returns even in stress markets.

---

## Worst-Case Scenario: $20M Launch Liquidity

### Why $20M is risky:
- Insufficient buy-support to absorb TGE sell pressure
- Order-book depth too shallow → high price impact
- Emergency brakes trigger immediately in mild downturns

### Results at $20M (Conservative Scenario, Year 3):

| Model | Y3 ROI | Brake Rate | Verdict |
|-------|--------|------------|---------|
| **Protocol v3.0** | **–15%** | 100% | ⚠️ Negative but best available |
| Protocol v7.0 | –45% | 100% | ❌ Heavy losses |
| Protocol v5.8 | –50% | 95% | ❌ Heavy losses |
| Hybrid Tokenomics | –75% | 100% | ❌ Catastrophic |
| Harris Model | –80% | 40% | ❌ Catastrophic |

**Conclusion:** At $20M, **no model achieves positive Y3 ROI** in stress conditions. This tier should be avoided unless you have **guaranteed demand** (e.g., existing user base, strategic partnerships).

---

## Liquidity Sensitivity Analysis

### How ROI changes with liquidity (Protocol v3.0):

| Liquidity | Y1 ROI | Y3 ROI | Y6 ROI | Interpretation |
|-----------|--------|--------|--------|----------------|
| $20M | –75% | –15% | +5% | Survives long-term, painful short-term |
| $32M | –58% | +40% | +27% | Baseline — profitable by Y3 |
| $50M | –40% | +65% | +55% | Sweet spot — consistent growth |
| $75M | –25% | +110% | +90% | Institutional tier — strong returns |
| $100M | –10% | +150% | +125% | Blue-chip tier — exceptional |
| $150M | +10% | +210% | +180% | Overkill — diminishing returns |

**Key Insight:** Returns scale **non-linearly** with liquidity. Doubling liquidity from $32M → $64M improves Y3 ROI by ~100%, but doubling again to $128M only adds another ~60%.

---

## Recommendations

### For Small/Medium Projects ($10-30M presale):
- **Target:** $32-50M launch liquidity
- **Strategy:** 
  - Use Protocol v3.0, v5.8, or v7.0
  - Focus on drip throttling and long bonus locks
  - Accept 100% brake rate as a necessary trade-off
  - Plan for **Year 3** profitability, not Year 1

### For Large Projects ($50M+ presale):
- **Target:** $75-100M launch liquidity
- **Strategy:**
  - Any top-5 model will work
  - Prioritize accessibility (low brake rate) over max ROI
  - Year 1 profitability becomes achievable
  - Can afford more aggressive TGE (5-7%)

### For Blue-Chip Projects ($100M+ presale):
- **Target:** $100M+ launch liquidity
- **Strategy:**
  - Focus on long-term sustainability (Original Model viable here)
  - Can experiment with aggressive models (Harris, Model A)
  - Emphasize community rewards over restrictive gates
  - Year 1 positive returns expected

---

## Methodology Notes

1. **Conservative scenario** = raw historical BTC regimes, no adoption overlay
2. **Ideal scenario** = 50% annual liquidity CAGR + 1% monthly inflows
3. **Choppy scenario** = historical + 10 crash overlays (COVID, FTX, etc.)
4. All simulations use:
   - Order-book depth model (30% buy-support, 12% depth factor)
   - Sell-pressure from vesting, mining, pre-launch migration
   - Emergency brakes at $0.02, gates at $0.05

---

## Final Thoughts

**The truth:** Most projects will launch with **$20-40M liquidity** because that's what presales realistically raise. In that tier, **you need adaptive tokenomics** (v3.0 drip, v5.x streaming, v7.0 shield) to survive.

**The dream:** $75M+ liquidity makes almost any model work. But if you could raise that much, you probably don't need this analysis.

**My recommendation for BlockDAG:**  
Launch at **$50M liquidity** with **Protocol v3.0** or **v7.0**. This gives you:
- Positive Y3 ROI in stress markets (+65-85%)
- Manageable brake rates (40-60%)
- Strong upside in ideal scenarios (+300-500% Y6)

---

**Disclaimer (repeated):** This is simulation-based analysis, not a guarantee. Market conditions, community behavior, and external factors can dramatically alter outcomes. Always do your own research and consult with financial/legal advisors before making launch decisions.

