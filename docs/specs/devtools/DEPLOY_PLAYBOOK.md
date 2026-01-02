# Deployment Playbook (Contracts)

Status: Draft (Implementation-Ready)
Owners: DevTools + Ops + Security

---

## Environments
- Local dev (simulated reorgs allowed)
- Testnet (Phoenix)
- Mainnet (Phoenix)

---

## Preflight Checklist
- Policy Gate: pass (0 Critical/High) or approved override with evidence
- Static: Slither/Mythril clean within thresholds
- Tests: unit/integration/fuzz + reorg harness green
- Parameters: caps, timelocks, roles, addresses double‑checked
- Multisig + Timelock addresses verified and funded

---

## Dry Run
- Deploy to ephemeral test env via scripts
- Run end‑to‑end playbooks (mint, pause, upgrade schedule)
- Archive artifacts (ABIs, addresses, reports)

---

## Rollout Steps
1) Deploy proxies + implementations
2) Initialize roles and caps
3) Wire TimelockController and transfer admin
4) Schedule and execute any initial config via timelock
5) Publish ABIs/addresses, verify on explorer

---

## Post‑Deploy Validation
- Health checks: calls to read endpoints, paused state, caps
- Small txs through critical paths (mint, transfer, withdraw queue)
- Indexer/explorer verification

---

## Rollback
- If upgrade misconfig: revert via Timelock scheduled rollback
- If critical issue: pause; switch to minimal safe mode; schedule fix

---

## Emergency
- Trigger pausability; disable dangerous entrypoints
- Block Treasury withdrawals; keep RefundVault operable
- Public notice + incident thread; track follow‑ups

---

## Artifacts
- deployment.json (addresses, tx hashes)
- policy-report.json, static-report.json, test-report.json
- operator-runbook.md with commands




