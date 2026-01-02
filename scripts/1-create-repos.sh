#!/bin/bash

# BlockDAG Phoenix - Repository Creation Script
# This script creates all repositories in the BlockDAGPhoenix organization
# Compatible with bash 3.2+ (no associative arrays)

set -e

echo "🚀 Creating BlockDAG Phoenix Repositories..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Install it: brew install gh"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

# Repositories and descriptions (using simple arrays)
repos=(
    "phoenix-node:Core blockchain node - Fork of Kaspa with EVM integration"
    "phoenix-explorer:Block explorer based on Blockscout"
    "phoenix-sdk-js:JavaScript/TypeScript SDK for Phoenix Network"
    "phoenix-sdk-python:Python SDK for Phoenix Network"
    "phoenix-sdk-go:Go SDK for Phoenix Network"
    "phoenix-devtools:Developer tools: Hardhat plugin, Foundry config, Remix integration"
    "phoenix-wallet-mobile:React Native mobile wallet for iOS and Android"
    "phoenix-wallet-extension:Browser extension wallet for Chrome, Firefox, Brave"
    "phoenix-pool:Mining pool software with Stratum protocol support"
    "phoenix-infrastructure:DevOps infrastructure: Terraform, K8s, monitoring"
    "phoenix-docs:Technical documentation site (Docusaurus)"
    "phoenix-website:Official marketing website"
    "phoenix-brand:Brand assets, logos, visual identity guidelines"
)

# Create each repository
for repo_info in "${repos[@]}"; do
    repo_name="${repo_info%%:*}"
    description="${repo_info#*:}"
    
    echo "📦 Creating: $repo_name"
    echo "   Description: $description"
    
    # Create repository
    gh repo create "BlockDAGPhoenix/$repo_name" \
        --public \
        --description "$description" \
        --add-readme \
        --license mit \
        --enable-issues \
        --enable-wiki=false || echo "   ⚠️  Repository may already exist"
    
    echo "   ✅ Created"
    echo ""
done

echo ""
echo "🎉 Repository creation complete!"
echo ""
echo "Next steps:"
echo "1. Run: ./scripts/2-setup-repo-structure.sh"
echo "2. Run: ./scripts/3-copy-specs.sh"
echo "3. Run: ./scripts/4-generate-agent-instructions.sh"
