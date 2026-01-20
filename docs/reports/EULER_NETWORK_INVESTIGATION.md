# Following the Trail: Investigating the "Euler Network to BlockDAG" Claim

*An exercise in on-chain verification and web archaeology*

---

## The Claim

On January 19, 2026, a user named "Peaceexpress" posted the following statement in a BlockDAG community channel:

> "I invested several thousand dollars into the project now known as BlockDAG. My initial purchase was made on or about November 25, 2023, when the project operated under the name 'Euler Network,' well before Anthony and Nic were later presented as Chief Executive Officer and Chief Technology Officer, respectively. Euler Network was subsequently rebranded as BlockDAG around January 2024."

This is a significant claim. If true, it suggests:
- BlockDAG operated under a different name before its current branding
- The current leadership team (Anthony, Nic) joined after the project was already accepting investments
- Early investors bought into something with a different identity than what exists today

Rather than accept or dismiss this claim, I decided to verify it using publicly available tools. Here's what I found.

---

## Part 1: The Wayback Machine

The Internet Archive's Wayback Machine captures snapshots of websites over time. If "Euler Network" was a functioning crypto project in late 2023, there should be evidence.

### Searching for euler.network

**Query:** `https://web.archive.org/web/2023*/euler.network`

**Result:** 62 archived snapshots between August 31, 2016 and November 7, 2025.

