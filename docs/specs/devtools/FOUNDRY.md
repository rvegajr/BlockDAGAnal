# BDP Foundry Specification

Status: Draft
Owner: DevTools Team

## Goal
Use Foundry (forge/cast/anvil) with Phoenix without code changes.

## Chain Config
- chainId: 888 (mainnet), 8888 (testnet)
- RPC URLs: https://rpc.bdp.network, https://testnet-rpc.bdp.network

## Example .env
```
RPC_URL=https://rpc.bdp.network
PRIVATE_KEY=0x...
```

## Example foundry.toml
```
[profile.default]
src = 'src'
out = 'out'
libs = ['lib']
via_ir = true
optimizer = true
optimizer_runs = 200
eth_rpc_url = '${RPC_URL}'
```

## Tasks
- forge test (works as-is)
- cast send/call (works as-is)





