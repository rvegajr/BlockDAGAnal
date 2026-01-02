#!/bin/bash

# BlockDAG Phoenix - Master Setup Script
# This script runs all setup steps in sequence

set -e

echo "╔═══════════════════════════════════════════════════╗"
echo "║  BlockDAG Phoenix - Agent Deployment Setup       ║"
echo "║  Complete Repository Initialization               ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "   Install: brew install gh"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub"
    echo "   Run: gh auth login"
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Confirm execution
echo "This script will:"
echo "  1. Create 13 repositories in BlockDAGPhoenix organization"
echo "  2. Clone them to ../phoenix-workspace/"
echo "  3. Copy all technical specifications"
echo "  4. Generate AGENT_INSTRUCTIONS.md files"
echo "  5. Commit and push everything"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🚀 Starting setup..."
echo ""

# Step 1: Create repositories
echo "═══════════════════════════════════════════════════"
echo "STEP 1/5: Creating GitHub repositories"
echo "═══════════════════════════════════════════════════"
chmod +x ./scripts/1-create-repos.sh
./scripts/1-create-repos.sh

echo ""
read -p "Press enter to continue to Step 2..."
echo ""

# Step 2: Clone and set up structure
echo "═══════════════════════════════════════════════════"
echo "STEP 2/5: Cloning repositories and setting up structure"
echo "═══════════════════════════════════════════════════"
chmod +x ./scripts/2-setup-repo-structure.sh
./scripts/2-setup-repo-structure.sh

echo ""
read -p "Press enter to continue to Step 3..."
echo ""

# Step 3: Copy specs
echo "═══════════════════════════════════════════════════"
echo "STEP 3/5: Copying technical specifications"
echo "═══════════════════════════════════════════════════"
chmod +x ./scripts/3-copy-specs.sh
./scripts/3-copy-specs.sh

echo ""
read -p "Press enter to continue to Step 4..."
echo ""

# Step 4: Generate agent instructions
echo "═══════════════════════════════════════════════════"
echo "STEP 4/5: Generating AGENT_INSTRUCTIONS.md files"
echo "═══════════════════════════════════════════════════"
chmod +x ./scripts/4-generate-agent-instructions.sh
./scripts/4-generate-agent-instructions.sh

echo ""
read -p "Press enter to continue to Step 5..."
echo ""

# Step 5: Commit and push
echo "═══════════════════════════════════════════════════"
echo "STEP 5/5: Committing and pushing to GitHub"
echo "═══════════════════════════════════════════════════"
chmod +x ./scripts/5-commit-and-push.sh
./scripts/5-commit-and-push.sh

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║           🎉 SETUP COMPLETE! 🎉                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "✅ 13 repositories created and configured"
echo "✅ All technical specifications copied"
echo "✅ All AGENT_INSTRUCTIONS.md files generated"
echo "✅ Everything committed and pushed to GitHub"
echo ""
echo "📍 Repositories are at: ../phoenix-workspace/"
echo "🔗 View online: https://github.com/BlockDAGPhoenix"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Review repositories on GitHub"
echo "   https://github.com/BlockDAGPhoenix"
echo ""
echo "2. Set up organization (manual on GitHub.com):"
echo "   - Add organization logo"
echo "   - Make members public"
echo "   - Create teams"
echo "   - Enable branch protection"
echo ""
echo "3. Deploy first wave of agents:"
echo "   - Agent-Core-1: phoenix-node (Consensus)"
echo "   - Agent-Core-2: phoenix-node (EVM)"
echo "   - Agent-SDK-1: phoenix-sdk-js"
echo "   - Agent-Docs-1: phoenix-docs"
echo ""
echo "4. Monitor agent progress:"
echo "   - Check GitHub Actions"
echo "   - Review PRs"
echo "   - Track issues"
echo ""
echo "📖 See AGENT_DEPLOYMENT_PLAN.md for full details"
echo ""






