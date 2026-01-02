#!/bin/bash

# BlockDAG Phoenix - Agent Instructions Generator
# This script creates AGENT_INSTRUCTIONS.md for each repository

set -e

echo "🤖 Generating AGENT_INSTRUCTIONS.md files..."
echo ""

WORKSPACE="../phoenix-workspace"

if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Workspace not found. Run ./scripts/2-setup-repo-structure.sh first"
    exit 1
fi

# Function to create agent instructions
create_instructions() {
    local repo=$1
    local purpose=$2
    local mission=$3
    local tech_stack=$4
    local spec_files=$5
    
    local file="$WORKSPACE/$repo/AGENT_INSTRUCTIONS.md"
    
    echo "📝 Creating: $repo/AGENT_INSTRUCTIONS.md"
    
    cat > "$file" << EOF
# Agent Instructions: $repo

## Repository Purpose
$purpose

## Your Mission
$mission

## Technical Specifications
$spec_files

## Technology Stack
$tech_stack

## Development Phases

### Phase 1: Setup & Foundation
- [ ] Set up project structure
- [ ] Configure build system
- [ ] Set up testing framework
- [ ] Create initial documentation

### Phase 2: Core Features
- [ ] Implement core functionality per spec
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Document APIs

### Phase 3: Testing & Polish
- [ ] Achieve 80%+ test coverage
- [ ] Performance optimization
- [ ] Security review
- [ ] Documentation completion

## Success Criteria
- [ ] All specs implemented
- [ ] All tests passing
- [ ] Documentation complete
- [ ] CI/CD passing
- [ ] Ready for integration

## Integration Points
See \`docs/specs/\` for detailed integration requirements.

## Testing Requirements
- Unit test coverage: 80%+
- Integration tests for all APIs
- E2E tests for critical paths

## Documentation Requirements
- README.md with usage examples
- API documentation
- Architecture decision records (ADRs)
- Inline code documentation

## Code Quality Standards
- Follow language-specific style guides
- Use linting tools
- Use formatting tools
- Enable pre-commit hooks
- All CI/CD checks must pass

## Security Considerations
- Follow security best practices for language/framework
- No hardcoded secrets
- Input validation on all external data
- Security audit before mainnet

## Getting Started (For Agent)
1. Read all files in \`docs/specs/\`
2. Review any upstream projects referenced in specs
3. Set up development environment (see CONTRIBUTING.md)
4. Start with Phase 1, Task 1
5. Create PR for each completed feature
6. Update this checklist as you progress

## Communication
- Create GitHub issues for questions
- Tag issues with \`[agent-question]\` for human review
- Update progress in main coordination issue
- Report blockers immediately

## Resources
- Specs: \`docs/specs/\`
- Examples: \`examples/\` (once created)
- Tests: \`tests/\` (once created)
- Main project: https://github.com/BlockDAGPhoenix/phoenix-node

---

**AI Agent**: You are responsible for implementing this repository according to the specifications. Break down tasks into small, testable increments. Create PRs frequently. Ask questions when specs are unclear. Your goal is to deliver production-ready code that passes all tests and meets all specs.

Good luck! 🚀
EOF

    echo "   ✅ Created"
    echo ""
}

# Generate instructions for each repository

create_instructions "phoenix-node" \
    "Core blockchain daemon that implements GHOSTDAG consensus with EVM smart contract support." \
    "Build the bdpd daemon by forking Kaspa, adding EVM integration, implementing dual mining (kHeavyHash + SHA-3), and creating the DAG-to-linear canonicalization layer." \
    "Language: Go, Framework: Kaspa (fork) + BSC EVM (fork), Key Dependencies: go-ethereum, kaspanet/kaspad" \
    "See: docs/specs/CONSENSUS.md, CANONICALIZATION.md, BLOCK_HEADER.md, EXECUTION.md, RPC.md, ALGORITHMS.md"

create_instructions "phoenix-explorer" \
    "Block explorer for visualizing the Phoenix blockchain and DAG structure." \
    "Fork Blockscout, customize for Phoenix network, add DAG visualization, integrate with Phoenix RPC." \
    "Language: Elixir (backend), TypeScript/React (frontend), Framework: Blockscout" \
    "See: docs/specs/BLOCKSCOUT.md"

create_instructions "phoenix-sdk-js" \
    "JavaScript/TypeScript SDK for interacting with Phoenix blockchain." \
    "Create ethers.js wrapper that works with Phoenix RPC, support for DAG-specific features, full EVM compatibility." \
    "Language: TypeScript, Framework: ethers.js (wrapper), Package: @phoenix/sdk" \
    "See: docs/specs/JS_TS.md"

create_instructions "phoenix-sdk-python" \
    "Python SDK for interacting with Phoenix blockchain." \
    "Create web3.py wrapper for Phoenix, support for all RPC methods, type hints, async support." \
    "Language: Python 3.11+, Framework: web3.py (wrapper), Package: phoenix-sdk" \
    "See: docs/specs/PYTHON.md"

create_instructions "phoenix-sdk-go" \
    "Go SDK for interacting with Phoenix blockchain." \
    "Native Go library for Phoenix RPC, wallet management, contract interaction." \
    "Language: Go, Native library, Package: github.com/BlockDAGPhoenix/phoenix-sdk-go" \
    "See: docs/specs/GO.md"

create_instructions "phoenix-devtools" \
    "Developer tools for smart contract development on Phoenix." \
    "Create Hardhat plugin, Foundry configuration, Remix integration for Phoenix network." \
    "Language: TypeScript (Hardhat), Rust (Foundry), Packages: @phoenix/hardhat-plugin" \
    "See: docs/specs/HARDHAT.md, FOUNDRY.md, REMIX.md"

create_instructions "phoenix-wallet-mobile" \
    "Mobile wallet for Phoenix blockchain (iOS and Android)." \
    "Build React Native wallet with secure key management, ERC-20/721 support, WalletConnect, beautiful UI." \
    "Language: TypeScript, Framework: React Native, Reference: Rainbow Wallet" \
    "See: docs/specs/MOBILE.md"

create_instructions "phoenix-wallet-extension" \
    "Browser extension wallet for Phoenix blockchain." \
    "Build WebExtension wallet compatible with Chrome/Firefox/Brave, MetaMask-compatible API." \
    "Language: TypeScript, Framework: WebExtension API, Reference: MetaMask" \
    "See: docs/specs/EXTENSION.md"

create_instructions "phoenix-pool" \
    "Mining pool software with Stratum protocol support." \
    "Build mining pool server with Stratum V1/V2, support for both kHeavyHash and SHA-3, payout system, pool dashboard." \
    "Language: Go/Rust, Protocol: Stratum V1/V2" \
    "See: docs/specs/POOL_SOFTWARE.md, POOL_PROTOCOL.md"

create_instructions "phoenix-infrastructure" \
    "DevOps infrastructure for Phoenix network." \
    "Create Terraform configs for seed nodes, RPC gateway, monitoring stack. Kubernetes configs. Ansible playbooks." \
    "Tools: Terraform, Kubernetes, Ansible, Grafana, Prometheus" \
    "See: docs/specs/SEED_NODES.md, GATEWAY.md, MONITORING.md"

create_instructions "phoenix-docs" \
    "Technical documentation site for Phoenix." \
    "Build Docusaurus site with getting started guides, tutorials, API reference, architecture docs." \
    "Framework: Docusaurus, Deploy: Vercel or GitHub Pages" \
    "See: All specs in docs/specs/"

create_instructions "phoenix-website" \
    "Official marketing website for Phoenix." \
    "Build Next.js marketing site with modern design, follow brand guidelines, SEO optimized." \
    "Framework: Next.js, Styling: Tailwind CSS, Deploy: Vercel" \
    "See: docs/brand/ for visual identity guidelines"

create_instructions "phoenix-brand" \
    "Brand assets and visual identity for Phoenix." \
    "Organize brand assets, create templates, maintain visual consistency." \
    "Assets: Logos, colors, typography, templates" \
    "See: guidelines/VISUAL_IDENTITY_DESIGN.md"

echo "✅ All AGENT_INSTRUCTIONS.md files generated!"
echo ""
echo "Next: Review the instructions and commit to repositories"






