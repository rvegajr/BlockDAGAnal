#!/bin/bash

# BlockDAG Phoenix - Specs Copy Script
# This script copies technical specs to their respective repositories

set -e

echo "📋 Copying technical specifications to repositories..."
echo ""

WORKSPACE="../phoenix-workspace"
SPECS_DIR="./docs/specs"
BRAND_DIR="./docs/brand"

if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Workspace not found. Run ./scripts/2-setup-repo-structure.sh first"
    exit 1
fi

# Function to copy specs and create directory structure
copy_specs() {
    local repo=$1
    local spec_path=$2
    local target_dir="$WORKSPACE/$repo/docs/specs"
    
    echo "📄 Copying to: $repo"
    
    mkdir -p "$target_dir"
    cp -r "$spec_path" "$target_dir/" 2>/dev/null || echo "   ⚠️  Spec not found: $spec_path"
    
    echo "   ✅ Done"
}

# phoenix-node (Core blockchain)
echo "🔹 phoenix-node"
mkdir -p "$WORKSPACE/phoenix-node/docs/specs"
cp -r "$SPECS_DIR/core-node/"* "$WORKSPACE/phoenix-node/docs/specs/" 2>/dev/null || true
cp -r "$SPECS_DIR/evm/"* "$WORKSPACE/phoenix-node/docs/specs/" 2>/dev/null || true
cp -r "$SPECS_DIR/mining/"* "$WORKSPACE/phoenix-node/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-explorer
echo "🔹 phoenix-explorer"
mkdir -p "$WORKSPACE/phoenix-explorer/docs/specs"
cp "$SPECS_DIR/explorer/BLOCKSCOUT.md" "$WORKSPACE/phoenix-explorer/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-sdk-js
echo "🔹 phoenix-sdk-js"
mkdir -p "$WORKSPACE/phoenix-sdk-js/docs/specs"
cp "$SPECS_DIR/sdk/JS_TS.md" "$WORKSPACE/phoenix-sdk-js/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-sdk-python
echo "🔹 phoenix-sdk-python"
mkdir -p "$WORKSPACE/phoenix-sdk-python/docs/specs"
cp "$SPECS_DIR/sdk/PYTHON.md" "$WORKSPACE/phoenix-sdk-python/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-sdk-go
echo "🔹 phoenix-sdk-go"
mkdir -p "$WORKSPACE/phoenix-sdk-go/docs/specs"
cp "$SPECS_DIR/sdk/GO.md" "$WORKSPACE/phoenix-sdk-go/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-devtools
echo "🔹 phoenix-devtools"
mkdir -p "$WORKSPACE/phoenix-devtools/docs/specs"
cp -r "$SPECS_DIR/devtools/"* "$WORKSPACE/phoenix-devtools/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-wallet-mobile
echo "🔹 phoenix-wallet-mobile"
mkdir -p "$WORKSPACE/phoenix-wallet-mobile/docs/specs"
cp "$SPECS_DIR/wallet/MOBILE.md" "$WORKSPACE/phoenix-wallet-mobile/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-wallet-extension
echo "🔹 phoenix-wallet-extension"
mkdir -p "$WORKSPACE/phoenix-wallet-extension/docs/specs"
cp "$SPECS_DIR/wallet/EXTENSION.md" "$WORKSPACE/phoenix-wallet-extension/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-pool
echo "🔹 phoenix-pool"
mkdir -p "$WORKSPACE/phoenix-pool/docs/specs"
cp -r "$SPECS_DIR/pool/"* "$WORKSPACE/phoenix-pool/docs/specs/" 2>/dev/null || true
cp "$SPECS_DIR/mining/POOL_PROTOCOL.md" "$WORKSPACE/phoenix-pool/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-infrastructure
echo "🔹 phoenix-infrastructure"
mkdir -p "$WORKSPACE/phoenix-infrastructure/docs/specs"
cp -r "$SPECS_DIR/ops/"* "$WORKSPACE/phoenix-infrastructure/docs/specs/" 2>/dev/null || true
cp -r "$SPECS_DIR/rpc/"* "$WORKSPACE/phoenix-infrastructure/docs/specs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-docs (gets ALL specs)
echo "🔹 phoenix-docs"
mkdir -p "$WORKSPACE/phoenix-docs/docs"
cp -r "$SPECS_DIR" "$WORKSPACE/phoenix-docs/docs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-website (gets brand guidelines)
echo "🔹 phoenix-website"
mkdir -p "$WORKSPACE/phoenix-website/docs"
cp -r "$BRAND_DIR" "$WORKSPACE/phoenix-website/docs/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

# phoenix-brand (gets brand guidelines)
echo "🔹 phoenix-brand"
mkdir -p "$WORKSPACE/phoenix-brand/guidelines"
cp -r "$BRAND_DIR/"* "$WORKSPACE/phoenix-brand/guidelines/" 2>/dev/null || true
echo "   ✅ Done"
echo ""

echo "✅ All specs copied!"
echo ""
echo "Next: Review copied specs and run ./scripts/4-generate-agent-instructions.sh"






