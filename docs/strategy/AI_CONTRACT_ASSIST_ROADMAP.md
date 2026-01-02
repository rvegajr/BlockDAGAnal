# AI Contract Assistant Roadmap (Deferred)

Status: Planning (No implementation in current phase)
Owners: DevTools + EVM Integration + Security

---

## Objective
Provide optional AI-powered assistance to help developers design, lint, test, and explain smart contracts on Phoenix—without compromising determinism, security, or transparency.

AI features are explicitly deferred until core network, EVM parity, and contract templates are production-stable.

---

## Guiding Principles
- Optional and explainable: outputs include rationale, code refs, and change diffs.
- Policy-first safety: enforcement rules precede automation; AI never bypasses policy.
- Privacy by default: local-first analysis; any telemetry is opt-in and redacted.
- Determinism respected: AI aids off-chain workflows; on-chain consensus remains unaffected.

---

## Dependencies (Gates)
- G1: Phoenix node testnet stable (canonicalization + reorg bounds verified)
- G2: EVM conformance (London→Shanghai tests pass)
- G3: Secure contract templates and policy rules finalized
- G4: CI pipelines for static/fuzz/regression testing in place

No AI deliverables start until G1–G3 are met.

---

## Phased Roadmap

### Phase 0 – Requirements & Policies (Post-G3)
- Deliverables:
  - POLICY_GATE.md (severity taxonomy, block/allow/override flow)
  - STATIC_RULESET.md (Slither/Mythril rules + thresholds)
  - CONTRACTS_TEMPLATES_SPEC.md (ERCs, vesting, timelock, governor)
  - DEVELOPER_TEST_GUIDE.md (Hardhat/Foundry + reorg harness runbooks)
- Success: Policy and templates approved; baseline tests green.

### Phase 1 – Advisory Lint & Test Suggestions
- Features:
  - AI-assisted lint hints (non-blocking): privilege surface, reentrancy probes
  - Test scaffolds: unit + property/fuzz skeletons for ERCs and core patterns
- Success: ≥50% of suggested tests adopted by devs; false-positive rate <10%.

### Phase 2 – Risk Scoring (Explainable)
- Features:
  - Risk report JSON (privileges, external-call topology, infinite-mint/fee-skim flags)
  - Human-readable rationale + remediation steps
- Success: Catches ≥90% of seeded issues in benchmark corpus; reviewers trust explanations.

### Phase 3 – Policy‑Aware Gate (Assist Mode)
- Features:
  - Run policy rules; block only if rules demand; otherwise warn
  - Multisig override with signed justification and evidence bundle
- Success: Zero unintended blocks; complete audit trail for overrides.

### Phase 4 – Test Generation (Property/Fuzz + Reorg Harness)
- Features:
  - Invariant/fuzz drafts for tokens, access control, upgrade paths
  - Reorg scenario scripts aligned with canonicalization spec
- Success: New issues revealed by generated tests on sample projects.

### Phase 5 – Template Wizard (Secure by Default)
- Features:
  - Parameterized ERC-20/721/1155, vesting, timelock, governor with guards
  - Emphasize caps, vesting, withdraw throttles, pausability
- Success: Deployed templates pass policy gate + external review.

### Phase 6 – IDE/Explorer Integrations (Optional)
- VS Code/Remix plugins: explain diffs, run checks, apply changes via PRs
- Explorer “Explain Events” panel using contract ABI and risk report

### Phase 7 – Continuous Learning (Optional)
- Curate postmortems from incidents; update rules/templates (human-reviewed)

---

## Out of Scope (Current Release)
- Autonomous code changes without review
- On-chain or consensus-facing AI components
- Any feature that weakens policy or auditability

---

## Success Metrics (When Activated)
- Time-to-first-deploy reduction without increased incident rate
- % critical issues caught pre-merge by policy/risk checks
- Developer satisfaction (surveys), override rate with justification quality

---

## Activation Criteria
This roadmap activates only after:
- Testnet stability proven under reorg tests
- EVM conformance suites green
- Contract templates and policy rules finalized

Until then, no AI work proceeds beyond documentation and design.





