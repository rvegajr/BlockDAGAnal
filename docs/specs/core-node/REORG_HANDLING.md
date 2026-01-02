# BDP Reorg Handling (Normative)

Status: Draft (Implementation-Ready)
Owners: Core Protocol + EVM Integration

---

## 1. Purpose
Define safe, bounded, and deterministic reorganization (reorg) behavior for DAG→linear canonical exposure and EVM state replay.

---

## 2. Reorg Model
- DAG consensus admits all valid blocks; canonical exposure L may change with new information.
- Reorg = change from L → L' after processing a new block.

---

## 3. Limits & Policy
- MaxReorgDepth := 100 blocks (initial policy; configurable)
- MaxReplayWallTime := 10s target
- CheckpointInterval := 1024 blocks
- FinalityHint := N=300 confirmations for economic finality (UX guidance)

---

## 4. Algorithm
```go
func HandleReorg(oldL, newL []*Block, state *State) error {
    lcp := LongestCommonPrefix(oldL, newL)
    if len(oldL)-lcp > MaxReorgDepth {
        return ErrReorgTooDeep
    }

    // 1) Roll back to checkpoint ≤ lcp
    cp := NearestCheckpointAtOrBefore(lcp)
    if err := state.RestoreCheckpoint(cp); err != nil { return err }

    // 2) Replay from checkpoint to tip of newL
    for i := cp; i < len(newL); i++ {
        if err := ExecuteBlock(newL[i], state); err != nil { return err }
        if i%CheckpointInterval == 0 { state.CreateCheckpoint(i) }
    }

    // 3) Recompute indices
    ReindexTransactions(newL)
    ReindexLogs(newL)

    return nil
}
```

---

## 5. Receipt/Log Stability
- Indices are canonical; they change on reorg, identical to Ethereum behavior.
- Indexing MUST be recomputed as part of reorg handling.

---

## 6. Mempool Interaction
- Pending txs against old suffix are revalidated on newL.
- Invalidated txs (nonce conflict or insuff. gas) are dropped.
- Nonce gaps are handled per Ethereum rules.

---

## 7. Telemetry & Operator Guidance
- Emit metrics: reorg_depth, replay_time, checkpoints_restored.
- Alert when depth > 10 or replay_time > 5s.
- Recommend user-facing UIs wait N confirmations (FinalityHint) for irreversible UX.

---

## 8. Security Considerations
- Adversaries attempting deep reorgs are bounded by MaxReorgDepth; nodes may refuse deeper reorgs absent manual override.
- Checkpointing reduces worst-case replay cost.

---

## 9. Test Cases
- 1–100 depth reorgs with random DAG branches
- Conflicting nonce transactions across branches
- Log/receipt index rewrites validated against new L
- Replay time under 10s across hardware profiles







