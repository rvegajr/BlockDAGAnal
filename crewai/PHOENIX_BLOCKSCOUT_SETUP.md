# Phoenix Blockscout Setup

## Fork Blockscout
1. Fork https://github.com/blockscout/blockscout repo at v5.3.0 tag
2. Clone the forked repo locally

## Configure for Phoenix
1. Update `apps/explorer/config/dev.exs`:
   - Set `ETHEREUM_JSONRPC_HTTP_URL` to Phoenix RPC endpoint
   - Set `ETHEREUM_JSONRPC_TRACE_URL` to Phoenix tracing RPC
   - Set `NETWORK_PATH` to `phoenix`
2. Update branding:
   - Modify CSS at `apps/block_scout_web/assets/css/theme/_variables.scss`
   - Replace logo at `apps/block_scout_web/assets/static/images/phoenix_logo.png`
   - Update strings in `apps/block_scout_web/priv/gettext/en/LC_MESSAGES/default.po`

## Add DAG Features
1. Extend API:
   - Add `/blocks/:hash/parents` endpoint to fetch parent block hashes
   - Add `/blocks/:hash/dag_info` endpoint for blue/red set status
2. Update database:
   - Add `block_parents` table to map block hash to parent hashes
   - Add `blue_red_sets` table to track blue/red set membership
   - Add `blue_red_status` column to `blocks` table
3. Update UI: 
   - Show full parent graph on block page
   - Display blue/red set indicators on blocks

## Deploy with Docker
1. Update `docker-compose.yml` with Phoenix config
2. Set env vars for Phoenix RPC URLs, chain ID, etc
3. Start containers:
   ```
   docker-compose up -d
   ```
4. Create and migrate database:
   ```
   docker-compose exec web mix do ecto.create, ecto.migrate 
   ```
5. Compile and start server:
   ```
   docker-compose exec web mix phx.server
   ```

## Verify and Monitor
1. Check Blockscout is accessible at `http://localhost:4000`  
2. Verify blocks are being synced and DAG features work
3. Monitor performance, tune as needed
4. Set up monitoring and alerting
