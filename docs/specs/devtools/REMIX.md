# BDP Remix Integration Specification

Status: Draft
Owner: DevTools Team

## Goal
Enable deploying/interacting via Remix with Phoenix networks.

## Steps
- In Remix, add Custom Network with:
  - ChainId: 888 (mainnet) / 8888 (testnet)
  - RPC URL: https://rpc.bdp.network / https://testnet-rpc.bdp.network
- Use Injected Provider (MetaMask/BDP extension) or Custom HTTP

## Verification
- Compile Solidity → Deploy via Remix → Verify on Blockscout





