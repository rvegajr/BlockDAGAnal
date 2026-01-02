# BDP RPC Gateway Specification

Status: Draft
Owner: SRE/Infra Team

## Topology
- Cloudflare CDN/WAF → NGINX/Envoy LB → BDP node pool (read/write) → Redis cache

## Endpoints
- Mainnet: https://rpc.bdp.network, wss://ws.bdp.network
- Testnet: https://testnet-rpc.bdp.network

## Features
- Rate limits: 100/1k/10k rpm tiers
- Caching: eth_getBlockByNumber, eth_getLogs (bounded)
- Health checks: block freshness, peer count, lag
- Sticky routing for tracing/debug

## Observability
- Prometheus exporters; dashboards for QPS, error rates, latency, cache hit ratio

## Security
- IP allowlists for write-heavy endpoints, API keys optional





