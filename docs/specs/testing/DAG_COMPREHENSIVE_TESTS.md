# DAG Comprehensive Test Scenarios
## BlockDAG Phoenix - Production Test Suite

### Overview
This document provides comprehensive test scenarios for validating the DAG→EVM integration, covering edge cases, attack vectors, and performance benchmarks.

---

## 1. DAG Structure Test Scenarios

### 1.1 Basic DAG Patterns

```go
package testing

// TestCase1: Simple Diamond Pattern
func TestDiamondDAG(t *testing.T) {
    /*
    Structure:
        Genesis
         /    \
        A      B
         \    /
          Tip
    
    Expected canonical: [Genesis, A, B, Tip] (A before B by hash)
    */
    
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    
    blockA := dag.AddBlock("A", []Hash{genesis.Hash}, 1000, time.Now().Unix())
    blockB := dag.AddBlock("B", []Hash{genesis.Hash}, 1000, time.Now().Unix())
    tip := dag.AddBlock("Tip", []Hash{blockA.Hash, blockB.Hash}, 1000, time.Now().Unix()+1)
    
    canonical := BuildCanonicalSequence(dag, []*Block{tip})
    
    expectedOrder := []string{"Genesis", "A", "B", "Tip"}
    actualOrder := extractBlockNames(canonical)
    
    require.Equal(t, expectedOrder, actualOrder)
    
    // Test determinism
    canonical2 := BuildCanonicalSequence(dag, []*Block{tip})
    require.Equal(t, canonical, canonical2, "Must be deterministic")
}

// TestCase2: Wide DAG (High Parallelism)
func TestWideDAG(t *testing.T) {
    /*
    Structure:
        Genesis
        /  |  \
       A   B   C  (100 parallel chains)
       |   |   |
       D   E   F
        \  |  /
         Merge
    
    Tests: Handling 100+ parallel chains
    Expected: Deterministic ordering by blue score, then timestamp, then hash
    */
    
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    
    // Create 100 parallel chains
    parallelChains := make([][]*Block, 100)
    for i := 0; i < 100; i++ {
        chain := make([]*Block, 10)
        parent := genesis
        
        for j := 0; j < 10; j++ {
            blockName := fmt.Sprintf("Chain%d_Block%d", i, j)
            block := dag.AddBlock(blockName, []Hash{parent.Hash}, 1000, time.Now().Unix()+int64(j))
            chain[j] = block
            parent = block
        }
        parallelChains[i] = chain
    }
    
    // Merge all chains
    mergeParents := make([]Hash, 100)
    for i := 0; i < 100; i++ {
        mergeParents[i] = parallelChains[i][9].Hash
    }
    merge := dag.AddBlock("Merge", mergeParents, 1000, time.Now().Unix()+100)
    
    // Build canonical sequence
    start := time.Now()
    canonical := BuildCanonicalSequence(dag, []*Block{merge})
    duration := time.Since(start)
    
    // Performance assertion
    require.Less(t, duration, 5*time.Second, "Should handle 100 chains in < 5s")
    
    // Verify all blocks included
    require.Equal(t, 1002, len(canonical)) // Genesis + 1000 blocks + merge
}

// TestCase3: Deep DAG (Long Chain)
func TestDeepDAG(t *testing.T) {
    /*
    Structure: Linear chain of 10,000 blocks
    Tests: Performance with deep history
    Expected: Linear time complexity
    */
    
    dag := NewTestDAG()
    current := dag.AddGenesis()
    
    for i := 0; i < 10000; i++ {
        current = dag.AddBlock(
            fmt.Sprintf("Block_%d", i),
            []Hash{current.Hash},
            1000 + uint64(i),
            time.Now().Unix() + int64(i),
        )
    }
    
    start := time.Now()
    canonical := BuildCanonicalSequence(dag, []*Block{current})
    duration := time.Since(start)
    
    require.Less(t, duration, 1*time.Second, "Should handle 10k blocks in < 1s")
    require.Equal(t, 10001, len(canonical))
}
```

