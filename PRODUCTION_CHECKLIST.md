# Phoenix Network - Detailed Production Checklist
**Software Architecture Roadmap: Framework → Production**

**Status**: All MVPs completed, now moving to integration and testing  
**Timeline**: 8-12 weeks to production-ready  
**Owner**: Solo Founder + AI Assistance

---

## 🎯 Current State Assessment

### ✅ What Works
- Phoenix-node daemon compiles and runs
- Kaspa fork successfully rebranded
- Binary builds: `phoenix-node` (25MB), `kaspaminer` (20MB)
- Repositories and infrastructure ready

### ⚠️ What Needs Work
- Canonicalization module needs Kaspa API integration
- EVM executor not wired to consensus
- No end-to-end testing
- SDK needs actual RPC endpoint
- No contracts deployed yet

---

## Phase 1: Immediate Fixes (Week 1)

### 1.1 Fix Canonicalization Compilation

**Current State**: Module exists but doesn't compile due to API mismatches

**Tasks**:
- [ ] Identify correct Kaspa API for accessing blocks
- [ ] Find how to get blue score from DomainBlock
- [ ] Locate header timestamp method (TimeInMilliseconds() or similar)
- [ ] Find hash method (BlockHash(), Hash(), or similar)
- [ ] Implement DAGReader interface using Kaspa's consensus manager
- [ ] Test compilation: `go build ./domain/canonical`

**Files to modify**:
```
domain/canonical/ordering.go:
- Update GetBlueScore() to match Kaspa's actual API
- Fix timestamp access: blockI.Header.TimeInMilliseconds()
- Fix hash access: blockI.Header.BlockHash() or similar
- Add error handling for all DAG operations
```

**How to find correct API**:
```bash
cd ../phoenix-workspace/phoenix-node
# Search for blue score usage
grep -r "BlueScore" domain/consensus/processes/ghostdagmanager/
# Search for timestamp usage  
grep -r "TimeInMilliseconds" domain/consensus/
# Search for hash methods
grep -r "BlockHash\|Hash()" domain/consensus/model/
```

**AI assistance option**:
```bash
# Deploy targeted task
cd /Users/admin/Dev/Crypto/BlockDAG/crewai
python deploy_crew.py --task "Fix canonical/ordering.go to use correct Kaspa consensus API"
```

**Success criteria**:
- `go build ./domain/canonical` succeeds
- No compilation errors
- Module ready for integration

**Estimated time**: 4-8 hours human + 2 hours AI

---

### 1.2 Create DAGReader Adapter

**Current State**: Interface defined but no implementation

**Tasks**:
- [ ] Create `domain/canonical/dag_adapter.go`
- [ ] Implement DAGReader interface using Kaspa's consensus manager
- [ ] Wire to existing Kaspa consensus data structures
- [ ] Add caching for performance
- [ ] Write unit tests

**Implementation**:
```go
// File: domain/canonical/dag_adapter.go
package canonical

import (
    "github.com/BlockDAGPhoenix/phoenix-node/domain/consensus"
    "github.com/BlockDAGPhoenix/phoenix-node/domain/consensus/model/externalapi"
)

type KaspaDAGAdapter struct {
    consensusManager consensus.ConsensusManager
    blockStore       consensus.BlockStore
}

func NewKaspaDAGAdapter(cm consensus.ConsensusManager) *KaspaDAGAdapter {
    return &KaspaDAGAdapter{
        consensusManager: cm,
        blockStore:      cm.BlockStore(),
    }
}

func (k *KaspaDAGAdapter) GetBlock(hash *externalapi.DomainHash) (*externalapi.DomainBlock, error) {
    // Use Kaspa's block store to retrieve block
    return k.blockStore.Block(hash)
}

func (k *KaspaDAGAdapter) GetBlueScore(block *externalapi.DomainBlock) uint64 {
    // Get blue score from GHOSTDAG data
    ghostdagData, err := k.blockStore.GHOSTDAGData(block.Header.Hash())
    if err != nil {
        return 0
    }
    return ghostdagData.BlueScore
}

// ... implement remaining interface methods
```

**Success criteria**:
- DAGReader fully implemented
- Compiles without errors
- Can read blocks from Kaspa's DAG

**Estimated time**: 6-8 hours

---

### 1.3 Test Daemon Startup

**Current State**: Daemon builds but not tested

**Tasks**:
- [ ] Start daemon in testnet mode
- [ ] Verify genesis block loads
- [ ] Check P2P network initializes
- [ ] Verify RPC server starts
- [ ] Monitor for crashes
- [ ] Review logs for errors

**Commands**:
```bash
cd ../phoenix-workspace/phoenix-node

# Start daemon
./phoenix-node --testnet --appdir=/tmp/phoenix-test --logdir=/tmp/phoenix-logs

# In another terminal, check RPC
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"getInfo","params":[],"id":1}' \
  http://localhost:16111

# Monitor logs
tail -f /tmp/phoenix-logs/*.log
```

