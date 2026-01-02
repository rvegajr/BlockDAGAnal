# AMA Analysis Template
## For Tracking BlockDAG AMAs Over Time

**Purpose:** Document each BlockDAG AMA to track patterns, claims, and changes over time. When Phoenix launches, release sanitized versions showing the contrast.

---

## Analysis Workflow

### 1. Download & Transcribe
```bash
# Download AMA
yt-dlp -x --audio-format mp3 "[YOUTUBE_URL]"

# Transcribe
nice -n 19 whisper "[FILENAME].mp3" --output_format txt --model tiny --language English --threads 2
```

### 2. Analyze Using Template Below

### 3. Store in `/video/` Directory
```
video/
├── AMA_2025-10-31_Binance/
│   ├── audio.mp3
│   ├── transcript.txt
│   ├── ANALYSIS.md
│   └── CLAIMS_VERIFICATION.md
├── AMA_2025-11-XX_[Platform]/
│   ├── audio.mp3
│   ├── transcript.txt
│   ├── ANALYSIS.md
│   └── CLAIMS_VERIFICATION.md
└── AMA_TRACKING_LOG.md (summary of all AMAs)
```

---

## Template: ANALYSIS.md

```markdown
# BlockDAG AMA Analysis - [DATE]
**Platform:** [Binance/YouTube/Twitter/etc]
**Date:** [YYYY-MM-DD]
**Duration:** [XX minutes]
**Transcript Length:** [XXX lines]

---

## Executive Summary

**Key Takeaways:**
- [3-5 bullet points]

**Major Announcements:**
- [List any announcements]

**Red Flags:**
- [Any concerning patterns]

**Progress Since Last AMA:**
- [What changed? What didn't?]

---

## Content Breakdown

### Time Allocation
| Topic | Approximate % | Line Numbers |
|-------|--------------|--------------|
| Technical discussion | X% | Lines XXX-XXX |
| Financial matters | X% | Lines XXX-XXX |
| Organizational updates | X% | Lines XXX-XXX |
| Community questions | X% | Lines XXX-XXX |
| Marketing/hype | X% | Lines XXX-XXX |

---

## Technical Claims Analysis

### New Technical Claims Made

**Claim 1: [Description]**
- **Quote:** "[Exact quote]" (Lines XXX-XXX)
- **Speaker:** [Who said it - host, CEO, team member]
- **Verification:** [Can this be verified? Does it already exist elsewhere?]
- **Follow-up:** [Did they provide evidence? Code? Demo?]

**Claim 2: [Description]**
- **Quote:** "[Exact quote]" (Lines XXX-XXX)
- **Speaker:** [Who said it]
- **Verification:** [Status]
- **Follow-up:** [Evidence provided?]

### Technical Claims Repeated from Previous AMAs
- [List claims that keep getting repeated without progress]

### Technical Evidence Provided
- [ ] GitHub repository shown
- [ ] Code walkthrough
- [ ] Testnet demonstration
- [ ] Working demo
- [ ] Technical documentation
- [ ] Developer tools
- [ ] None of the above

**Score: X/7 technical evidence items**

---

## Financial & Organizational Updates

### Financial Announcements
- [List any financial news - token sales, pricing, allocations, etc.]

### Organizational Changes
- [Leadership changes, restructuring, new partnerships, etc.]

### Presale/Token Sale Status
- **Current batch:** [Number]
- **Tokens sold:** [Amount claimed]
- **Price:** [Current price]
- **End date:** [When presale closes]
- **Changes since last AMA:** [Any adjustments]

---

## Accountability & Transparency

### Questions Asked by Community
1. **Question:** "[Quote]"
   - **Answer:** [Summary or "Not answered"]
   - **Line numbers:** XXX-XXX

2. **Question:** "[Quote]"
   - **Answer:** [Summary or "Not answered"]
   - **Line numbers:** XXX-XXX

### Questions NOT Answered
- [List important questions that were avoided or deflected]

### Transparency Indicators
- [ ] Clear timeline for deliverables
- [ ] Specific technical milestones
- [ ] GitHub repository access
- [ ] Testnet launch date
- [ ] Code audit status
- [ ] Clear leadership roles
- [ ] Financial transparency

**Score: X/7 transparency indicators**

---

## Comparison to Previous AMAs

### Promises Made in Previous AMAs
| Promise | AMA Date | Status This AMA |
|---------|----------|-----------------|
| [Promise] | [Date] | ✅ Delivered / 🔄 In progress / ❌ Not mentioned |
| [Promise] | [Date] | Status |

### Timeline Tracking
| Milestone | Originally Promised | Current Status | Delays |
|-----------|-------------------|----------------|--------|
| Testnet | [Date] | [Status] | [Days delayed] |
| Mainnet | [Date] | [Status] | [Days delayed] |
| [Feature] | [Date] | [Status] | [Days delayed] |

---

## Red Flags / Concerning Patterns

### Financial Red Flags
- [List any financial concerns]

### Technical Red Flags
- [List any technical concerns]

### Organizational Red Flags
- [List any organizational concerns]

### Communication Red Flags
- [List any communication concerns]

---

## Notable Quotes

### Positive Quotes
> "[Quote that sounds good]" (Lines XXX-XXX)
**Context:** [What does this actually mean?]

### Concerning Quotes
> "[Quote that raises concerns]" (Lines XXX-XXX)
**Context:** [Why is this concerning?]

### Vague/Non-Answer Quotes
> "[Non-answer to direct question]" (Lines XXX-XXX)
**Question was:** [Original question]

---

## Comparison to Kaspa/Other DAG Projects

### Claims That Already Exist Elsewhere
- **Claim:** [What they claimed]
- **Reality:** [Where this already exists - Kaspa, etc.]
- **Innovation:** [Is this actually new? No/Unclear]

---

## What Phoenix Does Differently

### Transparency Comparison
| Aspect | BlockDAG (This AMA) | Phoenix |
|--------|-------------------|---------|
| Code access | [Status] | Open source from day 1 |
| Technical docs | [Status] | Full architecture published |
| Timeline | [Status] | 9-month roadmap with milestones |
| [Add more] | [Status] | [Phoenix approach] |

---

## Overall Assessment

### Technical Progress Score: X/10
**Reasoning:** [Brief explanation]

### Financial Transparency Score: X/10
**Reasoning:** [Brief explanation]

### Organizational Stability Score: X/10
**Reasoning:** [Brief explanation]

### Overall Credibility Score: X/10
**Reasoning:** [Brief explanation]

---

## Predictions for Next AMA

Based on patterns, expect:
- [Prediction 1]
- [Prediction 2]
- [Prediction 3]

---

## Action Items

### For This Analysis
- [ ] Verify claims against external sources
- [ ] Check if GitHub repo appeared
- [ ] Compare to previous AMA claims
- [ ] Update tracking log

### For Phoenix Development
- [ ] Ensure Phoenix addresses issues raised
- [ ] Document transparent alternative
- [ ] Update comparison documents

---

## Files
- **Audio:** [filename]
- **Transcript:** [filename]
- **Video URL:** [URL]
- **Analysis Date:** [YYYY-MM-DD]
```