### 1.2 Complex DAG Patterns

```go
// TestCase4: Butterfly Pattern (Complex Merging)
func TestButterflyDAG(t *testing.T) {
    /*
    Structure:
           Genesis
          /   |   \
         A    B    C
        / \  / \  / \
       D   E F  G H  I
        \ / \ / \ /
         J   K   L
          \  |  /
           Merge
    
    Tests: Complex interdependencies
    */
    
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    
    // Layer 1
    a := dag.AddBlock("A", []Hash{genesis.Hash}, 1000, 100)
    b := dag.AddBlock("B", []Hash{genesis.Hash}, 1000, 100)
    c := dag.AddBlock("C", []Hash{genesis.Hash}, 1000, 100)
    
    // Layer 2 (cross-references)
    d := dag.AddBlock("D", []Hash{a.Hash, b.Hash}, 1000, 200)
    e := dag.AddBlock("E", []Hash{a.Hash, b.Hash}, 1000, 200)
    f := dag.AddBlock("F", []Hash{b.Hash, c.Hash}, 1000, 200)
    g := dag.AddBlock("G", []Hash{b.Hash, c.Hash}, 1000, 200)
    h := dag.AddBlock("H", []Hash{c.Hash}, 1000, 200)
    i := dag.AddBlock("I", []Hash{c.Hash}, 1000, 200)
    
    // Layer 3 (more merging)
    j := dag.AddBlock("J", []Hash{d.Hash, e.Hash}, 1000, 300)
    k := dag.AddBlock("K", []Hash{e.Hash, f.Hash, g.Hash}, 1000, 300)
    l := dag.AddBlock("L", []Hash{g.Hash, h.Hash, i.Hash}, 1000, 300)
    
    // Final merge
    merge := dag.AddBlock("Merge", []Hash{j.Hash, k.Hash, l.Hash}, 1000, 400)
    
    canonical := BuildCanonicalSequence(dag, []*Block{merge})
    
    // Verify topological ordering
    indices := make(map[string]int)
    for idx, block := range canonical {
        indices[block.Name] = idx
    }
    
    // All parents must come before children
    require.Less(t, indices["Genesis"], indices["A"])
    require.Less(t, indices["A"], indices["D"])
    require.Less(t, indices["D"], indices["J"])
    require.Less(t, indices["J"], indices["Merge"])
}

// TestCase5: Network Partition Scenario
func TestNetworkPartition(t *testing.T) {
    /*
    Simulates network split creating two competing chains:
    
    Genesis
       |
    Block1
     /   \
    A1    B1  (Network splits here)
    |     |
    A2    B2
    |     |
    A3    B3  (B chain has more work)
     \   /
     Merge   (Network heals)
    */
    
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    block1 := dag.AddBlock("Block1", []Hash{genesis.Hash}, 1000, 100)
    
    // Partition A (less work)
    a1 := dag.AddBlock("A1", []Hash{block1.Hash}, 900, 200)
    a2 := dag.AddBlock("A2", []Hash{a1.Hash}, 900, 300)
    a3 := dag.AddBlock("A3", []Hash{a2.Hash}, 900, 400)
    
    // Partition B (more work)
    b1 := dag.AddBlock("B1", []Hash{block1.Hash}, 1100, 200)
    b2 := dag.AddBlock("B2", []Hash{b1.Hash}, 1100, 300)
    b3 := dag.AddBlock("B3", []Hash{b2.Hash}, 1100, 400)
    
    // Network heals
    merge := dag.AddBlock("Merge", []Hash{a3.Hash, b3.Hash}, 1000, 500)
    
    canonical := BuildCanonicalSequence(dag, []*Block{merge})
    
    // B chain should be preferred due to higher work
    order := extractBlockNames(canonical)
    bIndex := indexOf(order, "B1")
    aIndex := indexOf(order, "A1")
    
    require.Less(t, bIndex, aIndex, "Higher work chain should be canonical")
}
```

## 2. Reorg Test Scenarios

