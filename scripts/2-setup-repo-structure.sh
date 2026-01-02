#!/bin/bash

# BlockDAG Phoenix - Repository Structure Setup Script
# This script clones repos and sets up directory structures

set -e

echo "📁 Setting up repository structures..."
echo ""

# Create workspace directory
WORKSPACE="../phoenix-workspace"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

echo "📂 Workspace: $WORKSPACE"
echo ""

# Clone all repositories
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
    echo "⬇️  Cloning: $repo"
    
    if [ -d "$repo" ]; then
        if [ -d "$repo/.git" ]; then
            echo "   ⚠️  Directory exists, pulling latest..."
            cd "$repo"
            git pull || echo "   ⚠️  Pull failed, continuing..."
            cd ..
        else
            echo "   ⚠️  Directory exists but not a git repo, removing and cloning..."
            rm -rf "$repo"
            gh repo clone "BlockDAGPhoenix/$repo" || echo "   ⚠️  Clone failed"
        fi
    else
        gh repo clone "BlockDAGPhoenix/$repo" || echo "   ⚠️  Clone failed"
    fi
    
    echo ""
done

echo "✅ All repositories cloned to: $WORKSPACE"
echo ""
echo "Next: Run ./scripts/3-copy-specs.sh"






