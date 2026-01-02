# Enhanced DAG→Linear Canonicalization Specification
## BlockDAG Phoenix - Production-Ready Implementation

### Overview
This document provides production-ready, code-level specifications for converting the DAG structure to a linear canonical chain for EVM execution.

---

## 1. Core Algorithm Implementation

### 1.1 Tip Selection (Precise Algorithm)

```go
package canonical

import (
    "bytes"
    "sort"
    "time"
)

const (
    MAX_REORG_DEPTH     = 100               // Maximum blocks to roll back
    CHECKPOINT_INTERVAL = 1000              // State checkpoint every N blocks
    MAX_REPLAY_TIME     = 10 * time.Second  // Maximum time for reorg replay
    MAX_PARENTS         = 10                // Maximum parents per block
)

// SelectTipSet finds the best tip set based on cumulative blue work
func SelectTipSet(dag *BlockDAG) ([]*Block, error) {
    // Step 1: Find all leaf blocks (no children)
    tips := dag.GetLeafBlocks()
    if len(tips) == 0 {
        return nil, ErrNoTipsFound
    }
    
    // Step 2: Calculate cumulative blue work for each tip
    tipScores := make(map[Hash]*TipScore)
    maxBlueWork := uint64(0)
    
    for _, tip := range tips {
        score := calculateCumulativeBlueWork(dag, tip)
        tipScores[tip.Hash] = score
        
        if score.BlueWork > maxBlueWork {
            maxBlueWork = score.BlueWork
        }
    }
    
    // Step 3: Select all tips with maximum blue work
    bestTips := []*Block{}
    for _, tip := range tips {
        if tipScores[tip.Hash].BlueWork == maxBlueWork {
            bestTips = append(bestTips, tip)
        }
    }
    
    // Step 4: If multiple tips, apply deterministic selection
    if len(bestTips) > 1 {
        bestTips = deterministicTipSelection(bestTips)
    }
    
    return bestTips, nil
}

// calculateCumulativeBlueWork computes total blue work for a tip
func calculateCumulativeBlueWork(dag *BlockDAG, tip *Block) *TipScore {
    // Implementation of GHOSTDAG blue score calculation
    visited := make(map[Hash]bool)
    blueWork := uint64(0)
    blueBlockCount := 0
    
    // BFS traversal from tip to genesis
    queue := []*Block{tip}
    
    for len(queue) > 0 {
        block := queue[0]
        queue = queue[1:]
        
        if visited[block.Hash] {
            continue
        }
        visited[block.Hash] = true
        
        // Calculate blue score using GHOSTDAG rules
        if isBlueBlock(dag, block) {
            blueWork += block.Difficulty.Uint64()
            blueBlockCount++
        }
        
        // Add parents to queue
        for _, parentHash := range block.Parents {
            parent := dag.GetBlock(parentHash)
            if parent != nil && !visited[parentHash] {
                queue = append(queue, parent)
            }
        }
    }
    
    return &TipScore{
        BlueWork:       blueWork,
        BlueBlockCount: blueBlockCount,
        TipHash:        tip.Hash,
    }
}
```

### 1.2 Canonical Ordering (Exact Implementation)

