# BDP Consensus Specification (GHOSTDAG)

Status: Draft
Owner: Core Protocol Team

## Overview
BDP consensus is a PoW-secured block DAG using GHOSTDAG ordering (Kaspa-derived). Blocks may have multiple parents. Security derives from cumulative blue work. Canonical chain exposure to EVM is provided by a deterministic ordering adaptor.

## Goals
- High throughput (sub-second blocks) with fast confirmations
- Deterministic canonical ordering for EVM/state
- Compatibility with Kaspa miner ecosystem (kHeavyHash)

## Inherited Design (Upstream: Kaspa)
- GHOSTDAG/PHANTOM k-cluster blue/red set selection
- Blue score as ordering metric
- P2P protocol for block/tx propagation

## BDP Parameters (initial)
- k (cluster parameter): 18 (subject to tuning)
- Target block interval: ~1s
- Orphaning model: None; all valid blocks included (red/blue)

## Normative Requirements
- Nodes MUST compute blue sets per GHOSTDAG.
- Blue score MUST be monotonically increasing along canonical ordering.
- Parent selection SHOULD prefer high blue-work ancestors.
- Difficulty adjustment MUST be per-algorithm (see mining spec) with combined security budget.

## Canonical Exposure
- The canonical sequence presented to EVM MUST be derived by topologically sorting the blue-preferred DAG per GHOSTDAG rules.
- Reorg handling MUST re-execute only the delta between prior and new canonical sequences.

## Security Considerations
- Finality guidance SHOULD be expressed as threshold on blue work or N-confirmations.
- Reorg depth MUST be bounded by practical network propagation; instrumentation required.

## References
- Kaspa GHOSTDAG papers and implementation (conceptual)





