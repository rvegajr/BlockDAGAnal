# Static Analysis Ruleset (Slither/Mythril) - Normative

Status: Draft (Implementation-Ready)
Owners: Security

---

## Purpose
Define deterministic static rules and thresholds that back the Policy Gate.

---

## Tooling
- Slither (structural/static)
- Mythril (symbolic execution)
- solc 0.8.x with optimizer enabled (200+ runs)

---

## Rule Table (Initial)

| ID | Description | Tool | Severity | Notes |
|----|-------------|------|----------|-------|
| SR-001 | Use of tx.origin for auth | Slither | Critical | Disallow always |
| SR-002 | Unrestricted delegatecall | Slither | High | Allow only via vetted patterns |
| SR-003 | Reentrancy (external call before state) | Slither | High | ReentrancyGuard or checks-effects-interactions |
| SR-004 | Arbitrary external call sinks (withdraw to any) | Slither | Critical | Treasury/withdraw whitelists required |
| SR-005 | Unbounded loops on user input | Slither | Medium | Gas griefing risk |
| SR-006 | Missing access control on sensitive functions | Slither | High | Require Ownable/AccessControl |
| SR-007 | Integer downcast/unchecked math hotpaths | Slither | Medium | 0.8 reverts on overflow; flag gas-unsafe blocks |
| SR-008 | Eventless critical state changes | Slither | Medium | Emit events for transparency |
| SR-009 | Inconsistent approvals (ERC-20) | Slither | High | Mitigate allowance race patterns |
| SR-010 | Code-size / init-code-size limits exceeded | Slither | Medium | Deployment reliability |
| MY-001 | Symbolic reentrancy path | Mythril | High | Must have guard or prove benign |
| MY-002 | Infinite-mint vector | Mythril | Critical | Cap or role-bound |
| MY-003 | Locked funds / no-withdraw path | Mythril | Medium | Ensure recovery or explicit design |

---

## Thresholds
- Critical: 0 allowed
- High: 0 allowed (override requires evidence + reviewer)
- Medium: ≤ N findings per contract (N=2 default) with rationale
- Low: Informational only

---

## Output Schema
```json
{
  "contract": "Token.sol",
  "findings": [
    {"rule": "SR-001", "severity": "critical", "span": {"file": "Token.sol", "line": 42}, "notes": "tx.origin used"}
  ]
}
```

---

## Acceptance Criteria
- Stable across solc versions pinned in CI
- Documented false-positive handling
- Mapped 1:1 to POLICY_GATE severities