**Expected issues**:
- Port conflicts (change port if needed)
- Missing database directory
- Configuration errors
- Network initialization failures

**Success criteria**:
- Daemon starts without crashing
- Genesis block loads
- RPC responds to queries
- Runs for 1+ hour stable

**Estimated time**: 2-4 hours

---

## Phase 2: Core Integration (Week 2-3)

### 2.1 Wire Canonicalization to Consensus

**Current State**: Canonicalization module isolated, not used by daemon

**Tasks**:
- [ ] Find where Kaspa processes new blocks
- [ ] Inject canonicalization call after block acceptance
- [ ] Store canonical index in block metadata
- [ ] Expose canonical chain via RPC
- [ ] Add logging for canonical ordering

**Integration points**:
```go
// File: domain/consensus/consensus.go (or similar)
// After block is added to DAG:

func (c *consensus) OnBlockAdded(block *externalapi.DomainBlock) error {
    // Existing Kaspa logic
    err := c.blockProcessor.ProcessBlock(block)
    if err != nil {
        return err
    }
    
    // NEW: Update canonical chain
    canonicalBuilder := canonical.NewCanonicalBuilder(c.dagAdapter)
    canonicalChain, err := canonicalBuilder.BuildCanonicalSequence()
    if err != nil {
        log.Warnf("Failed to build canonical chain: %v", err)
        return nil // Non-fatal for MVP
    }
    
    // Store canonical ordering
    c.storeCanonicalChain(canonicalChain)
    
    return nil
}
```

**Files to modify**:
- `domain/consensus/consensus.go` or similar
- Add canonical chain storage
- Expose via RPC method

**Success criteria**:
- Canonical chain updated on each new block
- Can query canonical chain via RPC
- Ordering is deterministic

**Estimated time**: 8-12 hours

---

### 2.2 Add go-ethereum Dependency

**Current State**: No EVM library integrated

**Tasks**:
- [ ] Add go-ethereum to go.mod
- [ ] Import core/vm package
- [ ] Import core/state package
- [ ] Import core/types package
- [ ] Resolve dependency conflicts
- [ ] Update to compatible versions

**Commands**:
```bash
cd ../phoenix-workspace/phoenix-node

# Add go-ethereum
go get github.com/ethereum/go-ethereum@latest

# Update go.mod
go mod tidy

# Test import
cat > test_evm_import.go << EOF
package main
import (
    "github.com/ethereum/go-ethereum/core/vm"
    "github.com/ethereum/go-ethereum/core/state"
)
func main() {}
EOF

go build test_evm_import.go
rm test_evm_import.go
```

**Expected issues**:
- Version conflicts with existing dependencies
- Need to use replace directives
- May need specific go-ethereum version

**Success criteria**:
- go-ethereum imports work
- No dependency conflicts
- Can create vm.EVM instance

**Estimated time**: 2-4 hours

---

### 2.3 Implement EVM State Database

**Current State**: StateDB interface defined, no implementation

**Tasks**:
- [ ] Create state database using go-ethereum's state.StateDB
- [ ] Wire to LevelDB or in-memory for testing
- [ ] Implement account management
- [ ] Add state root calculation
- [ ] Create state snapshots for reorgs

**Implementation**:
```go
// File: domain/evm/statedb.go
package evm

import (
    "github.com/ethereum/go-ethereum/core/state"
    "github.com/ethereum/go-ethereum/ethdb"
    "github.com/ethereum/go-ethereum/ethdb/memorydb"
    "github.com/ethereum/go-ethereum/trie"
)

type PhoenixStateDB struct {
    db    state.Database
    state *state.StateDB
}

func NewPhoenixStateDB() (*PhoenixStateDB, error) {
    // Use in-memory database for MVP
    memDB := memorydb.New()
    ethDB := rawdb.NewDatabase(memDB)
    
    trieDB := trie.NewDatabase(ethDB)
    stateDB, err := state.New(common.Hash{}, state.NewDatabase(trieDB), nil)
    if err != nil {
        return nil, err
    }
    
    return &PhoenixStateDB{
        db:    state.NewDatabase(trieDB),
        state: stateDB,
    }, nil
}

// Implement StateDB interface methods using state.StateDB
func (p *PhoenixStateDB) GetBalance(addr []byte) uint64 {
    address := common.BytesToAddress(addr)
    return p.state.GetBalance(address).Uint64()
}

// ... implement all interface methods
```

**Success criteria**:
- StateDB compiles
- Can create accounts
- Can modify balances
- State root changes correctly

**Estimated time**: 6-10 hours

---

