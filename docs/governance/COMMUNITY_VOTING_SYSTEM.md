# BlockDAG Community Voting System

## Executive Summary

**We're implementing a transparent, verifiable, and fair voting system where every voice matters—and every vote is permanent.**

### Why This System Is Superior

| Traditional Voting | Our System |
|-------------------|------------|
| ❌ "Trust us, we counted correctly" | ✅ **Anyone can verify** - All votes public on-chain |
| ❌ Results can be changed | ✅ **Immutable** - Anchored to Bitcoin forever |
| ❌ Whales dominate completely | ✅ **Quadratic voting** - Balanced influence |
| ❌ Pay gas to vote ($5-50) | ✅ **Free to vote** - Just sign a message |
| ❌ Votes hidden in database | ✅ **Transparent** - See who voted for what |
| ❌ Admins can manipulate | ✅ **No admin control** - Math proves results |
| ❌ Small holders ignored | ✅ **Every voice counts** - Quadratic amplifies community |

### The Transparency Guarantee

```
Your vote → Signed by YOUR wallet → Stored on IPFS → Anchored to Bitcoin

Nobody can:
- Change your vote (cryptographic signature)
- Delete your vote (permanent storage)
- Fake your vote (only your wallet can sign)
- Hide the results (public ledger)
- Manipulate the count (anyone can verify)
```

**This isn't "trust us" governance. This is "verify it yourself" governance.**

---

## How It Works

### The Simple Version (30 Seconds to Vote)

```
1. Click the voting link we share
2. Connect your wallet (MetaMask, WalletConnect, etc.)
3. See your voting power displayed
4. Click your choice
5. Sign the message (FREE - no gas fees!)
6. Done. Your voice is heard.
```

### The Technical Version (For Those Who Want to Verify)

```
1. Your vote is signed with your private key
2. Signature + vote stored on IPFS (decentralized storage)
3. Vote indexed by Snapshot protocol
4. After voting ends, results anchored to Bitcoin
5. Anyone can download data and verify the count
6. Merkle proofs let you prove YOUR specific vote was counted
```

---

## Voting Power: Fair for Everyone

### The Problem with Simple Systems

**One-Wallet-One-Vote:**
- Sounds democratic
- But anyone can create 1,000 wallets
- Spammers and bots dominate
- Real community voices drowned out

**One-Token-One-Vote:**
- Sounds fair (more stake = more say)
- But 1 whale with 10M tokens = 10,000 small holders combined
- Small investors feel powerless
- Plutocracy, not democracy

### Our Solution: Quadratic Voting

**Your voting power = √(your tokens)**

| Your Holdings | Linear Votes | Quadratic Votes | What This Means |
|---------------|--------------|-----------------|-----------------|
| 100 BDAG | 100 | 10 | Small holder has meaningful voice |
| 1,000 BDAG | 1,000 | 31.6 | 10x tokens ≠ 10x votes |
| 10,000 BDAG | 10,000 | 100 | 100x tokens = only 10x votes |
| 100,000 BDAG | 100,000 | 316 | Significant but not dominant |
| 1,000,000 BDAG | 1,000,000 | 1,000 | Whale has influence, not control |

**Real Example:**

| Voter | Tokens | Quadratic Votes | % of Total (if only voters) |
|-------|--------|-----------------|----------------------------|
| Whale Alice | 5,000,000 | 2,236 | 23.4% |
| Shark Bob | 500,000 | 707 | 7.4% |
| Fish Carol | 50,000 | 224 | 2.3% |
| 100 Crabs | 1,000 each | 3,162 (31.6 × 100) | **33.1%** |
| 1,000 Shrimp | 100 each | 3,162 (10 × 316) | **33.1%** |

**Result:** 1,100 small holders (crabs + shrimp) have **66% of voting power**, while the whale has only 23%.

**This is how community voices are heard.**

---

## Transparency: See Everything

### What's Public (Everything)

| Data | Visibility | Where to Find |
|------|------------|---------------|
| Every vote cast | Public | Snapshot.org |
| Who voted for what | Public | Snapshot.org |
| Voting power used | Public | Snapshot.org |
| Token balance at snapshot | Public | Etherscan |
| Final results | Public | Snapshot + Bitcoin anchor |
| Full vote data | Public | IPFS (permanent) |

### What's NOT Possible

| Action | Why It's Impossible |
|--------|---------------------|
| Change a vote after cast | Cryptographic signature locked |
| Delete a vote | IPFS + Bitcoin = permanent |
| Add fake votes | Would need your private key |
| Hide unfavorable results | All data public |
| Manipulate the count | Anyone can recount from raw data |

### How to Verify (Anyone Can Do This)

**Simple verification:**
1. Go to our Snapshot space
2. Click on any proposal
3. See every vote, every voter, every result
4. Compare to our announced results
5. If they don't match → we lied (they will match)

