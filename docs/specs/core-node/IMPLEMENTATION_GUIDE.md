# Core Blockchain Implementation Guide - Getting Started

**Status**: Implementation Roadmap  
**Purpose**: Step-by-step guide to start building BDP core node

---

## 🎯 The Core You're Building

**Main Deliverable**: `bdpd` - The Phoenix blockchain node daemon

**What it does**:
1. Runs GHOSTDAG consensus (Kaspa fork)
2. Integrates EVM execution (BSC fork)
3. Exposes JSON-RPC API
4. Mines blocks (dual algorithm: kHeavyHash + SHA-3)
5. Maintains DAG structure with canonical ordering

---

## 📦 Phase 1: Fork & Setup (Week 1)

### Step 1: Fork Kaspa Repository
```bash
# Clone Kaspa
git clone https://github.com/kaspanet/kaspad.git
cd kaspad

# Create new branch for Phoenix
git checkout -b phoenix-core

# Rename repository context
# (This is your starting point)
```

**What you get**: Complete GHOSTDAG implementation, P2P networking, block DAG structure

**What to change**:
- Rebrand: `kaspa` → `bdp` / `phoenix`
- Package names: `github.com/kaspanet/kaspad` → `github.com/blockdag-phoenix/bdp-node`
- Network parameters: chain ID, magic bytes, ports

---

### Step 2: Fork BSC EVM Layer
```bash
# Clone BSC
git clone https://github.com/bnb-chain/bsc.git
cd bsc

# Extract EVM layer
# Focus on: core/vm/, core/state/, core/types/
```

**What you get**: EVM execution engine, state management, transaction processing

**What to adapt**:
- Replace BSC's Parlia consensus with Phoenix's GHOSTDAG
- Adapt state management for DAG ordering
- Keep JSON-RPC compatibility

---

### Step 3: Create Phoenix Repository Structure
```bash
# Your new repository structure
bdp-node/
├── cmd/
│   ├── bdpd/           # Main daemon (from Kaspa)
│   └── bdp-cli/        # CLI tool (from Kaspa CLI)
├── app/
│   └── appmessage/     # Messages (rebranded)
├── domain/
│   ├── consensus/      # GHOSTDAG (from Kaspa)
│   ├── dag/            # DAG structure (from Kaspa)
│   ├── evm/            # EVM layer (from BSC)
│   └── canonical/      # Canonicalization (NEW - your unique code)
├── mining/
│   ├── kheavyhash/     # kHeavyHash (from Kaspa)
│   └── sha3/           # SHA-3 (NEW)
├── network/
│   └── protocol/       # P2P (from Kaspa)
└── rpc/
    └── server/         # JSON-RPC (from BSC/geth)
```

---

## 🔨 Phase 2: Core Implementation Order

### Week 1-2: Rebrand & Basic Fork

**Task 1: Rebrand Kaspa Codebase**
```go
// Find and replace across codebase:
// kaspa → bdp
// Kaspa → Phoenix
// kaspad → bdpd
// KASPA → BDP

// Update go.mod:
module github.com/blockdag-phoenix/bdp-node

// Update package imports:
import "github.com/blockdag-phoenix/bdp-node/domain/consensus"
```

**Files to modify**:
- `go.mod` - Module name
- All `*.go` files - Package names, imports
- `cmd/bdpd/main.go` - Entry point
- `app/protocol/protocol.go` - Network protocol

**Deliverable**: `bdpd` compiles and runs (Kaspa fork, rebranded)

---

### Week 3-4: Genesis Block & Network Parameters