```go
// BuildCanonicalSequence creates deterministic linear ordering from DAG
func BuildCanonicalSequence(dag *BlockDAG, tipSet []*Block) ([]*Block, error) {
    // Step 1: Collect all blocks reachable from tip set
    allBlocks := collectReachableBlocks(dag, tipSet)
    
    // Step 2: Sort blocks by blue score, timestamp, hash
    sortBlocksCanonically(allBlocks)
    
    // Step 3: Apply topological ordering
    canonical, err := topologicalSort(allBlocks)
    if err != nil {
        return nil, err
    }
    
    // Step 4: Validate ordering
    if err := validateCanonicalOrdering(canonical); err != nil {
        return nil, err
    }
    
    // Step 5: Assign canonical indices
    for i, block := range canonical {
        block.CanonicalIndex = uint64(i)
    }
    
    return canonical, nil
}

// sortBlocksCanonically applies deterministic sorting rules
func sortBlocksCanonically(blocks []*Block) {
    sort.SliceStable(blocks, func(i, j int) bool {
        blockI, blockJ := blocks[i], blocks[j]
        
        // Rule 1: Higher blue score first (descending)
        if blockI.BlueScore != blockJ.BlueScore {
            return blockI.BlueScore > blockJ.BlueScore
        }
        
        // Rule 2: Earlier timestamp first (ascending)
        if blockI.Timestamp != blockJ.Timestamp {
            return blockI.Timestamp < blockJ.Timestamp
        }
        
        // Rule 3: Lexicographic hash comparison (big-endian)
        return bytes.Compare(blockI.Hash[:], blockJ.Hash[:]) < 0
    })
}

// topologicalSort ensures parents come before children
func topologicalSort(blocks []*Block) ([]*Block, error) {
    // Build adjacency list and in-degree map
    inDegree := make(map[Hash]int)
    adjList := make(map[Hash][]*Block)
    blockMap := make(map[Hash]*Block)
    
    for _, block := range blocks {
        blockMap[block.Hash] = block
        inDegree[block.Hash] = 0
    }
    
    // Calculate in-degrees
    for _, block := range blocks {
        for _, parentHash := range block.Parents {
            if parent, exists := blockMap[parentHash]; exists {
                adjList[parentHash] = append(adjList[parentHash], block)
                inDegree[block.Hash]++
            }
        }
    }
    
    // Kahn's algorithm with deterministic tie-breaking
    queue := make([]*Block, 0)
    for _, block := range blocks {
        if inDegree[block.Hash] == 0 {
            queue = append(queue, block)
        }
    }
    
    // Sort initial queue for determinism
    sortBlocksCanonically(queue)
    
    result := make([]*Block, 0, len(blocks))
    
    for len(queue) > 0 {
        // Process block with zero in-degree
        block := queue[0]
        queue = queue[1:]
        result = append(result, block)
        
        // Reduce in-degree of children
        children := adjList[block.Hash]
        sortBlocksCanonically(children) // Deterministic child processing
        
        for _, child := range children {
            inDegree[child.Hash]--
            if inDegree[child.Hash] == 0 {
                // Insert in sorted position
                queue = insertSorted(queue, child)
            }
        }
    }
    
    // Check for cycles
    if len(result) != len(blocks) {
        return nil, ErrCycleDetected
    }
    
    return result, nil
}
```

### 1.3 Reorg Handling (Production-Ready)