### 2.4 Wire EVM Executor to Consensus

**Current State**: EVM executor exists but not integrated

**Tasks**:
- [ ] Call EVM executor from canonical chain processor
- [ ] Pass blocks in canonical order
- [ ] Execute transactions sequentially
- [ ] Generate receipts
- [ ] Store state roots
- [ ] Handle execution errors

**Integration**:
```go
// File: domain/evm/integration.go
package evm

func (e *Executor) ProcessNewCanonicalBlock(block *externalapi.DomainBlock, index uint64) error {
    // Create EVM block context
    ctx := e.createBlockContext(block, index)
    
    // Execute each transaction
    receipts := []*types.Receipt{}
    for i, tx := range block.Transactions {
        receipt, err := e.executeTransaction(tx, ctx, i)
        if err != nil {
            log.Warnf("Transaction %d failed: %v", i, err)
            // Store failed receipt
            receipt = createFailedReceipt(tx, err)
        }
        receipts = append(receipts, receipt)
    }
    
    // Commit state
    stateRoot, err := e.stateDB.Commit()
    if err != nil {
        return err
    }
    
    // Store receipts and state root
    e.storeBlockExecution(block, stateRoot, receipts)
    
    return nil
}
```

**Success criteria**:
- Transactions execute
- State changes persist
- Receipts generated
- No crashes on invalid transactions

**Estimated time**: 10-16 hours

---

## Phase 3: Contract Deployment Testing (Week 4)

### 3.1 Deploy Test Contract

**Current State**: SDK created but no contracts deployed

**Tasks**:
- [ ] Ensure RPC server exposes eth_* methods
- [ ] Create simple test contract (ERC20 or Hello World)
- [ ] Deploy using phoenix-sdk-js
- [ ] Verify contract storage
- [ ] Call contract methods
- [ ] Verify state changes

**Test contract**:
```solidity
// test/HelloPhoenix.sol
pragma solidity ^0.8.0;

contract HelloPhoenix {
    string public message;
    
    constructor() {
        message = "Hello Phoenix!";
    }
    
    function setMessage(string memory _msg) public {
        message = _msg;
    }
    
    function getMessage() public view returns (string memory) {
        return message;
    }
}
```

**Deployment script**:
```javascript
// test/deploy.js
const Phoenix = require('../phoenix-sdk-js/index.js');

async function deploy() {
    const provider = new Phoenix.Provider('http://localhost:8545');
    const wallet = new Phoenix.Wallet(PRIVATE_KEY, provider);
    
    // Deploy contract
    const factory = new Phoenix.Contract.ContractFactory(ABI, BYTECODE, wallet);
    const contract = await factory.deploy();
    await contract.deployed();
    
    console.log('Contract deployed at:', contract.address);
    
    // Test contract
    const msg = await contract.getMessage();
    console.log('Message:', msg);
}

deploy().catch(console.error);
```

**Success criteria**:
- Contract deploys successfully
- Address is returned
- Can call read methods
- Can call write methods
- State persists

**Estimated time**: 4-8 hours (plus debugging)

---

### 3.2 Implement eth_* RPC Methods

**Current State**: RPC server exists but may not have all eth_* methods

**Tasks**:
- [ ] Verify eth_blockNumber works
- [ ] Implement eth_getBlockByNumber
- [ ] Implement eth_getTransactionReceipt
- [ ] Implement eth_call (read-only execution)
- [ ] Implement eth_sendRawTransaction
- [ ] Implement eth_getCode
- [ ] Implement eth_getBalance
- [ ] Test with curl

**Implementation checklist**:

```go
// app/rpc/rpchandlers/eth_block.go
func (api *EthAPI) GetBlockByNumber(number uint64) (*types.Block, error) {
    // 1. Get block at canonical index 'number'
    block, err := api.canonicalChain.GetBlockByIndex(number)
    if err != nil {
        return nil, err
    }
    
    // 2. Convert to Ethereum block format
    ethBlock := convertToEthBlock(block)
    
    return ethBlock, nil
}

// app/rpc/rpchandlers/eth_transaction.go
func (api *EthAPI) SendRawTransaction(txBytes []byte) (common.Hash, error) {
    // 1. Parse RLP transaction
    tx := new(types.Transaction)
    err := tx.UnmarshalBinary(txBytes)
    if err != nil {
        return common.Hash{}, err
    }
    
    // 2. Validate transaction
    if err := api.validateTx(tx); err != nil {
        return common.Hash{}, err
    }
    
    // 3. Add to mempool
    api.txPool.AddTransaction(tx)
    
    return tx.Hash(), nil
}
```

**Test each method**:
```bash
# eth_blockNumber
curl -X POST -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' localhost:8545

# eth_getBlockByNumber  
curl -X POST -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x1",false],"id":1}' localhost:8545

# eth_sendRawTransaction
curl -X POST -d '{"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":["0x..."],"id":1}' localhost:8545
```

