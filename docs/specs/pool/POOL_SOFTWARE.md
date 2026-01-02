# BDP Mining Pool Software Specification

Status: Draft
Owner: Pool Platform Team

## Architecture
- Stratum frontends (per algorithm)
- Job manager (template generation from bdpd via RPC)
- Share validator (per algorithm)
- Accounting (shares, rounds, payouts)
- Payout engine (on-chain BDP transfers)
- Web UI (dashboard, miner stats, admin)

## Recommended Bases to Fork
- NOMP (Node Open Mining Portal): Node.js; pluggable stratum; mature
- Yiimp: C++/PHP; widely deployed; many algos
- open-ethereum-pool: Go; EVM-native payouts; adapt to BDP RPC
- Stratum V2 reference (Rust): next-gen protocol backbone

## BDP Integration Points
- New coin module: BDP (kHeavyHash, SHA-3)
- Node RPC: getWork/getBlockTemplate equivalent via JSON-RPC
- Payout: sendRawTransaction with BDP chainId; EVM address format support

## Non-Functional Requirements
- 10k+ concurrent miners
- HA deployment: multi-instance stateless frontends + shared DB (PostgreSQL/Redis)
- Metrics: Prometheus; alerts for orphan spikes, stale rate, pool hashrate

## Security & Compliance
- TLS everywhere; secrets in vault
- Anti-abuse: IP rate limits, share difficulty floors, ban policies





