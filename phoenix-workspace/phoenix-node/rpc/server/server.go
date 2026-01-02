package rpcserver

import (
	"context"
	"net/http"

	"github.com/ethereum/go-ethereum/rpc"
	"github.com/kaspanet/kaspad/domain/consensus/model/externalapi"
	"github.com/kaspanet/kaspad/infrastructure/network/rpc/rpccontext"
	"github.com/kaspanet/kaspad/infrastructure/network/rpc/rpchandlers"
	"github.com/kaspanet/kaspad/infrastructure/network/rpc/rpcserver"
)

// Server represents the JSON-RPC server
type Server struct {
	rpcServer *rpcserver.Server
}

// NewServer creates a new JSON-RPC server
func NewServer(ctx context.Context, dagTopologyManager externalapi.DAGTopologyManager) (*Server, error) {
	rpcCtx := &rpccontext.Context{DAGTopologyManager: dagTopologyManager}
	rpcServer := rpcserver.NewServer()

	// Register eth namespace
	ethAPI := rpchandlers.NewEthAPI(rpcCtx)
	rpcServer.RegisterName("eth", ethAPI)

	// TODO: Register other namespaces (web3, net, bdp)

	return &Server{rpcServer: rpcServer}, nil
}

// Start runs the JSON-RPC server
func (s *Server) Start(endpoint string) error {
	return s.rpcServer.Start(endpoint)
}

// Stop shuts down the JSON-RPC server 
func (s *Server) Stop() error {
	return s.rpcServer.Stop()
}

// ServeHTTP handles JSON-RPC requests over HTTP
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	s.rpcServer.ServeHTTP(w, r)
}