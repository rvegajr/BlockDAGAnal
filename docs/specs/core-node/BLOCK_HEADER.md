# BDP Block Header & Structure Mapping

Status: Draft
Owner: Core Protocol Team

## Header Fields (EVM-visible)
- parentHash: bytes32 (hash of prior canonical block)
- ommersHash: bytes32 (set to keccak256(EMPTY_LIST))
- beneficiary (coinbase): address (reward recipient)
- stateRoot: bytes32 (MPT root)
- transactionsRoot: bytes32 (Merkle root of txs)
- receiptsRoot: bytes32 (Merkle root of receipts)
- logsBloom: bytes256
- difficulty/prevRandao: bytes32 (per EIP-4399 mapping)
- number: uint256 (canonical index)
- gasLimit: uint256
- gasUsed: uint256
- timestamp: uint256
- extraData: bytes (max 32 bytes)
- mixHash: bytes32 (PoW mix; algorithm-specific)
- nonce: uint64 (PoW)
- baseFeePerGas: uint256 (if 1559 enabled)

## DAG-Native Fields (Non-EVM)
- parents: list<bytes32> (multi-parent DAG)
- algorithm: enum { kHeavyHash, SHA3 }
- blueScore: uint64

## Rules
- Header MUST be derivable from canonicalization output.
- stateRoot/tx/receipts roots MUST commit to the linear execution order.
- BLOCKHASH opcode MUST return hashes from the last 256 canonical headers.

## Compatibility
- Conforms to Ethereum header schema with additional DAG-only metadata not exposed via standard RPC unless requested.