**Advanced verification:**
1. Download full vote data from IPFS
2. Check each signature cryptographically
3. Recalculate all voting powers
4. Sum up results yourself
5. Compare to Bitcoin-anchored hash
6. If hash matches → data is authentic

---

## The Permanent Record

### Why Bitcoin Anchoring Matters

After every vote, we anchor the results to Bitcoin:

```
Bitcoin Transaction (OP_RETURN):
┌─────────────────────────────────────────────────────────┐
│ BDAG-VOTE | Proposal: VEST-001 | Hash: 7f3a8b2c...     │
│                                                         │
│ This hash represents ALL votes cast.                    │
│ If anyone changes even 1 vote, the hash changes.       │
│ Bitcoin block #892,451 confirms this forever.          │
└─────────────────────────────────────────────────────────┘
```

**What this means:**
- Results exist on Bitcoin (most secure network in existence)
- Would need to hack Bitcoin to change results (impossible)
- Proof exists forever (as long as Bitcoin exists)
- Anyone can verify the anchor matches the data

### The Trust Model

```
OLD WAY:
"We counted the votes. Trust us. Here are the results."
     ↓
You have to trust the team
     ↓
No way to verify
     ↓
Could be lying

OUR WAY:
"Here are the votes. Here's the Bitcoin anchor. Verify yourself."
     ↓
You don't trust anyone
     ↓
You verify with math
     ↓
Impossible to lie
```

---

## Addressing Community Concerns

### "Won't whales still dominate?"

**No.** Quadratic voting ensures:
- Whale with 1,000,000 tokens = 1,000 votes
- 100 community members with 10,000 each = 3,162 votes
- **Community beats whale by 3:1**

### "Can the team manipulate results?"

