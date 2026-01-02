# Reorg Simulation Harness Spec

Status: Draft (Implementation-Ready)
Owners: Testing + Core + EVM Integration

---

## Purpose
Provide an automated way to script DAG growth, induce canonical reorgs within MaxReorgDepth, and assert contract behavior/indices/state remain consistent under canonicalization.

---

## Interfaces

### CLI
```
phoenix-reorg --rpc http://127.0.0.1:16111 \
  --depth 10 \
  --script scripts/sequence.yaml \
  --checkpoint-interval 1024
```

### JS API (for Hardhat)
```ts
await harness.fork(depth);
await harness.mineOn(branchA, txsA);
await harness.mineOn(branchB, txsB);
await harness.reorgTo(branchBTip);
const report = await harness.assertCanonical({ receipts: true, logs: true, state: true });
```

### Foundry Cheatcodes (shim)
- forge-std style helper that calls the harness via RPC

---

## Script Format (YAML)
```yaml
steps:
  - name: deploy
    txs:
      - contract: SimpleStorage
        method: set
        args: [42]
  - name: branchA
    mine: 5
  - name: branchB
    fork: 3
    txs:
      - contract: SimpleStorage
        method: set
        args: [7]
  - name: reorg
    switchTo: branchB
```

---

## Assertions
- StateRoot matches after replay per CANONICALIZATION_DETAILED
- receipt.blockNumber/hash and (transactionIndex, logIndex) recomputed per L
- BLOCKHASH opcode semantics (last 256) preserved

---

## Outputs
- JSON report with before/after canonical heads, affected range, timing
- Artifacts: receipts, logs, stateRoots, block headers subset

---

## Acceptance Criteria
- Deterministic across runs
- Depth limited to policy (MaxReorgDepth)
- Performance targets: replay ≤ 10s at depth=100 on reference machine




