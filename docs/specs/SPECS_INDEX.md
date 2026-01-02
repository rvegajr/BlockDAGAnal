# BlockDAG Phoenix (BDP) - Technical Specifications Index

**Status**: Draft Complete ✅  
**Last Updated**: 2025-10-31  
**Owner**: BDP Engineering Team

---

## 📋 Complete Specifications Inventory

This directory contains **authoritative technical specifications** for every major component of the BDP stack. Each spec is standalone, implementation-ready, and references upstream projects to fork/integrate.

---

## 🏗️ Core Blockchain

### [core-node/CONSENSUS.md](core-node/CONSENSUS.md)
**GHOSTDAG Consensus (Kaspa-derived)**
- PoW-secured block DAG with k-cluster blue/red selection
- Blue score ordering for canonical exposure
- Target: ~1s block interval, high throughput

### [core-node/CANONICALIZATION.md](core-node/CANONICALIZATION.md)
**DAG → Linear Mapping for EVM**
- Deterministic ordering algorithm
- Reorg delta replay strategy
- Header mapping (NUMBER, BLOCKHASH, TIMESTAMP)

### [core-node/CANONICALIZATION_DETAILED.md](core-node/CANONICALIZATION_DETAILED.md)
**Canonicalization (Detailed, Normative)**
- Total ordering with strict tie-breakers (blueScore, timestamp, hash)
- Topological enforcement (Kahn’s algorithm)
- Determinism, performance targets, validation suite

### [core-node/BLOCK_HEADER.md](core-node/BLOCK_HEADER.md)
**Block Header Structure**
- EVM-visible fields (parentHash, stateRoot, gasLimit, etc.)
- DAG-native fields (parents, blueScore, algorithm)
- Compatibility with Ethereum tooling

### [core-node/REORG_HANDLING.md](core-node/REORG_HANDLING.md)
**Reorg Handling (Normative)**
- Max reorg depth policy, delta replay algorithm
- Checkpointing, indices rewrite, mempool interaction
- Telemetry, operator guidance, test cases

---

## 💻 EVM & Smart Contracts

### [evm/EXECUTION.md](evm/EXECUTION.md)
**EVM Execution Layer**
- Fork level: London → Shanghai (target)
- State model: Ethereum account (MPT)
- Engine: go-ethereum EVM (BSC-compatible)
- Gas accounting, precompiles, determinism

### [evm/RPC.md](evm/RPC.md)
**JSON-RPC Conformance (EIP-1474)**
- Required methods (eth_*, web3_*, net_*)
- Optional trace/debug modules
- Error codes and semantics

### [evm/EVM_CONTEXT_MAPPING.md](evm/EVM_CONTEXT_MAPPING.md)
**EVM Context & Header Mapping (Normative)**
- Exact mapping for number, parentHash, difficulty/prevRandao, baseFee
- Tx/receipt indices, BLOCKHASH opcode semantics, checkpoints
- EIP-1559 policy and legacy mode

---

## ⛏️ Mining

### [mining/ALGORITHMS.md](mining/ALGORITHMS.md)
**Dual PoW Algorithms**
- kHeavyHash (Kaspa-compatible)
- SHA-3 (Keccak-256)
- Separate difficulty tracks, identical rewards

### [mining/POOL_PROTOCOL.md](mining/POOL_PROTOCOL.md)
**Stratum Protocol for Mining Pools**
- Stratum V1 (baseline), V2 (preferred)
- Job templates, share validation
- Variable difficulty (VDIFF)

---

## 🏊 Mining Pool Software

### [pool/POOL_SOFTWARE.md](pool/POOL_SOFTWARE.md)
**Reference Pool Architecture**
- Recommended bases: NOMP, Yiimp, open-ethereum-pool, Stratum V2
- BDP integration points
- Performance targets: 10k+ miners

---

## 🌐 RPC & Infrastructure

### [rpc/GATEWAY.md](rpc/GATEWAY.md)
**Public RPC Gateway**
- Topology: Cloudflare → NGINX → node pool → Redis
- Endpoints: https://rpc.bdp.network, wss://ws.bdp.network
- Rate limits, caching, monitoring

