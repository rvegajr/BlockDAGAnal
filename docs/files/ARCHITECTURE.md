# Technical Architecture

## System Overview

DBP is a directed acyclic graph (DAG) blockchain forked from Kaspa, enhanced with smart contract capabilities through EVM integration, and supporting dual mining algorithms for hardware flexibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Application Layer                    │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Mobile     │  │  Web Wallet  │  │    dApps     │       │
│  │  Wallet     │  │              │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   RPC API   │  │  GraphQL API │  │  WebSocket   │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Smart Contract Layer                    │
│  ┌─────────────────────────────────────────────────┐        │
│  │           EVM (Ethereum Virtual Machine)         │        │
│  │  ┌──────────────┐  ┌──────────────────────┐    │        │
│  │  │   Solidity   │  │   State Management   │    │        │
│  │  │  Contracts   │  │   (Account Model)    │    │        │
│  │  └──────────────┘  └──────────────────────┘    │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Consensus Layer                         │
│  ┌─────────────────────────────────────────────────┐        │
│  │         GHOSTDAG Protocol (from Kaspa)          │        │
│  │  ┌──────────────┐  ┌──────────────────────┐    │        │
│  │  │   Block DAG  │  │  Transaction         │    │        │
│  │  │   Structure  │  │  Ordering            │    │        │
│  │  └──────────────┘  └──────────────────────┘    │        │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       Mining Layer                           │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │   kHeavyHash       │  │      SHA-3         │            │
│  │   (Kaspa-compat)   │  │   (BlockDAG-compat)│            │
│  └────────────────────┘  └────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Network Layer                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   P2P Node  │  │  Block       │  │  Transaction │       │
│  │   Network   │  │  Propagation │  │  Mempool     │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Consensus Layer (GHOSTDAG)

**Source**: Kaspa's GHOSTDAG implementation (Golang)

**Key Features**:
- Parallel block creation (no single chain)
- PHANTOM protocol for block ordering
- High throughput (blocks per second, not minutes)
- Byzantine fault tolerance
- Eventual consistency

**How It Works**:
```go
// Simplified GHOSTDAG logic
type Block struct {
    Hash        []byte
    Parents     [][]byte    // Multiple parents (DAG structure)
    Timestamp   int64
    Transactions []*Transaction
    BlueScore   uint64      // GHOSTDAG ordering score
}

// Block acceptance
func (dag *BlockDAG) AcceptBlock(block *Block) error {
    // 1. Validate block structure
    if err := dag.ValidateBlock(block); err != nil {
        return err
    }
    
    // 2. Add to DAG (multiple parents allowed)
    dag.AddToDAG(block)
    
    // 3. Run GHOSTDAG ordering
    dag.RecomputeBlueScore()
    
    // 4. Update UTXO set
    dag.ApplyTransactions(block)
    
    return nil
}
```

**Benefits**:
- No orphaned blocks (all blocks count)
- High transaction throughput
- Fast confirmation times
- Scalable design

### 2. Smart Contract Layer (EVM Integration)

**Challenge**: EVM expects linear blockchain, DAG is parallel

**Solution**: Ordered transaction execution on DAG

```go
type SmartContractEngine struct {
    EVM         *vm.EVM           // go-ethereum EVM
    StateDB     *state.StateDB    // Account state
    DAG         *BlockDAG         // Reference to DAG
    ChainConfig *params.ChainConfig
}

// Process smart contract transaction in DAG context
func (sc *SmartContractEngine) ExecuteTransaction(
    tx *Transaction, 
    block *Block,
) (*Receipt, error) {
    // 1. Get ordered parent blocks (GHOSTDAG ordering)
    orderedBlocks := sc.DAG.GetOrderedChain()
    
    // 2. Rebuild state from genesis to this block
    stateRoot := sc.ReplayState(orderedBlocks)
    
    // 3. Execute transaction in EVM
    receipt, err := sc.EVM.ApplyTransaction(tx, stateRoot)
    
    return receipt, err
}
```

**State Management**:
```
Genesis Block
     │
     ▼
Block 1 ──┐
     │    │
     ▼    ▼
Block 2  Block 3  (parallel blocks)
     │    │
     └────┴──▶ GHOSTDAG orders: [1, 2, 3] or [1, 3, 2]
                │
                ▼
         State = replay(Genesis → 1 → 2 → 3)
```

**Key Implementation Details**:
- State is deterministic (same order = same state)
- GHOSTDAG provides canonical ordering
- EVM sees linear history (DAG is abstracted)
- Gas costs same as Ethereum

### 3. Dual Mining Algorithm System

**Why Dual Algorithm?**
- kHeavyHash: Kaspa compatibility (existing miners)
- SHA-3: BlockDAG hardware support (capture that market)
- Flexibility: Miners can choose hardware
- Security: Combined hashrate protects network

**Implementation**:

