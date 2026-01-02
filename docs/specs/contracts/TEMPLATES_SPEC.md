# Secure Contract Templates Spec

Status: Draft (Implementation-Ready)
Owners: Contracts + Security

---

## Templates (Initial)
- ERC-20 (mint/burn, cap, pausability, roles)
- ERC-721 (metadata, royalties optional, roles)
- ERC-1155 (URI, batch ops, roles)
- Vesting (Linear, Cliff, Revocable)
- TimelockController (governance lock)
- Governor (token/weight-based, timelock wired)
- Treasury (multisig + timelock, rate limits)

---

## Required Guards
- AccessControl roles: DEFAULT_ADMIN_ROLE, MINTER_ROLE, PAUSER_ROLE, UPGRADER_ROLE
- Pausable on critical entrypoints
- Cap on ERC-20 totalSupply
- Safe withdraw with whitelist + timelock + daily rate limits
- Event emission for critical state transitions

---

## Upgradeability
- UUPS Proxy pattern with UUPSUpgradeable
- upgradeTo restricted to UPGRADER_ROLE
- All upgrades must pass through TimelockController (min delay ≥ 24h)
- Break-glass pause independent of upgrade path

---

## Presale Pattern Requirements
- Hard cap and soft cap
- RefundVault with deadline and automatic refunds if soft cap unmet
- All proceeds to Treasury with timelock
- Per-wallet min/max limits, allowlists/phases
- Post-sale vesting for team/founders

---

## Events (Canonical)
- Token: Transfer, Approval, Minted, Burned, Paused, Unpaused
- Vesting: GrantCreated, Released, Revoked
- Treasury: WithdrawalQueued, WithdrawalExecuted, LimitUpdated
- Upgrades: UpgradeScheduled, UpgradeExecuted

---

## Invariants (to test)
- Sum of balances == totalSupply (ERC-20/1155 for a tokenId)
- No mint beyond cap
- Only roles can mint/burn/pause/upgrade
- Vesting schedule monotonic; released ≤ vested
- Treasury cannot exceed daily rate limit

---

## Acceptance Criteria
- Compiles with solc 0.8.x
- Passes STATIC_RULESET with 0 Critical/High
- Passes CONTRACT_TEST_SUITE + fuzz invariants
- Includes DEPLOY_PLAYBOOK guidance




