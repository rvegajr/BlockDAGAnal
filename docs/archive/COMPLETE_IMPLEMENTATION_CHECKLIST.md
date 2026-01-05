# BlockDAG Phoenix: Complete Implementation Checklist
## ✅ From Specifications to Production-Ready System

**Version**: 1.0  
**Date**: November 23, 2025  
**Purpose**: Comprehensive checklist covering ALL features from specifications  
**Status Legend**: ✅ Done | ⚠️ Partial | ❌ Not Started | 🔄 In Progress

---

## 📋 TABLE OF CONTENTS

1. [P0: Critical Path (Core Functionality)](#p0-critical-path)
2. [P1: High Priority (Essential Features)](#p1-high-priority)
3. [P2: Medium Priority (Important Features)](#p2-medium-priority)
4. [P3: Nice to Have (Optional Features)](#p3-nice-to-have)
5. [Testing Requirements](#testing-requirements)
6. [Security & Compliance](#security--compliance)
7. [Operations & Infrastructure](#operations--infrastructure)
8. [Developer Experience](#developer-experience)
9. [Timeline Estimates](#timeline-estimates)

---

## P0: CRITICAL PATH (Core Functionality)
### Must be 100% complete before testnet launch

### 1. CORE CONSENSUS LAYER
**Spec**: `docs/specs/core-node/CONSENSUS.md`  
**Status**: ✅ **100% COMPLETE** (Kaspa fork)

- [x] GHOSTDAG consensus algorithm
- [x] Blue/red block classification
- [x] DAG topology management
- [x] Block validation
- [x] Transaction validation
- [x] Difficulty adjustment (DAA)
- [x] Proof-of-work verification
- [x] Mempool management
- [x] UTXO tracking
- [x] Pruning mechanism

**Location**: `phoenix-node/domain/consensus/`  
**Effort**: DONE (inherited from Kaspa)

---

### 2. CANONICALIZATION (DAG→LINEAR)
**Spec**: `docs/specs/core-node/CANONICALIZATION_DETAILED.md`  
**Status**: ⚠️ **90% COMPLETE** - Needs testing

#### Core Algorithm
- [x] Tip selection with blue score
- [x] Topological ordering (Kahn's algorithm)
- [x] Deterministic tie-breaking (blueScore → timestamp → hash)
- [x] DAG adapter implementation
- [x] Caching layer

#### Missing/Needs Work
- [ ] **Deep reorg testing** (depth 100+ blocks) - 6 hours
  - Test fork detection
  - Test state rollback
  - Test transaction reinjection
  - Validate determinism across reorgs

- [ ] **Performance profiling** - 4 hours
  - Benchmark with 100k+ blocks
  - Measure canonicalization latency
  - Optimize bottlenecks
  - Target: <10ms for tip selection

- [ ] **Edge case handling** - 4 hours
  - Simultaneous tips with equal blue score
  - Timestamp attacks (median time enforcement)
  - Clock skew scenarios
  - Network partition recovery

**Location**: `phoenix-node/domain/canonical/`  
**Effort**: 14 hours remaining

---

### 3. EVM EXECUTION ENGINE
**Spec**: `docs/specs/evm/EXECUTION.md`  
**Status**: ⚠️ **85% COMPLETE**

#### Working
- [x] go-ethereum v1.12.2 integration
- [x] EVM execution (London fork)
- [x] StateDB (Merkle Patricia Trie)
- [x] Transaction conversion (UTXO→Account)
- [x] Block context creation
- [x] Gas calculation

#### Critical Missing Features

##### A. Transaction Receipts ❌ **CRITICAL**
- [ ] Create receipt store - 1 hour
  ```go
  // domain/evm/receipts.go
  type ReceiptStore interface {
      StoreReceipt(txHash common.Hash, receipt *Receipt) error
      GetReceipt(txHash common.Hash) (*Receipt, error)
      GetReceipts(blockHash common.Hash) ([]*Receipt, error)
  }
  ```
- [ ] Generate receipts after execution - 0.5 hour
- [ ] Store receipts in database - 0.5 hour
- [ ] Wire to RPC `eth_getTransactionReceipt` - 1 hour
- [ ] Add receipt root calculation - 1 hour

**Subtotal**: 4 hours

##### B. Event Log Indexing ❌ **CRITICAL**
- [ ] Create log index store - 1 hour
  ```go
  // domain/evm/logs.go
  type LogIndex interface {
      IndexLogs(blockNum uint64, logs []*types.Log) error
      GetLogs(filter FilterCriteria) ([]*types.Log, error)
      DeleteLogsForBlock(blockNum uint64) error // for reorgs
  }
  ```
- [ ] Index logs after execution - 0.5 hour
- [ ] Implement `eth_getLogs` RPC - 2 hours
- [ ] Add bloom filter support - 1.5 hours
- [ ] Log filtering by address/topics - 1 hour

**Subtotal**: 6 hours

##### C. State Checkpointing ❌ **CRITICAL**
- [ ] Checkpoint manager implementation - 4 hours
  ```go
  // domain/evm/checkpoint.go
  type CheckpointManager interface {
      CreateCheckpoint(blockNum uint64) error
      RestoreCheckpoint(blockNum uint64) (*state.StateDB, error)
      PruneCheckpoints(keepLast int) error
  }
  ```
- [ ] Automatic checkpoint creation (every 1000 blocks) - 2 hours
- [ ] Checkpoint restoration logic - 2 hours
- [ ] Storage optimization (compress old checkpoints) - 2 hours

**Subtotal**: 10 hours

##### D. Genesis State Initialization ⚠️ **HIGH**
- [ ] Genesis account allocation - 1 hour
  ```go
  // domain/evm/genesis.go
  type GenesisAllocation struct {
      Address common.Address
      Balance *big.Int
      Code    []byte // For predeployed contracts
      Nonce   uint64
  }
  ```
- [ ] Initial balance distribution - 0.5 hour
- [ ] Genesis state root calculation - 0.5 hour
- [ ] Configuration file support - 1 hour

**Subtotal**: 3 hours

##### E. Gas Fee Distribution ⚠️ **MEDIUM**
- [ ] Collect gas fees to miner/coinbase - 0.5 hour
  ```go
  // In ExecuteTransaction:
  gasUsed := result.UsedGas
  gasPrice := msg.GasPrice()
  fee := new(big.Int).Mul(big.NewInt(int64(gasUsed)), gasPrice)
  stateDB.AddBalance(coinbase, fee)
  ```
- [ ] Track total fees per block - 0.5 hour
- [ ] Add to block rewards - 0.5 hour

**Subtotal**: 1.5 hours

##### F. Signature Extraction & Validation ⚠️ **HIGH**
- [ ] Extract sender from ECDSA signature - 2 hours
  ```go
  // domain/evm/txconverter.go
  func ExtractSender(tx *types.Transaction) (common.Address, error) {
      signer := types.LatestSignerForChainID(chainID)
      return types.Sender(signer, tx)
  }
  ```
- [ ] Validate signature before execution - 0.5 hour
- [ ] Handle EIP-155 (replay protection) - 1 hour
- [ ] Support legacy and EIP-1559 transactions - 1.5 hours

**Subtotal**: 5 hours

**Total EVM Execution Effort**: 29.5 hours

---

### 4. JSON-RPC SERVER (Ethereum Compatible)
**Spec**: `docs/specs/evm/RPC.md`  
**Status**: ⚠️ **85% COMPLETE**

#### Working Methods
- [x] `eth_blockNumber` ✅
- [x] `eth_getBalance` ✅ (returns 0, needs StateDB integration)
- [x] `eth_getCode` ✅ (stub)
- [x] `eth_call` ✅ (stub)
- [x] `eth_sendTransaction` ✅ (stub)
- [x] `eth_gasPrice` ✅
- [x] `eth_estimateGas` ✅
- [x] `eth_getBlockByNumber` ✅
- [x] `eth_getBlockByHash` ✅
- [x] `web3_clientVersion` ✅
- [x] `web3_sha3` ✅
- [x] `net_version` ✅
- [x] `net_listening` ✅
- [x] `net_peerCount` ✅

#### Missing/Needs Implementation

##### Required Methods ❌
- [ ] `eth_getTransactionReceipt` - 2 hours (depends on receipts)
- [ ] `eth_getLogs` - 3 hours (depends on log indexing)
- [ ] `eth_getTransactionByHash` - 1 hour
- [ ] `eth_getTransactionByBlockHashAndIndex` - 0.5 hour
- [ ] `eth_getTransactionByBlockNumberAndIndex` - 0.5 hour
- [ ] `eth_getTransactionCount` (nonce) - 1 hour
- [ ] `eth_sendRawTransaction` - 2 hours (full implementation with mempool)
- [ ] `eth_getBlockTransactionCountByHash` - 0.5 hour
- [ ] `eth_getBlockTransactionCountByNumber` - 0.5 hour
- [ ] `eth_getStorageAt` - 1 hour
- [ ] `eth_newFilter` / `eth_newBlockFilter` / `eth_newPendingTransactionFilter` - 3 hours
- [ ] `eth_getFilterChanges` / `eth_getFilterLogs` / `eth_uninstallFilter` - 2 hours

**Subtotal Required**: 17.5 hours

##### Optional but Highly Recommended ⚠️
- [ ] `eth_feeHistory` (EIP-1559) - 2 hours
- [ ] `eth_maxPriorityFeePerGas` - 1 hour
- [ ] `eth_chainId` - 0.25 hour
- [ ] `eth_accounts` - 0.25 hour (return empty for security)
- [ ] `eth_sign` - 0.5 hour (or disable for security)

**Subtotal Optional**: 4 hours

##### Debug/Trace Methods (Optional) ⚠️
- [ ] `debug_traceTransaction` - 6 hours
- [ ] `debug_traceBlock` - 4 hours
- [ ] `debug_traceCall` - 4 hours
- [ ] `trace_transaction` (OpenEthereum style) - 6 hours

**Subtotal Debug**: 20 hours (optional)

##### Phoenix-Specific Methods ✅
- [ ] `phoenix_getDAGInfo` - 2 hours
  ```typescript
  interface DAGInfo {
      blueScore: number;
      parents: string[];
      blueBlockCount: number;
      redBlockCount: number;
  }
  ```
- [ ] `phoenix_getBlueScore` - 0.5 hour

**Subtotal Phoenix**: 2.5 hours

**Location**: `phoenix-node/app/rpc/ethrpc/`  
**Total RPC Effort**: 24 hours (required) + 24 hours (optional) = **48 hours**

---

### 5. REORG HANDLING
**Spec**: `docs/specs/core-node/REORG_HANDLING.md`  
**Status**: ⚠️ **50% COMPLETE** - Exists but untested

#### Core Components
- [x] Fork detection basic logic
- [ ] **Complete reorg handler** - 6 hours
  ```go
  // domain/evm/reorg.go
  type ReorgHandler interface {
      DetectFork(oldChain, newChain []*Block) (*ForkPoint, error)
      RewindState(fromBlock, toBlock uint64) error
      ReplayBlocks(blocks []*Block) error
      ReinjectOrphanedTxs(txs []*Transaction) error
  }
  ```

#### Implementation Tasks
- [ ] Fork point detection - 2 hours
- [ ] State rollback to checkpoint - 2 hours
- [ ] Block replay with state updates - 3 hours
- [ ] Transaction reinjection to mempool - 2 hours
- [ ] Receipt/log updates after reorg - 2 hours
- [ ] Event emission for reorg notification - 1 hour
- [ ] RPC client notifications - 1 hour

#### Policy & Limits
- [ ] Max reorg depth configuration (100 blocks) - 0.5 hour
- [ ] Reorg telemetry/metrics - 1 hour
- [ ] Emergency halt on deep reorg - 0.5 hour

**Location**: `phoenix-node/domain/evm/reorg.go` (create)  
**Total Reorg Effort**: 15 hours

---

### 6. BLOCK HEADER MAPPING
**Spec**: `docs/specs/core-node/BLOCK_HEADER.md`  
**Status**: ⚠️ **70% COMPLETE**

#### EVM-Visible Fields
- [x] `number` (canonical block number) ✅
- [x] `hash` (block hash) ✅
- [x] `parentHash` ✅ (simplified, needs canonical parent)
- [x] `timestamp` ✅
- [x] `gasLimit` ✅ (hardcoded, needs dynamic)
- [x] `gasUsed` ✅ (returns 0, needs calculation)
- [x] `miner` / `coinbase` ✅ (returns 0x0, needs extraction)
- [ ] `stateRoot` - 1 hour (calculate from StateDB)
- [ ] `transactionsRoot` - 1 hour (Merkle root of txs)
- [ ] `receiptsRoot` - 1 hour (Merkle root of receipts)
- [ ] `logsBloom` - 1 hour (bloom filter of all logs)
- [ ] `difficulty` - 0.5 hour (map from DAG difficulty)
- [ ] `totalDifficulty` - 0.5 hour (cumulative)
- [ ] `extraData` - 0.25 hour
- [ ] `nonce` - 0.25 hour (PoW nonce)
- [ ] `baseFeePerGas` (EIP-1559) - 2 hours
- [ ] `mixHash` - 0.25 hour

#### DAG-Specific Fields (Phoenix Extensions)
- [ ] `parents` (array of parent hashes) - 0.5 hour
- [ ] `blueScore` - 0.25 hour
- [ ] `algorithm` (kHeavyHash or SHA-3) - 0.25 hour
- [ ] `blueWork` - 0.5 hour

**Location**: `phoenix-node/domain/evm/block_header.go`  
**Total Header Effort**: 9 hours

---

### P0 SUMMARY
| Component | Status | Effort Remaining |
|-----------|--------|------------------|
| Consensus | ✅ 100% | 0 hours |
| Canonicalization | ⚠️ 90% | 14 hours |
| EVM Execution | ⚠️ 85% | 29.5 hours |
| JSON-RPC | ⚠️ 85% | 24 hours |
| Reorg Handling | ⚠️ 50% | 15 hours |
| Block Headers | ⚠️ 70% | 9 hours |

**P0 Total Remaining**: **91.5 hours** (~2.5 weeks with 2 developers)

---

## P1: HIGH PRIORITY (Essential Features)
### Needed for quality testnet and mainnet preparation

### 7. MINING INFRASTRUCTURE
**Spec**: `docs/specs/mining/ALGORITHMS.md`, `docs/specs/mining/POOL_PROTOCOL.md`  
**Status**: ✅ **100% COMPLETE** (Kaspa inheritance)

- [x] kHeavyHash algorithm
- [x] SHA-3 algorithm
- [x] Dual difficulty tracking
- [x] Block template generation
- [x] Mining loop
- [x] Stratum protocol support

**Location**: `phoenix-node/cmd/kaspaminer/`, `phoenix-node/domain/miningmanager/`  
**Effort**: DONE

---

### 8. MINING POOL SOFTWARE
**Spec**: `docs/specs/pool/POOL_SOFTWARE.md`  
**Status**: ❌ **0% COMPLETE** - External dependency

#### Required Components
- [ ] Stratum server (fork NOMP/Yiimp) - 40 hours
- [ ] Job distribution - 10 hours
- [ ] Share validation - 10 hours
- [ ] Accounting system - 20 hours
- [ ] Payout engine - 15 hours
- [ ] Web UI dashboard - 30 hours
- [ ] API for stats - 10 hours

**Recommendation**: Partner with existing pool operators  
**Alternative**: Fork open-ethereum-pool (15-20 hours adaptation)  
**Total Effort (if building)**: 135 hours  
**Total Effort (if forking)**: 20 hours

---

### 9. BLOCK EXPLORER (Blockscout)
**Spec**: `docs/specs/explorer/BLOCKSCOUT.md`  
**Status**: ⚠️ **40% COMPLETE** - Configured but not deployed

#### Existing
- [x] docker-compose.yml
- [x] Configuration files
- [x] Phoenix branding files

#### Missing
- [ ] **Deploy infrastructure** - 10 hours
  - [ ] PostgreSQL database setup - 2 hours
  - [ ] Redis cache - 1 hour
  - [ ] Backend deployment - 3 hours
  - [ ] Frontend build & deploy - 2 hours
  - [ ] Reverse proxy (NGINX) - 2 hours

- [ ] **DAG Extensions** - 15 hours
  - [ ] Parent visualization UI - 8 hours
  - [ ] Blue/red block indicators - 4 hours
  - [ ] DAG graph view per block - 8 hours
  - [ ] API endpoint for block parents - 2 hours

- [ ] **Contract Verification** - 3 hours
  - [ ] Configure verification service - 1 hour
  - [ ] Test Standard JSON input - 1 hour
  - [ ] Test with Hardhat/Foundry - 1 hour

- [ ] **Token Tracking** - 2 hours
  - [ ] ERC-20 indexing (verify working)
  - [ ] ERC-721 indexing (verify working)
  - [ ] ERC-1155 support

**Location**: `phoenix-workspace/phoenix-explorer/`  
**Total Explorer Effort**: 30 hours

---

### 10. JAVASCRIPT/TYPESCRIPT SDK
**Spec**: `docs/specs/sdk/JS_TS.md`  
**Status**: ⚠️ **70% COMPLETE**

#### Existing
- [x] Core RPC wrapper code
- [x] Basic examples structure
- [x] Package structure

#### Missing
- [ ] **npm Package Setup** - 5 hours
  - [ ] package.json configuration - 1 hour
  - [ ] TypeScript definitions - 2 hours
  - [ ] Build scripts (ESM + CJS) - 1 hour
  - [ ] README and docs - 1 hour

- [ ] **Phoenix Extensions** - 4 hours
  ```typescript
  interface PhoenixProvider extends ethers.Provider {
      getDAGInfo(blockTag?: BlockTag): Promise<DAGInfo>;
      getBlueScore(blockTag?: BlockTag): Promise<number>;
      getParents(blockHash: string): Promise<string[]>;
  }
  ```

- [ ] **Examples** - 6 hours
  - [ ] ERC-20 token deployment - 1 hour
  - [ ] ERC-721 NFT minting - 1 hour
  - [ ] Contract interaction - 1 hour
  - [ ] Event listening - 1 hour
  - [ ] Wallet connection - 1 hour
  - [ ] Transaction signing - 1 hour

- [ ] **Testing** - 3 hours
  - [ ] Unit tests - 2 hours
  - [ ] Integration tests - 1 hour

- [ ] **Publication** - 1 hour
  - [ ] npm publish
  - [ ] Documentation site

**Location**: `phoenix-workspace/phoenix-sdk-js/`  
**Total SDK JS Effort**: 19 hours

---

### 11. HARDHAT PLUGIN
**Spec**: `docs/specs/devtools/HARDHAT.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] Create plugin package `@bdp/hardhat` - 8 hours
  ```typescript
  // packages/hardhat/src/index.ts
  export default function bdpHardhatPlugin() {
      extendConfig((config) => {
          config.networks.phoenix = {
              url: 'https://rpc.bdp.network',
              chainId: 888,
          };
          config.networks.phoenixTestnet = {
              url: 'https://testnet-rpc.bdp.network',
              chainId: 8888,
          };
      });
  }
  ```

- [ ] Custom tasks - 4 hours
  - [ ] `bdp:chain-info` - 2 hours
  - [ ] `bdp:verify` (Blockscout passthrough) - 2 hours

- [ ] Documentation - 2 hours
- [ ] Example project - 2 hours

**Total Hardhat Effort**: 16 hours

---

### 12. FOUNDRY SUPPORT
**Spec**: `docs/specs/devtools/FOUNDRY.md`  
**Status**: ⚠️ **80% COMPLETE** - Works as-is, needs docs

#### Minimal Requirements
- [ ] Example `foundry.toml` - 0.5 hour
  ```toml
  [profile.default]
  src = 'src'
  out = 'out'
  libs = ['lib']
  
  [rpc_endpoints]
  phoenix = "https://rpc.bdp.network"
  phoenixTestnet = "https://testnet-rpc.bdp.network"
  
  [etherscan]
  phoenix = { key = "${BLOCKSCOUT_API_KEY}", url = "https://explorer.bdp.network/api" }
  ```

- [ ] Usage guide - 1 hour
- [ ] Test examples - 1.5 hours

**Total Foundry Effort**: 3 hours

---

### 13. REMIX IDE INTEGRATION
**Spec**: `docs/specs/devtools/REMIX.md`  
**Status**: ✅ **90% COMPLETE** - Works, needs docs

#### Documentation Only
- [ ] Network addition guide - 0.5 hour
  ```
  Network Name: Phoenix Mainnet
  RPC URL: https://rpc.bdp.network
  Chain ID: 888
  Symbol: BDP
  Explorer: https://explorer.bdp.network
  ```

- [ ] Deploy tutorial - 0.5 hour
- [ ] Screenshots/video - 1 hour

**Total Remix Effort**: 2 hours

---

### 14. RPC GATEWAY (Public Infrastructure)
**Spec**: `docs/specs/rpc/GATEWAY.md`  
**Status**: ❌ **0% COMPLETE**

#### Architecture
```
Internet → Cloudflare → NGINX → Node Pool (3-5 nodes) → Redis Cache
```

#### Implementation
- [ ] **NGINX Configuration** - 4 hours
  - [ ] Load balancing - 1 hour
  - [ ] Rate limiting - 1 hour
  - [ ] Caching headers - 1 hour
  - [ ] SSL/TLS - 1 hour

- [ ] **Redis Cache Layer** - 6 hours
  - [ ] Cache eth_getBlockByNumber - 2 hours
  - [ ] Cache eth_getTransactionReceipt - 2 hours
  - [ ] Cache invalidation on new blocks - 2 hours

- [ ] **Node Pool Management** - 4 hours
  - [ ] Health checks - 2 hours
  - [ ] Automatic failover - 2 hours

- [ ] **Rate Limiting** - 3 hours
  - [ ] Per-IP limits - 1 hour
  - [ ] Per-API-key limits - 1 hour
  - [ ] Burst handling - 1 hour

- [ ] **Monitoring** - 2 hours
  - [ ] Prometheus metrics - 1 hour
  - [ ] Grafana dashboard - 1 hour

**Total Gateway Effort**: 19 hours

---

### 15. SEED NODES
**Spec**: `docs/specs/ops/SEED_NODES.md`  
**Status**: ❌ **0% COMPLETE**

#### Requirements
- [ ] Deploy 5 geo-distributed nodes - 10 hours
  - [ ] US East - 2 hours
  - [ ] US West - 2 hours
  - [ ] Europe - 2 hours
  - [ ] Asia - 2 hours
  - [ ] Backup - 2 hours

- [ ] DNS Configuration - 2 hours
  - [ ] seed1.bdp.network
  - [ ] seed-eu.bdp.network
  - [ ] seed-asia.bdp.network
  - [ ] seed-us.bdp.network

- [ ] Hardcoded bootstrap enodes - 1 hour
- [ ] Monitoring - 2 hours

**Total Seed Nodes Effort**: 15 hours

---

### P1 SUMMARY
| Component | Status | Effort Remaining |
|-----------|--------|------------------|
| Mining Infrastructure | ✅ 100% | 0 hours |
| Mining Pool | ❌ 0% | 20 hours (fork) |
| Block Explorer | ⚠️ 40% | 30 hours |
| SDK JavaScript | ⚠️ 70% | 19 hours |
| Hardhat Plugin | ❌ 0% | 16 hours |
| Foundry Support | ⚠️ 80% | 3 hours |
| Remix Integration | ⚠️ 90% | 2 hours |
| RPC Gateway | ❌ 0% | 19 hours |
| Seed Nodes | ❌ 0% | 15 hours |

**P1 Total Remaining**: **124 hours** (~3 weeks with 2 developers)

---

## P2: MEDIUM PRIORITY (Important Features)
### Enhances ecosystem but not blocking for launch

### 16. PYTHON SDK
**Spec**: `docs/specs/sdk/PYTHON.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] web3.py wrapper - 10 hours
- [ ] Phoenix extensions - 4 hours
- [ ] Type hints - 3 hours
- [ ] Examples - 4 hours
- [ ] Tests - 3 hours
- [ ] PyPI publication - 1 hour

**Total Python SDK Effort**: 25 hours

---

### 17. GO SDK
**Spec**: `docs/specs/sdk/GO.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] Ethereum-compatible types - 8 hours
- [ ] RPC client - 8 hours
- [ ] Contract bindings (abigen) - 6 hours
- [ ] Phoenix extensions - 4 hours
- [ ] Examples - 4 hours
- [ ] Tests - 4 hours
- [ ] Documentation - 2 hours

**Total Go SDK Effort**: 36 hours

---

### 18. MOBILE WALLET
**Spec**: `docs/specs/wallet/MOBILE.md`  
**Status**: ❌ **0% COMPLETE**

#### Full Implementation (React Native)
- [ ] Project setup - 8 hours
- [ ] Account management (BIP-39/44) - 12 hours
- [ ] Wallet UI - 20 hours
- [ ] Transaction sending - 10 hours
- [ ] Token support (ERC-20/721/1155) - 15 hours
- [ ] WalletConnect integration - 10 hours
- [ ] Biometric auth - 6 hours
- [ ] DApp browser (optional) - 20 hours
- [ ] Testing - 15 hours
- [ ] App store submission - 10 hours

**Total Mobile Wallet Effort**: 126 hours (~4 weeks)

**Alternative**: Fork Rainbow Wallet (40 hours adaptation)

---

### 19. BROWSER EXTENSION WALLET
**Spec**: `docs/specs/wallet/EXTENSION.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] Extension framework - 10 hours
- [ ] EIP-1193 provider injection - 8 hours
- [ ] Account management - 10 hours
- [ ] Transaction signing UI - 12 hours
- [ ] Network switching - 4 hours
- [ ] DApp permissions - 8 hours
- [ ] Testing - 8 hours
- [ ] Chrome/Firefox submission - 4 hours

**Total Extension Effort**: 64 hours (~2 weeks)

**Alternative**: Fork MetaMask or Core wallet (30 hours)

---

### 20. LAYERZERO BRIDGE
**Spec**: `docs/specs/bridges/LAYERZERO.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] Deploy LayerZero Endpoint - 4 hours
- [ ] Configure relayers/oracles - 4 hours
- [ ] Register Phoenix chainId - 2 hours
- [ ] Deploy OFTV2 for BDP token - 6 hours
- [ ] Deploy bridges for USDC, WETH - 6 hours
- [ ] Testing on testnet - 8 hours
- [ ] Security review - 8 hours
- [ ] Bridge UI - 20 hours
- [ ] Documentation - 4 hours

**Total LayerZero Effort**: 62 hours (~2 weeks)

---

### 21. REDSTONE ORACLE
**Spec**: `docs/specs/oracles/REDSTONE.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] Integration contract - 4 hours
- [ ] Price feed configuration - 2 hours
- [ ] Consumer contract examples - 4 hours
- [ ] Testing - 4 hours
- [ ] Documentation - 2 hours

**Total RedStone Effort**: 16 hours

---

### 22. THE GRAPH INDEXING
**Spec**: `docs/specs/indexing/THE_GRAPH.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] graph-node deployment - 8 hours
- [ ] Phoenix chain config - 4 hours
- [ ] Example subgraph - 6 hours
- [ ] Hosted service setup - 6 hours
- [ ] Documentation - 2 hours

**Total The Graph Effort**: 26 hours

---

### 23. MONITORING & OBSERVABILITY
**Spec**: `docs/specs/ops/MONITORING.md`  
**Status**: ❌ **0% COMPLETE**

#### Implementation
- [ ] **Prometheus Metrics** - 12 hours
  - [ ] Node health metrics - 3 hours
  - [ ] Performance metrics - 3 hours
  - [ ] Mining metrics - 2 hours
  - [ ] Network metrics - 2 hours
  - [ ] State/storage metrics - 2 hours

- [ ] **Grafana Dashboards** - 8 hours
  - [ ] Node operator dashboard - 3 hours
  - [ ] Network overview dashboard - 3 hours
  - [ ] RPC gateway dashboard - 2 hours

- [ ] **Alerting (AlertManager)** - 6 hours
  - [ ] Critical alerts - 2 hours
  - [ ] Warning alerts - 2 hours
  - [ ] PagerDuty/Slack integration - 2 hours

- [ ] **Logging (Loki/ELK)** - 8 hours
  - [ ] Structured logging - 3 hours
  - [ ] Log aggregation - 3 hours
  - [ ] Log queries/dashboards - 2 hours

- [ ] **SLO Configuration** - 2 hours

**Total Monitoring Effort**: 36 hours

---

### 24. CONTRACT TEMPLATES
**Spec**: `docs/specs/contracts/TEMPLATES_SPEC.md`  
**Status**: ⚠️ **30% COMPLETE** - Basic contracts exist

#### Existing
- [x] HelloWorld.sol
- [x] ERC20.sol
- [x] ERC721.sol

#### Missing Secure Templates
- [ ] **Governance Contracts** - 15 hours
  - [ ] Governor contract - 6 hours
  - [ ] Timelock - 3 hours
  - [ ] Token voting - 3 hours
  - [ ] Treasury - 3 hours

- [ ] **DeFi Primitives** - 20 hours
  - [ ] AMM pool - 8 hours
  - [ ] Staking contract - 6 hours
  - [ ] Vesting contract - 6 hours

- [ ] **Security Patterns** - 10 hours
  - [ ] Pausable - 2 hours
  - [ ] Access control - 2 hours
  - [ ] ReentrancyGuard - 2 hours
  - [ ] Rate limiting - 2 hours
  - [ ] Upgradeable patterns - 2 hours

**Total Contract Templates Effort**: 45 hours

---

### P2 SUMMARY
| Component | Status | Effort Remaining |
|-----------|--------|------------------|
| Python SDK | ❌ 0% | 25 hours |
| Go SDK | ❌ 0% | 36 hours |
| Mobile Wallet | ❌ 0% | 126 hours (or 40h fork) |
| Extension Wallet | ❌ 0% | 64 hours (or 30h fork) |
| LayerZero Bridge | ❌ 0% | 62 hours |
| RedStone Oracle | ❌ 0% | 16 hours |
| The Graph | ❌ 0% | 26 hours |
| Monitoring | ❌ 0% | 36 hours |
| Contract Templates | ⚠️ 30% | 45 hours |

**P2 Total Remaining**: **436 hours** (or **350 hours** with wallet forks)

---

## P3: NICE TO HAVE (Optional Features)
### Post-launch enhancements

### 25. DEBUG/TRACE RPC METHODS
- [ ] `debug_traceTransaction` - 6 hours
- [ ] `debug_traceBlock` - 4 hours
- [ ] `debug_traceCall` - 4 hours
- [ ] `trace_*` methods - 6 hours

**Total Debug Effort**: 20 hours

---

### 26. HARDWARE WALLET SUPPORT
- [ ] Ledger integration - 20 hours
- [ ] Trezor integration - 20 hours
- [ ] Testing - 8 hours

**Total Hardware Wallet Effort**: 48 hours

---

### 27. MULTI-LANGUAGE DOCUMENTATION
- [ ] Chinese translation - 20 hours
- [ ] Spanish translation - 20 hours
- [ ] Japanese translation - 20 hours

**Total Translation Effort**: 60 hours

---

### 28. ADVANCED ANALYTICS
- [ ] Network analytics dashboard - 30 hours
- [ ] MEV analysis tools - 40 hours
- [ ] Gas price oracle - 15 hours

**Total Analytics Effort**: 85 hours

---

### P3 SUMMARY
**Total Optional Features**: 213 hours

---

## TESTING REQUIREMENTS
### Spec: `docs/specs/testing/`

### 29. CORE FUNCTIONALITY TESTS

#### Unit Tests ⚠️ **Partial**
- [ ] Canonicalization tests - 8 hours
  - [ ] Determinism across reorgs
  - [ ] Tie-breaking scenarios
  - [ ] Edge cases (equal blue scores)

- [ ] EVM execution tests - 8 hours
  - [ ] Gas calculation
  - [ ] State transitions
  - [ ] Receipt generation

- [ ] RPC tests - 6 hours
  - [ ] All endpoint responses
  - [ ] Error handling
  - [ ] Input validation

**Subtotal**: 22 hours

#### Integration Tests ⚠️ **Structure exists, not run**
- [ ] End-to-end transaction flow - 4 hours
- [ ] Contract deployment & interaction - 4 hours
- [ ] ERC-20 token tests - 3 hours
- [ ] ERC-721 NFT tests - 3 hours
- [ ] Reorg simulation - 6 hours
- [ ] Multi-node sync tests - 8 hours

**Subtotal**: 28 hours

#### Contract Test Suite ⚠️ **Spec exists**
**Spec**: `docs/specs/testing/CONTRACT_TEST_SUITE.md`

- [ ] Core semantics (storage, events, reverts) - 6 hours
- [ ] CREATE/CREATE2 - 4 hours
- [ ] Precompiles - 4 hours
- [ ] ERC-20/721/1155 compliance - 6 hours
- [ ] Reentrancy tests - 4 hours
- [ ] Gas & performance tests - 4 hours

**Subtotal**: 28 hours

#### Ethereum Test Suite ❌ **Critical**
**Required for mainnet**

- [ ] GeneralStateTests (London fork) - 10 hours setup + validation
- [ ] BlockchainTests - 8 hours
- [ ] TransactionTests - 6 hours
- [ ] Fix any failures - 20 hours (estimate)

**Subtotal**: 44 hours

---

### 30. DAG-SPECIFIC TESTS
**Spec**: `docs/specs/testing/DAG_TEST_SCENARIOS.md`

- [ ] Parallel block scenarios - 8 hours
- [ ] Simultaneous tips - 4 hours
- [ ] Deep reorgs (100+ blocks) - 6 hours
- [ ] Nonce conflicts - 4 hours
- [ ] BLOCKHASH opcode tests - 4 hours
- [ ] Timestamp attack scenarios - 4 hours
- [ ] Network partition recovery - 6 hours

**Total DAG Tests**: 36 hours

---

### 31. PERFORMANCE BENCHMARKS

- [ ] Transaction throughput (target: 200+ TPS) - 4 hours
- [ ] Block processing time (<100ms) - 2 hours
- [ ] Canonicalization latency (<10ms) - 2 hours
- [ ] Reorg replay time (<10s for 100 blocks) - 4 hours
- [ ] State checkpoint creation (<1s) - 2 hours
- [ ] RPC response times (<200ms p95) - 4 hours
- [ ] Database query optimization - 6 hours
- [ ] Memory profiling - 4 hours

**Total Performance Tests**: 28 hours

---

### 32. SECURITY TESTS

- [ ] Fuzzing (Echidna/Medusa) - 16 hours
- [ ] Input validation tests - 8 hours
- [ ] DoS attack scenarios - 8 hours
- [ ] Replay attack tests - 4 hours
- [ ] Consensus attack vectors - 12 hours

**Total Security Tests**: 48 hours

---

### 33. CHAOS ENGINEERING

- [ ] Network partition simulation - 8 hours
- [ ] Random node failures - 6 hours
- [ ] Clock skew scenarios - 4 hours
- [ ] High load stress testing - 8 hours

**Total Chaos Tests**: 26 hours

---

### TESTING SUMMARY
| Category | Effort |
|----------|--------|
| Unit Tests | 22 hours |
| Integration Tests | 28 hours |
| Contract Tests | 28 hours |
| Ethereum Tests | 44 hours |
| DAG Tests | 36 hours |
| Performance | 28 hours |
| Security | 48 hours |
| Chaos | 26 hours |

**Total Testing Effort**: **260 hours** (~6.5 weeks with dedicated QA)

---

## SECURITY & COMPLIANCE

### 34. EXTERNAL SECURITY AUDIT ❌ **CRITICAL FOR MAINNET**

- [ ] Select audit firms (2 minimum) - included in cost
- [ ] Prepare audit scope - 8 hours
- [ ] Code freeze & documentation - 8 hours
- [ ] Audit execution - 80 hours (external)
- [ ] Address findings - 40 hours
- [ ] Re-audit critical fixes - 20 hours (external)

**Total Audit Effort**: 56 hours (internal) + $50k-$100k (external)

---

### 35. BUG BOUNTY PROGRAM

- [ ] Platform setup (Immunefi/HackerOne) - 4 hours
- [ ] Scope definition - 2 hours
- [ ] Reward structure - 2 hours
- [ ] Launch & monitoring - ongoing

**Total Bug Bounty Setup**: 8 hours

---

### 36. EIP CONFORMANCE
**Spec**: `docs/specs/security/EIP_CONFORMANCE.md`

- [ ] EIP-155 (replay protection) - verify ✅
- [ ] EIP-658 (receipt status) - verify
- [ ] EIP-1559 (fee market) - implement & test - 20 hours
- [ ] EIP-2718 (typed transactions) - verify
- [ ] EIP-2930 (access lists) - implement - 10 hours
- [ ] EIP-1474 (JSON-RPC) - verify coverage
- [ ] EIP-1193 (provider API) - document for wallets

**Total EIP Conformance**: 30 hours

---

### 37. STATIC ANALYSIS
**Spec**: `docs/specs/security/STATIC_RULESET.md`

- [ ] Slither integration - 4 hours
- [ ] Mythril integration - 4 hours
- [ ] Custom rules for Phoenix - 8 hours
- [ ] CI/CD integration - 4 hours

**Total Static Analysis**: 20 hours

---

### SECURITY SUMMARY
| Item | Effort |
|------|--------|
| External Audit | 56 hours + $50k-$100k |
| Bug Bounty | 8 hours |
| EIP Conformance | 30 hours |
| Static Analysis | 20 hours |

**Total Security Effort**: **114 hours** + external costs

---

## OPERATIONS & INFRASTRUCTURE

### 38. CI/CD PIPELINE

- [ ] GitHub Actions setup - 4 hours
- [ ] Automated testing - 4 hours
- [ ] Build & artifact generation - 4 hours
- [ ] Deployment automation - 6 hours
- [ ] Rollback procedures - 4 hours

**Total CI/CD**: 22 hours

---

### 39. DOCUMENTATION

#### Technical Documentation ⚠️ **70% complete**
- [ ] API reference generation - 8 hours
- [ ] Architecture deep-dive - 4 hours
- [ ] Deployment guide - 4 hours

#### Developer Documentation ⚠️ **50% complete**
- [ ] Quick start guide - 4 hours
- [ ] Tutorial series (5 tutorials) - 20 hours
- [ ] Video tutorials - 30 hours
- [ ] Migration guide from Ethereum - 6 hours

#### User Documentation ❌ **Not started**
- [ ] Wallet setup guide - 4 hours
- [ ] How to send transactions - 2 hours
- [ ] How to deploy contracts - 4 hours
- [ ] Troubleshooting guide - 4 hours
- [ ] FAQ - 4 hours

**Total Documentation**: 94 hours

---

### 40. MAINNET PREPARATION

- [ ] Genesis block configuration - 2 hours
- [ ] Token distribution plan - 4 hours
- [ ] Initial validator/node selection - 4 hours
- [ ] Launch checklist - 2 hours
- [ ] Rollback plan - 4 hours
- [ ] Emergency procedures - 4 hours
- [ ] Communication plan - 4 hours

**Total Mainnet Prep**: 24 hours

---

### 41. TESTNET OPERATION

- [ ] Deploy 5-node testnet - 10 hours
- [ ] Faucet setup - 4 hours
- [ ] Monitor & maintain - ongoing
- [ ] Community testing coordination - ongoing
- [ ] Minimum 30-day stability - 720 hours clock time

**Total Testnet Setup**: 14 hours + 30 days runtime

---

### OPERATIONS SUMMARY
| Item | Effort |
|------|--------|
| CI/CD | 22 hours |
| Documentation | 94 hours |
| Mainnet Prep | 24 hours |
| Testnet Setup | 14 hours |

**Total Operations Effort**: **154 hours**

---

## TIMELINE ESTIMATES

### PHASE 1: Core Completion (Testnet-Ready)
**Duration**: 3-4 weeks  
**Team**: 2-3 developers

| Task | Hours | Priority |
|------|-------|----------|
| EVM Critical Fixes | 29.5 | P0 |
| RPC Required Methods | 24 | P0 |
| Canonicalization Testing | 14 | P0 |
| Reorg Handler | 15 | P0 |
| Block Headers | 9 | P0 |
| Basic Testing | 30 | P0 |

**Phase 1 Total**: **121.5 hours**

**Deliverable**: Working testnet with basic functionality

---

### PHASE 2: Essential Features
**Duration**: 3-4 weeks  
**Team**: 3-4 developers

| Task | Hours | Priority |
|------|-------|----------|
| Block Explorer | 30 | P1 |
| SDK JavaScript | 19 | P1 |
| Hardhat Plugin | 16 | P1 |
| RPC Gateway | 19 | P1 |
| Seed Nodes | 15 | P1 |
| Mining Pool (fork) | 20 | P1 |
| Integration Tests | 28 | Testing |

**Phase 2 Total**: **147 hours**

**Deliverable**: Feature-complete testnet with developer tools

---

### PHASE 3: Quality & Testing
**Duration**: 4-6 weeks  
**Team**: 2 developers + 1 QA

| Task | Hours | Priority |
|------|-------|----------|
| Ethereum Test Suite | 44 | Testing |
| DAG-Specific Tests | 36 | Testing |
| Performance Tests | 28 | Testing |
| Security Tests | 48 | Testing |
| EIP Conformance | 30 | Security |
| Monitoring | 36 | P2 |

**Phase 3 Total**: **222 hours**

**Deliverable**: Production-quality, well-tested system

---

### PHASE 4: Security & Launch Prep
**Duration**: 4-6 weeks  
**Team**: 2 developers + external auditors

| Task | Hours | Priority |
|------|-------|----------|
| Audit Preparation | 16 | Security |
| External Audit | 80 (external) | Security |
| Address Findings | 40 | Security |
| Mainnet Prep | 24 | Ops |
| Documentation | 94 | Ops |
| Bug Bounty Setup | 8 | Security |

**Phase 4 Total**: **182 hours** + external audit time

**Plus**: 30-day testnet stability period

**Deliverable**: Mainnet-ready system

---

### PHASE 5: Ecosystem Enhancement (Post-Launch)
**Duration**: 8-12 weeks  
**Team**: 4-6 developers

| Task | Hours | Priority |
|------|-------|----------|
| Python SDK | 25 | P2 |
| Go SDK | 36 | P2 |
| LayerZero Bridge | 62 | P2 |
| Mobile Wallet | 40 (fork) | P2 |
| Extension Wallet | 30 (fork) | P2 |
| Contract Templates | 45 | P2 |
| The Graph | 26 | P2 |
| RedStone Oracle | 16 | P2 |

**Phase 5 Total**: **280 hours**

**Deliverable**: Rich ecosystem with multiple wallets, SDKs, and integrations

---

## TOTAL PROJECT SUMMARY

### By Phase
| Phase | Description | Hours | Duration |
|-------|-------------|-------|----------|
| Phase 1 | Core Completion | 121.5 | 3-4 weeks |
| Phase 2 | Essential Features | 147 | 3-4 weeks |
| Phase 3 | Quality & Testing | 222 | 4-6 weeks |
| Phase 4 | Security & Launch | 182 | 4-6 weeks + 30 days |
| Phase 5 | Ecosystem | 280 | 8-12 weeks |

**Total Development**: **952.5 hours** (~6 months with 4 developers)  
**Plus**: 30-day testnet stability period  
**Total Timeline**: **7-8 months to mainnet**

---

### By Priority
| Priority | Hours | % Complete | Remaining |
|----------|-------|------------|-----------|
| P0 (Critical) | 91.5 | 85% | 91.5 hours |
| P1 (High) | 124 | 60% | 124 hours |
| P2 (Medium) | 436 | 15% | 436 hours |
| P3 (Optional) | 213 | 0% | 213 hours |
| Testing | 260 | 20% | 260 hours |
| Security | 114 | 10% | 114 hours |
| Operations | 154 | 30% | 154 hours |

**Critical Path (P0+P1+Testing+Security)**: **589.5 hours** (~15 weeks with 4 devs)  
**To Full Feature Set**: **1,392.5 hours** (~35 weeks with 4 devs)

---

## RESOURCE REQUIREMENTS

### Minimum Viable Team (Testnet)
- **2 Backend Engineers** (Go, EVM, consensus)
- **1 Frontend Engineer** (Explorer, SDKs)
- **1 QA Engineer** (Testing)

**Timeline**: 4 months to testnet

---

### Recommended Team (Mainnet)
- **3 Backend Engineers**
- **2 Frontend Engineers**
- **1 DevOps Engineer**
- **1 QA Engineer**
- **1 Technical Writer**
- **External Security Auditors** (contract)

**Timeline**: 6-7 months to mainnet

---

### Optimal Team (Fast Track)
- **4 Backend Engineers**
- **2 Frontend Engineers**
- **2 DevOps Engineers**
- **2 QA Engineers**
- **1 Technical Writer**
- **1 Security Engineer**
- **External Auditors** (contract)

**Timeline**: 4-5 months to mainnet

---

## BUDGET ESTIMATE

### Personnel (6 months)
- 4 Senior Engineers @ $120k/yr: $240k
- 2 Mid Engineers @ $90k/yr: $90k
- 1 QA @ $80k/yr: $40k
- 1 Tech Writer @ $70k/yr: $35k

**Personnel Total**: **$405k**

---

### Infrastructure
- Seed nodes (5x $50/mo × 6 mo): $1,500
- RPC gateway: $300/mo × 6: $1,800
- Explorer: $150/mo × 6: $900
- Development servers: $200/mo × 6: $1,200
- Testing infrastructure: $100/mo × 6: $600

**Infrastructure Total**: **$6,000**

---

### External Services
- Security audits (2 firms): $80,000
- Bug bounty program: $20,000
- Legal/compliance: $10,000

**External Total**: **$110,000**

---

### Marketing/Community
- Documentation videos: $5,000
- Community management: $10,000
- Developer relations: $10,000

**Marketing Total**: **$25,000**

---

### TOTAL PROJECT BUDGET
**Conservative Estimate**: **$546,000** (6 months)  
**Realistic Estimate**: **$650,000** (7 months, includes buffer)

---

## SUCCESS CRITERIA

### Testnet Launch ✅
- [ ] All P0 features complete
- [ ] Basic integration tests passing
- [ ] 5-node testnet operational
- [ ] Explorer functional
- [ ] SDK published
- [ ] Documentation available

### Mainnet Launch ✅
- [ ] All P0 + P1 features complete
- [ ] Ethereum test suite passing
- [ ] Security audit complete with no critical issues
- [ ] 30-day testnet stability
- [ ] Bug bounty program active
- [ ] Production monitoring in place
- [ ] Emergency procedures documented

### Ecosystem Maturity ✅
- [ ] All P2 features complete
- [ ] Mobile wallet available
- [ ] Bridge operational
- [ ] Multiple SDKs available
- [ ] 10+ production DApps deployed
- [ ] Active developer community

---

## NEXT IMMEDIATE ACTIONS

### This Week (Priority Order)
1. **Transaction Receipts** (4 hours) - BLOCKING
2. **Event Log Indexing** (6 hours) - BLOCKING
3. **Genesis Allocation** (3 hours) - BLOCKING
4. **Gas Fee Distribution** (1.5 hours) - HIGH
5. **Signature Extraction** (5 hours) - HIGH
6. **RPC Method Implementation** (start with critical ones) - HIGH

**Total**: ~20 hours → **Basic functionality working**

---

### Next Two Weeks
1. **State Checkpointing** (10 hours)
2. **Reorg Handler** (15 hours)
3. **Block Header Fields** (9 hours)
4. **Canonicalization Testing** (14 hours)
5. **Integration Tests** (20 hours)

**Total**: 68 hours → **Testnet-ready**

---

### Month 1 Goal
**All P0 items complete + basic testing = Functional Testnet** 🎯

---

## TRACKING & ACCOUNTABILITY

### Weekly Milestones
- **Week 1-2**: EVM core complete
- **Week 3-4**: RPC server complete
- **Week 5-6**: Testing infrastructure
- **Week 7-8**: Explorer + SDKs
- **Week 9-12**: Security & optimization
- **Week 13+**: Testnet operation & mainnet prep

### Key Metrics
- [ ] Lines of code tested (target: 80% coverage)
- [ ] Ethereum tests passing (target: 100%)
- [ ] Performance benchmarks (target: 200+ TPS)
- [ ] Uptime (testnet: 99%+, mainnet: 99.9%+)
- [ ] Security audit score (target: no critical/high issues)

---

## APPENDIX: QUICK REFERENCE

### Most Critical Items (Do First)
1. Transaction receipts ❌
2. Event logs ❌
3. State checkpointing ❌
4. Reorg testing ⚠️
5. RPC methods ⚠️
6. Security audit ❌

### Biggest Time Investments
1. Testing (260 hours)
2. Mobile wallet (126 hours)
3. Security audit (56h + external)
4. Documentation (94 hours)
5. Extension wallet (64 hours)

### Quick Wins (High Impact, Low Effort)
1. Foundry docs (3 hours)
2. Remix docs (2 hours)
3. Genesis allocation (3 hours)
4. Gas fee distribution (1.5 hours)
5. Bug bounty setup (8 hours)

---

**END OF CHECKLIST**

*This comprehensive checklist covers ALL features from specifications, organized by priority with realistic time estimates. Use this as your master tracking document for implementation progress.*

---

**Document Status**: ✅ COMPLETE  
**Last Updated**: November 23, 2025  
**Maintained By**: Engineering Team  
**Version**: 1.0