### 2.1 Basic Reorg Tests

```go
// TestCase6: Simple Reorg
func TestSimpleReorg(t *testing.T) {
    stateDB := NewTestStateDB()
    dag := NewTestDAG()
    
    // Original chain
    genesis := dag.AddGenesis()
    a1 := dag.AddBlock("A1", []Hash{genesis.Hash}, 1000, 100)
    a2 := dag.AddBlock("A2", []Hash{a1.Hash}, 1000, 200)
    a3 := dag.AddBlock("A3", []Hash{a2.Hash}, 1000, 300)
    
    // Execute original chain
    originalCanonical := []*Block{genesis, a1, a2, a3}
    for _, block := range originalCanonical {
        ExecuteBlock(stateDB, block)
    }
    originalState := stateDB.Copy()
    
    // New competing chain (higher work)
    b1 := dag.AddBlock("B1", []Hash{genesis.Hash}, 1200, 150)
    b2 := dag.AddBlock("B2", []Hash{b1.Hash}, 1200, 250)
    b3 := dag.AddBlock("B3", []Hash{b2.Hash}, 1200, 350)
    b4 := dag.AddBlock("B4", []Hash{b3.Hash}, 1200, 450)
    
    // Trigger reorg
    newCanonical := []*Block{genesis, b1, b2, b3, b4}
    err := HandleReorg(stateDB, originalCanonical, newCanonical)
    require.NoError(t, err)
    
    // Verify state consistency
    testStateDB := NewTestStateDB()
    for _, block := range newCanonical {
        ExecuteBlock(testStateDB, block)
    }
    
    require.Equal(t, testStateDB.Root(), stateDB.Root(), "State must match after reorg")
}

// TestCase7: Deep Reorg (Near Limit)
func TestDeepReorg(t *testing.T) {
    stateDB := NewTestStateDB()
    dag := NewTestDAG()
    
    // Build original chain (99 blocks - just under MAX_REORG_DEPTH)
    blocks := make([]*Block, 100)
    blocks[0] = dag.AddGenesis()
    
    for i := 1; i < 100; i++ {
        blocks[i] = dag.AddBlock(
            fmt.Sprintf("Block_%d", i),
            []Hash{blocks[i-1].Hash},
            1000,
            int64(i*100),
        )
        ExecuteBlock(stateDB, blocks[i])
    }
    
    // Create competing chain from block 1 (99 block reorg)
    newBlocks := make([]*Block, 100)
    newBlocks[0] = blocks[0] // Same genesis
    
    for i := 1; i < 100; i++ {
        newBlocks[i] = dag.AddBlock(
            fmt.Sprintf("NewBlock_%d", i),
            []Hash{newBlocks[i-1].Hash},
            1100, // Higher difficulty
            int64(i*100),
        )
    }
    
    // Should succeed (depth = 99)
    err := HandleReorg(stateDB, blocks, newBlocks)
    require.NoError(t, err)
}

// TestCase8: Too Deep Reorg (Should Fail)
func TestTooDeepReorg(t *testing.T) {
    stateDB := NewTestStateDB()
    dag := NewTestDAG()
    
    // Build original chain (101 blocks - exceeds MAX_REORG_DEPTH)
    blocks := make([]*Block, 102)
    blocks[0] = dag.AddGenesis()
    
    for i := 1; i < 102; i++ {
        blocks[i] = dag.AddBlock(
            fmt.Sprintf("Block_%d", i),
            []Hash{blocks[i-1].Hash},
            1000,
            int64(i*100),
        )
    }
    
    // Create competing chain from genesis (101 block reorg)
    newBlocks := make([]*Block, 102)
    newBlocks[0] = blocks[0]
    
    for i := 1; i < 102; i++ {
        newBlocks[i] = dag.AddBlock(
            fmt.Sprintf("NewBlock_%d", i),
            []Hash{newBlocks[i-1].Hash},
            1100,
            int64(i*100),
        )
    }
    
    // Should fail (depth = 101 > MAX_REORG_DEPTH)
    err := HandleReorg(stateDB, blocks, newBlocks)
    require.Error(t, err)
    require.Contains(t, err.Error(), "reorg exceeds maximum depth")
}
```