---

## Template: CLAIMS_VERIFICATION.md

```markdown
# Technical Claims Verification - [DATE] AMA

**Purpose:** Forensically accurate extraction of technical claims with exact quotes and line numbers.

---

## Methodology

1. Read complete transcript line-by-line
2. Extract ALL technical claims
3. Identify who made each claim (host vs team)
4. Provide exact quotes with line numbers
5. Note what evidence was provided

---

## Technical Claims

### Claim 1: [Short Description]

**Speaker:** [Host / CEO / Team Member / Other]

**Exact Quote:**
> "[Complete quote]" (Lines XXX-XXX)

**Evidence Provided:**
- [ ] Code shown
- [ ] Demo performed
- [ ] Documentation referenced
- [ ] GitHub link provided
- [ ] Technical explanation given
- [ ] None - just claimed

**Verification:**
- **Can be independently verified:** Yes / No / Unclear
- **Already exists elsewhere:** Yes (where?) / No / Unknown
- **Status:** Proven / Unproven / Disproven

**Notes:**
[Any additional context]

---

### Claim 2: [Short Description]

[Repeat structure above]

---

## Claims by Speaker

### Claims Made by Binance/Platform Host
1. [Claim] (Lines XXX-XXX)
2. [Claim] (Lines XXX-XXX)

### Claims Made by CEO/Team
1. [Claim] (Lines XXX-XXX)
2. [Claim] (Lines XXX-XXX)

**Important Distinction:** Note who made technical claims vs who substantiated them

---

## Evidence Summary

**Total technical claims made:** X
**Claims with evidence provided:** X
**Claims substantiated with code/demo:** X
**Claims that are just assertions:** X

**Evidence percentage:** X%

---

## Comparison to Previous AMAs

### Repeated Claims (No New Evidence)
- [Claim that was repeated without progress]
- [Another repeated claim]

### New Claims This AMA
- [New claim]
- [Another new claim]

### Claims Dropped (Not Mentioned Anymore)
- [Claim from previous AMA not mentioned this time]

---

## Forensic Verdict

**Summary:**
[Neutral, factual summary of what was claimed vs what was proven]

**Key Findings:**
1. [Finding]
2. [Finding]
3. [Finding]
```

---

## Tracking Log Template

Create `AMA_TRACKING_LOG.md` in video directory:

