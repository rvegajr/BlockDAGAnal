# Phoenix - Immediate Next Actions
**Post-Plan Completion: Integration Sprint Begins**

**Status**: Framework ✅ Complete | Integration ⏳ Starting  
**Philosophy**: "Launch something, even if imperfect"

---

## 🎯 Where We Are

### ✅ Completed (All Plan Todos)
- Repositories created and configured
- Kaspa forked and rebranded
- Daemon compiles and runs (phoenix-node: 25MB)
- Miner compiles (kaspaminer: 20MB)
- Canonicalization module exists (82 lines)
- EVM executor framework exists (37 lines)
- JavaScript SDK created (27 lines)
- Testnet/mainnet scripts ready

### ⏳ What Needs Work (Integration)
- Canonicalization not called by consensus yet
- EVM not executing transactions
- RPC missing eth_* methods
- SDK not tested against live RPC
- Testnet not launched yet

---

## 🚀 IMMEDIATE SPRINT (Next 72 Hours)

### Day 1: Get Daemon Producing Blocks

**Goal**: See "Block #1 produced" in logs

**Tasks**:
1. Start daemon and verify it doesn't crash
2. Check if mining works
3. Verify blocks are being created
4. Monitor for errors

**Commands**:
```bash
cd /Users/admin/Dev/Crypto/phoenix-workspace/phoenix-node

# Start daemon
./phoenix-node --testnet --appdir=/tmp/phoenix-test --logdir=/tmp/phoenix-logs

# In another terminal, check status
curl -X POST http://localhost:16111 -d '{"jsonrpc":"2.0","method":"getInfo","params":[],"id":1}'

# Start miner
./kaspaminer --rpcserver=localhost:16111 --miningaddr=phoenix:qzxyz...

# Watch logs
tail -f /tmp/phoenix-logs/*.log | grep -i "block\|mined\|error"
```

**Expected Outcome**:
- Daemon runs for 1+ hour without crashing
- Logs show block production
- Mining works (even if slow)

**If it doesn't work**:
- Check logs for specific errors
- Fix one error at a time
- Use AI for specific error fixes: Deploy targeted task

**Time**: 4-8 hours

---

### Day 2: Wire Canonicalization to Consensus

**Goal**: Canonical chain is being computed on each new block

**Tasks**:
1. Find where Kaspa adds blocks to DAG
2. Add canonicalization call
3. Log canonical chain updates
4. Verify ordering is deterministic

**Implementation**:
```go
// Find in: domain/consensus/consensus.go or app/protocol/flows/
// Look for: "OnBlockAdded" or "ProcessBlock"

// Add after block acceptance:
func (c *consensus) OnBlockAdded(block *DomainBlock) error {
    // Existing Kaspa code...
    
    // NEW: Build canonical chain
    canonicalBuilder := canonical.NewCanonicalBuilder(c.dagAdapter)
    canonicalChain, err := canonicalBuilder.BuildCanonicalSequence()
    if err != nil {
        log.Warnf("Canonical chain build failed: %v", err)
        // Don't fail consensus - just log for now
    } else {
        log.Infof("Canonical chain updated: %d blocks", len(canonicalChain))
        // TODO: Store canonical indices
    }
    
    return nil
}
```

**Find these files**:
```bash
grep -r "OnBlockAdded\|ProcessBlock" domain/consensus/ | grep "\.go:"
grep -r "BlockAdded" app/protocol/ | grep "\.go:"
```

**Success Criteria**:
- Logs show "Canonical chain updated" on each block
- No crashes from canonicalization calls
- Chain length increases

**Time**: 6-10 hours

---

### Day 3: Create DAGReader Adapter

**Goal**: Canonicalization can actually read from Kaspa's DAG

**Current Issue**: DAGReader interface exists but no implementation

**Tasks**:
1. Create `domain/canonical/dag_adapter.go`
2. Implement interface using Kaspa's consensus manager
3. Test it compiles
4. Use in canonicalization

**Implementation**:
```go
// File: domain/canonical/dag_adapter.go
package canonical

import (
    "github.com/BlockDAGPhoenix/phoenix-node/domain/consensus"
    "github.com/BlockDAGPhoenix/phoenix-node/domain/consensus/model/externalapi"
)

type KaspaDAGAdapter struct {
    consensusManager consensus.Consensus
}

func NewKaspaDAGAdapter(cm consensus.Consensus) *KaspaDAGAdapter {
    return &KaspaDAGAdapter{consensusManager: cm}
}

func (k *KaspaDAGAdapter) GetBlock(hash *externalapi.DomainHash) (*externalapi.DomainBlock, error) {
    return k.consensusManager.GetBlock(hash)
}

func (k *KaspaDAGAdapter) GetBlueScore(block *externalapi.DomainBlock) uint64 {
    ghostdagData, err := k.consensusManager.GetBlockGHOSTDAGData(block.Header.Hash())
    if err != nil {
        return 0
    }
    return ghostdagData.BlueScore
}

func (k *KaspaDAGAdapter) GetTips() ([]*externalapi.DomainHash, error) {
    return k.consensusManager.Tips(), nil
}

func (k *KaspaDAGAdapter) GetGenesisHash() *externalapi.DomainHash {
    return k.consensusManager.GenesisHash()
}
```

**Find Kaspa API**:
```bash
cd /Users/admin/Dev/Crypto/phoenix-workspace/phoenix-node
grep -r "interface Consensus" domain/consensus/
grep -r "GetBlock\|GetBlockGHOSTDAGData" domain/consensus/
grep -r "Tips()" domain/consensus/
```