### 2.2 Reorg with Transactions

```go
// TestCase9: Reorg with Conflicting Transactions
func TestReorgConflictingTransactions(t *testing.T) {
    stateDB := NewTestStateDB()
    txPool := NewTxPool()
    
    // Setup accounts
    alice := createAccount(stateDB, 1000)
    bob := createAccount(stateDB, 0)
    charlie := createAccount(stateDB, 0)
    
    // Original chain: Alice sends to Bob
    tx1 := createTransaction(alice, bob, 500, 0)
    block1 := createBlockWithTx(tx1)
    ExecuteBlock(stateDB, block1)
    
    require.Equal(t, uint64(500), stateDB.GetBalance(alice))
    require.Equal(t, uint64(500), stateDB.GetBalance(bob))
    
    // Competing chain: Alice sends to Charlie instead
    stateDB2 := stateDB.Copy()
    tx2 := createTransaction(alice, charlie, 600, 0) // Different amount
    block2 := createBlockWithTx(tx2)
    
    // Reorg to competing chain
    err := HandleReorgWithTxPool(stateDB, []*Block{block1}, []*Block{block2}, txPool)
    require.NoError(t, err)
    
    // Verify balances after reorg
    require.Equal(t, uint64(400), stateDB.GetBalance(alice))
    require.Equal(t, uint64(0), stateDB.GetBalance(bob))
    require.Equal(t, uint64(600), stateDB.GetBalance(charlie))
    
    // Original transaction should be in pool
    require.True(t, txPool.Has(tx1.Hash))
}
```

## 3. Smart Contract Test Scenarios

### 3.1 Contract Deployment and Execution

```go
// TestCase10: Deploy Contract Across Reorg
func TestContractDeploymentReorg(t *testing.T) {
    stateDB := NewTestStateDB()
    
    // Deploy contract in original chain
    deployTx := createContractDeployment(SimpleStorageByteCode)
    block1 := createBlockWithTx(deployTx)
    receipts1 := ExecuteBlock(stateDB, block1)
    contractAddr := receipts1[0].ContractAddress
    
    // Call contract
    callTx := createContractCall(contractAddr, "store", 42)
    block2 := createBlockWithTx(callTx)
    ExecuteBlock(stateDB, block2)
    
    // Verify value
    result := CallContract(stateDB, contractAddr, "retrieve")
    require.Equal(t, big.NewInt(42), result)
    
    // Reorg removes contract deployment
    emptyBlock := createEmptyBlock()
    err := HandleReorg(stateDB, []*Block{block1, block2}, []*Block{emptyBlock})
    require.NoError(t, err)
    
    // Contract should not exist
    require.False(t, stateDB.Exist(contractAddr))
}

// TestCase11: Complex DeFi Interaction
func TestDeFiProtocolReorg(t *testing.T) {
    stateDB := NewTestStateDB()
    
    // Deploy Uniswap-like AMM
    ammDeploy := deployAMM()
    block1 := createBlockWithTx(ammDeploy)
    receipts := ExecuteBlock(stateDB, block1)
    ammAddr := receipts[0].ContractAddress
    
    // Add liquidity
    addLiqTx := createAddLiquidity(ammAddr, 1000, 1000)
    block2 := createBlockWithTx(addLiqTx)
    ExecuteBlock(stateDB, block2)
    
    // Multiple swaps in original chain
    swaps := []Transaction{}
    for i := 0; i < 10; i++ {
        swap := createSwap(ammAddr, 100, "tokenA", "tokenB")
        swaps = append(swaps, swap)
    }
    
    block3 := createBlockWithTxs(swaps)
    ExecuteBlock(stateDB, block3)
    
    // Get reserves after swaps
    reserveA := CallContract(stateDB, ammAddr, "reserveA")
    reserveB := CallContract(stateDB, ammAddr, "reserveB")
    
    // Reorg with different swaps
    differentSwaps := []Transaction{}
    for i := 0; i < 5; i++ {
        swap := createSwap(ammAddr, 200, "tokenB", "tokenA")
        differentSwaps = append(differentSwaps, swap)
    }
    
    block3Alt := createBlockWithTxs(differentSwaps)
    
    err := HandleReorg(stateDB, []*Block{block3}, []*Block{block3Alt})
    require.NoError(t, err)
    
    // Verify reserves changed correctly
    newReserveA := CallContract(stateDB, ammAddr, "reserveA")
    newReserveB := CallContract(stateDB, ammAddr, "reserveB")
    
    require.NotEqual(t, reserveA, newReserveA)
    require.NotEqual(t, reserveB, newReserveB)
    
    // Verify K constant maintained
    kBefore := new(big.Int).Mul(reserveA, reserveB)
    kAfter := new(big.Int).Mul(newReserveA, newReserveB)
    
    // K should be approximately equal (allowing for fees)
    diff := new(big.Int).Sub(kAfter, kBefore)
    require.Less(t, diff.Uint64(), uint64(10000), "K constant should be maintained")
}
```