**Success criteria**:
- All required eth_* methods respond
- Return correct data format
- SDK can interact successfully

**Estimated time**: 12-20 hours

---

## Phase 4: End-to-End Integration (Week 5-6)

### 4.1 Complete DAG→EVM Flow

**Current State**: Components exist separately, not connected

**Tasks**:
- [ ] Wire block acceptance → canonicalization → EVM execution
- [ ] Ensure flow happens automatically on new blocks
- [ ] Add transaction execution logging
- [ ] Store execution results in database
- [ ] Create state checkpoints

**Complete flow**:
```
1. Block arrives via P2P
   ↓
2. GHOSTDAG validation (Kaspa native)
   ↓
3. Add to DAG
   ↓
4. Trigger canonicalization
   ↓
5. Get updated canonical chain
   ↓
6. Execute new canonical blocks in EVM
   ↓
7. Update state root
   ↓
8. Store receipts
   ↓
9. Notify RPC subscribers
```

**Implementation location**:
```
app/protocol/flowcontext/block_processor.go or similar
- Add canonicalization call
- Add EVM execution call
- Handle errors gracefully
```

**Success criteria**:
- New block automatically triggers EVM execution
- State updates visible
- Receipts accessible via RPC

**Estimated time**: 16-24 hours

---

### 4.2 Transaction Pool Integration

**Current State**: Kaspa has mempool, but for native transactions

**Tasks**:
- [ ] Create EVM transaction type (different from Kaspa native)
- [ ] Add transaction validation for EVM txs
- [ ] Integrate with Kaspa's mempool
- [ ] Prioritize by gas price
- [ ] Add nonce tracking

**Implementation**:
```go
// domain/txpool/evm_tx.go
type EVMTransaction struct {
    Nonce    uint64
    GasPrice *big.Int
    GasLimit uint64
    To       *common.Address // nil for contract creation
    Value    *big.Int
    Data     []byte
    V, R, S  *big.Int // Signature
}

func (pool *TxPool) AddEVMTransaction(tx *EVMTransaction) error {
    // 1. Validate signature
    // 2. Check nonce
    // 3. Verify gas price
    // 4. Add to mempool
    // 5. Broadcast to network
}
```

**Success criteria**:
- Can submit EVM transactions
- Nonce validation works
- Transactions included in blocks
- Gas price prioritization works

**Estimated time**: 10-16 hours

---

### 4.3 State Root Management

**Current State**: State changes but roots not tracked

**Tasks**:
- [ ] Calculate state root after each block
- [ ] Store state root in canonical block metadata
- [ ] Verify state roots match across nodes
- [ ] Implement state root verification
- [ ] Add to RPC responses

**Implementation**:
```go
// domain/evm/state_manager.go
type StateManager struct {
    stateDB *PhoenixStateDB
    roots   map[uint64]common.Hash // blockNumber → stateRoot
}

func (sm *StateManager) CommitBlock(blockNumber uint64) (common.Hash, error) {
    // Commit state changes
    root, err := sm.stateDB.Commit()
    if err != nil {
        return common.Hash{}, err
    }
    
    // Store root for this block
    sm.roots[blockNumber] = root
    
    return root, nil
}

func (sm *StateManager) GetStateRoot(blockNumber uint64) common.Hash {
    return sm.roots[blockNumber]
}
```

**Success criteria**:
- State root calculated correctly
- Consistent across nodes (once multi-node)
- Accessible via RPC

**Estimated time**: 6-10 hours

---

## Phase 5: SDK and Testing (Week 7)

### 5.1 Complete JavaScript SDK

**Current State**: Basic wrapper created, not tested

**Tasks**:
- [ ] Test SDK connects to RPC
- [ ] Verify wallet signing works
- [ ] Test contract deployment
- [ ] Test contract calls
- [ ] Add error handling
- [ ] Write usage examples
- [ ] Publish to npm (optional)

**Testing script**:
```javascript
// test/sdk_test.js
const Phoenix = require('../phoenix-sdk-js');

async function testSDK() {
    // 1. Connect
    const provider = new Phoenix.Provider('http://localhost:8545');
    const blockNumber = await provider.getBlockNumber();
    console.log('Block number:', blockNumber);
    
    // 2. Create wallet
    const wallet = Phoenix.Wallet.createRandom().connect(provider);
    console.log('Wallet address:', wallet.address);
    
    // 3. Check balance
    const balance = await wallet.getBalance();
    console.log('Balance:', balance.toString());
    
    // 4. Phoenix-specific methods
    const dagInfo = await provider.getDAGInfo();
    console.log('DAG info:', dagInfo);
}

testSDK().catch(console.error);
```

