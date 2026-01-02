package rpcserver

import (
  "testing"
  "net/http/httptest"
  "github.com/stretchr/testify/assert"
)

func TestNewServer(t *testing.T) {
  // Test creating a new server 
  ctx := context.Background()
  dagMock := &externalapi.DAGTopologyManagerMock{}
  srv, err := NewServer(ctx, dagMock)
  assert.NoError(t, err)
  assert.NotNil(t, srv)
}

func TestServerStartStop(t *testing.T) {
  // Test starting and stopping the server
  ctx := context.Background() 
  dagMock := &externalapi.DAGTopologyManagerMock{}
  srv, _ := NewServer(ctx, dagMock)
  
  go func() {
    err := srv.Start(":8080")
    assert.NoError(t, err)
  }()

  err := srv.Stop()
  assert.NoError(t, err)
}

func TestServeHTTP(t *testing.T) {
  // Test serving HTTP requests
  ctx := context.Background()
  dagMock := &externalapi.DAGTopologyManagerMock{}
  srv, _ := NewServer(ctx, dagMock)

  req := httptest.NewRequest("POST", "/", nil) 
  rr := httptest.NewRecorder()
  srv.ServeHTTP(rr, req)

  assert.Equal(t, 200, rr.Code)
}

func TestEthBlockNumber(t *testing.T) {
  // Test eth_blockNumber RPC method
  ctx := context.Background()
  dagMock := &externalapi.DAGTopologyManagerMock{}
  dagMock.VirtualBlockHashFunc = func() string { return "0x1234" }
  dagMock.BlockHeaderByHashFunc = func(hash string) (*externalapi.BlockHeader, error) {
    return &externalapi.BlockHeader{Number: 42}, nil  
  }
  
  ethAPI := NewEthAPI(&rpccontext.Context{DAGTopologyManager: dagMock})
  blockNum := ethAPI.BlockNumber()
  assert.Equal(t, hexutil.Uint64(42), blockNum)
}

// TODO: Add more tests for EthAPI methods

func BenchmarkEthBlockNumber(b *testing.B) {
  // Benchmark eth_blockNumber
  ctx := context.Background()
  dagMock := &externalapi.DAGTopologyManagerMock{} 
  dagMock.VirtualBlockHashFunc = func() string { return "0x1234" }
  dagMock.BlockHeaderByHashFunc = func(hash string) (*externalapi.BlockHeader, error) {
    return &externalapi.BlockHeader{Number: 42}, nil
  }

  ethAPI := NewEthAPI(&rpccontext.Context{DAGTopologyManager: dagMock})
  
  for i := 0; i < b.N; i++ {
    ethAPI.BlockNumber()  
  }
}