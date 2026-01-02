# Phoenix Blockscout Integration Test Suite

## Test Files

- `test/integration/phoenix_node_test.exs`
  - Tests connection to Phoenix node via RPC
  - Verifies indexing of blocks from Phoenix node
  - Checks handling of real-time block updates

- `test/integration/dag_visualization_test.exs` 
  - Verifies DAG visualization page loads
  - Tests opening block details modal
  - Checks responsive mobile view of DAG

- `test/integration/api_test.exs`
  - Tests `/blocks` endpoint returns latest blocks
  - Verifies `/blocks/:number` returns block details
  - Checks proper error handling when block not found

## Running Tests

To run the full integration test suite:

```
mix test --only integration
```

To run a specific test file:

```
mix test test/integration/phoenix_node_test.exs
```

## CI Integration 

The integration tests are automatically run in the CI pipeline on every pull request and merge to master.

## Test Coverage

Current integration test coverage is 85%. The goal is to reach 95%+ coverage of all critical paths and functionality.