**Task 2: Create Genesis Block**
```go
// File: domain/consensus/genesis/genesis.go
package genesis

import (
    "github.com/blockdag-phoenix/bdp-node/domain/consensus/model"
)

var GenesisBlock = &model.Block{
    Header: &model.BlockHeader{
        Version:    1,
        Parents:    nil, // No parents (genesis)
        Timestamp:  1704067200, // Jan 1, 2024
        Bits:       0x1e0ffff0, // Initial difficulty
        Algorithm:  model.AlgoKHeavyHash,
        BlueScore:  0,
    },
    Transactions: []*model.Transaction{
        genesisCoinbaseTx,
    },
}

// File: domain/consensus/genesis/params.go
package genesis

const (
    MainnetChainID = 888
    TestnetChainID = 8888
    
    MainnetMagic = 0xbdbd0000
    TestnetMagic = 0xbdbd0001
    
    TargetBlockTime = 1 * time.Second
    
    // Mining
    InitialBlockReward = 50 * 1e8 // 50 BDP (8 decimals)
    HalvingInterval   = 210000    // blocks
)
```

**Deliverable**: Genesis block configures Phoenix network

---

### Week 5-6: Dual Mining Algorithms

**Task 3: Implement SHA-3 Mining**
```go
// File: mining/sha3/sha3.go
package sha3

import (
    "github.com/ethereum/go-ethereum/crypto/sha3"
)

func Hash(data []byte) []byte {
    hash := sha3.NewLegacyKeccak256()
    hash.Write(data)
    return hash.Sum(nil)
}

func Verify(header []byte, nonce uint64, target *big.Int) bool {
    hash := Hash(append(header, uint64ToBytes(nonce)...))
    hashInt := new(big.Int).SetBytes(hash)
    return hashInt.Cmp(target) < 0
}
```

**Task 4: Add Algorithm Selection to Block**
```go
// File: domain/consensus/model/block.go
type Block struct {
    Header *BlockHeader
    Transactions []*Transaction
}

type BlockHeader struct {
    // ... existing fields ...
    Algorithm MiningAlgorithm // NEW: kHeavyHash or SHA-3
}

type MiningAlgorithm uint8

const (
    AlgoKHeavyHash MiningAlgorithm = iota
    AlgoSHA3
)
```

**Deliverable**: Both algorithms validate blocks

---

### Week 7-8: Canonicalization (Your Unique Code)

**Task 5: Implement DAG → Linear Ordering**
```go
// File: domain/canonical/ordering.go
package canonical

import (
    "github.com/blockdag-phoenix/bdp-node/domain/dag"
)

// GetCanonicalChain returns deterministic linear sequence from DAG
func GetCanonicalChain(dag *dag.BlockDAG, tip *dag.Block) []*dag.Block {
    // 1. Select tip set (maximize blue work)
    tipSet := selectTipSet(dag, tip)
    
    // 2. Build ordered chain
    ordered := make([]*dag.Block, 0)
    
    // Get all ancestors
    ancestors := dag.GetAncestors(tipSet)
    
    // Sort by blue score (descending), then timestamp, then hash
    sort.Slice(ancestors, func(i, j int) bool {
        if ancestors[i].BlueScore != ancestors[j].BlueScore {
            return ancestors[i].BlueScore > ancestors[j].BlueScore
        }
        if ancestors[i].Timestamp != ancestors[j].Timestamp {
            return ancestors[i].Timestamp < ancestors[j].Timestamp
        }
        return bytes.Compare(ancestors[i].Hash[:], ancestors[j].Hash[:]) < 0
    })
    
    // Ensure topological order (parents before children)
    ordered = topologicalSort(ancestors)
    
    return ordered
}

// Map canonical index to block.number for EVM
func GetBlockNumber(canonicalChain []*dag.Block, block *dag.Block) uint64 {
    for i, b := range canonicalChain {
        if b.Hash == block.Hash {
            return uint64(i)
        }
    }
    return 0
}
```

**Deliverable**: Deterministic canonical ordering from DAG

---

### Week 9-10: EVM Integration

