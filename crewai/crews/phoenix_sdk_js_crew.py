"""
Phoenix JavaScript/TypeScript SDK Development Crew
===================================================
Builds the @phoenix/sdk package for Web3 developers.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool
)
import os

# LLM Configuration
USE_CLAUDE = os.getenv("USE_CLAUDE", "true").lower() == "true"

if USE_CLAUDE:
    from langchain_anthropic import ChatAnthropic
    claude_model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    llm = ChatAnthropic(
        model=claude_model,
        temperature=0.1,
        max_tokens=4000,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# Workspace configuration
WORKSPACE = "/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-sdk-js"
SPECS_DIR = f"{WORKSPACE}/docs"

# Initialize tools
file_read = FileReadTool()
file_write = FileWriterTool()
dir_read = DirectoryReadTool(directory=WORKSPACE)

# ============================================================================
# AGENTS
# ============================================================================

typescript_developer = Agent(
    role="Senior TypeScript Developer",
    goal="Build a comprehensive Web3 SDK for Phoenix Network",
    backstory="""You are an expert TypeScript developer who has built SDKs 
    for Ethereum, Polygon, and other blockchains. You understand ethers.js, 
    web3.js, and viem deeply. You know how to create developer-friendly APIs 
    that abstract complexity while providing power users with low-level access.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write, dir_read],
    llm=llm
)

web3_expert = Agent(
    role="Web3 Protocol Expert",
    goal="Ensure SDK properly implements Phoenix-specific features",
    backstory="""You are a Web3 expert who understands JSON-RPC protocols, 
    transaction signing, smart contract ABIs, and blockchain specifics. You 
    know how to handle DAG-specific features while maintaining Ethereum 
    compatibility.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write],
    llm=llm
)

api_designer = Agent(
    role="API Design Specialist",
    goal="Design intuitive and consistent SDK APIs",
    backstory="""You are an API design expert who has designed SDKs used by 
    thousands of developers. You understand the importance of consistency, 
    discoverability, and developer experience. You follow best practices for 
    TypeScript APIs and documentation.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write],
    llm=llm
)