```go
type MiningAlgorithm int

const (
    AlgoKHeavyHash MiningAlgorithm = iota
    AlgoSHA3
)

type Block struct {
    // ... other fields
    Algorithm   MiningAlgorithm
    Difficulty  *big.Int
}

// Separate difficulty tracking
type DifficultyManager struct {
    kHeavyHashDifficulty *big.Int
    sha3Difficulty       *big.Int
    targetBlockTime      time.Duration
}

func (dm *DifficultyManager) AdjustDifficulty(
    algo MiningAlgorithm,
    recentBlocks []*Block,
) *big.Int {
    // Filter blocks by algorithm
    algoBlocks := filterByAlgorithm(recentBlocks, algo)
    
    // Calculate average block time for this algo
    avgTime := calculateAvgBlockTime(algoBlocks)
    
    // Adjust difficulty for this specific algorithm
    if avgTime < dm.targetBlockTime {
        // Too fast, increase difficulty
        return increaseDifficulty(dm.getDifficulty(algo))
    } else {
        // Too slow, decrease difficulty
        return decreaseDifficulty(dm.getDifficulty(algo))
    }
}

func (dm *DifficultyManager) ValidateBlock(block *Block) error {
    // Get difficulty for block's algorithm
    difficulty := dm.getDifficulty(block.Algorithm)
    
    // Compute hash based on algorithm
    var hash []byte
    switch block.Algorithm {
    case AlgoKHeavyHash:
        hash = kHeavyHash(block.Header())
    case AlgoSHA3:
        hash = sha3.Sum256(block.Header())
    }
    
    // Verify hash meets difficulty
    if !hashMeetsDifficulty(hash, difficulty) {
        return ErrInsufficientDifficulty
    }
    
    return nil
}
```

**Mining Reward Calculation**:
```go
func CalculateBlockReward(
    blockHeight uint64,
    algorithm MiningAlgorithm,
) uint64 {
    // Base reward (same for both algorithms)
    baseReward := GetBaseReward(blockHeight)
    
    // Optional: Adjust for algorithm difficulty ratio
    // (if one algorithm is consistently harder)
    difficultyRatio := GetDifficultyRatio(algorithm)
    
    return baseReward * difficultyRatio / 100
}
```

### 4. Network Layer

**P2P Protocol**: Kaspa's libp2p-based networking

**Node Types**:
- **Full Nodes**: Store entire DAG, validate all blocks
- **Mining Nodes**: Full node + mining capability
- **Light Nodes**: SPV-style verification (future)
- **Archive Nodes**: Historical data retention

**Block Propagation**:
```go
// Gossip protocol for block distribution
func (n *Node) BroadcastBlock(block *Block) {
    // Send to connected peers
    for _, peer := range n.peers {
        go peer.SendBlock(block)
    }
    
    // Peers further propagate (gossip)
}

// Receive and validate
func (n *Node) OnReceiveBlock(block *Block, peer *Peer) {
    // Validate block
    if err := n.dag.ValidateBlock(block); err != nil {
        n.penalizePeer(peer)
        return
    }
    
    // Add to DAG
    n.dag.AddBlock(block)
    
    // Propagate to other peers (except sender)
    n.BroadcastBlockExcept(block, peer)
}
```

### 5. Transaction Processing

**Transaction Structure**:
```go
type Transaction struct {
    Version  uint32
    Inputs   []*TxInput
    Outputs  []*TxOutput
    GasLimit uint64          // For smart contract calls
    GasPrice *big.Int        // Gas price in DBP
    Data     []byte          // Smart contract data
    Signature []byte
}

type TxInput struct {
    PreviousTxID []byte
    Index        uint32
    ScriptSig    []byte
}

type TxOutput struct {
    Value        uint64
    ScriptPubKey []byte  // Or account address for EVM
}
```

**Transaction Types**:
1. **Native Transfers**: UTXO-based (Kaspa model)
2. **Smart Contract Calls**: Account-based (Ethereum model)
3. **Contract Deployments**: Create new contracts
4. **Hybrid**: Transfer + contract interaction

**Mempool**:
```go
type Mempool struct {
    transactions map[string]*Transaction
    maxSize      int
    feeQueue     *PriorityQueue  // Order by fee
}

func (mp *Mempool) AddTransaction(tx *Transaction) error {
    // Validate transaction
    if err := ValidateTransaction(tx); err != nil {
        return err
    }
    
    // Check for double spends
    if mp.hasDoubleSpend(tx) {
        return ErrDoubleSpend
    }
    
    // Add to mempool (fee-ordered)
    mp.feeQueue.Push(tx, tx.GasPrice)
    
    return nil
}
```

## Data Structures

### Block Structure
```go
type Block struct {
    Header    *BlockHeader
    Transactions []*Transaction
}

type BlockHeader struct {
    Version       uint32
    Parents       [][]byte      // Multiple parents (DAG)
    HashMerkleRoot []byte       // Transaction merkle root
    Timestamp     int64
    Bits          uint32        // Difficulty target
    Nonce         uint64        // Mining nonce
    Algorithm     MiningAlgorithm
    
    // GHOSTDAG fields
    BlueScore     uint64
    BlueWork      *big.Int
    SelectedParent []byte
}
```