**Task 6: Integrate BSC EVM Layer**
```go
// File: domain/evm/executor.go
package evm

import (
    "github.com/blockdag-phoenix/bdp-node/domain/canonical"
    "github.com/blockdag-phoenix/bdp-node/domain/dag"
    "github.com/ethereum/go-ethereum/core"
    "github.com/ethereum/go-ethereum/core/vm"
    "github.com/ethereum/go-ethereum/core/state"
)

type Executor struct {
    dag            *dag.BlockDAG
    canonicalizer  *canonical.Ordering
    chainConfig    *params.ChainConfig
    stateDB        *state.StateDB
}

// ExecuteBlock executes transactions in canonical order
func (e *Executor) ExecuteBlock(block *dag.Block) (*ExecutionResult, error) {
    // 1. Get canonical chain up to this block
    canonicalChain := e.canonicalizer.GetCanonicalChain(e.dag, block)
    
    // 2. Rebuild state from genesis to this block
    stateRoot := e.replayState(canonicalChain)
    
    // 3. Execute this block's transactions
    for _, tx := range block.Transactions {
        receipt, err := e.executeTransaction(tx, stateRoot)
        if err != nil {
            return nil, err
        }
    }
    
    return result, nil
}

// ReplayState rebuilds state by executing canonical chain
func (e *Executor) replayState(canonicalChain []*dag.Block) common.Hash {
    stateDB := state.New(genesisRoot, nil)
    
    for _, block := range canonicalChain {
        for _, tx := range block.Transactions {
            // Execute transaction
            applyTransaction(stateDB, tx)
        }
    }
    
    return stateDB.IntermediateRoot(false)
}
```

**Deliverable**: EVM executes transactions in canonical order

---

### Week 11-12: JSON-RPC Server

**Task 7: Expose Ethereum-Compatible RPC**
```go
// File: rpc/server/server.go
package rpc

import (
    "github.com/ethereum/go-ethereum/rpc"
    "github.com/blockdag-phoenix/bdp-node/domain/evm"
)

type Server struct {
    node *Node
    evm  *evm.Executor
}

// Start JSON-RPC server
func (s *Server) Start() error {
    rpcServer := rpc.NewServer()
    
    // Register Ethereum-compatible APIs
    rpcServer.RegisterName("eth", &EthAPI{s.node, s.evm})
    rpcServer.RegisterName("web3", &Web3API{})
    rpcServer.RegisterName("net", &NetAPI{s.node})
    
    // Phoenix-specific APIs
    rpcServer.RegisterName("bdp", &BDPAPI{s.node})
    
    // Start HTTP server
    return http.ListenAndServe(":16111", rpcServer)
}

// EthAPI implements Ethereum JSON-RPC
type EthAPI struct {
    node *Node
    evm  *evm.Executor
}

func (api *EthAPI) GetBlockByNumber(ctx context.Context, blockNumber rpc.BlockNumber) (map[string]interface{}, error) {
    // Get canonical block at number
    canonicalChain := api.node.GetCanonicalChain()
    if int(blockNumber) >= len(canonicalChain) {
        return nil, errors.New("block not found")
    }
    
    block := canonicalChain[blockNumber]
    
    // Map to Ethereum header format
    return map[string]interface{}{
        "number":           blockNumber,
        "hash":            block.Hash.Hex(),
        "parentHash":      block.ParentHash.Hex(),
        "stateRoot":       block.StateRoot.Hex(),
        "transactionsRoot": block.TransactionsRoot.Hex(),
        "receiptsRoot":    block.ReceiptsRoot.Hex(),
        "timestamp":       block.Timestamp,
        "gasLimit":        block.GasLimit,
        "gasUsed":         block.GasUsed,
        // ... other fields
    }, nil
}
```

**Deliverable**: JSON-RPC server responds to Ethereum-compatible requests

---

## 📋 Core Implementation Checklist