```go
// HandleReorg manages reorganization of the canonical chain
func HandleReorg(state *StateDB, oldCanonical, newCanonical []*Block) error {
    // Step 1: Find common ancestor
    commonAncestor, oldSuffix, newSuffix := findForkPoint(oldCanonical, newCanonical)
    
    // Step 2: Validate reorg depth
    if len(oldSuffix) > MAX_REORG_DEPTH {
        return ErrReorgTooDeep{
            Depth:    len(oldSuffix),
            MaxDepth: MAX_REORG_DEPTH,
        }
    }
    
    // Step 3: Create reorg context for atomic execution
    reorgCtx := &ReorgContext{
        CommonAncestor: commonAncestor,
        OldBlocks:      oldSuffix,
        NewBlocks:      newSuffix,
        StartTime:      time.Now(),
    }
    
    // Step 4: Execute reorg with rollback on failure
    if err := executeReorg(state, reorgCtx); err != nil {
        // Rollback to checkpoint
        if rollbackErr := state.RollbackToCheckpoint(commonAncestor.StateRoot); rollbackErr != nil {
            return ErrCriticalStateCorruption{
                OriginalErr: err,
                RollbackErr: rollbackErr,
            }
        }
        return err
    }
    
    // Step 5: Update indices and receipts
    updateCanonicalIndices(newCanonical)
    
    return nil
}

// executeReorg performs the actual state transition
func executeReorg(state *StateDB, ctx *ReorgContext) error {
    // Monitor execution time
    deadline := time.Now().Add(MAX_REPLAY_TIME)
    
    // Step 1: Rollback old chain
    for i := len(ctx.OldBlocks) - 1; i >= 0; i-- {
        block := ctx.OldBlocks[i]
        
        if time.Now().After(deadline) {
            return ErrReorgTimeout
        }
        
        // Revert state changes
        if err := state.RevertBlock(block); err != nil {
            return fmt.Errorf("failed to revert block %s: %w", block.Hash, err)
        }
        
        // Clear transaction receipts
        clearBlockReceipts(block)
    }
    
    // Step 2: Apply new chain
    for _, block := range ctx.NewBlocks {
        if time.Now().After(deadline) {
            return ErrReorgTimeout
        }
        
        // Execute block with EVM
        receipts, err := executeBlockTransactions(state, block)
        if err != nil {
            return fmt.Errorf("failed to execute block %s: %w", block.Hash, err)
        }
        
        // Store receipts
        storeBlockReceipts(block, receipts)
        
        // Verify state root
        if state.IntermediateRoot() != block.StateRoot {
            return ErrStateRootMismatch{
                Expected: block.StateRoot,
                Actual:   state.IntermediateRoot(),
                Block:    block.Hash,
            }
        }
    }
    
    // Step 3: Checkpoint if needed
    if shouldCheckpoint(ctx.NewBlocks[len(ctx.NewBlocks)-1]) {
        if err := state.Checkpoint(ctx.NewBlocks[len(ctx.NewBlocks)-1].StateRoot); err != nil {
            return fmt.Errorf("failed to checkpoint: %w", err)
        }
    }
    
    return nil
}
```

## 2. EVM Context Mapping

### 2.1 Block Context Translation

```go
// MapToEVMContext creates EVM execution context from DAG block
func MapToEVMContext(block *Block, canonical []*Block) *vm.BlockContext {
    return &vm.BlockContext{
        // Canonical position
        BlockNumber: big.NewInt(int64(block.CanonicalIndex)),
        
        // Time from block
        Time:        big.NewInt(block.Timestamp),
        
        // Deterministic coinbase selection
        Coinbase:    selectCoinbase(block, canonical),
        
        // Gas parameters
        GasLimit:    block.GasLimit,
        BaseFee:     calculateBaseFee(canonical, block.CanonicalIndex),
        
        // Difficulty normalization
        Difficulty:  normalizeDifficulty(block),
        
        // Hash lookups (last 256 blocks)
        GetHash:     createHashLookup(canonical, block.CanonicalIndex),
        
        // EIP-4399 random (derived from block hash)
        Random:      deriveRandomness(block),
        
        // Custom Phoenix fields
        DAGContext: &DAGContext{
            BlueScore:    block.BlueScore,
            Algorithm:    block.Algorithm,
            ParentHashes: block.Parents,
        },
    }
}

// selectCoinbase determines block reward recipient
func selectCoinbase(block *Block, canonical []*Block) common.Address {
    // Option 1: Use block miner
    if block.Algorithm == AlgoKHeavyHash {
        return block.MinerAddress
    }
    
    // Option 2: For SHA-3, rotate among recent miners for fairness
    if block.Algorithm == AlgoSHA3 {
        // Get last 10 unique miners
        recentMiners := getRecentMiners(canonical, block.CanonicalIndex, 10)
        if len(recentMiners) > 0 {
            // Deterministic selection based on block hash
            index := binary.BigEndian.Uint32(block.Hash[:4]) % uint32(len(recentMiners))
            return recentMiners[index]
        }
    }
    
    return block.MinerAddress
}

// calculateBaseFee implements EIP-1559 for DAG
func calculateBaseFee(canonical []*Block, index uint64) *big.Int {
    if index == 0 {
        return params.InitialBaseFee
    }
    
    parent := canonical[index-1]
    parentGasUsed := parent.GasUsed
    parentGasTarget := parent.GasLimit / 2
    
    // EIP-1559 base fee calculation
    baseFeeDelta := new(big.Int).Mul(parent.BaseFee, big.NewInt(int64(parentGasUsed-parentGasTarget)))
    baseFeeDelta.Div(baseFeeDelta, big.NewInt(int64(parentGasTarget)))
    baseFeeDelta.Div(baseFeeDelta, params.BaseFeeChangeDenominator)
    
    newBaseFee := new(big.Int).Add(parent.BaseFee, baseFeeDelta)
    
    // Apply bounds
    if newBaseFee.Cmp(params.MinBaseFee) < 0 {
        newBaseFee = params.MinBaseFee
    }
    
    return newBaseFee
}
```

