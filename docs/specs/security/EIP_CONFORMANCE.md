# BDP EIP Conformance Matrix

Status: Draft
Owner: Protocol Security Team

## Target EVM Fork Level
- **Primary**: London (EIP-1559, EIP-3529, EIP-3541)
- **Stretch**: Shanghai (EIP-3651, EIP-3855, EIP-3860, PUSH0)
- **Future**: Cancun (EIP-4844 blob txs, optional)

## Core EIPs (MUST Support)

### Consensus & Execution
- [EIP-2](https://eips.ethereum.org/EIPS/eip-2): Homestead hard fork changes
- [EIP-155](https://eips.ethereum.org/EIPS/eip-155): Replay protection (chainId in signature)
- [EIP-658](https://eips.ethereum.org/EIPS/eip-658): Receipt status field
- [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559): Fee market (baseFee, priorityFee)
- [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718): Typed transaction envelopes
- [EIP-2930](https://eips.ethereum.org/EIPS/eip-2930): Access lists
- [EIP-3529](https://eips.ethereum.org/EIPS/eip-3529): Gas refund reduction
- [EIP-3541](https://eips.ethereum.org/EIPS/eip-3541): Reject contracts starting with 0xEF

### JSON-RPC
- [EIP-1474](https://eips.ethereum.org/EIPS/eip-1474): Remote procedure call specification
- [EIP-1898](https://eips.ethereum.org/EIPS/eip-1898): Block param (number/hash/tag)

### Provider Interface
- [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193): Provider JavaScript API (wallet integration)

### Signatures
- [EIP-191](https://eips.ethereum.org/EIPS/eip-191): Signed data standard
- [EIP-712](https://eips.ethereum.org/EIPS/eip-712): Typed structured data hashing

### Tokens & Standards
- [EIP-20](https://eips.ethereum.org/EIPS/eip-20): Token standard (ERC-20)
- [EIP-721](https://eips.ethereum.org/EIPS/eip-721): Non-fungible token (ERC-721)
- [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155): Multi-token standard

### Precompiles
- [EIP-196](https://eips.ethereum.org/EIPS/eip-196): BN128 addition
- [EIP-197](https://eips.ethereum.org/EIPS/eip-197): BN128 pairing
- [EIP-198](https://eips.ethereum.org/EIPS/eip-198): MODEXP
- [EIP-152](https://eips.ethereum.org/EIPS/eip-152): BLAKE2b F compression

### PoW to PoS Mapping
- [EIP-4399](https://eips.ethereum.org/EIPS/eip-4399): DIFFICULTY → PREVRANDAO
  - Phoenix maps: DIFFICULTY := hash(parent block headers) or PoW randomness

## Phoenix-Specific Deviations

### Expected
- Block structure includes DAG-specific fields (parents, blueScore, algorithm)
- NUMBER field represents canonical index, not DAG height
- BLOCKHASH opcode limited to last 256 canonical blocks
- Finality semantics differ (confirmation count vs slot finality)

### Must Maintain Compatibility
- Transaction formats (legacy, 2930, 1559) identical
- Receipt/log structure identical
- Gas accounting per EIP gas tables
- Signature scheme (secp256k1, EIP-155 chainId)

## Conformance Testing

### Test Suites (MUST Pass)
1. **ethereum/tests**: https://github.com/ethereum/tests
   - StateTests (EVM execution)
   - BlockchainTests (block validation)
   - TransactionTests (tx validation)
   - Target: London fork tests

2. **go-ethereum test suite**
   - Run geth's internal tests against BDP node
   - Focus: state, tx, consensus compatibility

3. **evmone tests**: https://github.com/ethereum/evmone
   - EVM opcode validation
   - Gas measurement accuracy

### Custom Phoenix Tests
- DAG canonicalization determinism
- Reorg handling with state consistency
- Multi-parent block validation
- Dual-algorithm difficulty adjustment

## Gas Schedule Conformance

### London Gas Costs (Selected Examples)
| Operation | Gas Cost | EIP |
|-----------|----------|-----|
| ADD | 3 | - |
| MUL | 5 | - |
| SSTORE (cold) | 2100 | EIP-2929 |
| SLOAD (cold) | 2100 | EIP-2929 |
| CALL (cold) | 2600 | EIP-2929 |
| LOG0..LOG4 | 375 + topic*375 + data | - |
| CREATE | 32000 | - |
| SELFDESTRUCT refund | 0 | EIP-3529 |

Phoenix MUST match these exactly for targeted fork.

## Signature Validation
- chainId: 888 (mainnet), 8888 (testnet)
- v := {0,1} + chainId*2 + 35 (EIP-155)
- Recover address via secp256k1

## JSON-RPC Error Codes
- Parse error: -32700
- Invalid request: -32600
- Method not found: -32601
- Invalid params: -32602
- Internal error: -32603
- Custom (execution revert): -32000

## Audit Requirements
- Pass CertiK/Trail of Bits/Halborn audit for:
  - EVM execution correctness
  - State consistency under reorgs
  - Gas accounting accuracy
  - Signature validation
  - RPC conformance

## Monitoring
- Automated daily runs of ethereum/tests suite
- Gas consumption regression tests
- Fuzz testing with Echidna/Medusa






