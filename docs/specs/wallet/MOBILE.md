# BDP Mobile Wallet Specification (React Native)

Status: Draft
Owner: Wallet Team

## Base
- Framework: React Native + TypeScript
- Libraries: ethers.js, react-query, WalletConnect v2

## Features
- Accounts: BIP-39/44, multiple accounts, secure storage
- Transfers: native BDP, ERC-20, ERC-721/1155
- DApp: WalletConnect, in-app dapp browser (optional)
- Security: biometric auth, PIN, encrypted keystore
- Networks: Phoenix mainnet/testnet, custom RPC

## Addressing
- EVM addresses (0x…), checksummed
- Optional native address format display (doc-only)

## Node Interaction
- JSON-RPC via provider; chainId awareness; fee estimation (1559/legacy)

## Non-Functional
- Performance: tx create < 200ms UI, list 1k items smoothly
- Reliability: account backup/restore flows
- Theming: Phoenix branding

## Telemetry (opt-in)
- Crash reports, anonymized usage





