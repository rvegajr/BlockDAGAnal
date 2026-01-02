# DAG→EVM Integration Master Specification
## BlockDAG Phoenix - Complete Production Specification

**Version**: 1.0.0  
**Status**: Production-Ready  
**Last Updated**: November 14, 2025  
**Criticality**: CORE INNOVATION - HIGHEST PRIORITY

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Core Innovation Overview](#2-core-innovation-overview)
3. [Canonical Chain Construction](#3-canonical-chain-construction)
4. [State Management Architecture](#4-state-management-architecture)
5. [Transaction Ordering & Execution](#5-transaction-ordering--execution)
6. [EVM Context Mapping](#6-evm-context-mapping)
7. [Reorganization Handling](#7-reorganization-handling)
8. [Gas Economics & Fee Model](#8-gas-economics--fee-model)
9. [Cross-Block References](#9-cross-block-references)
10. [Performance Specifications](#10-performance-specifications)
11. [Security Considerations](#11-security-considerations)
12. [Testing Requirements](#12-testing-requirements)
13. [Implementation Checklist](#13-implementation-checklist)

---

## 1. Executive Summary

### 1.1 The Challenge
Traditional EVM requires linear blockchain; Phoenix uses DAG structure. This specification defines the bridge between parallel DAG consensus and sequential EVM execution.

### 1.2 The Innovation
A deterministic canonicalization algorithm that:
- Converts DAG to linear chain in real-time
- Maintains EVM compatibility
- Preserves DAG performance benefits
- Handles reorgs efficiently

### 1.3 Critical Success Factors
- **Determinism**: Same DAG → Same canonical chain across all nodes
- **Performance**: <10s reorg replay time for 100 block depth
- **Compatibility**: Pass all Ethereum state tests
- **Scalability**: Handle 1000+ parallel blocks efficiently

---

## 2. Core Innovation Overview

### 2.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                   DAG Layer (GHOSTDAG)              │
│  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐           │
│  │ B1 ├──┤ B3 ├──┤ B5 ├──┤ B7 ├──┤ B9 │           │
│  └──┬─┘  └──┬─┘  └──┬─┘  └──┬─┘  └────┘           │
│     │    ┌──┴─┐  ┌──┴─┐  ┌──┴─┐                   │
│     └────┤ B2 ├──┤ B4 ├──┤ B6 │                   │
│          └────┘  └────┘  └────┘                   │
└─────────────────────┬───────────────────────────────┘
                      │ Canonicalization
                      ▼
┌─────────────────────────────────────────────────────┐
│              Canonical Linear Chain                  │
│  [B0] → [B1] → [B2] → [B3] → [B4] → [B5] → ...     │
└─────────────────────┬───────────────────────────────┘
                      │ EVM Execution
                      ▼
┌─────────────────────────────────────────────────────┐
│                    EVM State                        │
│  Account States, Smart Contracts, Receipts, Logs    │
└─────────────────────────────────────────────────────┘
```

### 2.2 Key Components

| Component | Purpose | Criticality |
|-----------|---------|-------------|
| Canonicalizer | DAG → Linear ordering | CRITICAL |
| State Manager | EVM state transitions | CRITICAL |
| Context Mapper | DAG fields → EVM fields | CRITICAL |
| Reorg Handler | Chain reorganization | HIGH |
| Gas Calculator | Dynamic fee adjustment | MEDIUM |

---

## 3. Canonical Chain Construction

### 3.1 Tip Selection Algorithm

```go
package canonical

import (
    "sort"
    "bytes"
    "sync"
    "time"
)

const (
    // Critical constants for production
    MAX_TIP_SET_SIZE     = 100    // Maximum concurrent tips to process
    TIP_SELECTION_TIMEOUT = 5000   // 5 seconds max for tip selection
    MIN_BLUE_WORK_DELTA  = 1000    // Minimum work difference for clear winner
)

type TipSelector struct {
    mu              sync.RWMutex
    dag             *BlockDAG
    blueWorkCache   map[Hash]uint64
    tipScoreCache   map[Hash]*TipScore
    lastUpdate      time.Time
}

// SelectBestTipSet finds optimal tip set with comprehensive validation
func (ts *TipSelector) SelectBestTipSet() ([]*Block, error) {
    ts.mu.Lock()
    defer ts.mu.Unlock()
    
    // Start timer for timeout protection
    deadline := time.Now().Add(TIP_SELECTION_TIMEOUT * time.Millisecond)
    
    // Step 1: Get all current tips (leaf blocks)
    tips := ts.dag.GetLeafBlocks()
    if len(tips) == 0 {
        return nil, ErrNoTipsFound
    }
    if len(tips) > MAX_TIP_SET_SIZE {
        // Sort by timestamp and take most recent
        sort.Slice(tips, func(i, j int) bool {
            return tips[i].Timestamp > tips[j].Timestamp
        })
        tips = tips[:MAX_TIP_SET_SIZE]
    }
    
    // Step 2: Calculate cumulative blue work for each tip
    tipScores := make(map[Hash]*TipScore)
    maxBlueWork := uint64(0)
    secondMaxWork := uint64(0)
    
    for _, tip := range tips {
        if time.Now().After(deadline) {
            return nil, ErrTipSelectionTimeout
        }
        
        // Check cache first
        if cached, exists := ts.tipScoreCache[tip.Hash]; exists &&
           time.Since(cached.Timestamp) < 30*time.Second {
            tipScores[tip.Hash] = cached
            if cached.BlueWork > maxBlueWork {
                secondMaxWork = maxBlueWork
                maxBlueWork = cached.BlueWork
            }
            continue
        }
        
        // Calculate fresh
        score := ts.calculateCumulativeBlueWork(tip, deadline)
        tipScores[tip.Hash] = score
        ts.tipScoreCache[tip.Hash] = score
        
        if score.BlueWork > maxBlueWork {
            secondMaxWork = maxBlueWork
            maxBlueWork = score.BlueWork
        } else if score.BlueWork > secondMaxWork {
            secondMaxWork = score.BlueWork
        }
    }
    
    // Step 3: Select tips with maximum blue work
    // Include margin for near-ties to prevent flip-flopping
    threshold := maxBlueWork
    if maxBlueWork-secondMaxWork < MIN_BLUE_WORK_DELTA {
        threshold = secondMaxWork // Include both in tie-breaking
    }
    
    bestTips := []*Block{}
    for _, tip := range tips {
        if tipScores[tip.Hash].BlueWork >= threshold {
            bestTips = append(bestTips, tip)
        }
    }
    
    // Step 4: Apply deterministic tie-breaking
    if len(bestTips) > 1 {
        bestTips = ts.deterministicTieBreaking(bestTips, tipScores)
    }
    
    // Step 5: Validate selection
    if err := ts.validateTipSelection(bestTips); err != nil {
        return nil, err
    }
    
    ts.lastUpdate = time.Now()
    return bestTips, nil
}

// calculateCumulativeBlueWork computes total blue work with optimizations
func (ts *TipSelector) calculateCumulativeBlueWork(tip *Block, deadline time.Time) *TipScore {
    visited := make(map[Hash]bool)
    blueWork := uint64(0)
    blueBlockCount := 0
    redBlockCount := 0
    
    // Use iterative BFS instead of recursion for stack safety
    queue := [](*Block){tip}
    
    for len(queue) > 0 {
        // Check timeout
        if time.Now().After(deadline) {
            // Return partial result rather than error
            return &TipScore{
                BlueWork:       blueWork,
                BlueBlockCount: blueBlockCount,
                RedBlockCount:  redBlockCount,
                TipHash:        tip.Hash,
                Partial:        true,
                Timestamp:      time.Now(),
            }
        }
        
        // Process block
        block := queue[0]
        queue = queue[1:]
        
        if visited[block.Hash] {
            continue
        }
        visited[block.Hash] = true
        
        // GHOSTDAG blue/red classification
        if ts.isBlueBlock(block) {
            // Blue blocks contribute to security
            difficulty := ts.getEffectiveDifficulty(block)
            blueWork += difficulty
            blueBlockCount++
        } else {
            // Red blocks are included but don't add security
            redBlockCount++
        }
        
        // Add parents to queue
        for _, parentHash := range block.Parents {
            if parent := ts.dag.GetBlock(parentHash); parent != nil {
                if !visited[parentHash] {
                    queue = append(queue, parent)
                }
            }
        }
    }
    
    return &TipScore{
        BlueWork:       blueWork,
        BlueBlockCount: blueBlockCount,
        RedBlockCount:  redBlockCount,
        TipHash:        tip.Hash,
        Partial:        false,
        Timestamp:      time.Now(),
    }
}

// deterministicTieBreaking ensures consistent tip selection across nodes
func (ts *TipSelector) deterministicTieBreaking(tips []*Block, scores map[Hash]*TipScore) []*Block {
    // Multi-level deterministic sorting
    sort.SliceStable(tips, func(i, j int) bool {
        tipI, tipJ := tips[i], tips[j]
        scoreI, scoreJ := scores[tipI.Hash], scores[tipJ.Hash]
        
        // Level 1: Blue work (should be equal if we're here)
        if scoreI.BlueWork != scoreJ.BlueWork {
            return scoreI.BlueWork > scoreJ.BlueWork
        }
        
        // Level 2: Blue block count
        if scoreI.BlueBlockCount != scoreJ.BlueBlockCount {
            return scoreI.BlueBlockCount > scoreJ.BlueBlockCount
        }
        
        // Level 3: Timestamp (prefer newer)
        if tipI.Timestamp != tipJ.Timestamp {
            return tipI.Timestamp > tipJ.Timestamp
        }
        
        // Level 4: Hash comparison (lexicographic, big-endian)
        return bytes.Compare(tipI.Hash[:], tipJ.Hash[:]) < 0
    })
    
    // Return single best tip
    return tips[:1]
}
```

### 3.2 Canonical Ordering Algorithm

```go
// BuildCanonicalSequence creates deterministic linear ordering
func BuildCanonicalSequence(dag *BlockDAG, tipSet []*Block) ([]*Block, error) {
    builder := &CanonicalBuilder{
        dag:           dag,
        tipSet:        tipSet,
        blockIndex:    make(map[Hash]uint64),
        reverseIndex:  make(map[uint64]*Block),
    }
    
    // Step 1: Collect all blocks reachable from tips
    allBlocks, err := builder.collectReachableBlocks()
    if err != nil {
        return nil, fmt.Errorf("failed to collect blocks: %w", err)
    }
    
    // Step 2: Apply canonical sorting
    builder.sortBlocksCanonically(allBlocks)
    
    // Step 3: Ensure topological order (parents before children)
    canonical, err := builder.enforceTopologicalOrder(allBlocks)
    if err != nil {
        return nil, fmt.Errorf("topological sort failed: %w", err)
    }
    
    // Step 4: Assign canonical indices
    for i, block := range canonical {
        block.CanonicalIndex = uint64(i)
        builder.blockIndex[block.Hash] = uint64(i)
        builder.reverseIndex[uint64(i)] = block
    }
    
    // Step 5: Validate the sequence
    if err := builder.validateCanonicalSequence(canonical); err != nil {
        return nil, fmt.Errorf("validation failed: %w", err)
    }
    
    return canonical, nil
}

// sortBlocksCanonically implements deterministic multi-level sorting
func (cb *CanonicalBuilder) sortBlocksCanonically(blocks []*Block) {
    sort.SliceStable(blocks, func(i, j int) bool {
        blockI, blockJ := blocks[i], blocks[j]
        
        // Priority 1: Blue score (descending - higher is better)
        if blockI.BlueScore != blockJ.BlueScore {
            return blockI.BlueScore > blockJ.BlueScore
        }
        
        // Priority 2: Cumulative difficulty (descending)
        diffI := cb.getCumulativeDifficulty(blockI)
        diffJ := cb.getCumulativeDifficulty(blockJ)
        cmp := diffI.Cmp(diffJ)
        if cmp != 0 {
            return cmp > 0
        }
        
        // Priority 3: Timestamp (ascending - earlier first)
        // Prevents gaming by future-dating blocks
        if blockI.Timestamp != blockJ.Timestamp {
            return blockI.Timestamp < blockJ.Timestamp
        }
        
        // Priority 4: Parent count (ascending - simpler structure first)
        if len(blockI.Parents) != len(blockJ.Parents) {
            return len(blockI.Parents) < len(blockJ.Parents)
        }
        
        // Priority 5: Hash (lexicographic, big-endian)
        // Ensures global determinism
        return bytes.Compare(blockI.Hash[:], blockJ.Hash[:]) < 0
    })
}

// enforceTopologicalOrder ensures parent-child relationships
func (cb *CanonicalBuilder) enforceTopologicalOrder(blocks []*Block) ([]*Block, error) {
    // Build dependency graph
    graph := &TopologicalGraph{
        nodes:     make(map[Hash]*Block),
        inDegree:  make(map[Hash]int),
        outEdges:  make(map[Hash][]Hash),
    }
    
    // Initialize graph
    for _, block := range blocks {
        graph.nodes[block.Hash] = block
        graph.inDegree[block.Hash] = 0
    }
    
    // Calculate in-degrees
    for _, block := range blocks {
        for _, parentHash := range block.Parents {
            if _, exists := graph.nodes[parentHash]; exists {
                graph.outEdges[parentHash] = append(graph.outEdges[parentHash], block.Hash)
                graph.inDegree[block.Hash]++
            }
        }
    }
    
    // Kahn's algorithm with deterministic processing
    result := make([]*Block, 0, len(blocks))
    queue := cb.getZeroInDegreeNodes(graph)
    
    for len(queue) > 0 {
        // Sort queue for determinism
        cb.sortBlocksCanonically(queue)
        
        // Process next block
        current := queue[0]
        queue = queue[1:]
        result = append(result, current)
        
        // Update children
        for _, childHash := range graph.outEdges[current.Hash] {
            graph.inDegree[childHash]--
            if graph.inDegree[childHash] == 0 {
                child := graph.nodes[childHash]
                queue = append(queue, child)
            }
        }
    }
    
    // Check for cycles
    if len(result) != len(blocks) {
        return nil, cb.detectCycle(graph)
    }
    
    return result, nil
}
```

---

## 4. State Management Architecture

### 4.1 State Transition System

```go
package state

import (
    "sync"
    "time"
    "github.com/ethereum/go-ethereum/common"
    "github.com/ethereum/go-ethereum/core/state"
)

// StateManager handles EVM state during DAG operations
type StateManager struct {
    mu                sync.RWMutex
    currentState      *state.StateDB
    checkpoints       map[uint64]*StateCheckpoint
    pendingCheckpoint *StateCheckpoint
    pruneThreshold    uint64
    cacheSize         int
    
    // Performance metrics
    metrics           *StateMetrics
}

// StateCheckpoint represents a restorable state point
type StateCheckpoint struct {
    BlockNumber    uint64
    BlockHash      common.Hash
    StateRoot      common.Hash
    Timestamp      time.Time
    CompressedData []byte
    Size           uint64
    
    // Validation
    Signature      []byte
    ValidatorSet   []common.Address
}

// ExecuteCanonicalBlock processes a block in canonical order
func (sm *StateManager) ExecuteCanonicalBlock(block *Block, vmConfig vm.Config) (*ExecutionResult, error) {
    sm.mu.Lock()
    defer sm.mu.Unlock()
    
    startTime := time.Now()
    
    // Create execution context
    context := &ExecutionContext{
        Block:        block,
        State:        sm.currentState,
        VMConfig:     vmConfig,
        GasPool:      new(GasPool).AddGas(block.GasLimit),
        UsedGas:      uint64(0),
        Receipts:     make([]*Receipt, 0),
        Logs:         make([]*Log, 0),
    }
    
    // Pre-execution validation
    if err := sm.preExecuteValidation(context); err != nil {
        return nil, fmt.Errorf("pre-execution validation failed: %w", err)
    }
    
    // Order transactions within block
    orderedTxs := sm.orderTransactions(block.Transactions)
    
    // Execute transactions
    for i, tx := range orderedTxs {
        receipt, err := sm.executeTransaction(context, tx, i)
        if err != nil {
            // Transaction failure handling
            if IsConsensusError(err) {
                // Consensus errors abort block
                return nil, fmt.Errorf("consensus error in tx %d: %w", i, err)
            }
            // Regular errors create failed receipt
            receipt = sm.createFailedReceipt(tx, err)
        }
        
        context.Receipts = append(context.Receipts, receipt)
        context.Logs = append(context.Logs, receipt.Logs...)
    }
    
    // Post-execution processing
    if err := sm.postExecuteProcessing(context); err != nil {
        return nil, fmt.Errorf("post-execution processing failed: %w", err)
    }
    
    // Update metrics
    sm.metrics.RecordExecution(time.Since(startTime), len(orderedTxs), context.UsedGas)
    
    return &ExecutionResult{
        StateRoot:   sm.currentState.IntermediateRoot(),
        Receipts:    context.Receipts,
        Logs:        context.Logs,
        GasUsed:     context.UsedGas,
        Bloom:       CreateBloom(context.Logs),
    }, nil
}

// executeTransaction processes a single transaction
func (sm *StateManager) executeTransaction(ctx *ExecutionContext, tx *Transaction, index int) (*Receipt, error) {
    // Prepare message
    msg, err := TransactionToMessage(tx, ctx.Block.BaseFee)
    if err != nil {
        return nil, err
    }
    
    // Snapshot state for potential revert
    snapshot := ctx.State.Snapshot()
    
    // Create EVM instance
    txContext := vm.TxContext{
        Origin:   msg.From,
        GasPrice: msg.GasPrice,
    }
    
    blockContext := MapToEVMBlockContext(ctx.Block)
    evm := vm.NewEVM(blockContext, txContext, ctx.State, ctx.VMConfig)
    
    // Execute transaction
    result, err := ApplyMessage(evm, msg, ctx.GasPool)
    if err != nil {
        ctx.State.RevertToSnapshot(snapshot)
        return nil, err
    }
    
    // Update gas used
    ctx.UsedGas += result.UsedGas
    
    // Create receipt
    receipt := &Receipt{
        Type:              tx.Type(),
        PostState:         ctx.State.IntermediateRoot().Bytes(),
        CumulativeGasUsed: ctx.UsedGas,
        Bloom:             CreateBloom(result.Logs),
        Logs:              result.Logs,
        TxHash:            tx.Hash,
        ContractAddress:   result.ContractAddress,
        GasUsed:           result.UsedGas,
        
        // Canonical position
        BlockHash:         ctx.Block.Hash,
        BlockNumber:       big.NewInt(int64(ctx.Block.CanonicalIndex)),
        TransactionIndex:  uint(index),
    }
    
    // Set status
    if result.Failed() {
        receipt.Status = ReceiptStatusFailed
    } else {
        receipt.Status = ReceiptStatusSuccessful
    }
    
    return receipt, nil
}
```

### 4.2 Checkpoint Management

```go
// CheckpointManager handles state persistence
type CheckpointManager struct {
    storage        CheckpointStorage
    compression    CompressionEngine
    validator      CheckpointValidator
    
    // Configuration
    interval       uint64  // Blocks between checkpoints
    maxCheckpoints uint64  // Maximum stored checkpoints
    pruneAge       time.Duration
}

// CreateCheckpoint saves current state
func (cm *CheckpointManager) CreateCheckpoint(state *StateDB, block *Block) error {
    // Only checkpoint at intervals
    if block.CanonicalIndex % cm.interval != 0 {
        return nil
    }
    
    checkpoint := &StateCheckpoint{
        BlockNumber: block.CanonicalIndex,
        BlockHash:   block.Hash,
        StateRoot:   state.IntermediateRoot(),
        Timestamp:   time.Now(),
    }
    
    // Dump state with optimization flags
    stateData, err := state.DumpWithOptions(DumpOptions{
        OnlyWithAddresses: true,
        IncludeCode:       true,
        IncludeStorage:    true,
        MaxCodeSize:       24576,
    })
    if err != nil {
        return fmt.Errorf("state dump failed: %w", err)
    }
    
    // Compress state data
    compressed, err := cm.compression.Compress(stateData)
    if err != nil {
        return fmt.Errorf("compression failed: %w", err)
    }
    checkpoint.CompressedData = compressed
    checkpoint.Size = uint64(len(compressed))
    
    // Generate validation signature
    checkpoint.Signature = cm.validator.Sign(checkpoint)
    
    // Store checkpoint
    if err := cm.storage.Store(checkpoint); err != nil {
        return fmt.Errorf("storage failed: %w", err)
    }
    
    // Prune old checkpoints
    if err := cm.pruneOldCheckpoints(); err != nil {
        // Log but don't fail
        log.Warn("Checkpoint pruning failed", "error", err)
    }
    
    return nil
}

// RestoreCheckpoint loads state from checkpoint
func (cm *CheckpointManager) RestoreCheckpoint(blockNumber uint64) (*StateDB, error) {
    // Find nearest checkpoint
    checkpoint, err := cm.storage.GetNearestCheckpoint(blockNumber)
    if err != nil {
        return nil, fmt.Errorf("checkpoint not found: %w", err)
    }
    
    // Validate checkpoint
    if err := cm.validator.Validate(checkpoint); err != nil {
        return nil, fmt.Errorf("checkpoint validation failed: %w", err)
    }
    
    // Decompress state data
    stateData, err := cm.compression.Decompress(checkpoint.CompressedData)
    if err != nil {
        return nil, fmt.Errorf("decompression failed: %w", err)
    }
    
    // Reconstruct state
    state, err := LoadStateFromDump(stateData)
    if err != nil {
        return nil, fmt.Errorf("state load failed: %w", err)
    }
    
    return state, nil
}
```

---

## 5. Transaction Ordering & Execution

### 5.1 Intra-Block Ordering

```go
// TransactionOrderer handles deterministic tx ordering
type TransactionOrderer struct {
    priorityCalculator PriorityCalculator
    nonceTracker      *NonceTracker
}

// OrderTransactions deterministically orders transactions within a block
func (to *TransactionOrderer) OrderTransactions(txs []*Transaction, state *StateDB) ([]*Transaction, error) {
    // Create working copy
    ordered := make([]*Transaction, len(txs))
    copy(ordered, txs)
    
    // Group by sender
    txBySender := make(map[common.Address][]*Transaction)
    for _, tx := range ordered {
        from, err := tx.Sender()
        if err != nil {
            return nil, fmt.Errorf("invalid signature: %w", err)
        }
        txBySender[from] = append(txBySender[from], tx)
    }
    
    // Sort each sender's transactions by nonce
    for sender, senderTxs := range txBySender {
        sort.Slice(senderTxs, func(i, j int) bool {
            return senderTxs[i].Nonce < senderTxs[j].Nonce
        })
        
        // Validate nonce sequence
        expectedNonce := state.GetNonce(sender)
        for _, tx := range senderTxs {
            if tx.Nonce != expectedNonce {
                return nil, ErrNonceGap{
                    Address:  sender,
                    Expected: expectedNonce,
                    Got:      tx.Nonce,
                }
            }
            expectedNonce++
        }
    }
    
    // Global ordering with priority
    result := make([]*Transaction, 0, len(ordered))
    
    // Process high-priority transactions first
    priorities := to.calculatePriorities(ordered)
    sort.Slice(ordered, func(i, j int) bool {
        // Different senders: sort by priority
        fromI, _ := ordered[i].Sender()
        fromJ, _ := ordered[j].Sender()
        
        if fromI != fromJ {
            // Priority 1: Effective gas price (for MEV protection)
            priceI := priorities[ordered[i].Hash].EffectiveGasPrice
            priceJ := priorities[ordered[j].Hash].EffectiveGasPrice
            if cmp := priceI.Cmp(priceJ); cmp != 0 {
                return cmp > 0 // Higher price first
            }
            
            // Priority 2: Nonce (lower nonce = older tx)
            if ordered[i].Nonce != ordered[j].Nonce {
                return ordered[i].Nonce < ordered[j].Nonce
            }
        }
        
        // Same sender: maintain nonce order
        if fromI == fromJ {
            return ordered[i].Nonce < ordered[j].Nonce
        }
        
        // Final tie-breaker: hash
        return bytes.Compare(ordered[i].Hash[:], ordered[j].Hash[:]) < 0
    })
    
    return ordered, nil
}
```

### 5.2 Cross-Block Transaction Handling

```go
// CrossBlockTransactionHandler manages tx across DAG blocks
type CrossBlockTransactionHandler struct {
    txPool         *TxPool
    conflictCache  *ConflictCache
    mempoolBuffer  *MempoolBuffer
}

// HandleCrossingTransactions processes conflicting txs in parallel blocks
func (cbth *CrossBlockTransactionHandler) HandleCrossingTransactions(
    parallelBlocks []*Block,
    canonical []*Block,
) (*ConflictResolution, error) {
    
    resolution := &ConflictResolution{
        ValidTxs:      make([]*Transaction, 0),
        ConflictedTxs: make([]*Transaction, 0),
        RefundedTxs:   make([]*Transaction, 0),
    }
    
    // Build nonce usage map across all parallel blocks
    nonceUsage := make(map[common.Address]map[uint64][]*TxLocation)
    
    for _, block := range parallelBlocks {
        for txIndex, tx := range block.Transactions {
            from, _ := tx.Sender()
            if nonceUsage[from] == nil {
                nonceUsage[from] = make(map[uint64][]*TxLocation)
            }
            
            location := &TxLocation{
                Block:      block,
                TxIndex:    txIndex,
                Transaction: tx,
            }
            nonceUsage[from][tx.Nonce] = append(nonceUsage[from][tx.Nonce], location)
        }
    }
    
    // Resolve conflicts based on canonical ordering
    canonicalIndex := make(map[Hash]int)
    for i, block := range canonical {
        canonicalIndex[block.Hash] = i
    }
    
    for sender, nonceMap := range nonceUsage {
        for nonce, locations := range nonceMap {
            if len(locations) == 1 {
                // No conflict
                resolution.ValidTxs = append(resolution.ValidTxs, locations[0].Transaction)
            } else {
                // Conflict: select based on canonical order
                sort.Slice(locations, func(i, j int) bool {
                    idxI := canonicalIndex[locations[i].Block.Hash]
                    idxJ := canonicalIndex[locations[j].Block.Hash]
                    if idxI != idxJ {
                        return idxI < idxJ
                    }
                    // Same block: use transaction index
                    return locations[i].TxIndex < locations[j].TxIndex
                })
                
                // First is valid, rest are conflicts
                resolution.ValidTxs = append(resolution.ValidTxs, locations[0].Transaction)
                for i := 1; i < len(locations); i++ {
                    resolution.ConflictedTxs = append(resolution.ConflictedTxs, locations[i].Transaction)
                }
            }
        }
    }
    
    return resolution, nil
}
```

---

## 6. EVM Context Mapping

### 6.1 Block Context Translation

```go
// EVMContextMapper translates DAG context to EVM context
type EVMContextMapper struct {
    canonical         []*Block
    difficultyScaler  DifficultyScaler
    randomnessDeriver RandomnessDeriver
    coinbaseSelector  CoinbaseSelector
}

// MapToEVMBlockContext creates EVM execution context
func (ecm *EVMContextMapper) MapToEVMBlockContext(block *Block) *vm.BlockContext {
    return &vm.BlockContext{
        // Standard mappings
        CanTransfer: CanTransfer,
        Transfer:    Transfer,
        GetHash:     ecm.createHashLookup(block),
        
        // Block information
        Coinbase:    ecm.selectCoinbase(block),
        GasLimit:    block.GasLimit,
        BlockNumber: big.NewInt(int64(block.CanonicalIndex)),
        Time:        big.NewInt(block.Timestamp),
        Difficulty:  ecm.normalizeDifficulty(block),
        BaseFee:     ecm.calculateBaseFee(block),
        Random:      ecm.deriveRandomness(block),
        
        // DAG-specific context
        ExtraContext: &DAGContext{
            BlueScore:       block.BlueScore,
            BlueWork:        block.BlueWork,
            Algorithm:       block.Algorithm,
            ParentHashes:    block.Parents,
            IsBlueBlock:     block.IsBlue,
            RedScore:        block.RedScore,
            DAGSize:         ecm.getDAGSize(block),
        },
    }
}

// createHashLookup provides BLOCKHASH opcode functionality
func (ecm *EVMContextMapper) createHashLookup(current *Block) vm.GetHashFunc {
    return func(n uint64) common.Hash {
        // Cannot look up future blocks
        if n >= current.CanonicalIndex {
            return common.Hash{}
        }
        
        // EVM limit: last 256 blocks only
        if current.CanonicalIndex-n > 256 {
            return common.Hash{}
        }
        
        // Return canonical block at index n
        if block := ecm.canonical[n]; block != nil {
            return block.Hash
        }
        
        return common.Hash{}
    }
}

// selectCoinbase determines block beneficiary
func (ecm *EVMContextMapper) selectCoinbase(block *Block) common.Address {
    return ecm.coinbaseSelector.Select(CoinbaseContext{
        Block:        block,
        Algorithm:    block.Algorithm,
        ParentCount:  len(block.Parents),
        BlueScore:    block.BlueScore,
        Canonical:    ecm.canonical,
    })
}

// normalizeDifficulty handles dual-algo difficulty
func (ecm *EVMContextMapper) normalizeDifficulty(block *Block) *big.Int {
    return ecm.difficultyScaler.Normalize(
        block.Difficulty,
        block.Algorithm,
        block.BlueScore,
    )
}

// deriveRandomness provides PREVRANDAO value
func (ecm *EVMContextMapper) deriveRandomness(block *Block) *common.Hash {
    if block.CanonicalIndex < 2 {
        return &common.Hash{} // No randomness for genesis/first block
    }
    
    // Derive from previous two blocks for unpredictability
    prev1 := ecm.canonical[block.CanonicalIndex-1]
    prev2 := ecm.canonical[block.CanonicalIndex-2]
    
    data := append(prev1.Hash[:], prev2.Hash[:]...)
    data = append(data, block.Parents[0][:]...) // Include DAG structure
    
    hash := crypto.Keccak256Hash(data)
    return &hash
}
```

### 6.2 Opcode Implementations

```go
// DAGAwareOpcodes extends standard EVM opcodes
type DAGAwareOpcodes struct {
    interpreter *vm.EVMInterpreter
    dagContext  *DAGContext
}

// Custom Phoenix opcodes for DAG awareness
const (
    OPCODE_BLUESCORE   = 0xb0  // Get blue score of current block
    OPCODE_BLUEWORK    = 0xb1  // Get cumulative blue work
    OPCODE_PARENTCOUNT = 0xb2  // Number of parents
    OPCODE_PARENTHASH  = 0xb3  // Get specific parent hash
    OPCODE_ALGORITHM   = 0xb4  // Mining algorithm used
    OPCODE_ISBLUE      = 0xb5  // Is current block blue
    OPCODE_DAGSIZE     = 0xb6  // Current DAG size
)

// ExecuteDAGOpcode handles Phoenix-specific opcodes
func (dao *DAGAwareOpcodes) ExecuteDAGOpcode(
    pc *uint64,
    interpreter *vm.EVMInterpreter,
    scope *vm.ScopeContext,
) ([]byte, error) {
    
    op := scope.Contract.GetOp(*pc)
    stack := scope.Stack
    
    switch op {
    case OPCODE_BLUESCORE:
        score := new(big.Int).SetUint64(dao.dagContext.BlueScore)
        stack.Push(score)
        
    case OPCODE_BLUEWORK:
        work := new(big.Int).SetUint64(dao.dagContext.BlueWork)
        stack.Push(work)
        
    case OPCODE_PARENTCOUNT:
        count := new(big.Int).SetInt64(int64(len(dao.dagContext.ParentHashes)))
        stack.Push(count)
        
    case OPCODE_PARENTHASH:
        index := stack.Pop()
        if index.Uint64() >= uint64(len(dao.dagContext.ParentHashes)) {
            stack.Push(new(big.Int))
        } else {
            hash := dao.dagContext.ParentHashes[index.Uint64()]
            stack.Push(new(big.Int).SetBytes(hash[:]))
        }
        
    case OPCODE_ALGORITHM:
        algo := new(big.Int)
        switch dao.dagContext.Algorithm {
        case AlgoKHeavyHash:
            algo.SetInt64(0)
        case AlgoSHA3:
            algo.SetInt64(1)
        }
        stack.Push(algo)
        
    case OPCODE_ISBLUE:
        isBlue := new(big.Int)
        if dao.dagContext.IsBlueBlock {
            isBlue.SetInt64(1)
        }
        stack.Push(isBlue)
        
    case OPCODE_DAGSIZE:
        size := new(big.Int).SetUint64(dao.dagContext.DAGSize)
        stack.Push(size)
        
    default:
        return nil, ErrInvalidDAGOpcode
    }
    
    return nil, nil
}
```

---

## 7. Reorganization Handling

### 7.1 Reorg Detection and Processing

```go
// ReorgHandler manages chain reorganizations
type ReorgHandler struct {
    stateManager     *StateManager
    txPool          *TxPool
    receiptStore    *ReceiptStore
    logIndexer      *LogIndexer
    
    // Configuration
    maxReorgDepth   uint64
    maxReplayTime   time.Duration
    
    // Metrics
    metrics         *ReorgMetrics
}

// HandleReorg processes a detected reorganization
func (rh *ReorgHandler) HandleReorg(
    oldCanonical []*Block,
    newCanonical []*Block,
) (*ReorgResult, error) {
    
    startTime := time.Now()
    
    // Step 1: Find fork point
    forkPoint, oldBranch, newBranch := rh.findForkPoint(oldCanonical, newCanonical)
    
    // Step 2: Validate reorg depth
    if len(oldBranch) > int(rh.maxReorgDepth) {
        return nil, ErrReorgTooDeep{
            RequestedDepth: len(oldBranch),
            MaxDepth:       rh.maxReorgDepth,
            ForkPoint:      forkPoint,
        }
    }
    
    // Step 3: Create reorg context
    ctx := &ReorgContext{
        ForkPoint:      forkPoint,
        OldBranch:      oldBranch,
        NewBranch:      newBranch,
        StartTime:      startTime,
        Deadline:       startTime.Add(rh.maxReplayTime),
        OrphanedTxs:    make([]*Transaction, 0),
        ReplayedBlocks: make([]*Block, 0),
    }
    
    // Step 4: Execute reorg with rollback protection
    result, err := rh.executeReorgWithRollback(ctx)
    if err != nil {
        // Attempt recovery
        if recoveryErr := rh.recoverFromFailedReorg(ctx); recoveryErr != nil {
            // Critical failure
            return nil, ErrCriticalReorgFailure{
                OriginalError:  err,
                RecoveryError:  recoveryErr,
                ForkPoint:      forkPoint,
            }
        }
        return nil, err
    }
    
    // Step 5: Update metrics
    rh.metrics.RecordReorg(
        len(oldBranch),
        len(newBranch),
        time.Since(startTime),
        len(result.OrphanedTxs),
    )
    
    return result, nil
}

// executeReorgWithRollback performs the actual reorg
func (rh *ReorgHandler) executeReorgWithRollback(ctx *ReorgContext) (*ReorgResult, error) {
    // Create checkpoint for rollback
    checkpoint, err := rh.stateManager.CreateCheckpoint()
    if err != nil {
        return nil, fmt.Errorf("checkpoint creation failed: %w", err)
    }
    
    // Phase 1: Unwind old branch
    for i := len(ctx.OldBranch) - 1; i >= 0; i-- {
        if time.Now().After(ctx.Deadline) {
            return nil, ErrReorgTimeout
        }
        
        block := ctx.OldBranch[i]
        
        // Extract transactions for potential replay
        ctx.OrphanedTxs = append(ctx.OrphanedTxs, block.Transactions...)
        
        // Revert state changes
        if err := rh.stateManager.RevertBlock(block); err != nil {
            rh.stateManager.RestoreCheckpoint(checkpoint)
            return nil, fmt.Errorf("failed to revert block %s: %w", block.Hash, err)
        }
        
        // Clear receipts and logs
        rh.receiptStore.DeleteBlockReceipts(block.Hash)
        rh.logIndexer.RemoveBlockLogs(block.Hash)
    }
    
    // Phase 2: Apply new branch
    for _, block := range ctx.NewBranch {
        if time.Now().After(ctx.Deadline) {
            rh.stateManager.RestoreCheckpoint(checkpoint)
            return nil, ErrReorgTimeout
        }
        
        // Execute block
        result, err := rh.stateManager.ExecuteCanonicalBlock(block, vm.Config{})
        if err != nil {
            rh.stateManager.RestoreCheckpoint(checkpoint)
            return nil, fmt.Errorf("failed to execute block %s: %w", block.Hash, err)
        }
        
        // Store receipts
        rh.receiptStore.StoreBlockReceipts(block.Hash, result.Receipts)
        
        // Index logs
        rh.logIndexer.IndexBlockLogs(block, result.Logs)
        
        ctx.ReplayedBlocks = append(ctx.ReplayedBlocks, block)
    }
    
    // Phase 3: Handle orphaned transactions
    reinjected := rh.reinjectOrphanedTransactions(ctx.OrphanedTxs, ctx.NewBranch)
    
    return &ReorgResult{
        ForkPoint:          ctx.ForkPoint,
        OldBranchDepth:     len(ctx.OldBranch),
        NewBranchLength:    len(ctx.NewBranch),
        OrphanedTxs:        ctx.OrphanedTxs,
        ReinjectedTxs:      reinjected,
        ExecutionTime:      time.Since(ctx.StartTime),
    }, nil
}
```

### 7.2 Fork Point Detection

```go
// findForkPoint identifies where chains diverge
func (rh *ReorgHandler) findForkPoint(
    oldChain []*Block,
    newChain []*Block,
) (*Block, []*Block, []*Block) {
    
    // Find common ancestor using binary search for efficiency
    minLen := len(oldChain)
    if len(newChain) < minLen {
        minLen = len(newChain)
    }
    
    // Binary search for fork point
    left, right := 0, minLen-1
    forkIndex := -1
    
    for left <= right {
        mid := (left + right) / 2
        
        if oldChain[mid].Hash == newChain[mid].Hash {
            forkIndex = mid
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    
    if forkIndex == -1 {
        // No common ancestor in range
        return nil, oldChain, newChain
    }
    
    forkPoint := oldChain[forkIndex]
    oldBranch := oldChain[forkIndex+1:]
    newBranch := newChain[forkIndex+1:]
    
    return forkPoint, oldBranch, newBranch
}
```

---

## 8. Gas Economics & Fee Model

### 8.1 Dynamic Base Fee Calculation

```go
// GasOracle manages gas pricing in DAG context
type GasOracle struct {
    params           *GasParams
    history          *GasHistory
    dagAnalyzer      *DAGAnalyzer
}

// GasParams defines gas configuration
type GasParams struct {
    InitialBaseFee           *big.Int
    MinBaseFee              *big.Int
    MaxBaseFee              *big.Int
    BaseFeeChangeDenominator uint64
    ElasticityMultiplier    uint64
    TargetGasUsed           uint64
    BlockGasLimit           uint64
    
    // DAG-specific parameters
    ParallelBlockWeight     float64  // Weight for parallel block gas usage
    CongestionThreshold     float64  // Network congestion indicator
}

// CalculateBaseFee implements EIP-1559 adapted for DAG
func (go *GasOracle) CalculateBaseFee(canonical []*Block, currentIndex uint64) *big.Int {
    if currentIndex == 0 {
        return go.params.InitialBaseFee
    }
    
    // Get recent block window
    windowSize := uint64(10)
    if currentIndex < windowSize {
        windowSize = currentIndex
    }
    
    startIdx := currentIndex - windowSize
    recentBlocks := canonical[startIdx:currentIndex]
    
    // Calculate weighted gas usage
    weightedGasUsed := go.calculateWeightedGasUsage(recentBlocks)
    targetGasUsed := go.params.TargetGasUsed * windowSize
    
    // Get parent base fee
    parent := canonical[currentIndex-1]
    parentBaseFee := parent.BaseFee
    if parentBaseFee == nil {
        parentBaseFee = go.params.InitialBaseFee
    }
    
    // EIP-1559 formula with DAG adjustments
    var newBaseFee *big.Int
    
    if weightedGasUsed > targetGasUsed {
        // Increase base fee
        gasUsedDelta := weightedGasUsed - targetGasUsed
        baseFeeDelta := new(big.Int).Mul(
            parentBaseFee,
            new(big.Int).SetUint64(gasUsedDelta),
        )
        baseFeeDelta.Div(baseFeeDelta, new(big.Int).SetUint64(targetGasUsed))
        baseFeeDelta.Div(baseFeeDelta, new(big.Int).SetUint64(go.params.BaseFeeChangeDenominator))
        
        newBaseFee = new(big.Int).Add(parentBaseFee, baseFeeDelta)
    } else {
        // Decrease base fee
        gasUsedDelta := targetGasUsed - weightedGasUsed
        baseFeeDelta := new(big.Int).Mul(
            parentBaseFee,
            new(big.Int).SetUint64(gasUsedDelta),
        )
        baseFeeDelta.Div(baseFeeDelta, new(big.Int).SetUint64(targetGasUsed))
        baseFeeDelta.Div(baseFeeDelta, new(big.Int).SetUint64(go.params.BaseFeeChangeDenominator))
        
        newBaseFee = new(big.Int).Sub(parentBaseFee, baseFeeDelta)
    }
    
    // Apply bounds
    if newBaseFee.Cmp(go.params.MinBaseFee) < 0 {
        newBaseFee = new(big.Int).Set(go.params.MinBaseFee)
    }
    if newBaseFee.Cmp(go.params.MaxBaseFee) > 0 {
        newBaseFee = new(big.Int).Set(go.params.MaxBaseFee)
    }
    
    // Apply congestion multiplier if needed
    congestion := go.dagAnalyzer.GetCongestionLevel(canonical, currentIndex)
    if congestion > go.params.CongestionThreshold {
        multiplier := big.NewFloat(1.0 + (congestion - go.params.CongestionThreshold))
        adjustedFee := new(big.Float).SetInt(newBaseFee)
        adjustedFee.Mul(adjustedFee, multiplier)
        adjustedFee.Int(newBaseFee)
    }
    
    return newBaseFee
}

// calculateWeightedGasUsage accounts for parallel blocks
func (go *GasOracle) calculateWeightedGasUsage(blocks []*Block) uint64 {
    totalGasUsed := uint64(0)
    
    for _, block := range blocks {
        gasUsed := block.GasUsed
        
        // Apply weight based on block parallelism
        if len(block.Parents) > 1 {
            // Parallel block - reduce weight
            weight := 1.0 - (go.params.ParallelBlockWeight * float64(len(block.Parents)-1))
            if weight < 0.5 {
                weight = 0.5 // Minimum weight
            }
            gasUsed = uint64(float64(gasUsed) * weight)
        }
        
        totalGasUsed += gasUsed
    }
    
    return totalGasUsed
}
```

### 8.2 Transaction Fee Distribution

```go
// FeeDistributor handles fee allocation in DAG
type FeeDistributor struct {
    rewardPolicy    RewardPolicy
    burnRate       *big.Int  // EIP-1559 burn percentage
}

// DistributeFees allocates transaction fees
func (fd *FeeDistributor) DistributeFees(
    block *Block,
    receipts []*Receipt,
    state *StateDB,
) error {
    
    totalBaseFee := new(big.Int)
    totalPriorityFee := new(big.Int)
    
    for _, receipt := range receipts {
        tx := receipt.Transaction
        
        // Calculate fees
        baseFee := new(big.Int).Mul(
            block.BaseFee,
            new(big.Int).SetUint64(receipt.GasUsed),
        )
        
        effectiveGasPrice := tx.GasPrice
        if tx.Type() == TxTypeEIP1559 {
            effectiveGasPrice = new(big.Int).Add(block.BaseFee, tx.GasTipCap)
            if effectiveGasPrice.Cmp(tx.GasFeeCap) > 0 {
                effectiveGasPrice = tx.GasFeeCap
            }
        }
        
        priorityFee := new(big.Int).Sub(effectiveGasPrice, block.BaseFee)
        priorityFee.Mul(priorityFee, new(big.Int).SetUint64(receipt.GasUsed))
        
        totalBaseFee.Add(totalBaseFee, baseFee)
        totalPriorityFee.Add(totalPriorityFee, priorityFee)
    }
    
    // Burn base fee (EIP-1559)
    if fd.burnRate.Sign() > 0 {
        burnAmount := new(big.Int).Mul(totalBaseFee, fd.burnRate)
        burnAmount.Div(burnAmount, big.NewInt(100))
        
        // Send to burn address or reduce supply
        state.SubBalance(BurnAddress, burnAmount)
    }
    
    // Distribute priority fees to miners
    if totalPriorityFee.Sign() > 0 {
        minerReward := fd.rewardPolicy.CalculateMinerReward(
            block,
            totalPriorityFee,
        )
        
        state.AddBalance(block.Coinbase, minerReward)
        
        // Distribute remainder to validators/stakers if applicable
        remainder := new(big.Int).Sub(totalPriorityFee, minerReward)
        if remainder.Sign() > 0 {
            fd.distributeToValidators(remainder, state)
        }
    }
    
    return nil
}
```

---

## 9. Cross-Block References

### 9.1 Parent Selection Strategy

```go
// ParentSelector manages parent selection for new blocks
type ParentSelector struct {
    dag              *BlockDAG
    maxParents       int
    selectionPolicy  SelectionPolicy
}

// SelectParents chooses optimal parents for new block
func (ps *ParentSelector) SelectParents() ([]common.Hash, error) {
    tips := ps.dag.GetCurrentTips()
    
    if len(tips) == 0 {
        return nil, ErrNoAvailableParents
    }
    
    // Apply selection policy
    selectedParents := ps.selectionPolicy.Select(SelectionContext{
        Tips:           tips,
        MaxParents:     ps.maxParents,
        DAGState:       ps.dag.GetState(),
        NetworkLatency: ps.getNetworkLatency(),
    })
    
    // Validate selection
    if err := ps.validateParentSelection(selectedParents); err != nil {
        return nil, err
    }
    
    // Convert to hashes
    parentHashes := make([]common.Hash, len(selectedParents))
    for i, parent := range selectedParents {
        parentHashes[i] = parent.Hash
    }
    
    return parentHashes, nil
}

// GreedySelectionPolicy selects highest scoring parents
type GreedySelectionPolicy struct{}

func (gsp *GreedySelectionPolicy) Select(ctx SelectionContext) []*Block {
    // Sort tips by blue score
    sort.Slice(ctx.Tips, func(i, j int) bool {
        return ctx.Tips[i].BlueScore > ctx.Tips[j].BlueScore
    })
    
    // Select up to maxParents
    numParents := len(ctx.Tips)
    if numParents > ctx.MaxParents {
        numParents = ctx.MaxParents
    }
    
    return ctx.Tips[:numParents]
}
```

### 9.2 Uncle/Ommer Handling

```go
// UncleManager handles uncle blocks in DAG context
type UncleManager struct {
    maxUncleDepth   uint64
    maxUncles       int
    rewardCalculator UncleRewardCalculator
}

// IncludeUncles selects uncle blocks for inclusion
func (um *UncleManager) IncludeUncles(
    block *Block,
    canonical []*Block,
) ([]*Uncle, error) {
    
    uncles := make([]*Uncle, 0, um.maxUncles)
    
    // Find potential uncle blocks (not in canonical chain)
    potentialUncles := um.findPotentialUncles(block, canonical)
    
    // Score and sort uncles
    sort.Slice(potentialUncles, func(i, j int) bool {
        scoreI := um.scoreUncle(potentialUncles[i], block)
        scoreJ := um.scoreUncle(potentialUncles[j], block)
        return scoreI > scoreJ
    })
    
    // Select best uncles up to limit
    for i := 0; i < len(potentialUncles) && i < um.maxUncles; i++ {
        uncle := potentialUncles[i]
        
        // Validate uncle
        if err := um.validateUncle(uncle, block, canonical); err != nil {
            continue
        }
        
        uncles = append(uncles, &Uncle{
            Block:  uncle,
            Reward: um.rewardCalculator.Calculate(uncle, block),
        })
    }
    
    return uncles, nil
}
```

---

## 10. Performance Specifications

### 10.1 Performance Targets

| Metric | Target | Maximum | Critical |
|--------|--------|---------|----------|
| Block Processing | <100ms | 500ms | 1000ms |
| State Transition | <50ms | 200ms | 500ms |
| Canonicalization | <10ms | 50ms | 100ms |
| Reorg (100 blocks) | <5s | 10s | 30s |
| Checkpoint Creation | <1s | 5s | 10s |
| Checkpoint Restore | <2s | 10s | 20s |
| Transaction Ordering | <5ms | 20ms | 50ms |
| EVM Execution/tx | <1ms | 5ms | 10ms |

### 10.2 Optimization Strategies

```go
// PerformanceOptimizer manages system optimizations
type PerformanceOptimizer struct {
    cacheManager     *CacheManager
    parallelizer     *Parallelizer
    precomputer      *Precomputer
}

// OptimizationConfig defines performance parameters
type OptimizationConfig struct {
    // Caching
    StateCacheSize       int     // MB
    BlockCacheSize       int     // Number of blocks
    ReceiptCacheSize     int     // Number of receipts
    CodeCacheSize        int     // MB
    
    // Parallelization
    ValidationWorkers    int     // Parallel validation threads
    ExecutionWorkers     int     // Parallel execution threads
    IndexingWorkers      int     // Parallel indexing threads
    
    // Precomputation
    PrecomputeDepth      int     // Blocks to precompute
    PrecomputeStateRoot  bool    // Precompute state roots
    PrecomputeReceipts   bool    // Precompute receipts
    
    // Batching
    StateBatchSize       int     // State operations per batch
    DBWriteBatchSize     int     // Database writes per batch
    
    // Memory Management
    MaxMemoryUsage       int64   // Maximum memory in bytes
    GCTriggerThreshold   float64 // Trigger GC at % memory
}

// Production configuration
var ProductionOptimization = OptimizationConfig{
    // Caching
    StateCacheSize:      512,    // 512 MB state cache
    BlockCacheSize:      10000,  // 10k blocks in memory
    ReceiptCacheSize:    50000,  // 50k receipts cached
    CodeCacheSize:       256,    // 256 MB code cache
    
    // Parallelization
    ValidationWorkers:   8,       // 8 parallel validators
    ExecutionWorkers:    4,       // 4 parallel executors
    IndexingWorkers:     4,       // 4 parallel indexers
    
    // Precomputation
    PrecomputeDepth:     10,      // Precompute 10 blocks ahead
    PrecomputeStateRoot: true,    // Precompute roots
    PrecomputeReceipts:  true,    // Precompute receipts
    
    // Batching
    StateBatchSize:      1000,    // 1000 operations per batch
    DBWriteBatchSize:    5000,    // 5000 writes per batch
    
    // Memory Management
    MaxMemoryUsage:      8 << 30, // 8 GB maximum
    GCTriggerThreshold:  0.8,     // GC at 80% memory
}
```

---

## 11. Security Considerations

### 11.1 Attack Vectors and Mitigations

| Attack Vector | Description | Mitigation |
|---------------|-------------|------------|
| Timestamp Manipulation | Miners manipulate block timestamps | Median time rule + bounds checking |
| Blue Score Gaming | Manipulate blue scores for advantage | Multiple validation + deterministic scoring |
| Reorg Attacks | Deep reorganizations | Maximum reorg depth + checkpoints |
| State Explosion | Excessive state growth | State pruning + rent mechanisms |
| Gas Price Manipulation | Manipulate base fee calculation | Weighted averaging + bounds |
| Parent Selection Attack | Choose malicious parents | Parent validation + scoring |
| Parallel Block Conflicts | Conflicting transactions in parallel | Deterministic conflict resolution |
| Clock Skew Attacks | Exploit time differences | NTP sync + drift detection |

### 11.2 Security Validations

```go
// SecurityValidator performs comprehensive security checks
type SecurityValidator struct {
    timestampValidator  *TimestampValidator
    stateValidator     *StateValidator
    consensusValidator *ConsensusValidator
}

// ValidateBlock performs security validation
func (sv *SecurityValidator) ValidateBlock(block *Block, dag *BlockDAG) error {
    // Timestamp validation
    if err := sv.timestampValidator.Validate(block, dag); err != nil {
        return fmt.Errorf("timestamp validation failed: %w", err)
    }
    
    // State transition validation
    if err := sv.stateValidator.Validate(block); err != nil {
        return fmt.Errorf("state validation failed: %w", err)
    }
    
    // Consensus rules validation
    if err := sv.consensusValidator.Validate(block, dag); err != nil {
        return fmt.Errorf("consensus validation failed: %w", err)
    }
    
    return nil
}
```

---

## 12. Testing Requirements

### 12.1 Test Scenarios

```go
// Comprehensive test suite for DAG-EVM integration
type DAGEVMTestSuite struct {
    // Test categories
    CanonicalTests     []TestCase
    StateTests         []TestCase
    ReorgTests         []TestCase
    GasTests           []TestCase
    SecurityTests      []TestCase
    PerformanceTests   []TestCase
}

// Critical test scenarios
var CriticalTestScenarios = []TestScenario{
    {
        Name: "Diamond DAG Pattern",
        Description: "Parallel chains merging and splitting",
        Setup: CreateDiamondDAG(10, 3),
        Validate: ValidateDiamondCanonical,
    },
    {
        Name: "Wide DAG (1000 parallel chains)",
        Description: "Extreme parallelism handling",
        Setup: CreateWideDAG(1000, 100),
        Validate: ValidateWideDAGPerformance,
    },
    {
        Name: "Deep Reorg (100 blocks)",
        Description: "Maximum depth reorganization",
        Setup: CreateDeepReorg(100),
        Validate: ValidateReorgCompletion,
    },
    {
        Name: "Conflicting Transactions",
        Description: "Same nonce in parallel blocks",
        Setup: CreateConflictingTxDAG(),
        Validate: ValidateConflictResolution,
    },
    {
        Name: "State Attack",
        Description: "Attempt state manipulation via reorg",
        Setup: CreateStateAttackDAG(),
        Validate: ValidateStateConsistency,
    },
    {
        Name: "Gas Exhaustion",
        Description: "Blocks at gas limit",
        Setup: CreateGasExhaustionDAG(),
        Validate: ValidateGasAccounting,
    },
    {
        Name: "Network Partition Recovery",
        Description: "Two network halves reuniting",
        Setup: CreatePartitionedDAG(2, 1000),
        Validate: ValidatePartitionRecovery,
    },
    {
        Name: "Smart Contract Reorg",
        Description: "DeFi contracts during reorg",
        Setup: CreateDeFiReorgScenario(),
        Validate: ValidateDeFiConsistency,
    },
}
```

### 12.2 Conformance Requirements

```go
// ConformanceChecker validates Ethereum compatibility
type ConformanceChecker struct {
    testSuites map[string]TestSuite
}

// Required test suites for production
var RequiredTestSuites = []string{
    "ethereum/tests/GeneralStateTests",
    "ethereum/tests/BlockchainTests",
    "ethereum/tests/TransactionTests",
    "ethereum/tests/VMTests",
}

// MustPassTests defines tests that must pass for production
func (cc *ConformanceChecker) MustPassTests() []string {
    return []string{
        // EVM conformance
        "stArgsZeroOneBalance",
        "stCallCodes",
        "stCallCreateCallCodeTest",
        "stDelegatecallTestHomestead",
        "stEIP150singleCodeGasPrices",
        "stEIP1559",
        "stMemExpandingEIP150Calls",
        "stNonZeroCallsTest",
        "stPreCompiledContracts",
        "stRandom",
        "stRecursiveCreate",
        "stRefundTest",
        "stSelfBalance",
        "stSolidityTest",
        "stStaticCall",
        "stSystemOperationsTest",
        
        // State tests
        "stTransactionTest",
        "stTransitionTest",
        
        // Consensus tests
        "bcForkStressTest",
        "bcGasPricerTest",
        "bcMultiChainTest",
        "bcRandomBlockhashTest",
        "bcStateTests",
        "bcTotalDifficultyTest",
        "bcValidBlockTest",
    }
}
```

---

## 13. Implementation Checklist

### Phase 1: Core Components (Weeks 1-2)
- [ ] Implement tip selection algorithm
- [ ] Implement canonical ordering
- [ ] Implement topological sort
- [ ] Implement basic state manager
- [ ] Create EVM context mapper
- [ ] Add BLOCKHASH opcode support
- [ ] Unit tests for core algorithms

### Phase 2: State Management (Weeks 3-4)
- [ ] Implement state transitions
- [ ] Add checkpoint system
- [ ] Implement state pruning
- [ ] Add state validation
- [ ] Create recovery mechanisms
- [ ] Performance optimization
- [ ] State management tests

### Phase 3: Transaction Handling (Weeks 5-6)
- [ ] Implement transaction ordering
- [ ] Add nonce validation
- [ ] Handle conflicting transactions
- [ ] Implement receipt generation
- [ ] Add log indexing
- [ ] Create transaction pool integration
- [ ] Transaction handling tests

### Phase 4: Reorg Handling (Week 7)
- [ ] Implement fork detection
- [ ] Add reorg execution
- [ ] Create rollback mechanism
- [ ] Handle orphaned transactions
- [ ] Add reorg metrics
- [ ] Implement recovery system
- [ ] Comprehensive reorg tests

### Phase 5: Gas Economics (Week 8)
- [ ] Implement base fee calculation
- [ ] Add DAG-aware adjustments
- [ ] Create fee distribution
- [ ] Add EIP-1559 support
- [ ] Implement gas oracle
- [ ] Add congestion detection
- [ ] Gas economics tests

### Phase 6: Advanced Features (Week 9)
- [ ] Add custom DAG opcodes
- [ ] Implement parent selection
- [ ] Add uncle handling
- [ ] Create randomness derivation
- [ ] Add security validators
- [ ] Implement attack prevention
- [ ] Security tests

### Phase 7: Performance (Week 10)
- [ ] Add caching layers
- [ ] Implement parallelization
- [ ] Add precomputation
- [ ] Create batching systems
- [ ] Memory optimization
- [ ] Add metrics collection
- [ ] Performance benchmarks

### Phase 8: Integration Testing (Weeks 11-12)
- [ ] Ethereum test suite conformance
- [ ] DAG-specific test scenarios
- [ ] Load testing
- [ ] Security audit preparation
- [ ] Documentation completion
- [ ] Deployment readiness
- [ ] Final validation

---

## Conclusion

This master specification provides the complete blueprint for implementing the DAG→EVM integration - the core innovation of BlockDAG Phoenix. With this level of detail, development teams can produce production-quality code that:

1. **Maintains determinism** across all nodes
2. **Handles complex DAG patterns** efficiently
3. **Preserves EVM compatibility** completely
4. **Manages reorganizations** safely
5. **Scales performance** as needed
6. **Resists attacks** effectively

The specification addresses all identified gaps and provides concrete implementations for every critical component. This is your competitive advantage - implement it correctly, and Phoenix will successfully bridge the gap between DAG performance and EVM compatibility.
