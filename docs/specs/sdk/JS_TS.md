# BDP JavaScript/TypeScript SDK Specification

Status: Draft
Owner: DevRel SDK Team

## Base
- ethers.js wrapper with Phoenix extensions
- Package: @bdp/sdk

## API
- Provider: JsonRpcProvider(url)
- Wallet: Wallet(privateKey, provider)
- Contract: new Contract(address, abi, signer)
- Phoenix additions:
  - provider.getDAGInfo(): { blueScore, parents }
  - provider.getBlueScore(blockTag)

## Compatibility
- Works with Hardhat/Foundry
- Tree-shakeable ESM + CJS builds

## Error Handling
- Surface RPC errors; map to ethers errors where possible