### DAG State
```go
type BlockDAG struct {
    blocks        map[string]*Block
    tips          []*Block        // Current DAG tips
    genesis       *Block
    
    // GHOSTDAG data
    blueScores    map[string]uint64
    ordering      []*Block        // Canonical block order
    
    // UTXO set
    utxoSet       *UTXOSet
    
    // Smart contract state
    stateDB       *state.StateDB
}
```

## Key Algorithms

### GHOSTDAG Block Ordering
```
1. Start from genesis block
2. For each new block:
   a. Identify all parent blocks
   b. Compute "blue set" (honest chain)
   c. Compute "red set" (late/conflicting blocks)
   d. Assign blue score (order metric)
3. Result: Canonical ordering of all blocks
```

### Difficulty Adjustment (Per Algorithm)
```
1. Look at last N blocks for this algorithm
2. Calculate average block time
3. Compare to target (e.g., 1 block/second)
4. Adjust difficulty:
   - If too fast: difficulty *= 1.05
   - If too slow: difficulty *= 0.95
5. Clamp adjustment (max 4x change per period)
```

### Smart Contract State Transition
```
1. Get current state root
2. For each transaction in block order:
   a. Load contract code
   b. Execute in EVM
   c. Update account balances
   d. Store state changes
3. Compute new state root (merkle tree)
4. Persist to database
```

## Performance Characteristics

### Throughput
- **Target**: 10-100 blocks per second
- **Transaction capacity**: 1000+ tx/s
- **Confirmation time**: 1-5 seconds (fast)
- **Finality**: Probabilistic (like Bitcoin)

### Scalability
- **Block size**: 1-2 MB
- **Gas limit**: 30M per block (like Ethereum)
- **State growth**: Requires pruning/archival nodes
- **Network bandwidth**: 10-100 Mbps for full nodes

### Security
- **51% attack resistance**: Yes (PoW)
- **Double spend protection**: GHOSTDAG consensus
- **Smart contract safety**: EVM security model
- **Network security**: Combined hashrate from dual algorithms

## Technical Dependencies

### Core Libraries
- **kaspad**: Kaspa node implementation (Go)
- **go-ethereum**: EVM and state management (Go)
- **libp2p**: P2P networking (Go)
- **btcd**: Bitcoin utilities (Go)

### Database
- **LevelDB**: Block and state storage
- **Considerations**: RocksDB for better performance

### Cryptography
- **kHeavyHash**: Custom Kaspa hash function
- **SHA-3**: Standard cryptographic hash
- **secp256k1**: Elliptic curve (same as Bitcoin/Ethereum)

## Deployment Architecture

### Node Deployment
```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼───┐
│ Node 1│ │ Node 2│ │ Node 3│ │ Node N│
│ (RPC) │ │ (RPC) │ │ (RPC) │ │ (RPC) │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │        │        │
    └─────────┴────────┴────────┘
              │
      ┌───────▼────────┐
      │  P2P Network   │
      │  (All Nodes)   │
      └────────────────┘
```

### Infrastructure Requirements

**Single Full Node**:
- CPU: 4+ cores
- RAM: 8GB minimum, 16GB recommended
- Storage: 500GB SSD (growing)
- Network: 100 Mbps, unmetered
- Cost: ~$50/month (VPS)

**Mining Node**:
- Same as full node
- Plus: GPU/ASIC hardware
- Power: Depends on mining hardware

**API Node (Public RPC)**:
- CPU: 8+ cores
- RAM: 32GB+
- Storage: 1TB SSD
- Network: 1 Gbps
- Cost: ~$200/month

## Future Enhancements

### Planned Features
1. **Layer 2**: Payment channels, sidechains
2. **Cross-chain bridges**: Ethereum, Bitcoin
3. **Privacy**: Optional zk-SNARKs
4. **Sharding**: Horizontal scalability
5. **Light clients**: Mobile-friendly SPV

### Research Areas
1. **State rent**: Limit state growth
2. **Account abstraction**: Advanced contract wallets
3. **MEV protection**: Fair transaction ordering
4. **Quantum resistance**: Post-quantum cryptography

## References

### Academic Papers
- PHANTOM: "PHANTOM: A Scalable BlockDAG Protocol"
- GHOSTDAG: "GHOSTDAG: A Scalable BlockDAG Protocol"
- GhostDAG ordering: Kaspa implementation

### Codebases
- Kaspa: https://github.com/kaspanet/kaspad
- Go-Ethereum: https://github.com/ethereum/go-ethereum
- BlockDAG (reference): Documentation only

### Standards
- EVM: Ethereum Yellow Paper
- EIP standards: Ethereum Improvement Proposals
- DAG consensus: Academic literature

---

*This architecture document is living documentation and will evolve as the project develops.*
