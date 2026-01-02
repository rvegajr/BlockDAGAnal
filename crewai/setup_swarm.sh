#!/bin/bash

# Phoenix Network CrewAI Swarm Setup Script
# ==========================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner
clear
echo -e "${CYAN}============================================================${NC}"
echo -e "${BOLD}🔥 PHOENIX NETWORK - CREWAI SWARM SETUP 🔥${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check Python version
print_info "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Check if in correct directory
if [ ! -f "swarm_orchestrator.py" ]; then
    print_error "Please run this script from the crewai directory"
    print_info "cd /Users/admin/Dev/Crypto/BlockDAG/crewai"
    exit 1
fi

# Create virtual environment
print_info "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet
print_success "pip upgraded"

# Install requirements
print_info "Installing requirements (this may take a few minutes)..."
pip install -r requirements.txt --quiet
print_success "All requirements installed"

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    print_success "Logs directory created"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    echo ""
    echo -e "${YELLOW}Please create a .env file with your API keys:${NC}"
    echo ""
    cat << 'EOF'
# Create .env file with:
cat > .env << 'END'
# Choose one or both LLM providers
ANTHROPIC_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key

# Optional
GITHUB_TOKEN=your-github-token
USE_CLAUDE=true
END
EOF
    echo ""
    read -p "Press Enter after you've created the .env file..."
    
    if [ ! -f ".env" ]; then
        print_error ".env file still not found. Exiting."
        exit 1
    fi
fi

# Verify API keys
print_info "Checking API keys..."
if grep -q "your-" .env 2>/dev/null; then
    print_warning "Please update the API keys in .env file"
    print_info "Get Claude API: https://console.anthropic.com"
    print_info "Get OpenAI API: https://platform.openai.com"
    exit 1
else
    print_success "API keys configured"
fi

# Create crew files directory if missing
if [ ! -d "crews" ]; then
    mkdir -p crews
    print_success "Crews directory created"
fi

# Setup complete
echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${BOLD}✅ SETUP COMPLETE!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${CYAN}Available Commands:${NC}"
echo ""
echo -e "  ${BOLD}Interactive Mode:${NC}"
echo -e "  ${GREEN}python deploy_swarm.py${NC}"
echo ""
echo -e "  ${BOLD}Quick Deployment:${NC}"
echo -e "  ${GREEN}python deploy_swarm.py --quick${NC}     # Deploy P0+P1 components"
echo -e "  ${GREEN}python deploy_swarm.py --all${NC}       # Deploy all components"
echo ""
echo -e "  ${BOLD}Status & Monitoring:${NC}"
echo -e "  ${GREEN}python deploy_swarm.py --status${NC}    # Show component status"
echo -e "  ${GREEN}python swarm_orchestrator.py --monitor${NC}  # Real-time monitor"
echo ""
echo -e "  ${BOLD}Phase Deployment:${NC}"
echo -e "  ${GREEN}python deploy_swarm.py --phase P0${NC}  # Critical components"
echo -e "  ${GREEN}python deploy_swarm.py --phase P1${NC}  # High priority"
echo -e "  ${GREEN}python deploy_swarm.py --phase P2${NC}  # Medium priority"
echo -e "  ${GREEN}python deploy_swarm.py --phase P3${NC}  # Low priority"
echo ""
echo -e "${CYAN}============================================================${NC}"
echo ""

# Ask if user wants to start
read -p "Would you like to start the interactive deployment now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    print_info "Starting Phoenix CrewAI Swarm..."
    echo ""
    python deploy_swarm.py
fi

echo ""
print_success "Setup script completed!"
echo -e "${CYAN}Happy building! 🚀${NC}"