## 3. Edge Case Handling

### 3.1 Network Partition Recovery

```go
// HandleNetworkPartition manages competing tip sets after network split
func HandleNetworkPartition(dag *BlockDAG, partitionA, partitionB []*Block) (*ReconciliationResult, error) {
    // Step 1: Identify partition characteristics
    analysisA := analyzePartition(partitionA)
    analysisB := analyzePartition(partitionB)
    
    // Step 2: Determine winning partition (higher cumulative work)
    var winningPartition, losingPartition []*Block
    if analysisA.CumulativeWork.Cmp(analysisB.CumulativeWork) > 0 {
        winningPartition = partitionA
        losingPartition = partitionB
    } else if analysisA.CumulativeWork.Cmp(analysisB.CumulativeWork) < 0 {
        winningPartition = partitionB
        losingPartition = partitionA
    } else {
        // Equal work - use deterministic tie-breaker
        winningPartition = deterministicPartitionSelection(partitionA, partitionB)
        if winningPartition == partitionA {
            losingPartition = partitionB
        } else {
            losingPartition = partitionA
        }
    }
    
    // Step 3: Create reconciliation plan
    result := &ReconciliationResult{
        WinningChain:    winningPartition,
        OrphanedBlocks:  losingPartition,
        ReorgDepth:      calculateReorgDepth(dag, winningPartition, losingPartition),
    }
    
    // Step 4: Handle orphaned transactions
    result.OrphanedTxs = extractOrphanedTransactions(losingPartition)
    
    return result, nil
}
```

### 3.2 Clock Skew Attack Prevention

```go
// ValidateBlockTimestamp prevents timestamp manipulation
func ValidateBlockTimestamp(block *Block, canonical []*Block) error {
    now := time.Now().Unix()
    
    // Rule 1: Block timestamp cannot be in the future
    if block.Timestamp > now+MAX_FUTURE_BLOCK_TIME {
        return ErrTimestampTooFarInFuture{
            BlockTime: block.Timestamp,
            MaxTime:   now + MAX_FUTURE_BLOCK_TIME,
        }
    }
    
    // Rule 2: Median time past rule (like Bitcoin)
    if block.CanonicalIndex > 0 {
        medianTime := calculateMedianTimePast(canonical, block.CanonicalIndex)
        if block.Timestamp <= medianTime {
            return ErrTimestampTooEarly{
                BlockTime:  block.Timestamp,
                MedianTime: medianTime,
            }
        }
    }
    
    // Rule 3: Check for systematic clock skew
    if detectClockSkew(block, canonical) {
        return ErrSuspectedClockManipulation
    }
    
    return nil
}
```

## 4. Performance Optimizations

### 4.1 Checkpoint System