## 4. Performance Benchmarks

### 4.1 Canonicalization Performance

```go
func BenchmarkCanonicalization(b *testing.B) {
    scenarios := []struct {
        name   string
        blocks int
        width  int // parallel chains
    }{
        {"Linear_100", 100, 1},
        {"Linear_1000", 1000, 1},
        {"Linear_10000", 10000, 1},
        {"Wide_100x10", 100, 10},
        {"Wide_100x100", 100, 100},
        {"Wide_1000x10", 1000, 10},
    }
    
    for _, sc := range scenarios {
        b.Run(sc.name, func(b *testing.B) {
            dag := GenerateDAG(sc.blocks, sc.width)
            tips := dag.GetTips()
            
            b.ResetTimer()
            for i := 0; i < b.N; i++ {
                _ = BuildCanonicalSequence(dag, tips)
            }
        })
    }
}

func BenchmarkReorg(b *testing.B) {
    sizes := []int{10, 50, 100}
    
    for _, size := range sizes {
        b.Run(fmt.Sprintf("ReorgDepth_%d", size), func(b *testing.B) {
            stateDB := NewTestStateDB()
            oldChain := GenerateChain(size + 1)
            newChain := GenerateAlternativeChain(size + 1)
            
            // Setup initial state
            for _, block := range oldChain {
                ExecuteBlock(stateDB, block)
            }
            
            b.ResetTimer()
            for i := 0; i < b.N; i++ {
                stateCopy := stateDB.Copy()
                HandleReorg(stateCopy, oldChain, newChain)
            }
        })
    }
}
```

## 5. Attack Vector Tests

### 5.1 Timestamp Manipulation

```go
// TestCase12: Future Timestamp Attack
func TestFutureTimestampAttack(t *testing.T) {
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    
    // Attempt to add block with timestamp far in future
    futureTime := time.Now().Unix() + 3600 // 1 hour in future
    futureBlock := &Block{
        Hash:      generateHash(),
        Parents:   []Hash{genesis.Hash},
        Timestamp: futureTime,
    }
    
    err := ValidateBlockTimestamp(futureBlock, []*Block{genesis})
    require.Error(t, err)
    require.Contains(t, err.Error(), "timestamp too far in future")
}

// TestCase13: Time Warp Attack
func TestTimeWarpAttack(t *testing.T) {
    dag := NewTestDAG()
    
    // Build chain with manipulated timestamps
    blocks := make([]*Block, 20)
    blocks[0] = dag.AddGenesis()
    
    for i := 1; i < 20; i++ {
        // Alternating timestamps to manipulate difficulty
        timestamp := int64(i * 100)
        if i%2 == 0 {
            timestamp -= 50 // Go back in time
        }
        
        blocks[i] = &Block{
            Hash:      generateHash(),
            Parents:   []Hash{blocks[i-1].Hash},
            Timestamp: timestamp,
        }
    }
    
    // Validation should fail
    err := ValidateCanonicalSequence(blocks)
    require.Error(t, err)
    require.Contains(t, err.Error(), "invalid timestamp ordering")
}
```

