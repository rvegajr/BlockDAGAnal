# BDP Browser Extension Wallet Specification

Status: Draft
Owner: Wallet Team

## Base
- Framework: React + TypeScript (WebExtension)
- Optional fork candidates: Frame, Core (Avalanche)

## Features
- Injected provider (EIP-1193)
- Account management, network switching
- Tx signing (1559/legacy), message signing (EIP-191/712)
- DApp connection/permissions UI
- Hardware wallet support (Ledger/Trezor) roadmap

## Provider Semantics
- EIP-1193 events: connect, disconnect, chainChanged, accountsChanged
- Methods: request({ method: 'eth_*' }) routed to BDP RPC

## Security
- Site permission model, phishing list, connect whitelists

## Branding
- Phoenix theming and icons





