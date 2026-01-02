# BDP EVM Execution Specification

Status: Draft
Owner: EVM Integration Team

## Scope
- EVM compatibility level: London → Shanghai (target), Cancun optional later
- State model: Ethereum account model (MPT)
- Execution engine: go-ethereum EVM (BSC/geth compatible)

## Deterministic Context
- Block context values (NUMBER, TIMESTAMP, COINBASE, BASEFEE, PREVRANDAO) come from canonicalization + policy mapping.
- Gas accounting MUST use Ethereum fork gas tables for the selected fork.

## Transactions
- Supported types: Legacy, EIP-2930, EIP-1559
- Signature: secp256k1, EIP-155 chainId
- Nonce semantics: per-account, strictly increasing

## Receipts & Logs
- EIP-658 status field required
- Logs and bloom identical to Ethereum semantics

## Gas & Limits
- Block gas limit: configurable (default 30,000,000)
- Intrinsic gas rules per fork
- EIP-1559: baseFee/priorityFee optional; if disabled, legacy gasPrice applies

## Precompiles
- Standard precompiles (ECRECOVER, SHA256, RIPEMD160, ID, MODEXP, BN128 add/mul/pairing, BLAKE2f)

## Determinism
- Re-execution of L (canonical sequence) MUST yield identical stateRoot across honest nodes.

## Conformance
- MUST pass go-ethereum state tests for targeted fork set.
- SHOULD pass evmone/ethereum-tests vectors where applicable.