### Phase 1: Foundation (Weeks 1-4)
- [ ] Fork Kaspa repository
- [ ] Rebrand codebase (kaspa → bdp)
- [ ] Update go.mod and package names
- [ ] Create genesis block configuration
- [ ] Set network parameters (chain ID, magic bytes, ports)
- [ ] Test: `bdpd` compiles and runs

### Phase 2: Mining (Weeks 5-6)
- [ ] Implement SHA-3 algorithm
- [ ] Add algorithm field to block header
- [ ] Implement dual difficulty tracking
- [ ] Test: Both algorithms mine blocks

### Phase 3: Canonicalization (Weeks 7-8)
- [ ] Implement DAG → linear ordering
- [ ] Handle reorgs (delta replay)
- [ ] Map canonical index to block.number
- [ ] Test: Deterministic ordering across nodes

### Phase 4: EVM Integration (Weeks 9-10)
- [ ] Fork/extract BSC EVM layer
- [ ] Integrate canonical ordering → EVM execution
- [ ] Implement state replay
- [ ] Test: Deploy simple contract

### Phase 5: RPC (Weeks 11-12)
- [ ] Implement JSON-RPC server
- [ ] Expose Ethereum-compatible methods
- [ ] Add Phoenix-specific methods (getDAGInfo, etc.)
- [ ] Test: Hardhat connects to Phoenix

---

## 🎯 Minimum Viable Core (MVP)

**To get a working testnet, you need**:

1. ✅ **Kaspa fork** (GHOSTDAG consensus) - **Week 1-2**
2. ✅ **Genesis block** - **Week 2**
3. ✅ **Dual mining** (kHeavyHash + SHA-3) - **Week 5-6**
4. ✅ **Canonicalization** (DAG → linear) - **Week 7-8**
5. ✅ **Basic EVM** (execute contracts) - **Week 9-10**
6. ✅ **JSON-RPC** (deploy contracts) - **Week 11-12**

**Timeline**: 12 weeks (3 months) to MVP core

---

## 🔧 Key Files to Create First

### 1. `cmd/bdpd/main.go` (Entry Point)
```go
package main

import (
    "github.com/blockdag-phoenix/bdp-node/cmd/bdpd/config"
    "github.com/blockdag-phoenix/bdp-node/app/appmessage"
    "github.com/blockdag-phoenix/bdp-node/domain/consensus"
)

func main() {
    cfg := config.Load()
    
    node, err := consensus.NewNode(cfg)
    if err != nil {
        panic(err)
    }
    
    if err := node.Start(); err != nil {
        panic(err)
    }
    
    // Wait for shutdown
    <-node.ShutdownChan()
}
```

### 2. `domain/consensus/genesis/genesis.go` (Genesis Block)
```go
package genesis

var GenesisBlock = &Block{
    // ... (see above)
}
```

### 3. `domain/canonical/ordering.go` (Your Unique Code)
```go
package canonical

func GetCanonicalChain(dag *dag.BlockDAG, tip *dag.Block) []*dag.Block {
    // ... (see above)
}
```

---

## 🚀 Start Here

**Right now, start with**:

1. **Fork Kaspa**: `git clone https://github.com/kaspanet/kaspad.git`
2. **Rename**: Create new repo `github.com/blockdag-phoenix/bdp-node`
3. **Rebrand**: Replace `kaspa` → `bdp` in codebase
4. **Test**: Make sure it compiles (`go build ./cmd/bdpd`)

**This gives you**: Working GHOSTDAG consensus (your foundation)

**Then add**: Genesis block, dual mining, canonicalization, EVM

---

## 📚 Reference Implementation Order

1. **Kaspa** → Core consensus (start here)
2. **Genesis** → Network bootstrap (week 2)
3. **SHA-3** → Dual mining (week 5)
4. **Canonicalization** → Your unique code (week 7)
5. **BSC EVM** → Smart contracts (week 9)
6. **RPC** → Developer access (week 11)

---

**Ready to code?** Start with Step 1: Fork Kaspa and rebrand. Everything else builds on that foundation.