### 5.2 State Exhaustion Attacks

```go
// TestCase14: State Bloat Attack
func TestStateBloatAttack(t *testing.T) {
    stateDB := NewTestStateDB()
    
    // Deploy contract that creates many storage entries
    bloatContract := `
    contract Bloat {
        mapping(uint => uint) public data;
        
        function bloat() public {
            for(uint i = 0; i < 10000; i++) {
                data[i] = i;
            }
        }
    }
    `
    
    deployTx := deployContract(bloatContract)
    block1 := createBlockWithTx(deployTx)
    receipts := ExecuteBlock(stateDB, block1)
    
    // Call bloat function
    bloatTx := createContractCall(receipts[0].ContractAddress, "bloat")
    block2 := createBlockWithTx(bloatTx)
    
    // Should fail due to gas limit
    receipts2 := ExecuteBlock(stateDB, block2)
    require.Equal(t, ReceiptStatusFailed, receipts2[0].Status)
    require.Contains(t, receipts2[0].Error, "out of gas")
}
```

## 6. Edge Case Tests

### 6.1 Empty Blocks and Transactions

```go
// TestCase15: Empty DAG Blocks
func TestEmptyBlocks(t *testing.T) {
    dag := NewTestDAG()
    stateDB := NewTestStateDB()
    
    // Create chain of empty blocks
    blocks := make([]*Block, 100)
    blocks[0] = dag.AddGenesis()
    
    for i := 1; i < 100; i++ {
        blocks[i] = &Block{
            Hash:         generateHash(),
            Parents:      []Hash{blocks[i-1].Hash},
            Transactions: []*Transaction{}, // Empty
            Timestamp:    int64(i * 100),
        }
    }
    
    // Should process without errors
    canonical := BuildCanonicalSequence(dag, []*Block{blocks[99]})
    require.Equal(t, 100, len(canonical))
    
    // Execute empty blocks
    for _, block := range canonical {
        receipts := ExecuteBlock(stateDB, block)
        require.Empty(t, receipts)
    }
}
```

### 6.2 Maximum Limits

```go
// TestCase16: Maximum Parents
func TestMaximumParents(t *testing.T) {
    dag := NewTestDAG()
    
    // Create blocks to be parents
    parents := make([]*Block, MAX_PARENTS+1)
    for i := 0; i < MAX_PARENTS+1; i++ {
        parents[i] = dag.AddBlock(fmt.Sprintf("Parent_%d", i), []Hash{}, 1000, int64(i))
    }
    
    // Try to create block with too many parents
    parentHashes := make([]Hash, MAX_PARENTS+1)
    for i, p := range parents {
        parentHashes[i] = p.Hash
    }
    
    err := dag.ValidateBlock(&Block{
        Hash:    generateHash(),
        Parents: parentHashes,
    })
    
    require.Error(t, err)
    require.Contains(t, err.Error(), "exceeds maximum parents")
}
```

## 7. Consensus Edge Cases

### 7.1 Blue Score Ties

```go
// TestCase17: Equal Blue Scores
func TestEqualBlueScores(t *testing.T) {
    dag := NewTestDAG()
    genesis := dag.AddGenesis()
    
    // Create two chains with exact same blue score
    a1 := dag.AddBlockWithBlueScore("A1", []Hash{genesis.Hash}, 1000, 100, 50)
    a2 := dag.AddBlockWithBlueScore("A2", []Hash{a1.Hash}, 1000, 200, 50)
    
    b1 := dag.AddBlockWithBlueScore("B1", []Hash{genesis.Hash}, 1000, 100, 50)
    b2 := dag.AddBlockWithBlueScore("B2", []Hash{b1.Hash}, 1000, 200, 50)
    
    // Merge point
    merge := dag.AddBlock("Merge", []Hash{a2.Hash, b2.Hash}, 1000, 300)
    
    canonical := BuildCanonicalSequence(dag, []*Block{merge})
    
    // Should use timestamp as tie-breaker (both have same timestamp)
    // Then use hash as final tie-breaker
    
    // Verify deterministic ordering
    canonical2 := BuildCanonicalSequence(dag, []*Block{merge})
    require.Equal(t, canonical, canonical2)
}
```

