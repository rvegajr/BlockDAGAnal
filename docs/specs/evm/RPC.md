# BDP JSON-RPC Conformance (EIP-1474)

Status: Draft
Owner: Node API Team

## Required Methods
- web3_clientVersion, net_version, net_listening, net_peerCount
- eth_chainId, eth_syncStatus (optional), eth_blockNumber
- eth_getBlockByHash/Number, eth_getTransactionByHash/Block, eth_getTransactionReceipt
- eth_getBalance, eth_getCode, eth_getStorageAt, eth_call, eth_estimateGas
- eth_sendRawTransaction, eth_getLogs, eth_newFilter/Uninstall/Changes
- eth_feeHistory (if 1559), eth_gasPrice (legacy)

## Trace/Debug (Optional)
- debug_traceTransaction, debug_traceBlock, trace_* (OpenEthereum style)

## Semantics
- Blocks identified by canonical NUMBER; DAG details are abstracted.
- BLOCKHASH, receipts, logs MUST align with canonical execution.

## Errors & Codes
- Follow Ethereum JSON-RPC error structure; match geth where possible.

## Versioning
- Expose BDP node version/build in web3_clientVersion (e.g., "bdpd/v0.1.0" )





