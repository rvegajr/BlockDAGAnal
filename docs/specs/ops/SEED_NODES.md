# BDP Seed Nodes Specification

Status: Draft
Owner: SRE/Infra Team

## Purpose
Bootstrap new Phoenix nodes by providing initial peer discovery.

## Topology
- Minimum 5 geographically distributed seed nodes
- Each seed node runs full archive node (all history)

## Locations
1. **US East** (AWS us-east-1): seed1.bdp.network
2. **US West** (GCP us-west1): seed2.bdp.network
3. **Europe** (Hetzner Frankfurt): seed-eu.bdp.network
4. **Asia Pacific** (DigitalOcean Singapore): seed-asia.bdp.network
5. **Australia** (Vultr Sydney): seed-au.bdp.network

## DNS Configuration
```
# A records
seed1.bdp.network.      300 IN A    <IP_1>
seed2.bdp.network.      300 IN A    <IP_2>
seed-eu.bdp.network.    300 IN A    <IP_3>
seed-asia.bdp.network.  300 IN A    <IP_4>
seed-au.bdp.network.    300 IN A    <IP_5>

# SRV for service discovery (optional)
_phoenix._tcp.bdp.network. 300 IN SRV 0 5 16110 seed1.bdp.network.
```

## Node Configuration
- Ports: 16110 (P2P), 16111 (RPC, restricted), 16112 (WS, restricted)
- Max peers: 200 (higher than regular nodes)
- Archive mode: enabled
- Metrics: Prometheus exporter on :9090

## Security
- Firewall: allow 16110 (P2P) from all, restrict RPC/WS to specific IPs
- DDoS mitigation: rate limits, connection limits
- Monitoring: uptime, peer count, block height lag

## Deployment
- Docker/systemd service
- Auto-restart on failure
- Log rotation (max 1GB per node)
- Alerting: PagerDuty/Slack for downtime > 5 min

## Bootstrap File (Hardcoded in Client)
```go
// bdpd/params/bootnodes.go
var MainnetBootnodes = []string{
    "enode://<pubkey1>@seed1.bdp.network:16110",
    "enode://<pubkey2>@seed2.bdp.network:16110",
    "enode://<pubkey3>@seed-eu.bdp.network:16110",
    "enode://<pubkey4>@seed-asia.bdp.network:16110",
    "enode://<pubkey5>@seed-au.bdp.network:16110",
}
```

## Health Checks
- HTTP endpoint /health returns { "synced": true, "blockNumber": N, "peers": M }
- Grafana dashboard: https://status.bdp.network






