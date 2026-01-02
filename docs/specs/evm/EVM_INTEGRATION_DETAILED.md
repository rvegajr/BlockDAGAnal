# EVM Integration - Detailed Production Specification
## BlockDAG Phoenix - DAG↔EVM Bridge Implementation

### Overview
This document provides production-ready specifications for integrating EVM execution with the DAG structure, including exact field mappings, transaction ordering, and state management.

---

## 1. Transaction Ordering Within DAG Blocks

### 1.1 Intra-Block Transaction Ordering

```go
package evm

import (
    "math/big"
    "sort"
)

// OrderTransactions deterministically orders transactions within a DAG block
func OrderTransactions(txs []*Transaction) []*Transaction {
    // Create a copy to avoid mutating original
    ordered := make([]*Transaction, len(txs))
    copy(ordered, txs)
    
    // Multi-level sorting for determinism
    sort.SliceStable(ordered, func(i, j int) bool {
        txI, txJ := ordered[i], ordered[j]
        
        // Level 1: Nonce ordering (same sender)
        if bytes.Equal(txI.From[:], txJ.From[:]) {
            return txI.Nonce < txJ.Nonce
        }
        
        // Level 2: Gas price (higher first for MEV resistance)
        gasPriceCmp := txI.GasPrice.Cmp(txJ.GasPrice)
        if gasPriceCmp != 0 {
            return gasPriceCmp > 0
        }
        
        // Level 3: Transaction hash (deterministic tie-breaker)
        return bytes.Compare(txI.Hash[:], txJ.Hash[:]) < 0
    })
    
    return ordered
}

// ValidateTransactionOrder ensures nonce sequences are valid
func ValidateTransactionOrder(txs []*Transaction, state *StateDB) error {
    nonceTrackers := make(map[common.Address]uint64)
    
    for _, tx := range txs {
        currentNonce := state.GetNonce(tx.From)
        
        if trackedNonce, exists := nonceTrackers[tx.From]; exists {
            // Ensure sequential nonces
            if tx.Nonce != trackedNonce {
                return ErrNonceGap{
                    Address:  tx.From,
                    Expected: trackedNonce,
                    Got:      tx.Nonce,
                }
            }
            nonceTrackers[tx.From] = trackedNonce + 1
        } else {
            // First transaction from this sender
            if tx.Nonce != currentNonce {
                return ErrInvalidNonce{
                    Address:  tx.From,
                    Expected: currentNonce,
                    Got:      tx.Nonce,
                }
            }
            nonceTrackers[tx.From] = currentNonce + 1
        }
    }
    
    return nil
}
```

### 1.2 Cross-Block Transaction Handling During Reorgs

```go
// HandleReorgTransactions manages transaction pool during reorgs
func HandleReorgTransactions(oldBlocks, newBlocks []*Block, txPool *TxPool) error {
    // Step 1: Extract transactions from reorged blocks
    reorgedTxs := make([]*Transaction, 0)
    for _, block := range oldBlocks {
        reorgedTxs = append(reorgedTxs, block.Transactions...)
    }
    
    // Step 2: Remove transactions that appear in new blocks
    newTxHashes := make(map[common.Hash]bool)
    for _, block := range newBlocks {
        for _, tx := range block.Transactions {
            newTxHashes[tx.Hash] = true
        }
    }
    
    // Step 3: Re-add valid orphaned transactions to pool
    for _, tx := range reorgedTxs {
        if !newTxHashes[tx.Hash] {
            // Validate transaction is still valid
            if err := txPool.ValidateTransaction(tx); err == nil {
                txPool.Add(tx)
            }
        }
    }
    
    return nil
}
```

## 2. EVM Opcode Context Mappings

### 2.1 Block Context Opcodes

