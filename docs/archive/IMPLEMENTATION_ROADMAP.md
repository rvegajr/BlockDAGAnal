# Phoenix Network: Critical Implementation Roadmap

## 🎯 Goal: Working Crypto Project

## Critical Missing Components (In Order)

### 1. Transaction Conversion & Validation ⚠️ CRITICAL
**Problem**: Can't convert Ethereum transactions to Phoenix format
**Solution**: Implement transaction converter
**Files**: `domain/evm/txconverter.go`

### 2. Transaction Pool Integration ⚠️ CRITICAL  
**Problem**: Transactions aren't added to mempool
**Solution**: Wire eth_sendTransaction to mempool
**Files**: `app/rpc/ethrpc/api.go` (SendTransaction)

### 3. Account State Management ⚠️ CRITICAL
**Problem**: No balance tracking, no nonce management
**Solution**: Implement account state in StateDB
**Files**: `domain/evm/statedb.go` (enhance)

### 4. Block Building with Transactions ⚠️ CRITICAL
**Problem**: Blocks don't include EVM transactions
**Solution**: Modify block builder to include transactions
**Files**: `domain/consensus/processes/blockbuilder/`

### 5. Gas & Fee Collection ⚠️ HIGH
**Problem**: No gas fees collected
**Solution**: Implement fee collection in executor
**Files**: `domain/evm/executor.go`

### 6. Transaction Signing ⚠️ HIGH
**Problem**: Can't sign transactions
**Solution**: Implement ECDSA signing
**Files**: `domain/evm/signer.go`

## Implementation Order

### Step 1: Transaction Converter (2-3 hours)
- Convert Ethereum tx → Phoenix tx
- Extract from, to, value, data, nonce
- Handle signatures

### Step 2: Mempool Integration (2-3 hours)
- Add transaction to mempool
- Validate transaction
- Return transaction hash

### Step 3: Account State (3-4 hours)
- Track balances
- Track nonces
- Update on transactions

### Step 4: Block Building (3-4 hours)
- Include transactions in blocks
- Enforce gas limits
- Order transactions

### Step 5: Gas & Fees (2-3 hours)
- Calculate fees
- Collect fees
- Distribute to miners

**Total Estimated Time**: 12-17 hours

## Success Criteria

✅ Can send a transaction via RPC
✅ Transaction appears in mempool
✅ Transaction included in next block
✅ Transaction executes in EVM
✅ Balance updates correctly
✅ Gas fees collected

