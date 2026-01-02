# BDP EVM Context & Header Mapping (Normative)

Status: Draft (Implementation-Ready)
Owners: EVM Integration + Core Protocol

---

## 1. Purpose
Define exact mapping from DAG-native data to EVM-visible block/header fields, transaction/receipt indices, gas policy, and randomness.

---

## 2. EVM Header/Context Fields

| EVM Field | Source (Canonical) | Notes |
|---|---|---|
| number | block.CanonicalIndex | 0-based to uint64 |
| hash | block.Hash | canonical L[i] |
| parentHash | L[i-1].Hash | for i>0; genesis uses zero-hash |
| timestamp | block.Timestamp | bounded by drift policy |
| gasLimit | policy.GasLimit(i) | default 30,000,000 |
| baseFeePerGas | policy.BaseFee(i) | EIP-1559 or legacy mode |
| coinbase | MinerFrom(block) | see §3 |
| difficulty | EffectiveDifficulty(block) | see §4 (PoW present) |
| prevRandao | Randomness(i) | see §5 |

---

## 3. Coinbase (Miner) Selection

### 3.1 Default Policy
- coinbase := the miner/author recorded in the DAG block header at L[i].
- Rationale: preserves PoW incentives per block.

### 3.2 Optional Rotating Policy (Deferred)
- For fairness in very wide DAGs, a rotating aggregator could be considered; NOT in scope for MVP.

---

## 4. Difficulty & Dual-Algorithm Policy

### 4.1 Fields
- block.Header.Difficulty: emitted difficulty for this block's algorithm.
- block.Header.Algorithm ∈ {kHeavyHash, SHA3}.

### 4.2 EffectiveDifficulty(block)
- If Algorithm == kHeavyHash: return block.Difficulty.
- If Algorithm == SHA3: return NormalizeSHA3(block.Difficulty) to kHeavyHash-equivalent scale for display only; consensus difficulty remains per-algorithm in the DAG layer.

Note: Difficulty does not impact EVM execution semantics; included for tooling parity.

---

## 5. Randomness (prevRandao)

Ethereum post-Merge uses prevRandao. For PoW DAG, define deterministic randomness:

```
prevRandao(i) = keccak256( L[i-1].hash || L[i-2].hash )
```

- For i=0/1 (genesis/first), use zero-hash fallback.
- Provides unpredictability prior to mining and determinism at verification.

---

## 6. Gas Policy (EIP-1559 vs Legacy)

### 6.1 Modes
- Mode A (Default): EIP-1559 enabled.
- Mode B: Legacy gasPrice (no baseFee) — compile-time or chain-params toggle.

### 6.2 EIP-1559 Base Fee Update
- Use Ethereum’s EIP-1559 formula on canonical chain L:
```
baseFee[i] = update(baseFee[i-1], gasUsed[i-1], gasTarget)
```
- gasTarget = gasLimit / 2
- Conformance with London hardfork rules is required.

### 6.3 Gas Limit Policy
- Fixed or slow-changing per-block policy; start with constant 30,000,000 then govern via config.

---

## 7. Transaction Ordering & Semantics

### 7.1 Within a DAG Block
- Preserve author-specified order within each block.
- Validate nonces strictly increasing per account; reject invalid txs.

### 7.2 Across Canonical Blocks
- Execute blocks in canonical order L[...].
- If two blocks contain conflicting txs (same account & nonce), the earlier canonical block wins; the later tx is invalid and MUST fail validation (pre-exec) or revert with consistent error.

### 7.3 Transaction Indexing
- transactionIndex := position within canonical block, starting at 0.
- receipt.transactionIndex MUST reflect canonical position.

---

## 8. Receipts & Logs

- receipt.blockHash := canonical block hash.
- receipt.blockNumber := canonical index.
- Log ordering: (blockNumber, transactionIndex, logIndex)
- Reorgs MUST rewrite indices according to new L; dApps must follow standard Ethereum reorg handling.

---

## 9. BLOCKHASH Opcode Semantics

- BLOCKHASH(n) returns L[n].hash for the last 256 canonical blocks.
- If (currentNumber - n) > 256, return 0x0 as in Ethereum.

---

## 10. State Checkpoints & Fast Sync (Interface)

- Checkpoint every K=1024 blocks: (blockNumber, stateRoot, bloom, cumulativeGasUsed)
- Fast sync: download latest checkpoint + execute from checkpoint to tip.
- Nodes MUST verify stateRoot continuity across checkpoints.

---

## 11. Validation Requirements

- MUST pass ethereum/tests StateTests for selected forks (London→Shanghai).
- MUST pass JSON-RPC conformance (EIP-1474).
- SHOULD pass additional evmone vectors.

---

## 12. Constants (Initial)
- BlockGasLimitDefault = 30,000,000
- EIP1559Enabled = true
- CheckpointInterval = 1024

---

## 13. Open Items (Track)
- Optional rotating coinbase fairness
- Advanced randomness (VRF) integration
- Dynamic gas limit governance







