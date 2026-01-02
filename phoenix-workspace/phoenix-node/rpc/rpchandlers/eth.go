package rpchandlers

import (
	"context"
	"math/big"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/kaspanet/kaspad/infrastructure/network/rpc/rpccontext"
)

// EthAPI implements the eth_* RPC methods
type EthAPI struct {
	ctx *rpccontext.Context
}

// NewEthAPI creates a new EthAPI instance
func NewEthAPI(ctx *rpccontext.Context) *EthAPI {
	return &EthAPI{ctx: ctx}
}

// BlockNumber returns the current block number
func (api *EthAPI) BlockNumber() hexutil.Uint64 {
	blockHeader, err := api.ctx.DAGTopologyManager.BlockHeaderByHash(api.ctx.DAGTopologyManager.VirtualBlockHash())
	if err != nil {
		return 0
	}
	return hexutil.Uint64(blockHeader.BlockNumber())
}

// GetBlockByNumber returns the block for the given block number
func (api *EthAPI) GetBlockByNumber(ctx context.Context, number rpc.BlockNumber, fullTx bool) (map[string]interface{}, error) {
	// TODO: Implement
	return nil, nil
}

// SendRawTransaction sends a raw transaction
func (api *EthAPI) SendRawTransaction(ctx context.Context, encodedTx hexutil.Bytes) (common.Hash, error) {
	// TODO: Implement
	return common.Hash{}, nil
}