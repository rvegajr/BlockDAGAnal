# BDP DAG → Linear Canonicalization (Detailed, Normative)

Status: Draft (Implementation-Ready)
Owners: Core Protocol + EVM Integration

---

## 1. Purpose
Provide a precise, deterministic algorithm to map the block DAG to a linear sequence L used for EVM state execution while consensus remains DAG-based.

---

## 2. Definitions
- DAG: Directed acyclic graph of blocks with multiple parents per block.
- Blue score: GHOSTDAG cumulative quality metric per Kaspa.
- Tip: A block with no children yet observed by the node.
- Canonical index: The position of a block in the final linear sequence L (0-based).

---

## 3. Deterministic Ordering Algorithm

### 3.1 Tip-Set Selection
Select the set of best tips maximizing cumulative blue work.

Pseudocode (Go-style):
```go
// Tip set = leaves with maximal cumulative blue work
func SelectTipSet(dag *BlockDAG) []*Block {
    leaves := dag.GetLeaves()
    best := []*Block{}
    var bestWork big.Int

    for _, leaf := range leaves {
        work := dag.CumulativeBlueWork(leaf)
        if work.Cmp(&bestWork) > 0 {
            best = []*Block{leaf}
            bestWork = *new(big.Int).Set(&work)
        } else if work.Cmp(&bestWork) == 0 {
            best = append(best, leaf)
        }
    }
    return best
}
```

Notes:
- Ties are allowed; downstream ordering resolves deterministically.

### 3.2 Total Ordering with Stable Tie-Breakers

Sort all ancestors of the selected tip set using the following strict, stable key:
1) blueScore DESC
2) timestamp ASC (earlier first)
3) hash ASC (lexicographic big-endian byte comparison)

Then enforce topological order using Kahn’s algorithm to guarantee parents precede children.

```go
func BuildCanonicalSequence(dag *BlockDAG, tipSet []*Block) []*Block {
    ancestors := dag.GetAncestorsUnion(tipSet) // includes tipSet

    sort.SliceStable(ancestors, func(i, j int) bool {
        if ancestors[i].BlueScore != ancestors[j].BlueScore {
            return ancestors[i].BlueScore > ancestors[j].BlueScore // DESC
        }
        if ancestors[i].Timestamp != ancestors[j].Timestamp {
            return ancestors[i].Timestamp < ancestors[j].Timestamp // ASC
        }
        return bytes.Compare(ancestors[i].Hash[:], ancestors[j].Hash[:]) < 0 // ASC
    })

    return topoSortStable(ancestors)
}

func topoSortStable(blocks []*Block) []*Block {
    inDeg := map[Hash]int{}
    next := map[Hash][]*Block{}
    for _, b := range blocks {
        inDeg[b.Hash] = len(b.Parents)
        for _, p := range b.Parents {
            next[p] = append(next[p], b)
        }
    }
    // queue initialized in the already-sorted order to preserve stability
    q := []*Block{}
    for _, b := range blocks {
        if inDeg[b.Hash] == 0 {
            q = append(q, b)
        }
    }

    out := []*Block{}
    for len(q) > 0 {
        b := q[0]
        q = q[1:]
        out = append(out, b)
        for _, c := range next[b.Hash] {
            inDeg[c.Hash]--
            if inDeg[c.Hash] == 0 {
                q = append(q, c)
            }
        }
    }
    return out
}
```

### 3.3 Canonical Index Assignment
```go
func AssignCanonicalIndices(L []*Block) {
    for i, b := range L { b.CanonicalIndex = uint64(i) }
}
```

### 3.4 Determinism Requirements
- Same DAG -> same L on all honest nodes.
- Sorting keys are total and stable.
- Topological enforcement guarantees parent-before-child.

---

## 4. Reorg Handling (Delta Replay)

### 4.1 Procedure
- Let L be previous canonical sequence and L' be new sequence after a DAG update.
- Find longest common prefix (LCP).
- Roll back state to closest checkpoint ≤ LCP tail.
- Re-execute suffix of L' from checkpoint forward.

```go
const (
    MaxReorgDepth       = 100          // policy, adjustable
    CheckpointInterval  = 1024         // blocks
    MaxReplayWallTime   = 10 * time.Second
)

func Reorg(oldL, newL []*Block, state *State) error {
    lcp := longestCommonPrefix(oldL, newL)
    if len(oldL)-lcp > MaxReorgDepth { return ErrReorgTooDeep }

    cp := nearestCheckpoint(lcp)
    if err := state.RestoreCheckpoint(cp); err != nil { return err }

    for i := cp; i < len(newL); i++ {
        if err := ExecuteBlock(newL[i], state); err != nil { return err }
        if i%CheckpointInterval == 0 { state.CreateCheckpoint(i) }
    }
    return nil
}
```

### 4.2 Receipt/Index Stability
- transactionIndex: per canonical block, monotonically increasing.
- logIndex: stable within (block, tx) regardless of arrival order.
- On reorg, reassign indices according to new L; dApps must tolerate reorg semantics (as on Ethereum).

---

## 5. Header Exposure to EVM (Summary)
- number = canonical index
- parentHash = hash(L[i-1])
- timestamp = block.timestamp
- gasLimit, baseFee = policy (see EVM_CONTEXT_MAPPING.md)
- difficulty / prevRandao = policy (see EVM_CONTEXT_MAPPING.md)
- coinbase = miner selection policy (see EVM_CONTEXT_MAPPING.md)

---

## 6. Security & Edge Cases
- Network split: deterministic selection via blueScore sorting; reorg bounded by MaxReorgDepth.
- Timestamp skew: tie-break by hash; enforce max future drift at admission.
- Adversarial tie-flood: sorting remains O(n log n); topo O(n + m).
- Very wide DAGs: memory-bound by ancestors of tip set; apply pruning.

---

## 7. Performance Targets
- Canonical rebuild: ≤ 50 ms for 10k blocks in memory.
- Reorg replay: ≤ 10 s for MaxReorgDepth with CheckpointInterval=1024.
- State checkpoint size: ≤ 5 GB at 10M accounts (tunable).

---

## 8. Validation Suite
- Determinism: randomized arrival orders -> identical L.
- Topology: parents always precede children.
- Reorg: random forks; replay under MaxReorgDepth.
- Indices: tx/log indices stable per L.

---

## 9. Constants (Initial Policy)
- MaxReorgDepth = 100 blocks
- CheckpointInterval = 1024 blocks
- BlockGasLimitDefault = 30,000,000

---

## 10. Notes
- GHOSTDAG parameters (k) are inherited from consensus spec.
- Implementation must avoid re-sorting entire DAG on each tip; maintain incremental structures.







