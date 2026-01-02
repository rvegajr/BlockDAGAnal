# BDP Contract Test Suite (Authoritative)

Status: Draft (Executable Plan)
Owners: EVM Integration + DevTools + QA

---

## 1) Goals
- Prove full EVM parity on Phoenix canonical chain L
- Validate DAG→EVM mapping under reorgs/ordering changes
- Provide runnable samples for developers and CI

---

## 2) Coverage Matrix

### A. Core Semantics
- Storage/ABI: SimpleStorage (set/get)
- Events/Logs: LogEmitter (indexed/unindexed, topics, bloom)
- Reverts/Errors: require/assert/custom errors
- CREATE/CREATE2: Factory deploying child with salt
- SELFDESTRUCT: legacy cleanup behaviors (informational)
- Precompiles: ecrecover/sha256/ripemd160/blake2f/bn128/modexp smoke tests
- Randomness: prevRandao exposure wiring

### B. Token Standards
- ERC-20: mint/burn/transfer/approve/allowance/events
- ERC-721: mint/transfer/metadata/events
- ERC-1155: batch mint/transfer/URI/events

### C. Security
- Reentrancy: victim + attacker; ensure protections & expected failure modes
- Access Control: onlyOwner, role-based
- Nonce/Replay: tx ordering under reorg

### D. Gas & Performance
- Intrinsic gas rules (legacy/2930/1559)
- Base fee dynamics (EIP-1559) across target gas usage
- Busy block (many tx) log ordering and receipt determinism

---

## 3) Reorg & Canonicalization Tests (Cross-ref)
- Pair with [DAG_TEST_SCENARIOS.md](DAG_TEST_SCENARIOS.md)
- Execute: deploy → emit events → simulate reorg → assert indices and state

---

## 4) Runnable Examples (This Repo)
- Solidity examples: `docs/examples/contracts/`
- Hardhat suite: `docs/examples/hardhat/`
- Foundry suite: `docs/examples/foundry/`

All examples assume Phoenix JSON-RPC (local):
```
RPC_URL=http://127.0.0.1:16111
CHAIN_ID=8888
```

---

## 5) Required Assertions (Per Category)

### Storage/ABI
- set(value) then get() == value across multiple blocks
- State preserved after reorg to same canonical stateRoot

### Events/Logs
- topics ordering exact, bloom contains expected bits
- receipt.logIndex monotonic within tx; stable per canonical L

### Tokens
- Balances and allowances exact; events match OpenZeppelin semantics
- Fuzz mints/transfers to verify invariants

### CREATE/CREATE2
- Address calculation exact per EVM rules
- Deterministic across nodes; unaffected by DAG reordering when canonicalized

### Reentrancy
- Attack fails against protected function; succeeds against intentionally vulnerable function in test (for detection)

### Gas/Base Fee
- 1559 baseFee transitions exact given gasUsed deviations from target
- Legacy path identical when 1559 disabled

---

## 6) CI Integration Hints
- Hardhat: `npm run test` using `HARDHAT_NETWORK=phoenix`
- Foundry: `forge test -vvv` with `rpc_url` set to Phoenix
- Gate: run subset on PRs, full matrix nightly

---

## 7) Artifacts to Capture
- stateRoot per block, receipt roots, tx roots
- Gas used, baseFee, transactionIndex/logIndex triplets
- Event payload snapshots for diffing

---

## 8) Exit Criteria
- All tests pass against local node under synthetic reorgs up to MaxReorgDepth
- Parity with go-ethereum state tests (London→Shanghai)
- Determinism: identical stateRoots across 10 randomized arrival permutations

---

## 9) Pointers
- Mapping rules: [EVM_CONTEXT_MAPPING.md](../evm/EVM_CONTEXT_MAPPING.md)
- Canonicalization rules: [CANONICALIZATION_DETAILED.md](../core-node/CANONICALIZATION_DETAILED.md)
- Reorg policy: [REORG_HANDLING.md](../core-node/REORG_HANDLING.md)





