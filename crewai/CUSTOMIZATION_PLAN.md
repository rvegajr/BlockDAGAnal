# Blockscout Customization Plan for Phoenix Network

## Required Modifications

### Elixir Backend
- `Explorer.Chain`: Add functions to fetch block parents and parse DAG-specific attributes 
- `Explorer.Indexer`: Modify block and transaction fetchers to handle DAG structure
- Add new DAG-specific database tables (e.g. `block_parents`) and schemas
- `BlockScoutWeb.API.RPC`: Add endpoints to retrieve block parent data
- Estimated effort: 3-4 weeks

### React Frontend  
- `BlockPage`: Display parent block list and links
- `TransactionPage`: Show parent block(s) for transaction
- Add new `DAGVisualizer` component to render DAG graph
- Estimated effort: 2-3 weeks

## New Features

### DAG Visualizer
- Interactive D3.js based DAG graph
- Zoom, pan, hover interactions
- Highlight path from root to tip
- Estimated effort: 3-4 weeks

### Fork Tracking
- Detect and visualize forks in the DAG 
- Compare blue/red sets of blocks
- Estimated effort: 2 weeks

## API Changes
- `/api/v2/blocks/:hash/parents` - Fetch parent hashes for a block
- `/api/v2/dag/blocks` - Fetch block details for a set of blocks (bulk)
- `/api/v2/dag/graph` - Fetch graph data for DAG visualization

## Database Schema
- `block_parents` table to store block hash to parent hashes mapping
- Indexes on `block_hash` and `parent_hash`

## Testing Plan
- Update Blockscout Elixir test suite with DAG-specific test cases
- Integrate with Phoenix devnet and testnet
- Simulate reorgs and forks
- Benchmark indexer performance with Phoenix RPC
- Browser testing for DAG visualizer
- Estimated effort: 3-4 weeks

## Deployment
- Update Blockscout Docker and Helm configs for Phoenix 
- Set Phoenix-specific env vars (chain ID, RPC URL, etc)
- Estimated effort: 1 week

## Risks & Unknowns
- Impact of DAG structure on Blockscout's internal APIs and caching
- Ensuring DAG data is efficiently retrievable
- UX challenges with visualizing large DAGs

## Timeline
- Development: 8-10 weeks
- Testing & Hardening: 3-4 weeks
- Deployment & Monitoring: 1-2 weeks

Total estimated timeline: 3-4 months