**Success criteria**:
- All SDK methods work
- Can deploy and interact with contracts
- Error messages clear
- Compatible with ethers.js patterns

**Estimated time**: 4-6 hours

---

### 5.2 Create Test Suite

**Current State**: No automated tests

**Tasks**:
- [ ] Unit tests for canonicalization
- [ ] Unit tests for EVM executor
- [ ] Integration test: daemon + mining + EVM
- [ ] End-to-end test: contract deployment
- [ ] Performance test: 100 blocks
- [ ] Chaos test: random block arrival order

**Test structure**:
```
tests/
├── unit/
│   ├── canonical_test.go          # Canonicalization logic
│   ├── evm_executor_test.go       # EVM execution
│   └── state_db_test.go           # State management
├── integration/
│   ├── block_to_evm_test.go       # Full flow
│   └── multi_node_test.go         # Network sync
└── e2e/
    ├── contract_deployment_test.go
    └── contract_execution_test.go
```

**Example test**:
```go
// tests/unit/canonical_test.go
func TestCanonicalOrdering(t *testing.T) {
    // Create mock DAG with known structure
    dag := createMockDAG(t)
    
    // Build canonical sequence
    builder := canonical.NewCanonicalBuilder(dag)
    chain, err := builder.BuildCanonicalSequence()
    require.NoError(t, err)
    
    // Verify ordering is correct
    assert.Equal(t, 10, len(chain))
    assert.True(t, isTopologicallyOrdered(chain))
    assert.True(t, isDeterministic(chain))
}
```

**Success criteria**:
- All unit tests pass
- Integration tests pass
- E2E test deploys contract successfully

**Estimated time**: 16-24 hours

---

## Phase 6: Testnet Deployment (Week 8-9)

### 6.1 Local 3-Node Testnet

**Current State**: Script created but not tested

**Tasks**:
- [ ] Run testnet-setup.sh
- [ ] Start all 3 nodes
- [ ] Verify they connect
- [ ] Mine blocks on node 1
- [ ] Verify blocks propagate to nodes 2 and 3
- [ ] Test canonical chain matches across nodes
- [ ] Deploy contract from each node

**Commands**:
```bash
cd ../phoenix-workspace/phoenix-node

# Setup
./testnet-setup.sh

# Terminal 1: Node 1 (mining node)
./phoenix-node --configfile=testnet/node1/phoenix.conf

# Terminal 2: Node 2
./phoenix-node --configfile=testnet/node2/phoenix.conf

# Terminal 3: Node 3
./phoenix-node --configfile=testnet/node3/phoenix.conf

# Terminal 4: Miner
./kaspaminer --rpcserver=localhost:16111 --miningaddr=<address>

# Terminal 5: Monitor
watch -n 1 'curl -s -X POST -d "{\"method\":\"getInfo\"}" localhost:16111 | jq'
```

**Validation**:
```bash
# Check all nodes see same tip
curl -s localhost:16111 -d '{"method":"getSelectedTipHash"}' | jq
curl -s localhost:16121 -d '{"method":"getSelectedTipHash"}' | jq  
curl -s localhost:16131 -d '{"method":"getSelectedTipHash"}' | jq

# Should all return same hash
```

**Success criteria**:
- All 3 nodes running
- Blocks propagate < 2 seconds
- Canonical chains match
- No forks or divergence

**Estimated time**: 8-12 hours (including debugging)

---

### 6.2 Configure Blockscout Explorer

**Current State**: Configuration documented but not implemented

**Tasks**:
- [ ] Clone Blockscout repository
- [ ] Apply PHOENIX_CONFIG.md changes
- [ ] Configure RPC endpoint to Phoenix node
- [ ] Set chain ID to 8888 (testnet)
- [ ] Run database migrations
- [ ] Start explorer
- [ ] Verify blocks appear
- [ ] Test transaction history

**Commands**:
```bash
# Clone Blockscout
git clone https://github.com/blockscout/blockscout.git
cd blockscout

# Apply Phoenix config
cp ../phoenix-workspace/phoenix-explorer/PHOENIX_CONFIG.md docs/

# Edit config/dev.exs (per PHOENIX_CONFIG.md)
# Set RPC URL to http://localhost:8545
# Set chain_id to 8888

# Setup database
mix deps.get
mix ecto.create
mix ecto.migrate

# Start explorer
mix phx.server

# Open http://localhost:4000
```

**Success criteria**:
- Explorer shows blocks
- Transactions visible
- Contract addresses work
- Token transfers shown

**Estimated time**: 6-10 hours

---

## Phase 7: Public Testnet (Week 10-11)

### 7.1 Deploy to VPS

**Current State**: Local testnet working, need public deployment

