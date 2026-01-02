#!/bin/bash

# CrewAI Setup Script for BlockDAG Phoenix
# This script sets up the CrewAI environment

set -e

echo "🤖 Setting up CrewAI for BlockDAG Phoenix..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    echo "   Install: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null

# Install requirements
echo "📦 Installing CrewAI and dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ CrewAI setup complete!"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "❗ IMPORTANT: Edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY=your-key-here"
    echo "   - GITHUB_TOKEN=your-token-here"
    echo ""
    echo "Edit now:"
    echo "   nano .env"
else
    echo "✅ .env file exists"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "NEXT STEPS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Edit .env and add your API keys:"
echo "   nano .env"
echo ""
echo "3. Test the setup:"
echo "   python deploy_crew.py --crew phoenix-node --dry-run"
echo ""
echo "4. Deploy your first crew:"
echo "   python deploy_crew.py --crew phoenix-node"
echo ""
echo "5. Monitor progress:"
echo "   python monitor_crews.py"
echo ""






