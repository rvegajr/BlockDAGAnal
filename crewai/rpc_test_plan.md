# Phoenix JSON-RPC Server Test Plan

## Unit Tests
- Test NewServer() creates RPC server correctly 
- Test registering and calling RPC methods
- Test error handling 
- Aim for 80%+ code coverage

## Integration Tests
- Test server start/stop functionality
- Test serving HTTP requests
- Test eth_blockNumber RPC method
- Test eth_getBlockByNumber RPC method 
- Test eth_sendRawTransaction RPC method
- Verify integration with Kaspa consensus layer

## End-to-End Tests  
- Test syncing blocks over RPC
- Test deploying and calling smart contracts
- Verify Ethereum RPC compatibility 
- Test reorg and fork handling scenarios

## Performance Tests
- Benchmark RPC throughput 
- Test handling concurrent requests
- Profile resource utilization under load

## Other Considerations
- Set up CI pipeline to run tests automatically 
- Enforce test coverage thresholds
- Fuzz test RPC inputs
- Simulate adversarial network conditions