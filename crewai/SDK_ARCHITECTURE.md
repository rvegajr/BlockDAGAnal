# Phoenix SDK Architecture

## Overview
- Extend ethers.js v6 with Phoenix-specific functionality
- Provide familiar ethers.js interface (Provider, Wallet, Contract)
- Modular design with pluggable components
- Async-first promise-based API
- Strict TypeScript typing
- Comprehensive test suite and documentation

## Module Structure
- @phoenix/provider
  - Extends ethers.JsonRpcProvider
  - Adds Phoenix-specific methods (getDAGInfo, getBlueScore)
- @phoenix/wallet 
  - Extends ethers.Wallet
  - Manages Phoenix account keys and signing
- @phoenix/contract
  - Extends ethers.Contract 
  - Integrates Phoenix ABI encoding/decoding
- @phoenix/types
  - Phoenix-specific type definitions
  - DAG structures, transaction types, etc
- @phoenix/utils 
  - Standalone utility functions
  - Encoding, hashing, etc

## Phoenix Extensions
- DAG Queries
  - provider.getDAGInfo() -> { parents, blueScore }
  - provider.getBlueScore(blockTag)
- Finality
  - provider.getCanonicalBlock(blueScore)
- Multi-Parent Blocks  
  - provider.getBlockParents(blockHash)
- Potential New Transaction Types (TBD)

## Compatibility
- Maintain ethers.js interface for core functions
- Provide adapters for popular tools (Hardhat, Foundry, etc)
- Use tree-shakeable ESM build for bundlers
- Provide CommonJS build for Node.js

## Error Handling
- Extend ethers.js error classes
- Provide clear error messages and codes
- Validate method inputs and fail fast

## Testing
- Comprehensive unit tests with Jest
- Integration tests on Phoenix testnet
- Fuzz testing with Echidna
- Automated CI test runner

## Documentation
- API reference with examples
- Guides and tutorials 
- Sample dApps showcasing SDK usage
- Versioned docs with changelog

## Roadmap
- Initial MVP release with core functionality
- Progressive enhancements and optimizations
- Support for additional Phoenix features
- Ongoing maintenance and community support