**Tasks**:
- [ ] Provision 3 VPS instances (DigitalOcean/AWS)
- [ ] Configure security groups/firewall
- [ ] Deploy phoenix-node to each VPS
- [ ] Configure DNS for RPC endpoints
- [ ] Set up SSL/TLS for RPC
- [ ] Configure seed nodes
- [ ] Start all nodes
- [ ] Verify connectivity

**Infrastructure**:
```yaml
# infrastructure.yml
VPS1 (Seed Node):
  - phoenix-node (port 30303, 8545)
  - Public RPC endpoint
  - Blockscout explorer

VPS2 (Mining Node):
  - phoenix-node
  - kaspaminer

VPS3 (Archive Node):
  - phoenix-node (full history)
  - Public RPC endpoint
```

**Commands**:
```bash
# On each VPS
scp phoenix-node user@vps:/usr/local/bin/
ssh user@vps

# Configure systemd service
sudo cat > /etc/systemd/system/phoenix-node.service << EOF
[Unit]
Description=Phoenix Node
After=network.target

[Service]
Type=simple
User=phoenix
ExecStart=/usr/local/bin/phoenix-node --testnet --rpclisten=0.0.0.0:8545
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable phoenix-node
sudo systemctl start phoenix-node
```

**Success criteria**:
- All 3 nodes accessible publicly
- Block production stable
- RPC responds to queries
- Explorer accessible via domain

**Estimated time**: 12-16 hours

---

### 7.2 Community Testing

**Current State**: No external users

**Tasks**:
- [ ] Write testnet announcement
- [ ] Create faucet (manual or automated)
- [ ] Provide testnet tokens to testers
- [ ] Monitor for bugs
- [ ] Fix critical issues quickly
- [ ] Collect feedback

**Testnet info to publish**:
```markdown
# Phoenix Testnet

## RPC Endpoints
- https://rpc.testnet.bdp.network
- Chain ID: 8888

## Explorer
- https://explorer.testnet.bdp.network

## Faucet
- https://faucet.testnet.bdp.network
- Request tokens: Discord/Telegram

## SDK
```javascript
const provider = new Phoenix.Provider('https://rpc.testnet.bdp.network');
```

## Test Contract
Deploy your contracts and report any issues!
```

**Success criteria**:
- 10+ external users testing
- Contracts deployed by others
- No critical bugs reported
- Uptime > 95%

**Estimated time**: Ongoing during Week 10-11

---

## Phase 8: Mainnet Preparation (Week 12)

### 8.1 Stability Testing

**Current State**: Testnet running, need confidence for mainnet

**Tasks**:
- [ ] Run 48-hour stress test
- [ ] Deploy complex contracts (Uniswap clone, etc.)
- [ ] Simulate high transaction volume
- [ ] Test reorg handling (force by disconnecting nodes)
- [ ] Monitor memory usage
- [ ] Check for memory leaks
- [ ] Performance profiling

**Stress test script**:
```javascript
// Spam transactions for 48 hours
async function stressTest() {
    const provider = new Phoenix.Provider(RPC_URL);
    const wallet = new Phoenix.Wallet(PRIVATE_KEY, provider);
    
    for (let i = 0; i < 10000; i++) {
        // Send transaction
        const tx = await wallet.sendTransaction({
            to: randomAddress(),
            value: ethers.utils.parseEther("0.1")
        });
        
        console.log(`TX ${i}: ${tx.hash}`);
        
        // Don't overwhelm
        await sleep(1000);
    }
}
```

**Monitoring**:
```bash
# Monitor daemon
watch -n 5 'ps aux | grep phoenix-node'
top -p $(pgrep phoenix-node)

# Check logs for errors
tail -f /var/log/phoenix/node.log | grep -i error

# Monitor block production
watch -n 5 'curl -s localhost:8545 -d "{\"method\":\"eth_blockNumber\"}" | jq'
```

**Success criteria**:
- 48 hours uptime
- No crashes
- No memory leaks
- Block time stable
- Transactions process correctly

**Estimated time**: 48 hours + 8 hours setup/monitoring

---

### 8.2 Security Checklist

**Current State**: No security review

**Tasks**:
- [ ] Review consensus critical paths
- [ ] Check for DoS vectors
- [ ] Validate transaction signature verification
- [ ] Test invalid block handling
- [ ] Review state management for bugs
- [ ] Check RPC input validation
- [ ] Test p2p message handling

**Security tests**:
```go
// Test invalid signatures
func TestRejectInvalidSignature(t *testing.T) {
    // Create transaction with invalid signature
    // Verify it's rejected
}

// Test double spend
func TestRejectDoubleSpend(t *testing.T) {
    // Submit same transaction twice
    // Verify second is rejected
}

// Test malformed blocks
func TestRejectMalformedBlock(t *testing.T) {
    // Create block with invalid data
    // Verify consensus rejects it
}
```

