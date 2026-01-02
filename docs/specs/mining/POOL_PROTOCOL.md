# BDP Stratum Mining Protocol (Pool Integration)

Status: Draft
Owner: Mining/Pool Team

## Protocol
- Support Stratum V1 (baseline) and Stratum V2 (preferred) for future

## V1 Methods (baseline)
- mining.subscribe, mining.authorize, mining.set_difficulty, mining.notify, mining.submit

## Job Template
- Fields: jobId, prevhash (canonical tip), coinb1/coinb2, merkle branches, version, nbits (per algorithm), ntime, cleanJobs
- Algorithm flag included in job metadata

## Share Validation
- Miner computes candidate header hash per selected algorithm
- Pool validates against share target; submits block to bdpd if full target met

## Difficulty
- Variable difficulty per miner (VDIFF); separate ports per algorithm (e.g., :3333 kHeavyHash, :3334 SHA-3)

## Payouts
- Supported schemes: PPS, PPLNS, SOLO
- Payout currency: BDP

## Reference Implementations to Fork
- open-ethereum-pool (for EVM payout accounting)
- yiimp / NOMP (job management & frontends)
- stratum-mining/stratum (Stratum V2 reference; Rust)

## Security
- TLS on Stratum, per-miner ban scores, DDOS protection, nonce distribution policy