---

## 🔍 Block Explorer

### [explorer/BLOCKSCOUT.md](explorer/BLOCKSCOUT.md)
**Blockscout Integration**
- Upstream: Blockscout (Elixir/React)
- DAG extensions: parent visualization, blue/red indicators
- Contract verification, token tracking

---

## 📱 Wallets

### [wallet/MOBILE.md](wallet/MOBILE.md)
**React Native Mobile Wallet**
- Base: Rainbow wallet architecture (optional fork)
- Features: multi-account, ERC-20/721/1155, WalletConnect, biometrics
- Platforms: iOS + Android

### [wallet/EXTENSION.md](wallet/EXTENSION.md)
**Browser Extension Wallet**
- Base: Frame or Core (Avalanche)
- EIP-1193 provider injection
- Hardware wallet roadmap (Ledger/Trezor)

---

## 🛠️ SDKs

### [sdk/JS_TS.md](sdk/JS_TS.md)
**JavaScript/TypeScript SDK**
- Package: @bdp/sdk
- Base: ethers.js wrapper
- Phoenix extensions: getDAGInfo(), getBlueScore()

### [sdk/PYTHON.md](sdk/PYTHON.md)
**Python SDK**
- Package: blockdag-phoenix or bdp-sdk
- Base: web3.py wrapper
- Type hints, pytest fixtures

### [sdk/GO.md](sdk/GO.md)
**Go SDK**
- Package: github.com/blockdag-phoenix/bdp-go
- Ethereum-compatible types (common.Address, etc.)
- Contract binding generation (abigen)

---

## 🔧 Developer Tools

### [devtools/HARDHAT.md](devtools/HARDHAT.md)
**Hardhat Plugin**
- Package: @bdp/hardhat
- Networks preset (phoenix, phoenixTestnet)
- Tasks: chain-info, verify

### [devtools/FOUNDRY.md](devtools/FOUNDRY.md)
**Foundry Configuration**
- Works as-is with chainId config
- Example foundry.toml

### [devtools/REMIX.md](devtools/REMIX.md)
**Remix IDE Integration**
- Custom network addition
- Deploy/interact via browser

### [devtools/POLICY_GATE.md](devtools/POLICY_GATE.md)
**Deployment Policy Gate**
- Severity taxonomy, rule groups, evidence bundles, CI contract
- Presale safety, privileges, funds safety, reentrancy

### [devtools/DEPLOY_PLAYBOOK.md](devtools/DEPLOY_PLAYBOOK.md)
**Deployment Playbook**
- Preflight, dry-run, rollout, rollback, emergency, artifacts

---

## 🌉 Bridges & Oracles

### [bridges/LAYERZERO.md](bridges/LAYERZERO.md)
**LayerZero Omnichain Bridge**
- Upstream: LayerZero protocol
- Integration: Endpoint, ULN, Relayer, Oracle
- Token bridging: OFTV2 for BDP and stablecoins

### [oracles/REDSTONE.md](oracles/REDSTONE.md)
**RedStone Oracle Integration**
- Model: RedStone Classic (push with payload)
- Data feeds: BTC, ETH, BDP/USD (custom)
- Consumer contract examples

---

## 📊 Indexing

### [indexing/THE_GRAPH.md](indexing/THE_GRAPH.md)
**The Graph Subgraph Support**
- Upstream: graph-node (Rust)
- Chain config for Phoenix
- Hosted service deployment strategy

---

## 🔒 Security & Conformance

### [security/EIP_CONFORMANCE.md](security/EIP_CONFORMANCE.md)
**EIP Conformance Matrix**
### [security/STATIC_RULESET.md](security/STATIC_RULESET.md)
**Static Analysis Ruleset**
- Slither/Mythril mapping to severities and thresholds

---

## 🧪 Testing

### [testing/DAG_TEST_SCENARIOS.md](testing/DAG_TEST_SCENARIOS.md)
**DAG→EVM Test Scenarios**
- Determinism, tie-breakers, reorg matrices
- Nonce conflicts, BLOCKHASH window, EIP-1559 dynamics
- Checkpointing, performance, explorer parity, adversarial cases

