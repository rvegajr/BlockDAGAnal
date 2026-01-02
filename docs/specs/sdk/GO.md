# BDP Go SDK Specification

Status: Draft
Owner: DevRel SDK Team

## Base
- Native Go library wrapping JSON-RPC
- Package: github.com/blockdag-phoenix/bdp-go

## Installation
```bash
go get github.com/blockdag-phoenix/bdp-go
```

## API
```go
package main

import (
    "github.com/blockdag-phoenix/bdp-go/client"
    "github.com/blockdag-phoenix/bdp-go/common"
)

func main() {
    // Connect to Phoenix
    c, err := client.Dial("https://rpc.bdp.network")
    if err != nil {
        panic(err)
    }
    
    // Standard Ethereum client methods
    balance, _ := c.BalanceAt(ctx, common.HexToAddress("0x..."), nil)
    block, _ := c.BlockByNumber(ctx, nil)
    
    // Phoenix extensions
    dagInfo, _ := c.GetDAGInfo(ctx, nil)
    blueScore, _ := c.GetBlueScore(ctx, nil)
}
```

## Features
- Context-aware API (ctx parameter)
- Ethereum-compatible types (common.Address, common.Hash, big.Int)
- Contract binding generation (abigen compatible)
- WebSocket support
- Batch RPC requests

## Phoenix Extensions
```go
type DAGInfo struct {
    BlueScore uint64
    Parents   []common.Hash
    Algorithm string
}

func (c *Client) GetDAGInfo(ctx context.Context, blockNumber *big.Int) (*DAGInfo, error)
func (c *Client) GetBlueScore(ctx context.Context, blockNumber *big.Int) (uint64, error)
```

## Contract Bindings
- Use go-ethereum's abigen tool
- Bindings work unchanged with BDP RPC

## Testing
- Testify suite support
- Mock client for unit tests
- Integration test helpers for Phoenix testnet






