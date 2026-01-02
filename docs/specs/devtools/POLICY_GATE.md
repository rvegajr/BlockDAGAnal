# Phoenix Deployment Policy Gate (Normative)

Status: Draft (Implementation-Ready)
Owners: DevTools + Security

---

## Purpose
Define enforceable pre-deployment checks for smart contracts. Prevent high-risk patterns (esp. presales/treasuries) from reaching mainnet/testnet unless explicitly overridden by governance.

---

## Severity Taxonomy
- Critical: Must block. Only multisig override with signed justification + evidence bundle.
- High: Block by default. Maintainer may override with reason + reviewer approval.
- Medium: Warn and require acknowledgement.
- Low: Informational.

---

## Rule Groups (Initial)
1) Presale Safety
- Hard cap required (Critical)
- Soft cap + refund path (High)
- Per-wallet min/max (High)
- Withdraw throttling / timelocked (High)
- Pausable + emergency stop (High)
- Vesting for founders/team (High)

2) Privileges & Governance
- Owner-only mint/burn must be role-gated (High)
- Upgrades behind TimelockController (High)
- Break-glass (pause) limited and auditable (Medium)

3) Funds Safety
- No unrestricted withdraw to arbitrary address (Critical)
- Treasury withdrawals via multisig/timelock (High)
- No direct ETH sink without event (Medium)

4) Dangerous Primitives
- Forbid tx.origin auth (Critical)
- Dangerous delegatecall flagged (High)
- Unrestricted external calls flagged (High)

5) Reentrancy & Accounting
- External-call-before-state-change flagged (High)
- Missing reentrancy guards on payable/external (High)
- Balance/allowance invariants broken (Critical)

---

## Evidence Bundle (for overrides)
- Rule violations with code spans
- Rationale + remediation plan
- Test artifacts proving mitigations
- Signatures: approver multisig, author, reviewer

---

## CI Contract
- Input: bytecode + ABI + source map
- Output: JSON report {summary, rules:[{id, severity, passed, notes, spans[]}], evidence}
- Exit codes: 0 (pass), 2 (warn), 3 (blocked)

---

## Configuration
```yaml
policy:
  mode: strict            # strict|warn
  allowOverride: true
  requireMultisigFor:     # set of severities requiring multisig
    - critical
  timelockHoursMin: 24
  requiredCaps:
    hardCap: true
    softCap: true
  withdraw:
    timelockHoursMin: 24
    dailyLimitPctMax: 1.0
```

---

## Acceptance Criteria
- Rules must map to deterministic static/fuzz checks
- Overrides require evidence bundle archived in repo
- CI exit codes respected in pipelines (block merges to protected branches when blocked)

---

## References
- security/STATIC_RULESET.md
- testing/CONTRACT_TEST_SUITE.md




