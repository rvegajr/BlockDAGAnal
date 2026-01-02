# BDP DAG→EVM Test Scenarios (Authoritative)

Status: Draft (Executable Plan)
Owners: QA + Core + EVM Integration

---

## 1. Determinism Under Arrival Permutations
- Same set of blocks, 10k random arrival orders → identical L.
- Validate parent-before-child invariant always holds.

## 2. Tie-Breaking Exhaustives
- Equal blueScore, varying timestamps → ordered by timestamp.
- Equal blueScore & timestamp, varying hashes → lexicographic.
- Flood of equal-score blocks (1000+) → stable sort properties preserved.

## 3. Reorg Depth Matrix
- Depths: 1, 2, 5, 10, 50, 100.
- Measure replay time; enforce MaxReplayWallTime.
- Validate indices (txIndex, logIndex) rewritten consistently.

## 4. Nonce Conflict Resolution
- Two branches contain (acct A, nonce n) with different txs.
- Earlier canonical block wins; conflicting tx rejected.
- Validate stateRoot consistency and receipts.

## 5. BLOCKHASH Semantics
- Query last 256 block hashes across rolling window.
- Validate returns 0 for >256 distance.

## 6. Gas Policy (EIP-1559)
- Base fee update across high/low gas usage patterns.
- Gas limit at 30M; target at 15M.
- Validate fee markets match Ethereum rules exactly.

## 7. Randomness (prevRandao)
- Validate prevRandao(i) = keccak(L[i-1] || L[i-2]).
- Check determinism and distribution sanity.

## 8. Checkpointing & Fast Sync
- Create checkpoints every 1024 blocks.
- Restore from checkpoint; replay to tip; compare stateRoot.

## 9. Performance & Scale
- Canonical build for 10k/100k blocks ≤ targets.
- Memory usage bounded; no leaks under continuous operation.

## 10. Explorer/Indexing Parity
- Blockscout displays canonical numbers, tx indices, logs accurately after reorg.
- Subgraph reindexing correctness under reorg.

## 11. Security/Adversarial
- Timestamp skew near max allowed drift.
- Attempted tie-break manipulation via crafted hashes.
- Wide-DAG stress with 10k parallel parents at peak.

## 12. Compatibility Suite
- ethereum/tests StateTests pass (London→Shanghai).
- RPC conformance (EIP-1474) exact.

## 13. Documentation of Results
- Record metrics per run; attach artifacts (stateRoots, receipts, logs).
- Track regressions with thresholds.







