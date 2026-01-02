# BDP Mining Algorithms Specification

Status: Draft
Owner: Mining Team

## Overview
BDP supports dual-algorithm PoW: kHeavyHash (Kaspa-compatible) and SHA3-256 (Keccak-256). Both produce valid blocks; difficulty adjusted per-algorithm; rewards identical.

## kHeavyHash
- Prehash: SHA3-256
- HeavyHash rounds: 4; matrix-based transform (Kaspa-derived)
- Output: 256-bit
- Hardware: GPU-friendly; Kaspa ASICs compatible

## SHA-3 (Keccak-256)
- Standard FIPS 202 parameters
- Output: 256-bit
- Hardware: ASIC/GPU friendly; BlockDAG ASICs compatible

## Difficulty & Target
- Separate difficulty tracks: D_kheavyhash, D_sha3
- Target per algorithm: target = MAX / difficulty
- Acceptance: hash(header||nonce) < target_algo

## Adjustment Policy
- Window: 256 blocks per algorithm (tunable)
- Max change per step: 4x up/down (tunable)
- Goal: keep effective block rate near composite target

## Rewards
- Block subsidy: 50 BDP initial; halving every ~210,000 canonical blocks
- Algorithm neutrality: same reward regardless of algo

## Headers
- `algorithm` field enumerates PoW type
- `mixHash` semantics per algorithm
- `nonce` 64-bit





