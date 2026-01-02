# DAG→EVM Edge Cases and Error Handling Specification
## Critical Scenarios and Recovery Mechanisms

**Version**: 1.0.0  
**Status**: Production-Ready  
**Criticality**: HIGH - Required for Robust Production System

---

## Table of Contents

1. [Network Partition Scenarios](#1-network-partition-scenarios)
2. [Time-Related Edge Cases](#2-time-related-edge-cases)
3. [State Consistency Challenges](#3-state-consistency-challenges)
4. [Transaction Conflict Resolution](#4-transaction-conflict-resolution)
5. [Memory and Resource Exhaustion](#5-memory-and-resource-exhaustion)
6. [Consensus Edge Cases](#6-consensus-edge-cases)
7. [Recovery Mechanisms](#7-recovery-mechanisms)
8. [Error Propagation and Handling](#8-error-propagation-and-handling)

---

## 1. Network Partition Scenarios

### 1.1 Split-Brain Scenario

**Scenario**: Network splits into two or more partitions that continue mining independently.

```go
type PartitionScenario struct {
    Duration        time.Duration
    PartitionCount  int
    BlocksPerPartition map[int]int
}

// HandleNetworkReunification manages partition recovery
func HandleNetworkReunification(partitions []Partition) (*UnificationResult, error) {
    // Step 1: Identify partition characteristics
    partitionAnalysis := make([]PartitionAnalysis, len(partitions))
    for i, p := range partitions {
        partitionAnalysis[i] = AnalyzePartition(p)
    }
    
    // Step 2: Determine canonical partition (highest cumulative work)
    canonicalIdx := 0
    maxWork := big.NewInt(0)
    
    for i, analysis := range partitionAnalysis {
        if analysis.CumulativeWork.Cmp(maxWork) > 0 {
            maxWork = analysis.CumulativeWork
            canonicalIdx = i
        }
    }
    
    // Step 3: Calculate reorg requirements for non-canonical partitions
    reorgPlans := make([]ReorgPlan, 0)
    for i, partition := range partitions {
        if i == canonicalIdx {
            continue
        }
        
        plan := CalculateReorgPlan(
            partitions[canonicalIdx],
            partition,
            MAX_PARTITION_REORG_DEPTH,
        )
        
        if plan.ReorgDepth > MAX_PARTITION_REORG_DEPTH {
            return nil, ErrPartitionReorgTooDeep{
                RequestedDepth: plan.ReorgDepth,
                MaxDepth: MAX_PARTITION_REORG_DEPTH,
            }
        }
        
        reorgPlans = append(reorgPlans, plan)
    }
    
    // Step 4: Execute unification
    result := &UnificationResult{
        CanonicalPartition: canonicalIdx,
        ReorgPlans: reorgPlans,
        OrphanedBlocks: 0,
        OrphanedTransactions: make([]*Transaction, 0),
    }
    
    for _, plan := range reorgPlans {
        // Extract orphaned transactions
        for _, block := range plan.BlocksToRevert {
            result.OrphanedBlocks++
            result.OrphanedTransactions = append(
                result.OrphanedTransactions,
                block.Transactions...,
            )
        }
    }
    
    return result, nil
}

// Critical constants
const (
    MAX_PARTITION_REORG_DEPTH = 1000  // Maximum blocks to reorg after partition
    PARTITION_DETECTION_THRESHOLD = 30 * time.Second  // Time to detect partition
)
```

### 1.2 Asymmetric Partition

**Scenario**: Majority of network in one partition, minority isolated.

```go
func HandleAsymmetricPartition(majority, minority Partition) error {
    majoritySize := len(majority.Nodes)
    minoritySize := len(minority.Nodes)
    
    if float64(minoritySize)/float64(majoritySize+minoritySize) < 0.1 {
        // Less than 10% of network - automatic surrender
        return ForceReorgToMajority(minority, majority)
    }
    
    // Between 10-49% - use work-based resolution
    return WorkBasedResolution(majority, minority)
}
```

---

## 2. Time-Related Edge Cases

### 2.1 Clock Drift Attack

**Scenario**: Miners manipulate timestamps to gain advantage.

```go
type ClockDriftDetector struct {
    maxDrift        time.Duration
    medianWindow    int
    suspicionThreshold float64
}

func (cdd *ClockDriftDetector) ValidateTimestamp(block *Block, dag *BlockDAG) error {
    now := time.Now().Unix()
    
    // Rule 1: Block cannot be more than 15 seconds in future
    if block.Timestamp > now + MAX_FUTURE_TIME_SECONDS {
        return ErrTimestampTooFarInFuture{
            BlockTime: block.Timestamp,
            CurrentTime: now,
            MaxFuture: MAX_FUTURE_TIME_SECONDS,
        }
    }
    
    // Rule 2: Median time past (MTP) rule
    medianTime := cdd.calculateMedianTime(dag, block.CanonicalIndex)
    if block.Timestamp <= medianTime {
        return ErrTimestampBeforeMedian{
            BlockTime: block.Timestamp,
            MedianTime: medianTime,
        }
    }
    
    // Rule 3: Detect systematic manipulation
    drift := cdd.detectSystematicDrift(block, dag)
    if drift > cdd.suspicionThreshold {
        return ErrSuspectedTimestampManipulation{
            DriftScore: drift,
            Threshold: cdd.suspicionThreshold,
        }
    }
    
    return nil
}

func (cdd *ClockDriftDetector) calculateMedianTime(dag *BlockDAG, index uint64) int64 {
    // Get last 11 blocks
    blockCount := 11
    if index < uint64(blockCount) {
        blockCount = int(index)
    }
    
    timestamps := make([]int64, blockCount)
    for i := 0; i < blockCount; i++ {
        block := dag.GetBlockAtIndex(index - uint64(i))
        timestamps[i] = block.Timestamp
    }
    
    sort.Slice(timestamps, func(i, j int) bool {
        return timestamps[i] < timestamps[j]
    })
    
    return timestamps[len(timestamps)/2]
}
```

### 2.2 Time Warp Attack

**Scenario**: Coordinated timestamp manipulation to adjust difficulty.

```go
func DetectTimeWarpAttack(blocks []*Block, window int) bool {
    if len(blocks) < window {
        return false
    }
    
    // Check for alternating timestamp pattern (classic time warp)
    suspiciousPattern := 0
    for i := 1; i < len(blocks)-1; i++ {
        prev := blocks[i-1].Timestamp
        curr := blocks[i].Timestamp
        next := blocks[i+1].Timestamp
        
        // Detect sawtooth pattern
        if (curr > prev+3600 && next < curr-3600) ||
           (curr < prev-3600 && next > curr+3600) {
            suspiciousPattern++
        }
    }
    
    // If more than 30% show pattern, likely attack
    return float64(suspiciousPattern)/float64(len(blocks)) > 0.3
}
```

---

## 3. State Consistency Challenges

### 3.1 State Root Mismatch After Reorg

**Scenario**: State root doesn't match expected after reorganization.

```go
type StateRecovery struct {
    checkpointManager *CheckpointManager
    stateRebuilder   *StateRebuilder
    validator        *StateValidator
}

func (sr *StateRecovery) HandleStateRootMismatch(
    expected common.Hash,
    actual common.Hash,
    block *Block,
) error {
    // Level 1: Try re-execution
    reexecuted, err := sr.stateRebuilder.ReexecuteBlock(block)
    if err == nil && reexecuted.StateRoot == expected {
        return nil // Fixed by re-execution
    }
    
    // Level 2: Restore from checkpoint and replay
    checkpoint, err := sr.checkpointManager.GetNearestCheckpoint(block.CanonicalIndex)
    if err != nil {
        return sr.handleNoCheckpoint(block)
    }
    
    state, err := sr.checkpointManager.RestoreCheckpoint(checkpoint.BlockNumber)
    if err != nil {
        return fmt.Errorf("checkpoint restore failed: %w", err)
    }
    
    // Replay blocks from checkpoint
    for i := checkpoint.BlockNumber + 1; i <= block.CanonicalIndex; i++ {
        replayBlock := GetCanonicalBlock(i)
        if _, err := ExecuteBlock(state, replayBlock); err != nil {
            return fmt.Errorf("replay failed at block %d: %w", i, err)
        }
    }
    
    if state.IntermediateRoot() != expected {
        // Level 3: Full resync required
        return ErrStateCorruption{
            Block: block.Hash,
            Expected: expected,
            Actual: state.IntermediateRoot(),
            Action: "full_resync_required",
        }
    }
    
    return nil
}

func (sr *StateRecovery) handleNoCheckpoint(block *Block) error {
    // No checkpoint available - must rebuild from genesis
    log.Error("No checkpoint available for recovery", "block", block.CanonicalIndex)
    
    // Option 1: Rebuild from genesis (slow)
    if block.CanonicalIndex < GENESIS_REBUILD_THRESHOLD {
        return sr.rebuildFromGenesis(block)
    }
    
    // Option 2: Request state from peers (fast but requires trust)
    return sr.requestStateFromPeers(block)
}

const GENESIS_REBUILD_THRESHOLD = 10000 // Rebuild from genesis if less than this
```

### 3.2 Storage Trie Corruption

**Scenario**: Contract storage trie becomes corrupted.

```go
func HandleStorageCorruption(address common.Address, state *StateDB) error {
    // Attempt to rebuild storage trie
    account := state.GetAccount(address)
    if account == nil {
        return ErrAccountNotFound
    }
    
    // Create new storage trie
    newStorageRoot, err := RebuildStorageTrie(address, state)
    if err != nil {
        // Storage unrecoverable - mark for cleanup
        state.MarkStorageCorrupted(address)
        return ErrStorageUnrecoverable{
            Address: address,
            Error: err,
        }
    }
    
    // Update account with new storage root
    account.StorageRoot = newStorageRoot
    state.UpdateAccount(address, account)
    
    return nil
}
```

---

## 4. Transaction Conflict Resolution

### 4.1 Same Nonce in Parallel Blocks

**Scenario**: Same account sends transactions with same nonce in parallel blocks.

```go
type ConflictResolver struct {
    policy ConflictPolicy
}

func (cr *ConflictResolver) ResolveNonceConflict(
    conflicts []TxConflict,
    canonical []*Block,
) (*Resolution, error) {
    
    resolution := &Resolution{
        Valid: make([]*Transaction, 0),
        Invalid: make([]*Transaction, 0),
        Refund: make([]*Transaction, 0),
    }
    
    for _, conflict := range conflicts {
        // Sort by canonical order
        sort.Slice(conflict.Transactions, func(i, j int) bool {
            blockI := conflict.Blocks[i]
            blockJ := conflict.Blocks[j]
            
            idxI := GetCanonicalIndex(blockI, canonical)
            idxJ := GetCanonicalIndex(blockJ, canonical)
            
            if idxI != idxJ {
                return idxI < idxJ
            }
            
            // Same block - use transaction index
            return conflict.TxIndices[i] < conflict.TxIndices[j]
        })
        
        // First transaction is valid
        resolution.Valid = append(resolution.Valid, conflict.Transactions[0])
        
        // Rest are invalid but may be refunded based on policy
        for i := 1; i < len(conflict.Transactions); i++ {
            tx := conflict.Transactions[i]
            
            if cr.policy.ShouldRefund(tx) {
                resolution.Refund = append(resolution.Refund, tx)
            } else {
                resolution.Invalid = append(resolution.Invalid, tx)
            }
        }
    }
    
    return resolution, nil
}
```

### 4.2 Double-Spend Across Forks

**Scenario**: Account attempts to spend same funds in different DAG branches.

```go
func DetectDoubleSpend(tx1, tx2 *Transaction, state *StateDB) bool {
    from1, _ := tx1.Sender()
    from2, _ := tx2.Sender()
    
    if from1 != from2 {
        return false // Different senders
    }
    
    balance := state.GetBalance(from1)
    required1 := new(big.Int).Add(tx1.Value, tx1.GasPrice)
    required2 := new(big.Int).Add(tx2.Value, tx2.GasPrice)
    total := new(big.Int).Add(required1, required2)
    
    return total.Cmp(balance) > 0 // Insufficient for both
}
```

---

## 5. Memory and Resource Exhaustion

### 5.1 DAG Size Explosion

**Scenario**: DAG grows too large for memory.

```go
type DAGPruner struct {
    maxDAGSize      int
    pruneThreshold  float64
    keepDepth       int
}

func (dp *DAGPruner) PruneIfNeeded(dag *BlockDAG) error {
    currentSize := dag.GetSize()
    
    if currentSize > int(float64(dp.maxDAGSize) * dp.pruneThreshold) {
        // Prune old branches keeping only canonical chain + recent forks
        prunedCount := 0
        
        // Get canonical chain
        canonical := dag.GetCanonicalChain()
        keepAfter := len(canonical) - dp.keepDepth
        
        if keepAfter < 0 {
            keepAfter = 0
        }
        
        // Mark blocks to keep
        toKeep := make(map[common.Hash]bool)
        for i := keepAfter; i < len(canonical); i++ {
            // Keep canonical block and its ancestors
            MarkAncestors(canonical[i], toKeep, dp.keepDepth)
        }
        
        // Prune unmarked blocks
        for hash, block := range dag.GetAllBlocks() {
            if !toKeep[hash] {
                dag.RemoveBlock(hash)
                prunedCount++
            }
        }
        
        log.Info("DAG pruned", "removed", prunedCount, "remaining", dag.GetSize())
    }
    
    return nil
}
```

### 5.2 State Cache Overflow

**Scenario**: State cache grows beyond memory limits.

```go
type StateCacheManager struct {
    maxSize         int64
    currentSize     int64
    evictionPolicy  EvictionPolicy
    mu             sync.RWMutex
}

func (scm *StateCacheManager) HandleCacheOverflow() error {
    scm.mu.Lock()
    defer scm.mu.Unlock()
    
    if scm.currentSize <= scm.maxSize {
        return nil
    }
    
    // Calculate how much to evict
    targetSize := int64(float64(scm.maxSize) * 0.8) // Free 20%
    toEvict := scm.currentSize - targetSize
    
    // Evict based on policy
    evicted := scm.evictionPolicy.Evict(toEvict)
    
    scm.currentSize -= evicted
    
    // Force GC if still over limit
    if scm.currentSize > scm.maxSize {
        runtime.GC()
        
        // If still over, emergency eviction
        if scm.currentSize > scm.maxSize {
            return scm.emergencyEviction()
        }
    }
    
    return nil
}

func (scm *StateCacheManager) emergencyEviction() error {
    // Clear all non-essential caches
    scm.ClearNonEssential()
    
    // If still over limit, restart may be needed
    if scm.currentSize > scm.maxSize {
        return ErrMemoryExhaustion{
            Current: scm.currentSize,
            Max: scm.maxSize,
            Action: "restart_required",
        }
    }
    
    return nil
}
```

---

## 6. Consensus Edge Cases

### 6.1 Competing Tip Sets with Equal Work

**Scenario**: Multiple tip sets have exactly equal cumulative work.

```go
func ResolveEqualWorkTips(tipSets []TipSet) *TipSet {
    // Level 1: Blue block count
    maxBlueBlocks := 0
    var bestByBlue []*TipSet
    
    for _, ts := range tipSets {
        blueCount := CountBlueBlocks(ts)
        if blueCount > maxBlueBlocks {
            maxBlueBlocks = blueCount
            bestByBlue = []*TipSet{&ts}
        } else if blueCount == maxBlueBlocks {
            bestByBlue = append(bestByBlue, &ts)
        }
    }
    
    if len(bestByBlue) == 1 {
        return bestByBlue[0]
    }
    
    // Level 2: Total transaction count
    maxTxCount := 0
    var bestByTx []*TipSet
    
    for _, ts := range bestByBlue {
        txCount := CountTransactions(ts)
        if txCount > maxTxCount {
            maxTxCount = txCount
            bestByTx = []*TipSet{ts}
        } else if txCount == maxTxCount {
            bestByTx = append(bestByTx, ts)
        }
    }
    
    if len(bestByTx) == 1 {
        return bestByTx[0]
    }
    
    // Level 3: Earliest timestamp
    earliestTime := int64(math.MaxInt64)
    var bestByTime *TipSet
    
    for _, ts := range bestByTx {
        avgTime := GetAverageTimestamp(ts)
        if avgTime < earliestTime {
            earliestTime = avgTime
            bestByTime = ts
        }
    }
    
    // Level 4: Deterministic hash selection
    if bestByTime == nil {
        return SelectByHashDeterministic(bestByTx)
    }
    
    return bestByTime
}
```

### 6.2 Cyclic DAG Detection

**Scenario**: Bug introduces cycle in DAG.

```go
func DetectCycle(dag *BlockDAG) (*Cycle, error) {
    visited := make(map[common.Hash]int)
    recStack := make(map[common.Hash]bool)
    
    const (
        WHITE = iota // Not visited
        GRAY         // Being processed
        BLACK        // Processed
    )
    
    var cycle *Cycle
    
    var dfs func(hash common.Hash, path []common.Hash) bool
    dfs = func(hash common.Hash, path []common.Hash) bool {
        visited[hash] = GRAY
        recStack[hash] = true
        path = append(path, hash)
        
        block := dag.GetBlock(hash)
        for _, parentHash := range block.Parents {
            if visited[parentHash] == GRAY && recStack[parentHash] {
                // Cycle detected
                cycleStart := 0
                for i, h := range path {
                    if h == parentHash {
                        cycleStart = i
                        break
                    }
                }
                
                cycle = &Cycle{
                    Blocks: path[cycleStart:],
                    Entry: parentHash,
                }
                return true
            }
            
            if visited[parentHash] == WHITE {
                if dfs(parentHash, path) {
                    return true
                }
            }
        }
        
        visited[hash] = BLACK
        recStack[hash] = false
        return false
    }
    
    // Check all blocks
    for hash := range dag.GetAllBlocks() {
        if visited[hash] == WHITE {
            if dfs(hash, []common.Hash{}) {
                return cycle, ErrCycleDetected
            }
        }
    }
    
    return nil, nil
}
```

---

## 7. Recovery Mechanisms

### 7.1 Catastrophic Failure Recovery

```go
type DisasterRecovery struct {
    checkpoints     CheckpointStore
    peerNetwork     PeerNetwork
    genesisState    *StateDB
}

func (dr *DisasterRecovery) RecoverFromCatastrophicFailure() error {
    // Level 1: Try recent checkpoint
    checkpoint, err := dr.checkpoints.GetMostRecent()
    if err == nil {
        if err := dr.restoreFromCheckpoint(checkpoint); err == nil {
            return nil
        }
    }
    
    // Level 2: Request state from peers
    trustedPeers := dr.peerNetwork.GetTrustedPeers()
    for _, peer := range trustedPeers {
        state, err := peer.RequestState()
        if err == nil {
            if err := dr.validateAndRestoreState(state); err == nil {
                return nil
            }
        }
    }
    
    // Level 3: Rebuild from genesis
    log.Warn("Rebuilding from genesis - this will take time")
    return dr.rebuildFromGenesis()
}

func (dr *DisasterRecovery) rebuildFromGenesis() error {
    state := dr.genesisState.Copy()
    
    // Get canonical chain from network
    canonical, err := dr.peerNetwork.GetCanonicalChain()
    if err != nil {
        return err
    }
    
    // Replay all blocks
    for i, block := range canonical {
        if i%1000 == 0 {
            log.Info("Rebuilding progress", "block", i, "total", len(canonical))
        }
        
        if _, err := ExecuteBlock(state, block); err != nil {
            return fmt.Errorf("rebuild failed at block %d: %w", i, err)
        }
        
        // Create checkpoint every 10000 blocks
        if i%10000 == 0 {
            dr.checkpoints.CreateCheckpoint(state, block)
        }
    }
    
    return nil
}
```

### 7.2 Gradual State Repair

```go
type StateRepairer struct {
    validator StateValidator
    repairer  StateRepairEngine
}

func (sr *StateRepairer) RepairCorruptedState(state *StateDB) error {
    // Identify corrupted accounts
    corrupted := sr.validator.FindCorruptedAccounts(state)
    
    if len(corrupted) == 0 {
        return nil
    }
    
    log.Warn("Found corrupted accounts", "count", len(corrupted))
    
    // Repair each account
    repaired := 0
    failed := 0
    
    for _, address := range corrupted {
        if err := sr.repairAccount(state, address); err != nil {
            log.Error("Failed to repair account", "address", address, "error", err)
            failed++
        } else {
            repaired++
        }
    }
    
    if failed > 0 {
        return fmt.Errorf("repaired %d accounts, %d failed", repaired, failed)
    }
    
    return nil
}

func (sr *StateRepairer) repairAccount(state *StateDB, address common.Address) error {
    // Try multiple repair strategies
    strategies := []RepairStrategy{
        sr.repairer.RepairFromCache,
        sr.repairer.RepairFromDisk,
        sr.repairer.RepairFromPeers,
        sr.repairer.ResetToEmpty,
    }
    
    for _, strategy := range strategies {
        if err := strategy(state, address); err == nil {
            // Validate repair
            if sr.validator.ValidateAccount(state, address) {
                return nil
            }
        }
    }
    
    return ErrAccountUnrepairable
}
```

---

## 8. Error Propagation and Handling

### 8.1 Error Classification

```go
type ErrorSeverity int

const (
    SeverityInfo     ErrorSeverity = iota // Log only
    SeverityWarning                        // Log and metric
    SeverityError                          // Recoverable error
    SeverityCritical                       // Requires intervention
    SeverityFatal                          // System must stop
)

type SystemError struct {
    Severity    ErrorSeverity
    Component   string
    Error       error
    Timestamp   time.Time
    Context     map[string]interface{}
    Recovery    RecoveryAction
}

type RecoveryAction func() error

func ClassifyError(err error) *SystemError {
    switch {
    case errors.Is(err, ErrStateCorruption):
        return &SystemError{
            Severity: SeverityCritical,
            Component: "state",
            Error: err,
            Recovery: RecoverState,
        }
        
    case errors.Is(err, ErrCycleDetected):
        return &SystemError{
            Severity: SeverityFatal,
            Component: "consensus",
            Error: err,
            Recovery: nil, // Cannot recover from cycle
        }
        
    case errors.Is(err, ErrReorgTooDeep):
        return &SystemError{
            Severity: SeverityError,
            Component: "reorg",
            Error: err,
            Recovery: LimitedReorg,
        }
        
    case errors.Is(err, ErrMemoryExhaustion):
        return &SystemError{
            Severity: SeverityCritical,
            Component: "memory",
            Error: err,
            Recovery: EmergencyGC,
        }
        
    default:
        return &SystemError{
            Severity: SeverityWarning,
            Component: "unknown",
            Error: err,
            Recovery: nil,
        }
    }
}
```

### 8.2 Error Recovery Pipeline

```go
type ErrorHandler struct {
    classifier  ErrorClassifier
    recoverers  map[string]Recoverer
    alerts      AlertSystem
    metrics     MetricsCollector
}

func (eh *ErrorHandler) HandleError(err error) error {
    // Classify error
    sysErr := eh.classifier.Classify(err)
    
    // Record metrics
    eh.metrics.RecordError(sysErr)
    
    // Log based on severity
    switch sysErr.Severity {
    case SeverityInfo:
        log.Info("System event", "error", err)
        
    case SeverityWarning:
        log.Warn("System warning", "error", err, "component", sysErr.Component)
        
    case SeverityError:
        log.Error("System error", "error", err, "component", sysErr.Component)
        
    case SeverityCritical:
        log.Error("CRITICAL ERROR", "error", err, "component", sysErr.Component)
        eh.alerts.SendCriticalAlert(sysErr)
        
    case SeverityFatal:
        log.Error("FATAL ERROR - SYSTEM WILL STOP", "error", err)
        eh.alerts.SendFatalAlert(sysErr)
        eh.initiateGracefulShutdown()
        return err
    }
    
    // Attempt recovery if available
    if sysErr.Recovery != nil {
        log.Info("Attempting recovery", "component", sysErr.Component)
        
        if recoveryErr := sysErr.Recovery(); recoveryErr != nil {
            // Recovery failed - escalate severity
            sysErr.Severity++
            return eh.HandleError(fmt.Errorf("recovery failed: %w", recoveryErr))
        }
        
        log.Info("Recovery successful", "component", sysErr.Component)
        eh.metrics.RecordRecovery(sysErr.Component)
    }
    
    return nil
}

func (eh *ErrorHandler) initiateGracefulShutdown() {
    log.Info("Initiating graceful shutdown")
    
    // Save current state
    eh.saveEmergencyCheckpoint()
    
    // Notify peers
    eh.notifyPeersOfShutdown()
    
    // Clean shutdown
    os.Exit(1)
}
```

---

## Critical Constants

```go
const (
    // Partition handling
    MAX_PARTITION_DURATION = 24 * time.Hour
    MAX_PARTITION_REORG_DEPTH = 1000
    PARTITION_DETECTION_THRESHOLD = 30 * time.Second
    
    // Time validation
    MAX_FUTURE_TIME_SECONDS = 15
    MEDIAN_TIME_WINDOW = 11
    TIMESTAMP_DRIFT_THRESHOLD = 3600 // 1 hour
    
    // State management
    MAX_STATE_RECOVERY_ATTEMPTS = 3
    STATE_CORRUPTION_DETECTION_INTERVAL = 1000 // blocks
    CHECKPOINT_VALIDATION_FREQUENCY = 100 // blocks
    
    // Resource limits
    MAX_DAG_SIZE_BLOCKS = 1000000
    MAX_STATE_CACHE_MB = 4096
    EMERGENCY_GC_THRESHOLD = 0.9 // 90% memory usage
    
    // Error recovery
    MAX_RECOVERY_TIME = 5 * time.Minute
    RECOVERY_RETRY_DELAY = 10 * time.Second
    CRITICAL_ERROR_THRESHOLD = 10 // Critical errors before shutdown
)
```

---

## Testing Edge Cases

```go
func TestEdgeCases(t *testing.T) {
    testCases := []EdgeCaseTest{
        {
            Name: "Network partition with equal work",
            Setup: CreateEqualWorkPartitions,
            Validate: ValidatePartitionResolution,
        },
        {
            Name: "Clock drift attack detection",
            Setup: CreateClockDriftScenario,
            Validate: ValidateTimestampRejection,
        },
        {
            Name: "State corruption recovery",
            Setup: CorruptStateRandomly,
            Validate: ValidateStateRecovery,
        },
        {
            Name: "Memory exhaustion handling",
            Setup: CreateMemoryPressure,
            Validate: ValidateMemoryRecovery,
        },
        {
            Name: "Cycle detection in DAG",
            Setup: IntroduceCycle,
            Validate: ValidateCycleDetection,
        },
        {
            Name: "Catastrophic failure recovery",
            Setup: SimulateTotalFailure,
            Validate: ValidateFullRecovery,
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.Name, func(t *testing.T) {
            env := tc.Setup()
            err := tc.Validate(env)
            require.NoError(t, err)
        })
    }
}
```

---

This specification provides comprehensive coverage of edge cases and error handling mechanisms essential for a production-ready DAG→EVM integration system.