```go
// ExecuteBlockInfoOpcodes handles block-related opcodes in DAG context
type BlockInfoOpcodes struct {
    canonical []*Block
    current   *Block
}

// NUMBER - Returns canonical index
func (b *BlockInfoOpcodes) OpNumber() *big.Int {
    return big.NewInt(int64(b.current.CanonicalIndex))
}

// TIMESTAMP - Returns block timestamp
func (b *BlockInfoOpcodes) OpTimestamp() *big.Int {
    return big.NewInt(b.current.Timestamp)
}

// DIFFICULTY - Returns normalized difficulty
func (b *BlockInfoOpcodes) OpDifficulty() *big.Int {
    // Normalize difficulty across both algorithms
    if b.current.Algorithm == AlgoKHeavyHash {
        return b.current.Difficulty
    }
    // SHA-3 difficulty normalized to kHeavyHash equivalent
    return NormalizeSHA3Difficulty(b.current.Difficulty)
}

// COINBASE - Returns deterministic beneficiary
func (b *BlockInfoOpcodes) OpCoinbase() common.Address {
    // For DAG with multiple miners, select deterministically
    if len(b.current.Parents) > 1 {
        // Use round-robin or weighted selection
        return SelectDAGCoinbase(b.current, b.canonical)
    }
    return b.current.MinerAddress
}

// BLOCKHASH - Returns hash of block at canonical index
func (b *BlockInfoOpcodes) OpBlockhash(number uint64) common.Hash {
    // Can only access last 256 blocks
    if number >= b.current.CanonicalIndex {
        return common.Hash{}
    }
    
    if b.current.CanonicalIndex - number > 256 {
        return common.Hash{}
    }
    
    return b.canonical[number].Hash
}

// BASEFEE - EIP-1559 base fee
func (b *BlockInfoOpcodes) OpBaseFee() *big.Int {
    return CalculateDAGBaseFee(b.canonical, b.current.CanonicalIndex)
}

// PREVRANDAO - EIP-4399 randomness
func (b *BlockInfoOpcodes) OpPrevRandao() common.Hash {
    // Derive randomness from DAG structure
    return DeriveDAGRandomness(b.current, b.canonical)
}
```

### 2.2 DAG-Specific Opcode Extensions

```go
// Phoenix-specific opcodes for DAG awareness
const (
    OPCODE_BLUEHASH    = 0xb0  // Get blue hash of current block
    OPCODE_BLUESCORE   = 0xb1  // Get blue score
    OPCODE_PARENTCOUNT = 0xb2  // Number of parents
    OPCODE_PARENTHASH  = 0xb3  // Get specific parent hash
    OPCODE_ALGORITHM   = 0xb4  // Mining algorithm used
)

// ExecuteDAGOpcodes handles Phoenix-specific opcodes
func ExecuteDAGOpcodes(op byte, stack *Stack, block *Block) error {
    switch op {
    case OPCODE_BLUEHASH:
        stack.Push(new(big.Int).SetBytes(block.BlueHash[:]))
        
    case OPCODE_BLUESCORE:
        stack.Push(big.NewInt(int64(block.BlueScore)))
        
    case OPCODE_PARENTCOUNT:
        stack.Push(big.NewInt(int64(len(block.Parents))))
        
    case OPCODE_PARENTHASH:
        index := stack.Pop().Uint64()
        if index >= uint64(len(block.Parents)) {
            stack.Push(big.NewInt(0))
        } else {
            stack.Push(new(big.Int).SetBytes(block.Parents[index][:]))
        }
        
    case OPCODE_ALGORITHM:
        algo := big.NewInt(0)
        if block.Algorithm == AlgoSHA3 {
            algo = big.NewInt(1)
        }
        stack.Push(algo)
        
    default:
        return ErrInvalidOpcode
    }
    
    return nil
}
```

## 3. State Management During Canonicalization

### 3.1 State Transition System

