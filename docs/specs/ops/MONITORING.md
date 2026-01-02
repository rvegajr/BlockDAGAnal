# BDP Monitoring & Observability Specification

Status: Draft
Owner: SRE Team

## Stack
- **Metrics**: Prometheus + Grafana
- **Logs**: Loki or ELK
- **Traces**: Jaeger (optional)
- **Alerting**: AlertManager → PagerDuty/Slack

## Metrics to Track

### Node Health
- `bdp_sync_status` (bool): synced vs syncing
- `bdp_block_height` (gauge): latest canonical block number
- `bdp_blue_score` (gauge): latest GHOSTDAG blue score
- `bdp_peer_count` (gauge): connected peers
- `bdp_chain_reorgs_total` (counter): reorg events

### Performance
- `bdp_block_processing_duration_seconds` (histogram): time to validate/execute block
- `bdp_tx_processing_duration_seconds` (histogram): per-tx execution time
- `bdp_rpc_request_duration_seconds` (histogram): RPC latency by method
- `bdp_rpc_requests_total` (counter): RPC call count by method/status

### Mining (if mining enabled)
- `bdp_hashrate` (gauge): local hashrate
- `bdp_blocks_mined_total` (counter): blocks found
- `bdp_shares_submitted_total` (counter): pool shares

### Network
- `bdp_network_in_bytes_total` (counter): inbound traffic
- `bdp_network_out_bytes_total` (counter): outbound traffic
- `bdp_p2p_messages_total` (counter): by message type

### State & Storage
- `bdp_state_size_bytes` (gauge): state trie size
- `bdp_db_size_bytes` (gauge): total DB size
- `bdp_mempool_size` (gauge): pending tx count

## Dashboards

### Node Operator Dashboard
- Panels: block height, peer count, sync status, reorg rate, CPU/mem/disk
- Use case: monitor single node health

### Network Overview Dashboard
- Panels: total nodes (estimated), avg block time, network hashrate, tx/sec
- Use case: ecosystem health

### RPC Gateway Dashboard
- Panels: QPS by endpoint, error rate, latency percentiles, cache hit ratio
- Use case: SRE monitoring public RPC

## Alerts

### Critical (PagerDuty)
- Node out of sync > 5 minutes
- RPC error rate > 5% over 2 min
- Seed node down > 5 min
- Chain reorg depth > 10 blocks

### Warning (Slack)
- Peer count < 10
- Block processing lag > 10s
- Disk usage > 80%
- Memory usage > 90%

## Logging

### Log Levels
- ERROR: consensus failures, RPC errors, critical issues
- WARN: peer disconnects, slow queries, reorgs
- INFO: block mined, tx received, peer connected
- DEBUG: detailed tracing (disabled in prod)

### Structured Logging (JSON)
```json
{
  "timestamp": "2025-10-31T12:00:00Z",
  "level": "INFO",
  "msg": "Block validated",
  "block_number": 12345,
  "block_hash": "0x...",
  "tx_count": 42,
  "duration_ms": 123
}
```

## Tracing (Optional)
- Jaeger for distributed tracing across RPC → node → DB
- Trace expensive RPC calls (eth_getLogs, debug_traceTransaction)

## SLOs (Service Level Objectives)
- **RPC availability**: 99.9% uptime
- **Block sync lag**: < 10 seconds (p95)
- **RPC latency**: < 200ms (p95)
- **Reorg recovery**: < 60 seconds

## Runbooks
- Playbook for common issues (out of sync, high CPU, peer issues)
- Escalation paths
- Incident response checklist