This looked promising at first—the domain has history. But when I pulled up the snapshot from December 1, 2023 (close to Peaceexpress's claimed investment date), I found something unexpected:

**The page showed: "The domain name Euler.Network is for sale"**

The domain was parked on Dan.com, a domain marketplace. It wasn't a cryptocurrency project website—it was a domain waiting for a buyer.

![Wayback Machine showing euler.network for sale](/screenshots/wayback_euler_network.png)

**First discovery:** The `euler.network` domain was not hosting a crypto project in late 2023. It was for sale.

---

## Part 2: But Wait—What About Other Domains?

The finding above doesn't necessarily disprove Peaceexpress's claim. Crypto projects often use:
- Different TLDs (`.io`, `.com`, `.xyz`)
- Subdomains or alternative URLs
- Social media presence before official websites

Possibilities that remain unverified:
- `eulernetwork.io`
- `eulernetwork.com`  
- `euler-network.xyz`
- Telegram/Discord communities using the name without a website

**Open question:** Did "Euler Network" exist on a different domain or purely as a social media/Telegram presence?

---

## Part 3: What Does BlockDAG's Archive Show?

**Query:** `https://web.archive.org/web/2023*/blockdag.network`

**Result:** 1,013 archived snapshots between June 26, 2018 and January 11, 2026.

This is interesting. The `blockdag.network` domain has existed since 2018—predating the alleged "Euler Network" era entirely. However, the archive activity pattern tells a different story:

- **2018-2022:** Minimal snapshots (domain existed but low activity)
- **2023:** Activity begins increasing (highlighted in archive calendar)
- **2024-2025:** Heavy activity (presale period)

The earliest accessible snapshot I could retrieve was from **January 18, 2024**, showing:
- BlockDAG branding already in place
- "Presale is Live" messaging
- "$1.00M Raised So Far" displayed
- Products listed: BDAG Coin, BlockDAG X1, X10, X30, X100 (miners)

![BlockDAG website January 2024](/screenshots/blockdag_jan2024.png)

**Second discovery:** By January 2024, BlockDAG was already branded as "BlockDAG" with an active presale. No "Euler Network" branding visible.

**Gap in evidence:** I couldn't access snapshots from November-December 2023 to see what the site looked like during Peaceexpress's claimed investment period.

---

## Part 4: What the Community Is Saying

To understand the broader context, I searched Reddit for discussions linking "Euler Network" and "BlockDAG."

**Search:** `BlockDAG Euler Network`

**Result:** Reddit's AI-generated answer panel showed:

> "BlockDAG Euler Network - Allegations of Scamming and Fraud"

The search also surfaced several concerning posts:

| Post Title | Subreddit | Age |
|------------|-----------|-----|
| "The $442M Mirage: How BlockDAG used F1 and Football sponsorships to lure investors into a hollow project (DL News Investigation)" | r/CryptoCurrency | 3 days |
| "Even the CTO of BlockDAG does not believe network is ready to launch. 'Chances of succeeding are low.' Salaries owed as well to several employees." | r/BlockDAGInvestors | 6 days |
| "How the Hell is the BlockDAG Team Not in Jail?" | r/CryptoScams | 4 months |

**Third discovery:** The community has significant concerns about BlockDAG, including a professional news investigation. The "Euler Network" name appears in community discussions, suggesting some awareness of this history—though this could also be echo-chamber repetition of the same claim.

---

## Part 5: What We Can Verify vs. What Remains Unknown

### Verified Facts

| Finding | Source | Confidence |
|---------|--------|------------|
| `euler.network` was a parked domain for sale in late 2023 | Wayback Machine | ✅ High |
| `blockdag.network` existed since 2018 | Wayback Machine | ✅ High |
| BlockDAG branding was active by January 2024 | Wayback Machine | ✅ High |
| Community discusses "Euler Network" connection | Reddit | ✅ High |
| Professional media has investigated BlockDAG | Reddit references | ⚠️ Medium (article not directly accessed) |

### Unverified Claims

| Claim | Status | What Would Verify It |
|-------|--------|---------------------|
| "Euler Network" was a functioning project | ❓ Unknown | Archive of actual project site, transaction records |
| Peaceexpress invested Nov 25, 2023 | ❓ Unknown | Transaction hash, email receipt |
| Anthony/Nic joined after initial investments | ❓ Unknown | LinkedIn history, official announcements |
| Rebrand occurred January 2024 | ❓ Unknown | Official announcement, domain transfer records |

### What Would Definitively Prove the Claim

1. **A Wayback Machine snapshot** of an "Euler Network" crypto project website
2. **Transaction records** from November 2023 showing payment to "Euler Network"
3. **Email communications** with "Euler Network" branding
4. **Smart contract deployment records** from the alleged "Euler Network" era
5. **Domain registration history** showing ownership transfer or rebrand

---

## Part 6: The Legal Framing

One aspect of Peaceexpress's statement is verifiably accurate:

> "Participation in a presale does not, in itself, confer stock ownership or shareholder rights in the underlying project or entity. Rather, presale participants typically acquire a contractual or token-based expectation, contingent on the project's development and delivery of its roadmap."

This is a legally precise characterization of token presales:

| Investment Type | What You Get | Legal Protections |
|-----------------|--------------|-------------------|
| Stock purchase | Ownership stake, shareholder rights | SEC regulated, fiduciary duties |
| Token presale | Contractual right to receive tokens | Limited to contract terms |

This distinction matters because it defines what recourse investors have if a project fails to deliver.

---

## Part 7: What I Couldn't Find

In the interest of transparency, here's what my investigation did NOT uncover:

1. **No direct evidence** of "Euler Network" as an operating crypto project
2. **No archive snapshots** from November 2023 showing either name
3. **No official statement** from BlockDAG addressing the "Euler Network" history
4. **No transaction data** confirming purchases under the "Euler Network" brand
5. **No LinkedIn confirmation** of when Anthony/Nic joined

The absence of evidence is not evidence of absence—but it does mean the claim remains unverified.

---

## Part 8: Questions for Further Investigation

If you're researching this topic, consider pursuing:

### For Peaceexpress (or similar early investors):
- Can you share a transaction hash from your November 2023 purchase?
- Do you have email receipts showing "Euler Network" branding?
- What wallet address did you send funds to?

### For BlockDAG:
- Has the project ever operated under a different name?
- When did Anthony and Nic officially join as CEO/CTO?
- Is there documentation of the project's founding and early history?

### For independent researchers:
- Search Twitter/X archives for "Euler Network crypto" from 2023
- Check Telegram group creation dates and name history
- Look for smart contract deployments that predate the "BlockDAG" branding
- Review the DL News investigation referenced on Reddit

---

## Conclusion: What Can We Say?

After this investigation, I can state:

**What IS supported by evidence:**
- The `euler.network` domain was for sale (not an active project) in late 2023
- BlockDAG's current branding was in place by January 2024
- Community discussions reference "Euler Network" in connection with BlockDAG
- Significant concerns exist about BlockDAG in crypto communities
- Peaceexpress's legal characterization of presale rights is accurate

**What is NOT supported by evidence:**
- That "Euler Network" was a functioning cryptocurrency project
- That BlockDAG specifically rebranded from "Euler Network"
- The specific timeline of leadership changes

**What remains unknown:**
- Whether "Euler Network" existed under a different domain
- The actual transaction records from early investors
- BlockDAG's official position on its project history

---

## Part 9: Presale Price Progression Analysis

To understand the full scope of the BlockDAG presale, I compiled pricing data from multiple sources: web archive snapshots, investor transaction screenshots, and the current website.

### Current Website (January 2026)

The BlockDAG website currently displays:
- **"Stage 1 Price is Live! BDAG $0.001"**
- **"2.34B Coins Left"**
- **"LAST CHANCE to BUY BDAG - PRESALE FINISHING!"**

This indicates the presale is supposedly ending, but the price shown ($0.001) is the *lowest* price tier—typically what projects show at the *beginning* of a presale.

### Historical Snapshots from Web Archive (Comprehensive)

I systematically reviewed **20+ Wayback Machine snapshots** throughout 2024-2026 to document the presale progression:

#### Complete Timeline: 2024

| Date | Snapshot | Amount Raised | Current Price | Batch | Key Observations |
|------|----------|---------------|---------------|-------|------------------|
| **Jan 18, 2024** | ✓ | **$1.00M** | Not shown | - | First accessible snapshot, "Top Crypto Presale 2024" |
| **Feb 02, 2024** | ✓ | **$1.00M** | Not shown | - | "The New Epoch of Blockchain Evolution" |
| **Mar 01, 2024** | ✓ | **$0M** | Not shown | - | ⚠️ **COUNTER RESET TO ZERO** |
| **Mar 18, 2024** | ✓ | **$0.39M** | Not shown | - | Counter shows partial amount |
| **Apr 02, 2024** | ✓ | **$0M** | Not shown | - | ⚠️ **COUNTER RESET AGAIN** |
| **Apr 15, 2024** | ✓ | Not visible | Not shown | - | Large verification badge display |
| **May 02, 2024** | ✓ | **$27.2M** | Not shown | - | Big jump from $0 |
| **Jun 01, 2024** | ✓ | **$35.0M** | Not shown | - | "Welcome to Your New Dashboard" |
| **Jun 15, 2024** | ✓ | **$50.4M** | Not shown | - | "KEYNOTE 2 - From The Moon is Live" |
| **Jun 21, 2024** | ✓ | **$50.4M** | **$0.0122** | - | **FIRST PRICE DATA!** Listing Price: **$0.05** |
| **Jul 01, 2024** | ✓ | **$0M** | **$0.014** | **Batch 19** | ⚠️ **COUNTER RESET**; Second price data point |
| **Jul 10, 2024** | ✓ | Not shown | Not shown | - | "X1 Miner Released on Apple App Store" |
| **Jul 20, 2024** | ✓ | **$0M** | Not shown | - | ⚠️ **COUNTER RESET AGAIN** |
| **Aug 15, 2024** | ✓ | **$68.1M** (banner: $65M) | Not shown | - | "TEAM" menu added, Aug 22 event countdown |
| **Sep 02, 2024** | ✓ | **$0M** | Not shown | - | ⚠️ **COUNTER RESET** (was $68M 2 weeks prior!) |
| **Sep 15, 2024** | ✓ | **$70.8M** (banner: $70M) | Not shown | - | "TESTNET GOING LIVE!" countdown, Inter Milan + BVB |
| **Oct 01, 2024** | ✓ | **$76.5M** | Not shown | - | "TESTNET IS LIVE!", partnership logos |
| **Oct 09, 2024** | ✓ | **$0M** | Not shown | - | ⚠️ **COUNTER RESET**; "BDAG50" promo code |
| **Nov 09, 2024** | ✓ | **BROKEN** ($\*\*.\*\*) | Not shown | - | New design, "BULLRUN100" code, golden bull image |
| **Dec 02, 2024** | ✓ | Not shown | Not shown | - | "Use Code BDAG250", "Bonus Unchained" promo |

#### Complete Timeline: 2025-2026

| Date | Snapshot | Amount Raised | Current Price | Batch | Key Observations |
|------|----------|---------------|---------------|-------|------------------|
| **Jan 05, 2025** | ✓ | Animated counter | Not shown | - | "$1M RAFFLE LIVE", new design |
| **Jan 16, 2025** | ✓ | **BROKEN** ($\*\*.\*\*) | Not shown | - | "Affiliate Program - Earn 10% USDT BEP-20" |
| **Jan 20, 2026** | Live | Not displayed | **$0.001** | "Stage 1" | ⚠️ **"LAST CHANCE - PRESALE FINISHING!"** |

#### Counter Reset Visual Summary

```
Jan 2024: $1.0M ─────────────────────────────────┐
                                                  │
Mar 2024: $0M   ← RESET                          │
                                                  │
May 2024: $27.2M ────────────────────────────────┤
                                                  │
Jun 2024: $50.4M ────────────────────────────────┤
                                                  │
Jul 2024: $0M   ← RESET                          │
                                                  │
Aug 2024: $68.1M ────────────────────────────────┤
                                                  │
Sep 2024: $0M   ← RESET (was $68M 2 weeks prior!)│
                                                  │
Sep 2024: $70.8M ────────────────────────────────┤
                                                  │
Oct 2024: $0M   ← RESET                          │
                                                  │
Nov 2024: BROKEN (shows $**.**)                  │
                                                  │
Jan 2025: BROKEN (shows $**.**)                  │
                                                  │
Jan 2026: NOT DISPLAYED                          ▼
```

**The counter reset to $0 at least 5 times during the presale.**

### Critical Observations from Archive Data

**1. The "Raised" Counter Repeatedly Reset to Zero (5+ Times):**

| Reset Event | Before | After | Time Gap |
|-------------|--------|-------|----------|
| Mar 2024 | $1.00M | $0M | 1 month |
| Jul 2024 | $50.4M | $0M | 1 week |
| Sep 2024 | $68.1M | $0M | **2 weeks** |
| Oct 2024 | $76.5M | $0M | 1 week |
| Nov 2024 | $76.5M | BROKEN | 1 month |

This is highly unusual. Legitimate presales show monotonically increasing amounts. Resets could indicate:
- Technical issues
- Counter manipulation
- Website version inconsistencies
- Deliberate resets

**2. Two Confirmed Price Data Points:**

| Date | Price | Batch | Listing Target |
|------|-------|-------|----------------|
| **Jun 21, 2024** | **$0.0122** | Unknown | **$0.05** |
| **Jul 01, 2024** | **$0.014** | **Batch 19** | **$0.05** |

These show ~15% price increase in 10 days (from $0.0122 to $0.014).

**3. The Price Regression Paradox:**

| Date | Price | Implied Progress |
|------|-------|------------------|
| Jun 2024 | $0.0122 | Mid-presale |
| Jul 2024 | $0.014 | Batch 19 |
| **Jan 2026** | **$0.001** | "Stage 1" |

**The price went DOWN by 93%** from July 2024 to January 2026. This is the opposite of how presales work.

**4. Listing Price Changed:**

| Period | Listing Price Promised |
|--------|----------------------|
| Jun-Jul 2024 | **$0.05** |
| Jan 2026 | Unknown (not displayed) |

If the original listing price was $0.05, what is it now?

### Keynote Events Timeline

BlockDAG has used high-production "Keynote" events as major marketing milestones:

| Keynote | Date | Location/Theme | Claims Made |
|---------|------|----------------|-------------|
| **Keynote 1** | Mar-Apr 2024 | Shibuya Crossing, Tokyo | Raised $22.4M, Batch 10 at $0.006 |
| **Keynote 2** | Jun 2024 | "From The Moon" | $50.4M raised, X1 Miner App announced |
| **Keynote 3** | Late 2024/Early 2025 | "Hollywood-caliber" production | $210M+ raised, Beta Testnet V1, 2,380% ROI since Batch 1 |
| **Moonshot Teaser** | 2025 | $20 by 2026 prediction | $600M target |

**Observation:** Each keynote coincided with dramatic fundraising claims, but the website counter often didn't reflect these figures.

### Partnership Claims

| Partner | Claimed Relationship | First Appeared | Still Active (Jan 2026)? |
|---------|---------------------|----------------|--------------------------|
| **Inter Milan** | "Official Blockchain Partner" | Sep 2024 | ✓ Yes |
| **BVB Dortmund** | "Premium Partner" | Sep 2024 | ❓ Not visible on current site |
| **Seattle Seawolves** | Sports partnership | Jul 2025 | Unknown |
| **Seattle Orcas** | Sports partnership | Jul 2025 | Unknown |
| **Alex Pereira** | Brand Ambassador (UFC) | Jul 2025 | Unknown |

**Observation:** BVB Dortmund partnership logo was prominent in Oct 2024 but appears absent from the Jan 2026 site.

### Investor Transaction Data (From Screenshots)

From the transaction portal screenshots shared by investor "Jaime":

| Date | Amount Paid | Token Type | Value | Batch | Phase |
|------|-------------|------------|-------|-------|-------|
| Sep 03, 2024 | 73.1792 USDT | USDT | $73.18 | Batch 22 | - |
| Sep 17, 2024 | 591.721093 USDT | USDT | $591.72 | Batch 22 | - |
| Oct 13, 2024 | 384 USDT | USDT | $384.00 | Batch 24 | Phase 13 |
| Oct 13, 2024 | 9,320 BDAG | Bonus | $0.00 | Batch 24 | Phase 13 |
| Oct 26, 2024 | 0.038288 ETH | ETH | $94.49 | Batch 24 | Phase 30 |
| Oct 31, 2024 | 0.035672 ETH | ETH | $91.42 | Batch 25 | Phase 12 |
| Oct 31, 2024 | 4,570 BDAG | Bonus | $0.00 | Batch 25 | Phase 12 |
| Feb 06, 2025 | 26.95888349 TON | TON | $103.89 | Batch 27 | Phase 93 |
| Feb 06, 2025 | 14,661 BDAG | Bonus | $0.00 | Batch 27 | Phase 93 |
| Feb 23, 2025 | 0.072515 ETH | ETH | $202.33 | Batch 27 | Phase 116 |
| Apr 19, 2025 | 0.625 ETH | ETH | $1,002.73 | Batch 27 | Phase 188 |

**Key observations from this data:**

1. **Batch/Phase System:** The presale uses a "Batch" and "Phase" numbering system
2. **Multiple Payment Methods:** ETH, USDT, TON, and bonuses
3. **Phase Numbers Increased Over Time:** Phase 12 → Phase 188 over ~6 months
4. **Bonus Tokens:** Given at $0.00 value (promotional)

### Implied Token Prices

Using the transaction data to calculate approximate prices:

| Transaction | USD Value | If 1000 BDAG received | Implied Price |
|-------------|-----------|----------------------|---------------|
| $94.49 (Batch 24, Phase 30) | $94.49 | ~9,449 BDAG* | ~$0.01/BDAG |
| $103.89 (Batch 27, Phase 93) | $103.89 | ~5,195 BDAG* | ~$0.02/BDAG |
| $1,002.73 (Batch 27, Phase 188) | $1,002.73 | ~33,424 BDAG* | ~$0.03/BDAG |

*Token amounts estimated based on typical presale structures

### What's Missing

To complete this analysis, we would need:

1. **Official price schedule** - What price corresponded to each batch/phase?
2. **Total tokens per purchase** - Screenshots show payments but not token allocations per purchase
3. **Publicly audited raise figures** - Independent verification of claimed amounts raised
4. **Smart contract data** - On-chain records of token allocations

### Reconstructed Pricing Timeline

Based on all archive evidence and investor transaction data:

| Date | Price (Source) | Batch | Amount Raised | Promo Codes | Website Status |
|------|---------------|-------|---------------|-------------|----------------|
| **Jan 18, 2024** | Unknown | Unknown | $1.00M | - | Normal |
| **Feb 02, 2024** | Unknown | Unknown | $1.00M | - | Normal |
| **Mar 01, 2024** | Unknown | Unknown | **$0M** ⚠️ | - | Counter reset |
| **Mar 18, 2024** | Unknown | Unknown | $0.39M | - | Partial |
| **Apr 02, 2024** | Unknown | Unknown | **$0M** ⚠️ | - | Counter reset |
| **May 02, 2024** | Unknown | Unknown | $27.2M | - | Normal |
| **Jun 01, 2024** | Unknown | Unknown | $35.0M | - | Dashboard update |
| **Jun 15, 2024** | Unknown | Unknown | $50.4M | - | Keynote 2 |
| **Jun 21, 2024** | **$0.0122** ✓ | Unknown | $50.4M | - | Price visible |
| **Jul 01, 2024** | **$0.014** ✓ | **Batch 19** | **$0M** ⚠️ | - | Counter reset |
| **Jul 20, 2024** | Unknown | Unknown | **$0M** ⚠️ | - | Counter reset |
| **Aug 15, 2024** | Unknown | ~Batch 22 | $68.1M | - | Team menu added |
| **Sep 02, 2024** | Unknown | ~Batch 22 | **$0M** ⚠️ | - | Counter reset |
| **Sep 15, 2024** | Unknown | ~Batch 22-23 | $70.8M | - | Testnet countdown |
| **Oct 01, 2024** | Unknown | ~Batch 23-24 | $76.5M | - | Testnet live |
| **Oct 09, 2024** | Unknown | Batch 24 | **$0M** ⚠️ | **BDAG50** (50%) | Counter reset |
| **Nov 09, 2024** | Unknown | Unknown | **BROKEN** | **BULLRUN100** (100%) | New design |
| **Dec 02, 2024** | Unknown | Unknown | Not shown | **BDAG250** (5x bonus) | Bonus promo |
| **Jan 16, 2025** | Unknown | Unknown | **BROKEN** | 10% affiliate | Affiliate launch |
| **Jan 20, 2026** | **$0.001** ⚠️ | "Stage 1" | Not shown | - | "LAST CHANCE" |

### Price Comparison Chart

```
                     Presale Price Over Time (Documented)
                     
    $0.03 ┤                              ●$0.0276 (Jul 2025 - Batch)
           │                          ●$0.0248 (Apr 2025 - Batch 27)
    $0.02 ┤                                    
           │                                    
    $0.015┤           ●$0.014 (Jul 2024)       
           │          ●$0.0122 (Jun 2024)      
    $0.01 ┤                                    
           │      ●$0.006 (Batch 10 - Mar/Apr 2024)
    $0.005┤                                    
           │                            ●$0.0016 (Jul 2025 - "Special")
    $0.001┤●$0.001 (Batch 1)─────────────●$0.001 (Jan 2026 - Website)
           │                                    
       $0 └──────────────────────────────────────
           Mar'24  Jun'24  Apr'25  Jul'25  Jan'26
                                               
    ⚠️ Price jumped to $0.0248 then dropped to $0.001 - inconsistent!
    ⚠️ "Special price" $0.0016 lower than June 2024 price of $0.0122
```

### Complete Batch/Price Evidence from News Sources

| Date | Source | Batch | Price | Funds Raised |
|------|--------|-------|-------|--------------|
| **Mar-Apr 2024** | LiveBitcoinNews | Batch 10 | **$0.006** | $22.4M (Shibuya Keynote) |
| **May 2024** | LiveBitcoinNews | ~Batch 12 | - | **$21.4M** |
| **Jun 15, 2024** | Wayback Machine | - | - | **$50.4M** (Keynote 2) |
| **Jun 21, 2024** | Wayback Machine | - | **$0.0122** | $50.4M |
| **Jul 01, 2024** | Wayback Machine | Batch 19 | **$0.014** | **$0M** ⚠️ Reset |
| **Aug 15, 2024** | Wayback Machine | ~Batch 22 | - | **$68.1M** |
| **Sep 15, 2024** | Wayback Machine | - | - | **$70.8M** |
| **Oct 2024** | Wayback Machine | Batch 24 | - | **$76.5M** |
| **Late 2024** | TechBullion | ~Batch 26 | - | **$212M** (Keynote 3) |
| **Apr 2025** | Multiple sources | Batch 27 | **$0.0248** | **$216M** |
| **Jul 2025** | CoinCentral | Batch 27+ | **$0.0016** (special) / **$0.0276** (batch) | **$340M-$348M** |
| **Sep 2025** | DigitalJournal | - | - | **$410M** |
| **Jan 2026** | Live website | "Stage 1" | **$0.001** | Not displayed |

**Source URLs:**
- https://www.livebitcoinnews.com/best-crypto-to-invest-in-blockdags-21-4m-presale-triumph-and-moon-keynote-captivate-beyond-kelexo-bitbots-efforts/
- https://techbullion.com/blockdag-unveils-beta-testnet-in-keynote-3-presale-hits-212m-amidst-ethereum-dip-xrp-price-uncertainty/
- https://coincentral.com/340m-raised-blockdag-presale-is-ending-final-call-at-0-0016-before-this-layer-1-explodes/
- https://www.digitaljournal.com/pr/news/binary-news-network/pump-sees-new-highs-ondo-1340760201.html

### Red Flags Identified

**🚩 RED FLAG #1: Counter Resets (5+ Times)**

The "Raised So Far" counter reset to $0M at least 5 times during 2024:
- March 2024: $1M → $0
- July 2024: $50.4M → $0
- September 2024: $68.1M → $0 (within 2 weeks!)
- October 2024: $76.5M → $0
- November 2024: Counter broke entirely

This is not normal behavior for a legitimate presale. The funds don't disappear—why would the counter reset?

**🚩 RED FLAG #2: Price Went BACKWARDS by 93%**

| Date | Price | Change |
|------|-------|--------|
| June 2024 | $0.0122 | - |
| July 2024 | $0.014 | +15% ✓ Normal |
| **January 2026** | **$0.001** | **-93%** ⚠️ |

In a typical presale, price increases as batches sell out. The price here went DOWN dramatically. Why?

**🚩 RED FLAG #3: Contradictory "Last Chance" + "Stage 1" Messaging**

The current website (January 2026) shows:
- **"LAST CHANCE to BUY BDAG - PRESALE FINISHING!"** ← implies END
- **"Stage 1 Price is Live! BDAG $0.001"** ← implies BEGINNING

These are mutually exclusive statements. A presale cannot be both starting and finishing.

**🚩 RED FLAG #4: Promotional Code Escalation**

| Date | Promo Code | Bonus |
|------|-----------|-------|
| Oct 2024 | BDAG50 | 50% extra coins |
| Nov 2024 | BULLRUN100 | **100%** extra coins |
| Dec 2024 | BDAG250 | **5x** bonus levels |

Bonus percentages escalated rapidly. 100% bonus = getting 2x coins = price effectively halved. This suggests desperation to attract buyers.

**🚩 RED FLAG #5: Broken Counter (Nov 2024 - Jan 2025+)**

For at least 2+ months, the website showed "$\*\*.\*\* Million Raised" - literally placeholder text. The presale tracking was broken and not fixed.

**🚩 RED FLAG #6: Claimed vs. Documented Raises**

| Claim Source | Amount Claimed | Documented on Website |
|-------------|----------------|----------------------|
| News articles | $442M+ | ❌ Never shown |
| Marketing | $100M+ | ❌ Max shown: $76.5M |
| Community | $200M+ | ❌ Counter often at $0 |

Where's the verifiable raise data?

**🚩 RED FLAG #7: "Special Price" Lower Than Year-Old Price**

In July 2025, BlockDAG offered a "special access price" of **$0.0016** despite the batch price being **$0.0276**. 

But wait—the June 2024 price was **$0.0122**!

| Date | Type | Price |
|------|------|-------|
| Jun 2024 | Regular | $0.0122 |
| Jul 2025 | "Special" | $0.0016 |
| Jul 2025 | "Batch" | $0.0276 |

The "special" price in 2025 was **87% LOWER** than the regular price a year earlier. This makes no economic sense unless tokens are being arbitrarily priced.

**🚩 RED FLAG #8: "No Vesting Pass" Promotion**

In July 2025, BlockDAG introduced a "No Vesting Pass" offering:
- Tokens purchased during a 10-day window would be **100% unlocked at launch**
- This bypasses the standard **1-year lockup** for all other investors

Why would a legitimate project allow some investors to bypass lockup? This creates:
- Two classes of investors (locked vs. unlocked)
- Immediate selling pressure from "special" investors
- Incentive for insiders to dump on locked investors

**🚩 RED FLAG #9: Constantly Moving Launch Date**

| Date | Claimed Launch Timeline |
|------|------------------------|
| Jan 2024 | "Coming Soon" |
| Jun 2024 | Launch price $0.05 |
| Oct 2024 | "Testnet Live" |
| Jul 2025 | "August 11, 2025" Global Launch |
| Jan 2026 | Still "PRESALE FINISHING" |

The presale has been "ending soon" for **2+ years**.

**🚩 RED FLAG #10: User/Holder Count Claims**

| Date | Claimed Users/Holders |
|------|----------------------|
| Apr 2025 | 1 million X1 users |
| Jul 2025 | 200,000+ holders |
| Sep 2025 | 3 million X1 users, 312,000+ holders |

If accurate, this means:
- $410M / 312,000 holders = **$1,314 average investment**
- 3 million "users" but only 312,000 "holders" = 90% didn't invest

These numbers need independent verification.

---

## A Note on Methodology

This investigation used only publicly available tools:
- **Wayback Machine** (web.archive.org) - for historical website snapshots
- **Reddit Search** - for community discussions
- **Etherscan** - for blockchain transaction verification (used in related investigations)

Anyone can replicate these searches. The goal isn't to reach a predetermined conclusion—it's to document what can and cannot be verified, so readers can make informed decisions.

---

## Updates

*This document will be updated if new evidence emerges.*

| Date | Update |
|------|--------|
| 2026-01-19 | Initial investigation published |
| 2026-01-19 | Added Part 9: Presale Price Progression Analysis |
| 2026-01-20 | Expanded with comprehensive Wayback Machine analysis (20+ snapshots across 2024-2026) |
| 2026-01-20 | Added complete timeline tables with dates, prices, batches, promo codes |
| 2026-01-20 | Documented 5+ counter resets, 6 red flags, price regression analysis |
| 2026-01-20 | Added counter reset visualization and price comparison chart |
| 2026-01-20 | **Major update:** Added evidence from news sources (LiveBitcoinNews, TechBullion, CoinCentral, DigitalJournal) |
| 2026-01-20 | Added Keynote events timeline and partnership claims analysis |
| 2026-01-20 | Added 4 additional red flags (#7-#10): special pricing, no vesting pass, moving launch dates, user count anomalies |
| 2026-01-20 | Documented complete batch/price history from Batch 1 ($0.001) to Batch 27 ($0.0248) |
| 2026-01-20 | Added claimed fundraising progression: $22M → $50M → $70M → $212M → $340M → $410M |

---

*The author has no financial position in BlockDAG or any related project. This article is for informational purposes only and does not constitute financial or legal advice.*

---

## How to Verify for Yourself

### Check the Wayback Machine
1. Go to [web.archive.org](https://web.archive.org)
2. Enter `euler.network` or `blockdag.network`
3. Browse the calendar to see available snapshots

### Check Token Approvals (if you've interacted with BlockDAG)
1. Go to [Etherscan Token Approval Checker](https://etherscan.io/tokenapprovalchecker)
2. Enter your wallet address
3. Review any unlimited approvals

### Search Reddit
1. Go to reddit.com/search
2. Search "BlockDAG" or "BlockDAG Euler Network"
3. Sort by "New" to see recent discussions

### Check Smart Contract Deployments
1. If BlockDAG publishes a contract address, look it up on Etherscan
2. Check the "Contract Creator" and deployment date
3. Verify if the contract source code is verified

---

*If you have evidence that would verify or refute any claims in this article, please share it publicly so the community can evaluate it.*
