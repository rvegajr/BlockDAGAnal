# 🚀 CrewAI Quick Start Guide

## Installation

```bash
cd /Users/xcode/Documents/BlockDAG/crewai

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Add your API keys to .env
nano .env
```

## Deploy Your First Crew

### 1. Phoenix Node Crew (Core Blockchain)

```bash
# Test deployment (dry run)
python deploy_crew.py --crew phoenix-node --dry-run

# Deploy for real
python deploy_crew.py --crew phoenix-node
```

This will:
- ✅ Analyze all technical specs
- ✅ Fork and rebrand Kaspa
- ✅ Implement genesis block
- ✅ Add SHA-3 mining
- ✅ Create DAG→Linear canonicalization
- ✅ Integrate EVM
- ✅ Build JSON-RPC server

**Expected time**: 4-8 hours (depends on LLM speed)

### 2. Monitor Progress

```bash
# Watch crew progress
python monitor_crews.py

# Check logs
tail -f logs/phoenix-node-crew.log
```

### 3. Review Results

```bash
# Check generated code
cd ../phoenix-workspace/phoenix-node

# See changes
git status
git diff

# Run tests
go test ./...

# Build
go build ./cmd/bdpd
```

## Deploy All Crews (Parallel Development)

```bash
# Deploy all crews at once
python deploy_crew.py --deploy-all
```

This deploys crews to:
- phoenix-node
- phoenix-sdk-js
- phoenix-sdk-python
- phoenix-sdk-go
- phoenix-explorer
- phoenix-devtools
- phoenix-wallet-mobile
- phoenix-wallet-extension
- phoenix-pool
- phoenix-infrastructure
- phoenix-docs
- phoenix-website

## Crew Configuration

Each crew is defined in `crews/{crew_name}_crew.py`

To create a new crew:
1. Copy `crews/phoenix_node_crew.py`
2. Modify agents and tasks
3. Add to `deploy_crew.py`

## API Keys Required

### OpenAI (Required)
```bash
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-...
```

### GitHub (Optional but recommended)
```bash
# Get from: https://github.com/settings/tokens
# Permissions needed: repo (full control)
GITHUB_TOKEN=ghp_...
```

## Cost Estimation

Using GPT-4:
- **Per crew per task**: ~$1-5
- **Full phoenix-node crew**: ~$20-50
- **All 13 crews**: ~$200-500

Using GPT-3.5-turbo (cheaper):
- **Per crew per task**: ~$0.10-0.50
- **Full phoenix-node crew**: ~$2-5
- **All 13 crews**: ~$20-50

*Actual costs depend on code complexity and iterations*

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
# Edit .env
nano .env

# Add:
OPENAI_API_KEY=your-key-here
```

### "Module 'crewai' not found"
```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Crew taking too long
```bash
# Use faster model in .env
OPENAI_MODEL_NAME=gpt-3.5-turbo

# Or reduce task complexity by editing crew file
```

### Rate limits hit
```bash
# Slow down in .env
RATE_LIMIT=10
```

## Next Steps

1. ✅ Set up CrewAI (`./setup.sh`)
2. ✅ Add API keys (`.env`)
3. ✅ Deploy first crew (`python deploy_crew.py --crew phoenix-node`)
4. ⏳ Wait for completion (4-8 hours)
5. ✅ Review code
6. ✅ Test and merge
7. ✅ Deploy next crews

## Support

- **CrewAI Docs**: https://docs.crewai.com
- **Your Specs**: `../docs/specs/`
- **Agent Instructions**: Each repo's `AGENT_INSTRUCTIONS.md`

**Let's build Phoenix with AI! 🚀**