```markdown
# BlockDAG AMA Tracking Log

**Purpose:** Track all AMAs over time to identify patterns, delays, and changes.

---

## AMA Timeline

| Date | Platform | Duration | Key Topics | Technical Evidence | Red Flags | Analysis Link |
|------|----------|----------|------------|-------------------|-----------|---------------|
| 2025-10-31 | Binance | XX min | Financial crisis, restructuring | 0/7 | 125B oversale, CEO accountability | [Link](./AMA_2025-10-31_Binance/ANALYSIS.md) |
| 2025-11-XX | [Platform] | XX min | [Topics] | X/7 | [Flags] | [Link] |

---

## Promise Tracking

### Testnet Launch
| AMA Date | Promise | Status |
|----------|---------|--------|
| 2025-10-31 | "Coming soon" | Not delivered |
| 2025-11-XX | [New promise] | [Status] |

### Mainnet Launch
| AMA Date | Promise | Status |
|----------|---------|--------|
| 2025-10-31 | February 2025 | Not delivered |
| 2025-11-XX | [Updated] | [Status] |

### GitHub Repository
| AMA Date | Promise | Status |
|----------|---------|--------|
| 2025-10-31 | Not mentioned | Not delivered |
| 2025-11-XX | [Mentioned?] | [Status] |

---

## Technical Claims Over Time

### Claim: "GhostDAG / co-stag Protocol"
- **First mentioned:** 2025-10-31
- **Evidence provided:** None
- **Status:** Unverified
- **Repeated in AMAs:** [List dates]

### Claim: "UTXO + EVM Hybrid"
- **First mentioned:** 2025-10-31
- **Evidence provided:** None
- **Status:** Unverified
- **Repeated in AMAs:** [List dates]

---

## Financial Tracking

### Token Sale Progress
| AMA Date | Batch | Tokens Sold (Claimed) | Price | Status |
|----------|-------|----------------------|-------|--------|
| 2025-10-31 | 45+ | 125B+ (oversold) | [Price] | Active |
| 2025-11-XX | [Batch] | [Amount] | [Price] | [Status] |

### Financial Issues
| Issue | First Mentioned | Status | Resolution |
|-------|----------------|--------|------------|
| 125B oversale | 2025-10-31 | Admitted | 75% haircut proposed |
| [Other issue] | [Date] | [Status] | [Resolution] |

---

## Leadership Changes
| Date | Change | Context |
|------|--------|---------|
| 2025-10-31 | CEO taking full control | During restructuring, admitted no previous financial responsibility |
| [Date] | [Change] | [Context] |

---

## Patterns Observed

### Positive Patterns
- [Any positive developments]

### Concerning Patterns
- Testnet delays: [Track delays]
- Technical claims without evidence: [Count]
- Financial restructuring: [Track changes]
- Leadership instability: [Track changes]

---

## Predictions vs Reality

### Predictions Made After [Previous AMA]
- **Predicted:** [What we predicted]
- **Reality:** [What actually happened]

---

## Overall Trend Analysis

**Technical Progress:** ⬇️ Declining / ➡️ Stagnant / ⬆️ Improving
**Financial Stability:** ⬇️ Declining / ➡️ Stagnant / ⬆️ Improving
**Transparency:** ⬇️ Declining / ➡️ Stagnant / ⬆️ Improving
**Credibility:** ⬇️ Declining / ➡️ Stagnant / ⬆️ Improving
```

---

## Release Strategy (When Phoenix Launches)

### Private Version (Keep)
- Full analysis with all red flags
- Detailed concerns
- Predictions
- Internal notes

### Public Version (Release)
- Sanitized, neutral language
- Focus on factual comparisons
- "What they promised vs what was delivered"
- Side-by-side with Phoenix's delivery

### Release Timing
**Don't release until:**
1. Phoenix testnet is live and working
2. Phoenix demonstrates the features BlockDAG promised
3. The contrast is undeniable

**Then release:**
- "Case Study: Two Approaches to Building a DAG Blockchain"
- "What We Learned From Analyzing 12 Months of BlockDAG AMAs"
- "Building in Public: A Comparison"

---

## Automation Possibilities

**Future enhancement - automate some of this:**

```bash
# Script to download and transcribe
#!/bin/bash
# download_ama.sh

DATE=$1
URL=$2
PLATFORM=$3

mkdir -p "video/AMA_${DATE}_${PLATFORM}"
cd "video/AMA_${DATE}_${PLATFORM}"

yt-dlp -x --audio-format mp3 "$URL" -o "audio.mp3"
nice -n 19 whisper "audio.mp3" --output_format txt --model tiny --language English --threads 2

echo "Transcription complete. Now analyze manually using template."
```

---

## Final Notes

**This is your private research.**

- Track everything
- Stay neutral and factual
- Use exact quotes
- Document patterns
- Build your case over time

**When Phoenix launches with working code, you'll have months of documented evidence showing:**
- What they promised
- What they delivered (or didn't)
- How Phoenix did it differently
- Why open source matters

**You don't need to be right now.**

**You just need to build Phoenix and let the evidence speak for itself.**

---

**Remember:** The goal isn't to attack BlockDAG. The goal is to document reality and demonstrate a better way.
