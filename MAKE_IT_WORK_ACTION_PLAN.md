# Make Phoenix a Working Crypto Project - Action Plan

## 🎯 Current Status: 85% Complete, 15% Critical Missing

## ✅ What Works

1. **Node Infrastructure**: Phoenix node runs, mines blocks, maintains DAG
2. **EVM Execution**: EVM can execute contracts (when transactions are provided)
3. **RPC Server**: Ethereum-compatible RPC endpoints exist
4. **Canonicalization**: DAG→Linear conversion working
5. **State Management**: StateDB infrastructure in place
6. **Security**: Input validation, rate limiting, replay protection

## ⚠️ Critical Missing (Blocks Functionality)

### 1. Transaction Signing & Validation (CRITICAL - 4-6 hours)

**Problem**: `eth_sendTransaction` accepts unsigned transactions but can't sign them

**Solution**:
```go
// In app/rpc/ethrpc/api.go SendTransaction:
// Option A: Accept pre-signed transactions (eth_sendRawTransaction)
// Option B: Sign with provided private key (NOT RECOMMENDED for production)
// Option C: Use wallet integration (RECOMMENDED)
```

**Implementation**:
- Implement `eth_sendRawTransaction` (accepts signed hex)
- Users sign transactions client-side (MetaMask, SDK)
- Node validates signature and processes

**Files to Modify**:
- `app/rpc/ethrpc/api.go` - Add `SendRawTransaction` method
- `domain/evm/txconverter.go` - Add signature validation

### 2. Account Balance Management (CRITICAL - 3-4 hours)

**Problem**: No account balances, can't track who has what

**Solution**:
- Initialize genesis accounts with balances
- Update balances on transactions
- Track nonces per account

**Implementation**:
```go
// In domain/evm/executor.go ProcessCanonicalChain:
// 1. Initialize genesis balances
// 2. Before each transaction:
//    - Check balance >= value + gas
//    - Check nonce is correct
// 3. After transaction:
//    - Deduct value + gas from sender
//    - Add value to recipient
//    - Increment nonce
```

**Files to Modify**:
- `domain/evm/executor.go` - Add balance checks
- `domain/evm/genesis.go` - NEW: Genesis account setup

### 3. Gas Fee Collection (CRITICAL - 2-3 hours)

**Problem**: Gas calculated but fees not collected/distributed

**Solution**:
- Deduct gas fees from sender
- Add fees to miner/coinbase
- Track total fees per block

**Implementation**:
```go
// In domain/evm/executor.go processTransaction:
gasFee := gasPrice * gasUsed
stateDB.SubBalance(sender, value + gasFee)
stateDB.AddBalance(coinbase, gasFee)
```

**Files to Modify**:
- `domain/evm/executor.go` - Add fee collection

### 4. Transaction Receipts (HIGH - 2-3 hours)

**Problem**: No way to check if transaction succeeded

**Solution**:
- Store receipts after execution
- Index by transaction hash
- Implement `eth_getTransactionReceipt`

**Implementation**:
```go
// Store receipt in database
type Receipt struct {
    TxHash    common.Hash
    BlockHash common.Hash
    BlockNumber uint64
    Status    uint64 // 1 = success, 0 = failure
    GasUsed   uint64
    Logs      []*types.Log
}
```

**Files to Create**:
- `domain/evm/receipts.go` - Receipt storage
- `app/rpc/ethrpc/api.go` - GetTransactionReceipt implementation

### 5. Block Building Integration (HIGH - 2-3 hours)

**Problem**: Transactions in mempool but may not be included in blocks

**Solution**:
- Verify block builder includes EVM transactions
- Ensure transactions are ordered correctly
- Enforce gas limits per block

**Files to Check**:
- `domain/consensus/processes/blockbuilder/` - Verify EVM tx inclusion

## Implementation Order (Priority)

### Day 1: Core Transaction Flow
1. ✅ Transaction converter (DONE)
2. ✅ SendTransaction to mempool (DONE)
3. ⚠️ SendRawTransaction (accept signed txs) - 2 hours
4. ⚠️ Balance initialization - 2 hours
5. ⚠️ Balance validation - 1 hour

### Day 2: Execution & Fees
6. ⚠️ Gas fee collection - 2 hours
7. ⚠️ Transaction receipts - 3 hours
8. ⚠️ GetTransactionReceipt RPC - 1 hour

### Day 3: Testing & Polish
9. ⚠️ End-to-end test - 2 hours
10. ⚠️ Fix any issues - 2 hours
11. ⚠️ Documentation update - 1 hour

**Total**: ~16 hours (2-3 days)

## Quick Win: Make It Work Now

### Minimal Working Version (4-6 hours)

1. **Accept Pre-Signed Transactions** (1 hour)
   - Implement `eth_sendRawTransaction`
   - Users sign with MetaMask/SDK
   - Node validates and processes

2. **Initialize Test Account** (1 hour)
   - Genesis account with 1000 PHX
   - Hardcode for testing

3. **Basic Balance Check** (1 hour)
   - Check balance before execution
   - Deduct value + gas

4. **Simple Receipt** (1 hour)
   - Store basic receipt
   - Return in GetTransactionReceipt

5. **Test End-to-End** (1-2 hours)
   - Send transaction
   - Verify in block
   - Check balance updated

## Success Criteria

✅ Can send a signed transaction
✅ Transaction appears in mempool
✅ Transaction included in block
✅ Transaction executes in EVM
✅ Balance updates correctly
✅ Receipt available via RPC

## Next Steps

1. Implement `eth_sendRawTransaction`
2. Add genesis account initialization
3. Add balance validation
4. Add gas fee collection
5. Test with real transaction