**Success criteria**:
- Basic security tests pass
- No obvious vulnerabilities
- Input validation on all RPC methods
- Known issues documented

**Estimated time**: 12-16 hours

**Note**: Full security audit post-mainnet

---

### 8.3 Mainnet Launch

**Current State**: Testnet stable, ready for mainnet

**Tasks**:
- [ ] Final configuration review
- [ ] Set mainnet genesis time
- [ ] Configure mainnet chain ID (888)
- [ ] Prepare seed nodes
- [ ] Write launch announcement
- [ ] Deploy mainnet nodes
- [ ] Monitor intensively for 24 hours
- [ ] Fix critical bugs immediately

**Launch checklist**:
```bash
# 1. Update configuration
cd ../phoenix-workspace/phoenix-node
# Edit domain/dagconfig/params.go - set mainnet params

# 2. Build release binary
go build -o phoenix-node-mainnet ./cmd/bdpd
./phoenix-node-mainnet --version

# 3. Launch seed nodes (3 minimum)
# VPS 1-3 with public IPs

# 4. Announce on social media
# Twitter, Reddit, Discord, GitHub

# 5. Monitor 24/7
# First 48 hours critical
```

**Launch announcement template**:
```markdown
# Phoenix Mainnet Launch 🚀

We're excited to announce Phoenix mainnet is LIVE!

## What is Phoenix?
- DAG-based blockchain (Kaspa-derived GHOSTDAG)
- Full EVM smart contract support
- Sub-second block times
- Open source

## Mainnet Details
- Chain ID: 888
- RPC: https://rpc.bdp.network
- Explorer: https://explorer.bdp.network
- Symbol: BDP

## For Developers
Deploy contracts using standard Ethereum tools.
GitHub: https://github.com/BlockDAGPhoenix

## Warning
This is experimental software. Use at your own risk.
Not audited. Expect bugs. Report issues on GitHub.
```

**Success criteria**:
- Mainnet launched
- Blocks being produced
- At least 5 external nodes join
- No critical crashes in first 48 hours

**Estimated time**: 16-24 hours + ongoing monitoring

---

## Phase 9: Post-Launch Iteration (Week 13+)

### 9.1 Bug Fixes

**Track all issues**:
- GitHub Issues for bug reports
- Priority: Critical (crashes) > High (data loss) > Medium > Low
- Fix critical within 24 hours
- Release patches frequently

### 9.2 Performance Optimization

**After stability achieved**:
- [ ] Profile CPU usage
- [ ] Optimize canonical chain building
- [ ] Cache state roots
- [ ] Implement state pruning
- [ ] Optimize P2P message handling

### 9.3 Feature Additions

**Post-MVP features** (Month 4+):
- [ ] Add kHeavyHash mining (second algorithm)
- [ ] Implement EIP-1559 gas pricing
- [ ] Add reorg handling beyond 10 blocks
- [ ] State pruning and archival nodes
- [ ] Mining pool software
- [ ] Additional SDKs (Python, Go)
- [ ] Mobile wallet

---

## Critical Path Summary

### Must-Complete for Production

**Week 1**: 
- ✅ Fix canonicalization compilation
- ✅ Daemon runs stable
- ✅ RPC works

**Week 2-3**:
- ✅ EVM executor wired
- ✅ Transactions execute
- ✅ State persists

**Week 4-6**:
- ✅ First contract deployed
- ✅ SDK tested end-to-end
- ✅ Local testnet stable

**Week 7-9**:
- ✅ Public testnet launched
- ✅ External testing
- ✅ Bugs fixed

**Week 10-12**:
- ✅ 48-hour stability test
- ✅ Security review (basic)
- ✅ Mainnet launched

---

## Resource Requirements

### Time Commitment
- **Week 1-4**: 60-80 hours (debugging, integration)
- **Week 5-8**: 40-60 hours (testing, refinement)
- **Week 9-12**: 60-80 hours (deployment, monitoring)
- **Total**: 160-220 hours over 12 weeks

### AI Assistance Budget
- **Targeted fixes**: $200
- **Testing generation**: $100
- **Documentation**: $50
- **Iterations**: $150
- **Total**: ~$500

