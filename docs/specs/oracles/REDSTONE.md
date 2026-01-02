# BDP RedStone Oracle Integration Specification

Status: Draft
Owner: Oracle Team

## Overview
Integrate RedStone oracles for price feeds and off-chain data on Phoenix. RedStone provides push-based and modular oracle architecture easier to integrate than Chainlink for new chains.

## Upstream
- Repository: https://github.com/redstone-finance/redstone-oracles
- License: MIT
- Documentation: https://docs.redstone.finance

## Architecture Models

### 1. RedStone Classic (Recommended for Phoenix)
```
Off-chain:
  RedStone Nodes → Sign data → IPFS/Arweave

On-chain (Phoenix):
  Contract calls with signed data payload → Validation → Price available
```

### 2. RedStone Core (Alternative)
Traditional push model with relayer updating on-chain price feeds.

## Integration (RedStone Classic)

### Consumer Contract Example
```solidity
import "@redstone-finance/evm-connector/contracts/data-services/MainDemoConsumerBase.sol";

contract BDPPriceFeed is MainDemoConsumerBase {
    function getBDPPrice() public view returns (uint256) {
        return getOracleNumericValueFromTxMsg(bytes32("BDP"));
    }
    
    function getETHPrice() public view returns (uint256) {
        return getOracleNumericValueFromTxMsg(bytes32("ETH"));
    }
}
```

### Data Feeds Available
- BTC, ETH, BNB (major crypto)
- USDC, USDT, DAI (stablecoins)
- Custom: BDP/USD (requires RedStone node operator coordination)

## Deployment Steps
1. Deploy RedStone adapter contracts on Phoenix
2. Register Phoenix chain with RedStone
3. Configure data feeds (symbols, update intervals)
4. Set up validation parameters (signers, threshold)
5. Deploy example consumer contracts

## Gas Optimization
- Payload caching to reduce redundant validations
- Batched price updates
- Configurable staleness thresholds

## Security
- Multi-signature validation (minimum 3/5 signers)
- Time-weighted average price (TWAP) for manipulation resistance
- Heartbeat monitoring for liveness

## Custom BDP Feed
Request RedStone to add BDP/USD feed:
- Provide liquidity sources (DEX pools on Phoenix, CEX listings)
- Minimum liquidity threshold: $1M
- Update frequency: 10 seconds (configurable)

## Testing
- Testnet deployment with mock feeds
- Hardhat RedStone plugin for local dev
- Price deviation alerts

## Resources
- RedStone docs: https://docs.redstone.finance
- EVM connector: https://github.com/redstone-finance/redstone-oracles/tree/main/packages/evm-connector
- Integration guide: https://docs.redstone.finance/docs/get-started/integrations






