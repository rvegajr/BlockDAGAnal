#!/bin/bash

# BlockDAG Phoenix - Commit and Push Script
# This script commits all changes and pushes to GitHub

set -e

echo "🚀 Committing and pushing changes to all repositories..."
echo ""

WORKSPACE="../phoenix-workspace"

if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Workspace not found."
    exit 1
fi

repos=(
    "phoenix-node"
    "phoenix-explorer"
    "phoenix-sdk-js"
    "phoenix-sdk-python"
    "phoenix-sdk-go"
    "phoenix-devtools"
    "phoenix-wallet-mobile"
    "phoenix-wallet-extension"
    "phoenix-pool"
    "phoenix-infrastructure"
    "phoenix-docs"
    "phoenix-website"
    "phoenix-brand"
)

for repo in "${repos[@]}"; do
    echo "📦 Processing: $repo"
    
    cd "$WORKSPACE/$repo"
    
    # Check if there are changes
    if [[ -n $(git status -s) ]]; then
        echo "   📝 Changes detected, committing..."
        
        git add .
        git commit -m "docs: Add technical specifications and agent instructions

- Add technical specs from main documentation
- Add AGENT_INSTRUCTIONS.md for AI agent development
- Set up repository structure
- Ready for agent deployment"
        
        git push origin main || git push origin master
        
        echo "   ✅ Pushed"
    else
        echo "   ℹ️  No changes to commit"
    fi
    
    cd - > /dev/null
    echo ""
done

echo "✅ All repositories updated!"
echo ""
echo "🎉 Setup complete! Repositories are ready for agent deployment."
echo ""
echo "Next steps:"
echo "1. Review repositories on GitHub"
echo "2. Set up branch protection rules"
echo "3. Deploy first wave of agents"