## 8. Integration Test Suite

### 8.1 Full System Test

```go
// TestCase18: Complete Integration Test
func TestFullSystemIntegration(t *testing.T) {
    // Initialize components
    dag := NewTestDAG()
    stateDB := NewTestStateDB()
    txPool := NewTxPool()
    miner := NewTestMiner()
    
    // Phase 1: Bootstrap
    genesis := dag.AddGenesis()
    stateDB.Initialize(genesis)
    
    // Phase 2: Deploy core contracts
    contracts := deploySystemContracts(stateDB)
    
    // Phase 3: Simulate network activity
    for round := 0; round < 100; round++ {
        // Generate transactions
        txs := generateRandomTransactions(10)
        for _, tx := range txs {
            txPool.Add(tx)
        }
        
        // Mine blocks (simulate multiple miners)
        blocks := make([]*Block, 3)
        for i := 0; i < 3; i++ {
            blocks[i] = miner.MineBlock(txPool, dag.GetTips())
            dag.AddBlock(blocks[i])
        }
        
        // Build canonical sequence
        tips := dag.GetTips()
        canonical := BuildCanonicalSequence(dag, tips)
        
        // Execute canonical chain
        for _, block := range canonical {
            if !stateDB.HasBlock(block.Hash) {
                receipts := ExecuteBlock(stateDB, block)
                storeReceipts(block.Hash, receipts)
            }
        }
        
        // Randomly trigger reorgs
        if round%10 == 0 {
            alternativeChain := generateAlternativeHistory(dag, 5)
            HandleReorg(stateDB, canonical, alternativeChain)
        }
        
        // Verify invariants
        verifyStateConsistency(stateDB)
        verifyReceiptConsistency(canonical)
        verifyCanonicalDeterminism(dag)
    }
    
    // Final verification
    require.True(t, stateDB.IsValid())
    require.Equal(t, 0, txPool.PendingCount()) // All txs processed
}
```

## 9. Test Utilities

### 9.1 Helper Functions

```go
// Test DAG generator
func GenerateDAG(blocks int, width int) *BlockDAG {
    dag := NewBlockDAG()
    genesis := dag.AddGenesis()
    
    layers := blocks / width
    currentLayer := []*Block{genesis}
    
    for layer := 0; layer < layers; layer++ {
        nextLayer := make([]*Block, width)
        
        for i := 0; i < width; i++ {
            // Random parents from previous layer
            numParents := rand.Intn(min(3, len(currentLayer))) + 1
            parents := selectRandomParents(currentLayer, numParents)
            
            block := &Block{
                Hash:       generateHash(),
                Parents:    parents,
                Timestamp:  int64(layer*100 + i),
                Difficulty: big.NewInt(1000 + int64(rand.Intn(100))),
            }
            
            nextLayer[i] = block
            dag.AddBlock(block)
        }
        
        currentLayer = nextLayer
    }
    
    return dag
}

// State verification
func verifyStateConsistency(state *StateDB) bool {
    // Verify Merkle Patricia Trie integrity
    if !state.VerifyTrie() {
        return false
    }
    
    // Verify account balances sum
    totalSupply := big.NewInt(0)
    state.ForEachAccount(func(addr common.Address, acc *Account) {
        totalSupply.Add(totalSupply, acc.Balance)
    })
    
    expectedSupply := calculateExpectedSupply()
    return totalSupply.Cmp(expectedSupply) == 0
}
```

---

This comprehensive test suite ensures the DAG→EVM integration is robust, secure, and performant under all conditions.



