# Developer Test Guide (Phoenix EVM)

Status: Draft
Owners: DevRel + QA

---

## Prereqs
- Phoenix node: `bdpd` running at http://127.0.0.1:16111 (testnet or local)
- Node.js 18+, pnpm/npm; Foundry (forge/cast)

Env:
```
export RPC_URL=http://127.0.0.1:16111
export CHAIN_ID=8888
```

---

## Hardhat
```
npm install
npx hardhat test --network phoenix
```
Network config example:
```ts
phoenix: { url: process.env.RPC_URL!, chainId: Number(process.env.CHAIN_ID) }
```

---

## Foundry
```
forge test -vvv --fork-url $RPC_URL --chain-id $CHAIN_ID
```
`foundry.toml` snippet:
```
rpc_endpoints = { phoenix = "${RPC_URL}" }
```

---

## Reorg Harness
- Write `scripts/sequence.yaml` per REORG_HARNESS_SPEC
- From Hardhat: `await harness.run("scripts/sequence.yaml")`
- Assertions: receipts/log indices/stateRoot match canonical L

---

## Reports (CI Artifacts)
- policy-report.json, static-report.json
- test-report.json (unit/integration/fuzz)
- reorg-report.json (affected range, timing)

---

## Common Failures
- Nonce conflicts across branches → fix ordering or guard
- Missing roles/timelocks → policy gate blocks
- Gas spikes → re-test under EIP‑1559 scenarios