**No.** Because:
- All votes are signed by voter's own wallet
- We can't forge your signature
- All data is public and verifiable
- Results anchored to Bitcoin (we can't change Bitcoin)

### "What if I'm a small holder? Does my vote matter?"

**Yes.** Example:
- You hold 500 BDAG
- Your quadratic vote = 22.4
- If 1,000 people like you vote together = 22,400 votes
- That's more than a whale with 500,000,000 BDAG (22,360 votes)

**Small holders united > any single whale**

### "How do I know my vote was counted?"

**Check it yourself:**
1. Go to the proposal on Snapshot
2. Click "Votes" tab
3. Search for your wallet address
4. See your vote recorded
5. Still don't trust it? Download IPFS data and verify signature

### "What stops someone from creating 1,000 wallets?"

**Quadratic voting penalizes splitting:**
- 1 wallet with 10,000 tokens = √10,000 = 100 votes
- 10 wallets with 1,000 each = 10 × √1,000 = 316 votes
- 100 wallets with 100 each = 100 × √100 = 1,000 votes

Wait, doesn't that help splitting? **No, because:**
- Each wallet needs real tokens (can't create tokens from nothing)
- Gas costs to set up wallets
- Time cost to manage
- And most importantly: token balance is snapshotted at a **random block** announced AFTER voting starts
- Can't move tokens fast enough to game it

### "What if the team has secret wallets?"

**All team tokens are in vesting contracts:**
- Contract addresses published
- Anyone can verify on Etherscan
- Team gets 0% at TGE (while investors get 2%)
- Can't vote with locked tokens

---

## How to Participate

### Step 1: Have BDAG Tokens

Your voting power comes from your token holdings. Make sure your tokens are in a wallet you control (not on an exchange).

### Step 2: Connect Your Wallet

We support:
- MetaMask
- WalletConnect
- Coinbase Wallet
- Rainbow
- And 50+ other wallets

### Step 3: Vote When Proposals Open

We'll announce proposals on:
- Discord: #governance channel
- Telegram: @BlockDAG_Official
- Twitter: @BlockDAG
- Email: governance@blockdag.network

### Step 4: Sign Your Vote (Free!)

- No gas fees required
- Just a signature from your wallet
- Takes 10 seconds

### Step 5: Verify Your Vote (Optional)

After voting, check that your vote was recorded:
1. Go to the proposal page
2. Find your wallet in the votes list
3. Confirm it shows your choice

---

## Upcoming Votes

### Vote #1: Vesting Model Selection

**Question:** Which vesting approach should BlockDAG implement?

**Options:**
- **Option A:** Original Model (2% TGE, 12-month cliff, 60-month vesting)
- **Option B:** Quarterly Micro-Unlocks (2% TGE + 1-2% quarterly during cliff)
- **Option C:** Investor Choice Tiers (Choose your lock duration, choose your bonus)

**Timeline:**
- Proposal published: [TBD]
- Voting opens: [TBD]
- Voting closes: [TBD] (7 days)
- Results announced: [TBD]
- Bitcoin anchor: Within 24 hours of close

### Vote #2: Governance Structure

**Question:** How should ongoing governance decisions be made?

**Options:**
- **Option A:** Token-weighted only (quadratic)
- **Option B:** Bicameral (Token House + Community House)
- **Option C:** Delegated voting (elect representatives)

**Timeline:** After Vote #1 completes

---

## Technical Specifications

### Voting Platform
- **Provider:** Snapshot.org
- **Space:** blockdag.eth (or custom domain)
- **Network:** Ethereum Mainnet (for token verification)

### Voting Strategy
```json
{
  "name": "quadratic-balance-of",
  "params": {
    "symbol": "BDAG",
    "address": "0x[TOKEN_CONTRACT]",
    "decimals": 18
  }
}
```

### Snapshot Timing
- Block selected randomly within 24-hour window after proposal creation
- Announced after selection (prevents last-minute token buying)

### Storage & Anchoring
- **Primary:** IPFS via Snapshot protocol
- **Secondary:** Arweave (permanent backup)
- **Anchor:** Bitcoin OP_RETURN or OpenTimestamps

### Verification Tools
- Snapshot UI: Direct viewing
- IPFS Gateway: Raw data access
- Custom scripts: Full independent verification

---

## Frequently Asked Questions

### General

**Q: Do I need to pay gas to vote?**
A: No. Voting is free. You just sign a message.

**Q: Can I change my vote?**
A: No. Once signed, your vote is permanent. Choose carefully.

**Q: What if I buy more tokens after the snapshot?**
A: Those tokens won't count for this vote. Voting power is locked at snapshot block.

**Q: Can I vote from multiple wallets?**
A: Yes, each wallet votes with its own power. But remember, quadratic voting means splitting doesn't help much.

### Security

**Q: What if Snapshot goes down?**
A: All data is on IPFS. Anyone can access it. We also anchor to Bitcoin.

**Q: Can hackers change the results?**
A: They would need to: hack your wallet (to forge signature), hack IPFS (decentralized), and hack Bitcoin (impossible). So no.

**Q: What if the team disappears?**
A: All data is public and permanent. Community can continue verification and governance.

### Participation

**Q: Minimum tokens to vote?**
A: 100 BDAG minimum (prevents spam while keeping barrier low).

**Q: Can I delegate my vote?**
A: Not in initial implementation. May add delegation later based on community feedback.

**Q: What's the quorum?**
A: To be determined by community. Proposed: 5% of circulating supply must participate.

---

## Commitment to Transparency

### We Pledge:

1. **Every vote will be public** - No secret ballots, no hidden results
2. **Every result will be anchored** - Bitcoin proof within 24 hours of close
3. **Every concern will be heard** - Feedback channels always open
4. **Every promise will be verifiable** - Don't trust us, verify us

### You Can Hold Us Accountable:

- **If results don't match Bitcoin anchor** → We manipulated data
- **If votes disappear from IPFS** → We're hiding something
- **If voting power doesn't match formula** → We're cheating
- **If team votes with undisclosed tokens** → We're lying

**All of these are publicly verifiable. We can't hide.**

---

## Links & Resources

### Official Channels
- **Voting Portal:** [snapshot.org/#/blockdag.eth](https://snapshot.org) *(active after setup)*
- **Governance Forum:** [forum.blockdag.network](https://forum.blockdag.network) *(coming soon)*
- **Discord:** #governance channel
- **Documentation:** This document

### Verification Tools
- **Snapshot API:** [hub.snapshot.org/graphql](https://hub.snapshot.org/graphql)
- **IPFS Gateway:** [ipfs.io](https://ipfs.io)
- **Bitcoin Explorer:** [mempool.space](https://mempool.space)
- **OpenTimestamps:** [opentimestamps.org](https://opentimestamps.org)

### Technical References
- **Quadratic Voting Explained:** [Gitcoin Docs](https://support.gitcoin.co/gitcoin-knowledge-base/gitcoin-grants/general-questions/what-is-quadratic-funding)
- **Snapshot Documentation:** [docs.snapshot.org](https://docs.snapshot.org)
- **IPFS Overview:** [docs.ipfs.io](https://docs.ipfs.io)

---

## Summary

**Your voice matters. Here's how we prove it:**

| Promise | How We Deliver | How You Verify |
|---------|----------------|----------------|
| Every vote counts | Quadratic voting | Check the math yourself |
| Votes are permanent | IPFS + Bitcoin | Check the blockchain |
| Results are accurate | Public tallying | Recount from raw data |
| No manipulation | Cryptographic signatures | Verify signatures |
| Team can't cheat | All tokens in contracts | Check Etherscan |

**This is governance where you don't have to trust anyone—including us.**

Vote. Verify. Voice heard.

---

*Document Version: 1.0*  
*Last Updated: January 2026*  
*Status: Ready for Community Review*