testing_engineer = Agent(
    role="SDK Testing Specialist",
    goal="Create comprehensive test suite for the SDK",
    backstory="""You are a testing expert who specializes in SDK testing. 
    You know how to test async operations, mock blockchain interactions, 
    and ensure reliability across different environments. You write both 
    unit and integration tests.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write, dir_read],
    llm=llm
)

# ============================================================================
# TASKS
# ============================================================================

task_analyze_requirements = Task(
    description="""Analyze SDK requirements and existing solutions.
    
    1. Read SDK specifications in docs/
    2. Study ethers.js v6 architecture
    3. Review Phoenix node RPC methods
    4. Identify Phoenix-specific features:
       - DAG information queries
       - Blue score tracking
       - Canonical chain access
       - Multi-parent block queries
    5. Create SDK_ARCHITECTURE.md with:
       - Module structure
       - API design patterns
       - Phoenix extensions
       - Compatibility strategy
    """,
    agent=typescript_developer,
    expected_output="Comprehensive SDK architecture document"
)

task_setup_project = Task(
    description="""Set up TypeScript project with best practices.
    
    1. Initialize npm package:
       - Package name: @phoenix/sdk
       - TypeScript configuration
       - ESLint and Prettier setup
       - Jest testing framework
    2. Project structure:
       src/
         providers/     - Network providers
         wallets/       - Wallet management
         contracts/     - Contract interactions
         utils/         - Utility functions
         types/         - TypeScript types
         phoenix/       - Phoenix-specific features
    3. Configure build system:
       - Rollup for bundling
       - Multiple output formats (ESM, CJS, UMD)
       - Type declarations
    4. Set up CI/CD pipeline configuration
    """,
    agent=typescript_developer,
    expected_output="Configured TypeScript project with tooling",
    context=[task_analyze_requirements]
)

task_implement_provider = Task(
    description="""Implement Phoenix Provider extending ethers Provider.
    
    1. Create PhoenixProvider class:
       - Extends ethers.JsonRpcProvider
       - Maintains full Ethereum compatibility
       - Adds Phoenix-specific methods
    2. Implement standard methods:
       - getBlock, getTransaction, getBalance
       - sendTransaction, call, estimateGas
       - Event subscription system
    3. Add Phoenix methods:
       - getDAGInfo() - Current DAG state
       - getBlueScore(block) - Block blue score
       - getCanonicalChain(from, to) - Canonical blocks
       - getBlockParents(block) - Multiple parents
    4. Connection management:
       - Auto-reconnection
       - Multiple endpoint support
       - Load balancing
    """,
    agent=typescript_developer,
    expected_output="Complete PhoenixProvider implementation",
    context=[task_setup_project]
)

task_implement_wallet = Task(
    description="""Implement wallet management functionality.
    
    1. Create PhoenixWallet class:
       - Extends ethers.Wallet
       - HD wallet support (BIP39/BIP44)
       - Multiple account management
    2. Transaction signing:
       - EIP-155 replay protection
       - Phoenix chain ID handling
       - Gas estimation
    3. Wallet features:
       - Mnemonic generation/import
       - Private key import/export
       - Keystore file support
       - Hardware wallet preparation
    4. Security:
       - Secure key storage
       - Memory cleanup
       - Encryption utilities
    """,
    agent=web3_expert,
    expected_output="Secure wallet implementation with signing",
    context=[task_implement_provider]
)

task_contract_interaction = Task(
    description="""Implement smart contract interaction layer.
    
    1. Contract factory:
       - Deploy contracts
       - Attach to existing contracts
       - ABI management
    2. Contract class:
       - Method calls
       - Event listening
       - Gas estimation
       - Transaction building
    3. Type generation:
       - TypeChain integration
       - Auto-generate types from ABIs
    4. Common contracts:
       - ERC20 helper
       - ERC721 helper
       - ERC1155 helper
       - Phoenix-specific contracts
    """,
    agent=typescript_developer,
    expected_output="Complete contract interaction system",
    context=[task_implement_wallet]
)

task_phoenix_features = Task(
    description="""Implement Phoenix-specific features.
    
    1. DAG utilities:
       - DAG traversal helpers
       - Blue/red block identification
       - Confirmation tracking
    2. Mining utilities:
       - Difficulty calculation
       - Hash rate estimation
       - Mining statistics
    3. Advanced queries:
       - UTXO set queries
       - Mempool inspection
       - Network statistics
    4. Utilities:
       - Address validation
       - Unit conversion (PHX, vPHX)
       - Block time calculations
    """,
    agent=web3_expert,
    expected_output="Phoenix-specific feature implementations",
    context=[task_contract_interaction]
)

task_create_examples = Task(
    description="""Create comprehensive examples and documentation.
    
    1. Basic examples:
       - Connect to network
       - Check balances
       - Send transactions
       - Deploy contracts
    2. Advanced examples:
       - DeFi interactions
       - NFT minting
       - DEX integration
       - Multi-sig wallets
    3. Phoenix examples:
       - Query DAG structure
       - Track confirmations
       - Mining pool integration
    4. Documentation:
       - API reference (TypeDoc)
       - Getting started guide
       - Migration from ethers.js
       - Troubleshooting guide
    """,
    agent=api_designer,
    expected_output="Complete examples and documentation",
    context=[task_phoenix_features]
)

task_comprehensive_testing = Task(
    description="""Create comprehensive test suite.
    
    1. Unit tests:
       - Provider methods
       - Wallet operations
       - Utility functions
       - Type validation
    2. Integration tests:
       - Network connections
       - Transaction flow
       - Contract deployment
       - Event subscriptions
    3. Mock testing:
       - Mock RPC responses
       - Offline testing
       - Error scenarios
    4. Performance tests:
       - Connection pooling
       - Batch requests
       - Memory usage
    5. Achieve 90%+ code coverage
    """,
    agent=testing_engineer,
    expected_output="Complete test suite with high coverage",
    context=[task_create_examples]
)

task_publish_package = Task(
    description="""Prepare and publish NPM package.
    
    1. Package preparation:
       - Update package.json
       - Create .npmignore
       - Write CHANGELOG.md
       - Update README.md
    2. Build artifacts:
       - Generate bundles (ESM, CJS, UMD)
       - Generate type definitions
       - Minified versions
    3. Publishing setup:
       - NPM account configuration
       - Scoped package setup (@phoenix)
       - Version management
    4. CDN distribution:
       - Configure for unpkg
       - Configure for jsDelivr
    5. Create release notes
    """,
    agent=typescript_developer,
    expected_output="Published NPM package @phoenix/sdk",
    context=[task_comprehensive_testing]
)

# ============================================================================
# CREW
# ============================================================================

phoenix_sdk_js_crew = Crew(
    agents=[
        typescript_developer,
        web3_expert,
        api_designer,
        testing_engineer
    ],
    tasks=[
        task_analyze_requirements,
        task_setup_project,
        task_implement_provider,
        task_implement_wallet,
        task_contract_interaction,
        task_phoenix_features,
        task_create_examples,
        task_comprehensive_testing,
        task_publish_package
    ],
    process=Process.sequential,
    verbose=True,
    memory=True,
    cache=True,
    output_log_file="logs/phoenix_sdk_js_crew.log"
)

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PHOENIX JAVASCRIPT SDK DEVELOPMENT CREW")
    print("=" * 70)
    print("\nBuilding @phoenix/sdk for Web3 developers...")
    print(f"Using LLM: {'Claude' if USE_CLAUDE else 'GPT-4'}")
    print(f"Workspace: {WORKSPACE}\n")
    
    result = phoenix_sdk_js_crew.kickoff()
    
    print("\n" + "=" * 70)
    print("SDK CREW EXECUTION COMPLETE")
    print("=" * 70)
    print("\nResults:", result)