```go
// StateTransitioner manages state during DAG→Linear execution
type StateTransitioner struct {
    stateDB      *StateDB
    checkpoints  map[uint64]*StateCheckpoint
    pruneDepth   uint64
}

// ExecuteCanonicalBlock applies all transactions in canonical order
func (st *StateTransitioner) ExecuteCanonicalBlock(block *Block, vmConfig vm.Config) ([]*Receipt, error) {
    // Create block context for EVM
    blockContext := MapToEVMContext(block, st.canonical)
    
    // Order transactions deterministically
    orderedTxs := OrderTransactions(block.Transactions)
    
    // Execute transactions
    receipts := make([]*Receipt, 0, len(orderedTxs))
    gasUsed := uint64(0)
    
    for i, tx := range orderedTxs {
        // Create message
        msg, err := TransactionToMessage(tx, block.BaseFee)
        if err != nil {
            return nil, fmt.Errorf("tx %d: %w", i, err)
        }
        
        // Create EVM instance
        txContext := vm.TxContext{
            Origin:   msg.From,
            GasPrice: msg.GasPrice,
        }
        evm := vm.NewEVM(blockContext, txContext, st.stateDB, vmConfig)
        
        // Execute transaction
        result, err := ApplyMessage(evm, msg, gasUsed)
        if err != nil {
            return nil, fmt.Errorf("tx %d execution: %w", i, err)
        }
        
        // Create receipt
        receipt := &Receipt{
            Type:              tx.Type(),
            PostState:         st.stateDB.IntermediateRoot().Bytes(),
            CumulativeGasUsed: gasUsed + result.UsedGas,
            Bloom:             CreateBloom(result.Logs),
            Logs:              result.Logs,
            TxHash:            tx.Hash,
            ContractAddress:   result.ContractAddress,
            GasUsed:           result.UsedGas,
            
            // DAG-specific fields
            BlockHash:       block.Hash,
            BlockNumber:     big.NewInt(int64(block.CanonicalIndex)),
            TransactionIndex: uint(i),
        }
        
        // Handle status (post-Byzantium)
        if result.Failed() {
            receipt.Status = ReceiptStatusFailed
        } else {
            receipt.Status = ReceiptStatusSuccessful
        }
        
        receipts = append(receipts, receipt)
        gasUsed += result.UsedGas
    }
    
    // Finalize block
    st.stateDB.Finalise(true)
    
    return receipts, nil
}
```

### 3.2 State Pruning and Checkpointing

```go
// PruneAndCheckpoint manages state storage efficiently
func (st *StateTransitioner) PruneAndCheckpoint(block *Block) error {
    // Checkpoint at intervals
    if block.CanonicalIndex % CHECKPOINT_INTERVAL == 0 {
        checkpoint := &StateCheckpoint{
            BlockNumber: block.CanonicalIndex,
            BlockHash:   block.Hash,
            StateRoot:   st.stateDB.IntermediateRoot(),
            Timestamp:   time.Now(),
        }
        
        // Serialize state
        stateData, err := st.stateDB.Dump(false, false, true)
        if err != nil {
            return err
        }
        
        // Compress and store
        compressed := snappy.Encode(nil, stateData)
        if err := st.storage.StoreCheckpoint(checkpoint, compressed); err != nil {
            return err
        }
        
        st.checkpoints[block.CanonicalIndex] = checkpoint
    }
    
    // Prune old states (keep last N checkpoints)
    if len(st.checkpoints) > MAX_CHECKPOINTS {
        oldestToKeep := block.CanonicalIndex - (MAX_CHECKPOINTS * CHECKPOINT_INTERVAL)
        for num := range st.checkpoints {
            if num < oldestToKeep {
                delete(st.checkpoints, num)
                st.storage.DeleteCheckpoint(num)
            }
        }
    }
    
    // Prune trie nodes
    if block.CanonicalIndex % PRUNE_INTERVAL == 0 {
        st.stateDB.TrieDB().CommitPreimages()
        st.stateDB.TrieDB().Prune(st.stateDB.IntermediateRoot())
    }
    
    return nil
}
```

## 4. Receipt and Log Management