### Infrastructure
- **VPS** (3 nodes): $60/month × 3 months = $180
- **Domain**: $12/year
- **SSL**: Free (Let's Encrypt)
- **Total**: ~$200

### Grand Total: ~$700

---

## Risk Mitigation

### High-Risk Areas

1. **DAG→EVM Integration** (NEW CODE)
   - Risk: Doesn't work correctly
   - Mitigation: Extensive testing, simple first version
   - Fallback: Use simpler DAG or fork Ethereum instead

2. **State Consistency** (CRITICAL)
   - Risk: Nodes diverge on state
   - Mitigation: Deterministic ordering, thorough testing
   - Fallback: Checkpoint system

3. **Performance** (UNCERTAIN)
   - Risk: Too slow for production use
   - Mitigation: Profile and optimize
   - Fallback: Accept lower throughput for MVP

### Contingency Plans

**If Week 4: Canonicalization not working**
- Simplify to single-tip only (no parallel blocks)
- Reduces to linear chain temporarily

**If Week 8: EVM integration failing**
- Use existing Ethereum as sidechain
- Bridge to Phoenix later

**If Week 12: Not production-ready**
- Launch as "experimental mainnet"
- Clearly mark as alpha
- Accept bugs, iterate quickly

---

## Success Metrics

### Technical Milestones

- [ ] Daemon: 7 days uptime without restart
- [ ] Blocks: 100,000+ blocks produced
- [ ] Transactions: 10,000+ processed
- [ ] Contracts: 50+ deployed
- [ ] Nodes: 10+ independent operators

### Business Milestones

- [ ] GitHub: 100+ stars
- [ ] Community: 500+ Discord members
- [ ] Developers: 20+ deploying contracts
- [ ] Recognition: Mentioned by crypto media

### Go/No-Go Criteria for Mainnet

**GO if**:
- 48-hour stability test passes
- Contract deployment works
- At least 3 nodes ready
- Critical bugs fixed

**NO-GO if**:
- Consensus divergence
- Data corruption
- Critical security flaw
- Blocks stop producing

---

## Daily Checklist Template

Use this for daily focus:

```markdown
## Day X - Phoenix Development

### Morning (4 hours)
- [ ] Review overnight test results
- [ ] Fix top priority bug
- [ ] Deploy fix to testnet

### Afternoon (4 hours)  
- [ ] Implement next feature
- [ ] Write tests
- [ ] Run integration tests

### Evening (2 hours)
- [ ] Deploy AI tasks for overnight
- [ ] Update documentation
- [ ] Plan tomorrow

### Success: Define 1 thing that MUST work by end of day
Today's goal: _______________
```

---

## Week-by-Week Targets

### Week 1: Foundation
**Goal**: Daemon runs without crashing  
**Deliverable**: Running node, producing blocks

### Week 2-3: Integration
**Goal**: Canonicalization wired to EVM  
**Deliverable**: Canonical chain visible via RPC

### Week 4: Contracts
**Goal**: First contract deployed  
**Deliverable**: Working EVM execution

### Week 5-6: SDK
**Goal**: SDK works end-to-end  
**Deliverable**: Example app using SDK

### Week 7-8: Local Testnet
**Goal**: 3-node network stable  
**Deliverable**: Multi-node testnet

### Week 9-10: Public Testnet
**Goal**: External users testing  
**Deliverable**: Public RPC and explorer

### Week 11: Stability
**Goal**: 48-hour stress test passes  
**Deliverable**: Confidence for mainnet

### Week 12: Launch
**Goal**: Mainnet launched  
**Deliverable**: Production blockchain live

---

## The Honest Assessment

### What This Plan Achieves

✅ Proves DAG→EVM concept works  
✅ Creates working blockchain  
✅ Demonstrates technical capability  
✅ Provides base for iteration

### What This Plan Doesn't Achieve

❌ Production-quality code  
❌ Full security audit  
❌ High performance  
❌ Complete feature set  
❌ Enterprise-ready

### But That's Okay Because...

This is an MVP to prove the concept. You'll iterate in production.

**v1**: Rough but functional (Month 3)  
**v2**: Refined and tested (Month 6)  
**v3**: Production-quality (Month 12)  

---

## Final Recommendations

### Do This First (Priority Order)

1. **Fix canonicalization compilation** (Today)
2. **Test daemon startup** (Today)
3. **Wire to EVM executor** (This week)
4. **Deploy test contract** (This week)
5. **Local testnet** (Next week)

### Don't Do Yet

- Performance optimization
- Advanced features
- Professional UI
- Comprehensive docs
- Marketing

### Accept These Limitations

- Bugs will exist
- Performance will be low
- Features will be minimal
- Documentation will be sparse
- **But it will work**

---

## Next Action (Right Now)

```bash
cd /Users/admin/Dev/Crypto/BlockDAG/../phoenix-workspace/phoenix-node

# Fix the compilation
grep -r "GetBlueScore\|BlueScore" domain/consensus/processes/ | head -5
# Find correct API

# Update domain/canonical/ordering.go with correct calls

# Test
go build ./domain/canonical

# Then test daemon
./phoenix-node --testnet --appdir=/tmp/test
```

**Focus**: Get canonicalization compiling first. Everything else depends on this.

---

**Remember**: The goal is a working blockchain in 3 months, not a perfect one. Launch, iterate, improve. You've completed the framework - now make it functional.