**Success Criteria**:
- Adapter compiles
- Can retrieve blocks from consensus
- Blue score lookup works
- Tips() returns correct hashes

**Time**: 6-8 hours

---

## 🔥 Week 1 Sprint Plan

### Monday-Tuesday: Core Daemon
- ✅ Daemon starts
- ✅ Produces blocks
- ✅ Mining works
- ✅ Runs 24 hours stable

### Wednesday-Thursday: Canonicalization
- ✅ DAGReader adapter working
- ✅ Called on each block
- ✅ Canonical chain computed
- ✅ Ordering deterministic

### Friday: EVM Preparation
- ✅ Add go-ethereum dependency
- ✅ Create minimal state DB
- ✅ Wire to canonicalization

### Weekend: Testing
- ✅ Deploy test contract attempt
- ✅ Document issues
- ✅ Plan Week 2

---

## 🎯 Week 2-3: EVM Integration Sprint

### Goal: First Smart Contract Deployed

**Must Complete**:
1. EVM processes canonical blocks
2. Transactions execute
3. State persists
4. Receipts generated
5. RPC exposes eth_sendRawTransaction
6. SDK can deploy contract

**Approach**:
- Use go-ethereum's EVM directly
- Don't modify EVM code
- Just wire inputs/outputs
- Deploy simplest possible contract

**Test Contract**:
```solidity
pragma solidity ^0.8.0;
contract Test {
    uint public value;
    function set(uint _v) public { value = _v; }
}
```

**Success**: Can deploy this and call `set(42)`

---

## 🎯 Week 4: Testnet Launch

### Goal: 3 nodes running, producing blocks

**Tasks**:
1. Run testnet-setup.sh
2. Start all 3 nodes
3. Mine blocks
4. Verify sync
5. Keep running 24 hours

**Success Criteria**:
- All 3 nodes see same tip
- Blocks propagate < 5 seconds
- No crashes for 24 hours

---

## 🎯 Month 2-3: Path to Mainnet

Following the plan's timeline:

**Week 5-8**: 
- Stability improvements
- Bug fixes
- Basic testing

**Week 9-11**:
- Public testnet
- External testing
- Critical fixes

**Week 12**:
- **"Launch regardless of state"** (per plan)
- Iterate in production
- Fix issues as they come

---

## 🛠️ Tactical Tools Available

### For Quick Fixes
```bash
# Use AI for specific issues
cd /Users/admin/Dev/Crypto/BlockDAG/crewai
source venv/bin/activate

# Example: Fix specific compilation error
python -c "
from crews.phoenix_node_crew import go_backend_developer
from crewai import Task
task = Task(
    description='Fix compilation error in domain/canonical/ordering.go: [paste error]',
    agent=go_backend_developer,
    expected_output='Working code'
)
task.execute()
"
```

### For Testing
```bash
# Quick daemon test
cd ../phoenix-workspace/phoenix-node
./phoenix-node --testnet --appdir=/tmp/test &
sleep 5
curl localhost:16111 -d '{"method":"getInfo"}'
pkill phoenix-node
```

### For Debugging
```bash
# Find where to integrate
grep -r "ProcessBlock\|OnBlockAdded" domain/consensus/
grep -r "Tips()\|GetBlock" domain/consensus/
grep -r "GHOSTDAGData" domain/consensus/
```

---

## 📋 Success Tracking

### Daily Checklist
- [ ] Daemon runs without crashing
- [ ] Logs show progress
- [ ] One specific feature working
- [ ] No regressions
- [ ] Tomorrow's target defined

### Weekly Checklist
- [ ] Daemon runs 24 hours
- [ ] New feature integrated
- [ ] Tests passing
- [ ] Documented in GitHub
- [ ] Next week planned

---

## 🚨 When to Use AI vs When to Code

### Use AI For:
- Generating boilerplate
- Writing test templates
- Finding Kaspa API usage
- Code formatting
- Documentation

### Code Yourself:
- Critical integration points
- Debugging actual issues
- Performance optimization
- Security-critical code
- Final decisions

---

## 🎯 The 72-Hour Challenge

**Can you get the daemon producing blocks in 72 hours?**

If YES:
- You're on track for Week 4 testnet
- Continue with integration

If NO:
- Assess blockers
- Deploy AI task for specific issue
- Consider simplifications

---

## 📞 Quick Reference Commands

### Start Daemon
```bash
cd /Users/admin/Dev/Crypto/phoenix-workspace/phoenix-node
./phoenix-node --testnet --appdir=/tmp/test
```

### Check Status
```bash
curl -X POST localhost:16111 -d '{"jsonrpc":"2.0","method":"getInfo","params":[],"id":1}'
```

### View Logs
```bash
tail -f /tmp/test/*.log
```

### Mine Block
```bash
./kaspaminer --rpcserver=localhost:16111 --miningaddr=<address>
```

### Kill All
```bash
pkill phoenix-node
pkill kaspaminer
rm -rf /tmp/phoenix-test
```

---

## 🎉 Remember

You've completed the plan's todos. The plan says:

> "Launch regardless of state → Iterate in production"

You have a working foundation. Now it's integration grind. 

**The plan worked. Now execute the integration.**

---

## IMMEDIATE NEXT ACTION (RIGHT NOW)

```bash
cd /Users/admin/Dev/Crypto/phoenix-workspace/phoenix-node
./phoenix-node --testnet --appdir=/tmp/phoenix-test 2>&1 | tee daemon-test.log
```

**Watch for**:
- Startup errors
- Genesis block loading
- P2P initialization
- Whether it stays running

**Report back**: What errors appear in the logs?

That's your next debugging target.