### 4.1 Receipt Generation with DAG Context

```go
// GenerateReceipt creates receipts with DAG-aware fields
func GenerateReceipt(tx *Transaction, result *ExecutionResult, block *Block, txIndex int) *Receipt {
    receipt := &Receipt{
        // Standard Ethereum fields
        Type:              tx.Type(),
        Status:            result.Status,
        CumulativeGasUsed: result.CumulativeGasUsed,
        Bloom:             types.CreateBloom([]*types.Log{result.Logs...}),
        Logs:              result.Logs,
        TxHash:            tx.Hash,
        ContractAddress:   result.ContractAddress,
        GasUsed:           result.UsedGas,
        
        // Block context (canonical)
        BlockHash:        block.Hash,
        BlockNumber:      big.NewInt(int64(block.CanonicalIndex)),
        TransactionIndex: uint(txIndex),
        
        // DAG-specific extensions
        DAGContext: &DAGReceiptContext{
            BlueScore:      block.BlueScore,
            ParentHashes:   block.Parents,
            MiningAlgorithm: block.Algorithm,
            CanonicalDepth: CalculateDepth(block),
        },
    }
    
    // Update log indices
    logIndex := result.LogIndex
    for _, log := range receipt.Logs {
        log.BlockNumber = block.CanonicalIndex
        log.TxHash = tx.Hash
        log.TxIndex = uint(txIndex)
        log.BlockHash = block.Hash
        log.Index = logIndex
        logIndex++
    }
    
    return receipt
}
```

### 4.2 Log Indexing During Reorgs

```go
// ReindexLogs updates log indices after reorg
func ReindexLogs(oldBlocks, newBlocks []*Block) error {
    // Remove old logs from index
    for _, block := range oldBlocks {
        if err := RemoveBlockLogs(block); err != nil {
            return err
        }
    }
    
    // Add new logs with updated indices
    cumulativeLogIndex := uint(0)
    for _, block := range newBlocks {
        for txIndex, tx := range block.Transactions {
            receipt := block.Receipts[txIndex]
            
            for logIndex, log := range receipt.Logs {
                // Update all indices
                log.BlockNumber = block.CanonicalIndex
                log.BlockHash = block.Hash
                log.TxIndex = uint(txIndex)
                log.Index = cumulativeLogIndex
                
                // Store in index
                if err := StoreLog(log); err != nil {
                    return err
                }
                
                cumulativeLogIndex++
            }
        }
    }
    
    return nil
}
```

## 5. Gas Calculation in DAG Context

### 5.1 Dynamic Base Fee Adjustment

```go
// CalculateDAGBaseFee implements EIP-1559 for DAG structure
func CalculateDAGBaseFee(canonical []*Block, currentIndex uint64) *big.Int {
    if currentIndex == 0 {
        return params.InitialBaseFee
    }
    
    // Get recent blocks for calculation (consider multiple parents)
    recentBlocks := getRecentBlocks(canonical, currentIndex, BASE_FEE_WINDOW)
    
    // Calculate average gas usage across recent blocks
    totalGasUsed := uint64(0)
    totalGasLimit := uint64(0)
    
    for _, block := range recentBlocks {
        totalGasUsed += block.GasUsed
        totalGasLimit += block.GasLimit
    }
    
    avgGasUsed := totalGasUsed / uint64(len(recentBlocks))
    avgGasTarget := totalGasLimit / uint64(len(recentBlocks)) / 2
    
    // Apply EIP-1559 formula with DAG smoothing
    parent := canonical[currentIndex-1]
    baseFee := new(big.Int).Set(parent.BaseFee)
    
    if avgGasUsed > avgGasTarget {
        // Increase base fee
        delta := new(big.Int).Sub(big.NewInt(int64(avgGasUsed)), big.NewInt(int64(avgGasTarget)))
        delta.Mul(delta, baseFee)
        delta.Div(delta, big.NewInt(int64(avgGasTarget)))
        delta.Div(delta, params.BaseFeeChangeDenominator)
        
        baseFee.Add(baseFee, delta)
    } else {
        // Decrease base fee
        delta := new(big.Int).Sub(big.NewInt(int64(avgGasTarget)), big.NewInt(int64(avgGasUsed)))
        delta.Mul(delta, baseFee)
        delta.Div(delta, big.NewInt(int64(avgGasTarget)))
        delta.Div(delta, params.BaseFeeChangeDenominator)
        
        if delta.Cmp(baseFee) > 0 {
            baseFee = params.MinBaseFee
        } else {
            baseFee.Sub(baseFee, delta)
        }
    }
    
    // Apply bounds
    if baseFee.Cmp(params.MinBaseFee) < 0 {
        baseFee = params.MinBaseFee
    }
    if baseFee.Cmp(params.MaxBaseFee) > 0 {
        baseFee = params.MaxBaseFee
    }
    
    return baseFee
}
```