### [testing/CONTRACT_TEST_SUITE.md](testing/CONTRACT_TEST_SUITE.md)
**Contract Test Suite & Runnable Examples**
- Core semantics, events/logs, CREATE/CREATE2, precompiles
- ERC-20/721/1155 parity, reentrancy and security
- Hardhat/Foundry runnable examples against Phoenix RPC

### [testing/REORG_HARNESS_SPEC.md](testing/REORG_HARNESS_SPEC.md)
**Reorg Simulation Harness**
- CLI/JS interfaces, script format, assertions, outputs

### [developers/DEVELOPER_TEST_GUIDE.md](developers/DEVELOPER_TEST_GUIDE.md)
**Developer Test Guide**
- Hardhat/Foundry config, reorg harness usage, artifacts

---

## 📜 Contract Templates

### [contracts/TEMPLATES_SPEC.md](contracts/TEMPLATES_SPEC.md)
**Secure-by-default Templates**
- Roles, caps, pausability, vesting, timelock, treasury
- Invariants and acceptance criteria
- Target fork: London (primary), Shanghai (stretch)
- Required EIPs: 155, 658, 1559, 2718, 2930, 1474, 1193, etc.
- Test suites: ethereum/tests, go-ethereum, evmone
- Gas schedule conformance
- Audit requirements

---

## 🚀 Operations

### [ops/SEED_NODES.md](ops/SEED_NODES.md)
**Seed Node Infrastructure**
- Minimum 5 geo-distributed nodes
- DNS: seed1.bdp.network, seed-eu.bdp.network, etc.
- Hardcoded bootstrap enodes

### [ops/MONITORING.md](ops/MONITORING.md)
**Monitoring & Observability**
- Stack: Prometheus, Grafana, Loki, AlertManager
- Metrics: block height, peer count, reorgs, RPC latency
- Dashboards: node operator, network overview, RPC gateway
- SLOs: 99.9% uptime, <10s sync lag, <200ms RPC p95

---

## 📦 Technology Borrowing Summary

| Component | Upstream Source | License | Integration Effort |
|-----------|----------------|---------|-------------------|
| **Consensus** | Kaspa | ISC | Fork (1 month) |
| **EVM** | BSC/geth | LGPL-3.0 | Fork + adapt (2 months) |
| **Explorer** | Blockscout | GPL-3.0 | Fork (1 month) |
| **Wallet** | Rainbow | GPL-3.0 | Fork (2 months) |
| **Pool** | Stratum V2 | MIT | Implement (1 month) |
| **SDK (JS/TS)** | ethers.js | MIT | Wrapper (<1 week) |
| **SDK (Python)** | web3.py | MIT | Wrapper (<1 week) |
| **Bridge** | LayerZero | BSL | Integration (2 months) |
| **Oracle** | RedStone | MIT | Integration (1 month) |
| **Indexing** | The Graph | Apache-2.0 | Adapt (1 month) |

---

## 🎯 Implementation Priorities

### P0 (Critical Path - Months 1-3)
1. core-node/CONSENSUS.md
2. core-node/CANONICALIZATION.md
3. evm/EXECUTION.md
4. evm/RPC.md
5. mining/ALGORITHMS.md

### P1 (High Priority - Months 3-6)
6. rpc/GATEWAY.md
7. explorer/BLOCKSCOUT.md
8. sdk/JS_TS.md
9. devtools/HARDHAT.md
10. pool/POOL_SOFTWARE.md

### P2 (Medium Priority - Months 6-9)
11. wallet/MOBILE.md
12. sdk/PYTHON.md, sdk/GO.md
13. bridges/LAYERZERO.md
14. oracles/REDSTONE.md
15. ops/SEED_NODES.md

### P3 (Post-Launch - Months 9-12)
16. indexing/THE_GRAPH.md
17. wallet/EXTENSION.md
18. security/EIP_CONFORMANCE.md (ongoing)
19. ops/MONITORING.md (continuous)

---

