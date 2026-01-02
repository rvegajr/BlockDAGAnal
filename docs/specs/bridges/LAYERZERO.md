# BDP LayerZero Bridge Integration Specification

Status: Draft
Owner: Cross-Chain Team

## Overview
Integrate LayerZero omnichain messaging protocol to enable bridging between Phoenix and 50+ supported chains (Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, etc.).

## Upstream
- Repository: https://github.com/LayerZero-Labs/LayerZero
- License: Business Source License 1.1
- Documentation: https://layerzero.network/developers

## Architecture
```
Phoenix Chain                     Ethereum
    │                                │
    ├─ LayerZero Endpoint           ├─ LayerZero Endpoint
    ├─ Ultra Light Node (ULN)       ├─ Ultra Light Node
    ├─ Relayer                      ├─ Relayer
    ├─ Oracle (Chainlink/custom)    ├─ Oracle
    └─ OApp (OFTV2 for tokens)      └─ OApp
```

## Core Contracts (Deploy on Phoenix)
1. **Endpoint**: Core messaging contract
2. **UltraLightNodeV2**: Validation and security
3. **Relayer**: Message relay network participant
4. **Oracle**: Independent message verification

## Token Bridging (OFTV2)
```solidity
// Deploy on Phoenix for BDP token
contract BDPToken is OFTV2 {
    constructor(address _lzEndpoint) OFTV2("BlockDAG Phoenix", "BDP", _lzEndpoint) {}
}

// Usage: bridge BDP to Ethereum
bdpToken.sendFrom(
    msg.sender,
    ethereumChainId,
    toAddress,
    amount,
    refundAddress,
    zroPaymentAddress,
    adapterParams
);
```

## Chain Configuration
- Phoenix chainId (LayerZero): TBD (apply for allocation)
- Phoenix mainnet: 888 (EVM chainId)
- Phoenix testnet: 8888 (EVM chainId)

## Integration Steps
1. Deploy LayerZero Endpoint on Phoenix
2. Configure trusted relayers and oracles
3. Register Phoenix chainId with LayerZero
4. Deploy OFTV2 for BDP token
5. Deploy example bridges for USDC, WETH

## Security
- Multi-sig admin for endpoint upgrades
- Relayer/Oracle decentralization (minimum 3 independent)
- Rate limits on bridge contracts
- Emergency pause mechanism

## Gas Considerations
- LayerZero messages require gas on both chains
- Users pay: source gas + destination gas estimate + protocol fee
- Phoenix fast finality reduces wait times vs PoS chains

## Testing
- Testnet integration: Phoenix testnet ↔ Ethereum Sepolia
- Mock endpoints for unit tests
- Bridge UI for manual testing

## Resources
- LayerZero docs: https://layerzero.gitbook.io
- OFTV2 standard: https://github.com/LayerZero-Labs/solidity-examples