```go
// CheckpointManager handles state persistence for fast sync
type CheckpointManager struct {
    interval    uint64
    storage     CheckpointStorage
    cache       *lru.Cache
}

func (cm *CheckpointManager) ShouldCheckpoint(block *Block) bool {
    return block.CanonicalIndex%cm.interval == 0
}

func (cm *CheckpointManager) CreateCheckpoint(state *StateDB, block *Block) error {
    checkpoint := &Checkpoint{
        BlockHash:      block.Hash,
        BlockNumber:    block.CanonicalIndex,
        StateRoot:      state.IntermediateRoot(),
        Timestamp:      time.Now(),
        CompressedSize: 0, // Will be set after compression
    }
    
    // Compress state data
    stateData := state.Dump()
    compressed := snappy.Encode(nil, stateData)
    checkpoint.CompressedSize = uint64(len(compressed))
    
    // Store checkpoint
    if err := cm.storage.Store(checkpoint, compressed); err != nil {
        return err
    }
    
    // Update cache
    cm.cache.Add(block.CanonicalIndex, checkpoint)
    
    return nil
}
```

## 5. Testing Scenarios

### 5.1 Complex DAG Patterns

```go
// TestComplexDAGPatterns verifies canonicalization handles edge cases
func TestComplexDAGPatterns(t *testing.T) {
    testCases := []struct {
        name     string
        pattern  DAGPattern
        expected []Hash
    }{
        {
            name:     "Diamond pattern",
            pattern:  CreateDiamondDAG(4),
            expected: []Hash{genesis, left, right, tip}, // Deterministic ordering
        },
        {
            name:     "Wide DAG (100 parallel chains)",
            pattern:  CreateWideDAG(100, 10),
            expected: deterministicWideOrdering(100, 10),
        },
        {
            name:     "Deep DAG (1000 sequential blocks)",
            pattern:  CreateDeepDAG(1000),
            expected: sequentialOrdering(1000),
        },
        {
            name:     "Butterfly pattern (complex merging)",
            pattern:  CreateButterflyDAG(8),
            expected: butterflyOrdering(8),
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            dag := BuildDAG(tc.pattern)
            canonical, err := BuildCanonicalSequence(dag, dag.GetTips())
            
            require.NoError(t, err)
            require.Equal(t, tc.expected, extractHashes(canonical))
            
            // Verify determinism
            canonical2, _ := BuildCanonicalSequence(dag, dag.GetTips())
            require.Equal(t, canonical, canonical2, "canonicalization must be deterministic")
        })
    }
}
```

## 6. Error Types

```go
// Comprehensive error definitions
var (
    ErrNoTipsFound        = errors.New("no tips found in DAG")
    ErrCycleDetected      = errors.New("cycle detected in DAG")
    ErrReorgTimeout       = errors.New("reorg exceeded maximum time limit")
    ErrInvalidTopology    = errors.New("canonical sequence violates topological order")
    ErrStateRootMismatch  = errors.New("state root mismatch after execution")
)

type ErrReorgTooDeep struct {
    Depth    int
    MaxDepth int
}

type ErrStateRootMismatch struct {
    Expected common.Hash
    Actual   common.Hash
    Block    common.Hash
}

type ErrTimestampTooFarInFuture struct {
    BlockTime int64
    MaxTime   int64
}
```

## 7. Configuration Constants

```go
const (
    // Reorg limits
    MAX_REORG_DEPTH     = 100               // Maximum blocks to roll back
    MAX_REPLAY_TIME     = 10 * time.Second  // Maximum time for reorg
    
    // Checkpoint configuration
    CHECKPOINT_INTERVAL = 1000               // Blocks between checkpoints
    CHECKPOINT_CACHE    = 10                 // Checkpoints to keep in memory
    
    // DAG structure limits
    MAX_PARENTS         = 10                 // Maximum parents per block
    MAX_BLUE_SCORE      = 1000000            // Maximum blue score value
    
    // Timing constraints
    MAX_FUTURE_BLOCK_TIME = 15               // Seconds into future allowed
    MEDIAN_TIME_BLOCKS    = 11               // Blocks for median time calculation
    
    // Performance tuning
    PARALLEL_VALIDATION   = true              // Enable parallel validation
    VALIDATION_WORKERS    = 8                 // Number of validation goroutines
)
```

---

This enhanced specification provides the code-level detail needed for AI agents to implement production-ready DAG→EVM integration.



