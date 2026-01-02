# BDP DAG → Canonical Linearization Spec

Status: Draft
Owner: Core Protocol Team

## Purpose
Define how BDP derives a deterministic linear sequence of blocks for EVM/state while consensus remains a DAG.

## Inputs
- Block DAG with GHOSTDAG metadata: blue/red sets, blue scores, timestamps, parents.

## Algorithm (Normative)
1. Select tip set maximizing cumulative blue work.
2. Build an ordered chain:
   - Prefer blue blocks by descending blue score.
   - Break ties deterministically: (timestamp, hash lexicographic).
   - Ensure topological order (parents precede children).
3. Emit linear sequence L = [b0..bn].

## Constraints
- Ordering MUST be stable across honest nodes given identical DAG.
- Last 256 block hashes of L MUST be addressable for EVM BLOCKHASH opcode.
- `block.number` presented to EVM MUST reflect the index in L.

## Reorg Handling
- On new block arrival, recompute delta between previous L and new L'.
- Re-execute only affected suffix; persist state checkpoints every M blocks (configurable) to cap replay cost.

## Exposed Header Mapping
- number := index in L
- parentHash := L[i-1].hash
- timestamp := block.timestamp
- difficulty/prevRandao := mapped per mining/randomness policy
- gasLimit/baseFee := policy (see EVM/GAS spec)
- miner/coinbase := selected reward address

## Testing
- Determinism tests under concurrent arrival orders
- Reorg delta replay benchmarks
- Consistency of receipts/logs under reordering