## 🔗 Cross-References

### EVM Conformance Dependencies
- core-node/BLOCK_HEADER.md → evm/EXECUTION.md (header mapping)
- core-node/CANONICALIZATION.md → evm/EXECUTION.md (state ordering)
- security/EIP_CONFORMANCE.md → evm/EXECUTION.md, evm/RPC.md (compliance)

### Developer Experience Chain
- evm/RPC.md → sdk/JS_TS.md, sdk/PYTHON.md, sdk/GO.md (SDK layer)
- sdk/* → devtools/HARDHAT.md, devtools/FOUNDRY.md (tooling)
- explorer/BLOCKSCOUT.md ← evm/RPC.md (indexer data source)

### Mining Stack
- mining/ALGORITHMS.md → core-node/CONSENSUS.md (PoW validation)
- mining/POOL_PROTOCOL.md → pool/POOL_SOFTWARE.md (implementation)
- mining/ALGORITHMS.md ← core-node/BLOCK_HEADER.md (algorithm field)

### Infrastructure Dependencies
- ops/SEED_NODES.md → core-node/* (bootstrap)
- ops/MONITORING.md → all components (observability)
- rpc/GATEWAY.md → evm/RPC.md (public access)

---

## ✅ Conformance Checklist (Use for Validation)

### Core Protocol
- [ ] GHOSTDAG blue/red selection passes Kaspa test vectors
- [ ] Canonicalization is deterministic across nodes
- [ ] Block headers conform to Ethereum schema + DAG extensions

### EVM Compatibility
- [ ] Pass ethereum/tests StateTests for London fork
- [ ] Gas accounting matches EIP gas schedules exactly
- [ ] JSON-RPC methods return Ethereum-compatible responses
- [ ] Hardhat/Foundry/Remix work without modification

### Mining
- [ ] kHeavyHash validation matches Kaspa reference
- [ ] SHA-3 validation uses standard Keccak-256
- [ ] Difficulty adjusts independently per algorithm
- [ ] Stratum protocol supports both algorithms

### Developer Experience
- [ ] ethers.js connects and queries successfully
- [ ] Smart contracts deploy via Hardhat
- [ ] Blockscout indexes blocks and contracts
- [ ] Mobile wallet sends transactions

### Security
- [ ] External audit (2 firms minimum) completed
- [ ] No critical/high findings unresolved
- [ ] Fuzz testing passes (Echidna/Medusa)
- [ ] Penetration testing on RPC/P2P

---

## 📞 Spec Ownership

| Area | Owner | Contact |
|------|-------|---------|
| **Core Protocol** | Protocol Team | protocol@bdp.network |
| **EVM/Smart Contracts** | Smart Contract Team | evm@bdp.network |
| **Mining** | Mining Team | mining@bdp.network |
| **Infrastructure** | SRE Team | sre@bdp.network |
| **Developer Tools** | DevRel Team | devrel@bdp.network |
| **Security** | Security Team | security@bdp.network |

---

## 🔄 Spec Lifecycle

### Status Definitions
- **Draft**: Initial specification; subject to change
- **Review**: Under team review; accepting feedback
- **Final**: Approved for implementation
- **Implemented**: Code matches spec; deployed to testnet
- **Production**: Live on mainnet

### Change Process
1. Propose change via GitHub issue
2. Team review (async + sync if needed)
3. Update spec with version bump
4. Notify dependent specs/teams
5. Update implementation

---

## 📚 Additional Resources

- **Kaspa**: https://github.com/kaspanet/kaspad
- **BSC**: https://github.com/bnb-chain/bsc
- **go-ethereum**: https://github.com/ethereum/go-ethereum
- **Blockscout**: https://github.com/blockscout/blockscout
- **LayerZero**: https://github.com/LayerZero-Labs/LayerZero
- **The Graph**: https://github.com/graphprotocol/graph-node
- **ethereum/tests**: https://github.com/ethereum/tests

---

**Next Step**: Review all specs → assign implementation owners → begin P0 development sprint.

🔥 **All specifications complete. Ready to build BlockDAG Phoenix.** 🔥

