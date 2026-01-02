# BDP Hardhat Plugin Specification

Status: Draft
Owner: DevTools Team

## Package
- Name: @bdp/hardhat

## Capabilities
- Networks preset: phoenix, phoenixTestnet
- Tasks:
  - bdp:chain-info → prints chainId, blueScore
  - bdp:verify → passthrough to Blockscout verify endpoint
- Ethers provider patching for Phoenix RPC quirks (if any)

## Config Example
```ts
import '@bdp/hardhat';
export default {
  networks: {
    phoenix: { url: 'https://rpc.bdp.network', chainId: 888, accounts: [PK] },
    phoenixTestnet: { url: 'https://testnet-rpc.bdp.network', chainId: 8888, accounts: [PK] },
  },
  solidity: '0.8.24',
};
```