## 6. Testing Framework

### 6.1 EVM Integration Tests

```go
func TestEVMIntegration(t *testing.T) {
    tests := []struct {
        name     string
        setup    func() *BlockDAG
        contract string
        expected string
    }{
        {
            name: "Deploy and call simple storage",
            setup: func() *BlockDAG {
                return CreateTestDAG(10, 3) // 10 blocks, 3 parallel chains
            },
            contract: SimpleStorageContract,
            expected: "42",
        },
        {
            name: "Complex DeFi interaction during reorg",
            setup: func() *BlockDAG {
                dag := CreateTestDAG(20, 5)
                TriggerReorg(dag, 10) // Reorg at block 10
                return dag
            },
            contract: UniswapV2Contract,
            expected: "liquidity maintained",
        },
        {
            name: "NFT minting across DAG branches",
            setup: func() *BlockDAG {
                return CreateBranchingDAG(15)
            },
            contract: ERC721Contract,
            expected: "unique token IDs",
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            dag := tt.setup()
            canonical := BuildCanonicalSequence(dag)
            state := NewStateDB()
            
            // Deploy contract
            contractAddr := DeployContract(state, tt.contract)
            
            // Execute across canonical chain
            for _, block := range canonical {
                receipts, err := ExecuteBlock(state, block)
                require.NoError(t, err)
                require.NotEmpty(t, receipts)
            }
            
            // Verify result
            result := CallContract(state, contractAddr, "getValue")
            require.Equal(t, tt.expected, result)
        })
    }
}
```

## 7. Configuration Parameters

```go
// EVM integration configuration
const (
    // EVM Configuration
    EVM_VERSION        = "Shanghai"          // Target EVM version
    MAX_CODE_SIZE      = 24576              // Maximum contract code size
    MAX_STACK_DEPTH    = 1024               // EVM stack depth
    
    // Gas Configuration  
    BLOCK_GAS_LIMIT    = 30_000_000         // Gas limit per block
    MIN_BASE_FEE       = 1_000_000_000      // 1 Gwei minimum
    MAX_BASE_FEE       = 10_000_000_000_000 // 10,000 Gwei maximum
    BASE_FEE_WINDOW    = 10                 // Blocks to average for base fee
    
    // State Management
    STATE_CACHE_SIZE   = 256 * 1024 * 1024  // 256MB state cache
    PRUNE_INTERVAL     = 100                // Blocks between pruning
    MAX_CHECKPOINTS    = 10                 // Checkpoints to retain
    
    // Transaction Pool
    TX_POOL_SIZE       = 5000               // Maximum pending transactions
    TX_POOL_PRICE_BUMP = 10                 // Percent price increase for replacement
    
    // DAG-specific
    MAX_UNCLE_DEPTH    = 7                  // Maximum depth for uncle inclusion
    BLUE_SCORE_WEIGHT  = 0.7                // Weight for blue score in selection
)
```

---

This specification provides production-ready details for implementing the EVM integration layer with full DAG awareness.



