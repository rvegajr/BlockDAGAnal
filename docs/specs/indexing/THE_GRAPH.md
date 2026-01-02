# BDP The Graph Integration Specification

Status: Draft
Owner: Indexing Team

## Overview
Enable subgraph deployment on Phoenix for DApp developers to index and query blockchain data via GraphQL.

## Upstream
- Repository: https://github.com/graphprotocol/graph-node
- License: Apache-2.0/MIT
- Documentation: https://thegraph.com/docs

## Architecture
```
Phoenix Chain (RPC)
    ↓
graph-node (Rust)
    ↓ indexes blocks/events
PostgreSQL (storage)
    ↓ serves
GraphQL API (queries)
```

## Components
1. **graph-node**: Indexes Phoenix blocks, executes subgraph mappings
2. **IPFS**: Stores subgraph manifests and schemas
3. **PostgreSQL**: Stores indexed data
4. **GraphQL server**: Exposes query API

## Phoenix Integration

### Chain Configuration
```toml
# config.toml for graph-node
[chains.phoenix]
shard = "primary"
provider = [
  { label = "phoenix-mainnet", url = "https://rpc.bdp.network", features = ["archive", "traces"] }
]
```

### Subgraph Manifest Example
```yaml
specVersion: 0.0.5
schema:
  file: ./schema.graphql
dataSources:
  - kind: ethereum
    name: BDPToken
    network: phoenix
    source:
      address: "0x..."
      abi: ERC20
      startBlock: 100
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.7
      language: wasm/assemblyscript
      entities:
        - Transfer
      abis:
        - name: ERC20
          file: ./abis/ERC20.json
      eventHandlers:
        - event: Transfer(indexed address,indexed address,uint256)
          handler: handleTransfer
      file: ./src/mapping.ts
```

## Required RPC Methods
- eth_getLogs (with historical support)
- eth_getBlockByNumber/Hash
- eth_getTransactionReceipt
- trace_block (optional, for call handlers)

## Archive Node Requirement
- graph-node requires full history; Phoenix nodes MUST retain all blocks or serve via archive node cluster

## Deployment Options

### Hosted Service (Recommended for Launch)
- Deploy graph-node infrastructure in-house
- Offer free subgraph hosting for Phoenix dApps
- URL: https://graph.bdp.network

### Decentralized Network (Future)
- Apply for The Graph decentralized network support
- Phoenix becomes supported network
- Indexers earn query fees

## Developer Experience
```bash
# Initialize subgraph
graph init --product subgraph-studio --from-contract 0x... phoenix-subgraph

# Build
graph codegen && graph build

# Deploy to Phoenix hosted service
graph deploy --node https://graph.bdp.network phoenix-subgraph
```

## Performance
- Indexing lag target: < 30 seconds behind chain tip
- Query response p95: < 100ms
- Support 1000+ concurrent subgraphs

## Resources
- Graph Node docs: https://github.com/graphprotocol/graph-node/blob/master/docs/getting-started.md
- Subgraph developer docs: https://thegraph.com/docs/en/developing/creating-a-subgraph/






