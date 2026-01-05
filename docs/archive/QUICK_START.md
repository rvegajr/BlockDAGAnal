# Quick Start Guide - Phoenix MVP

## Prerequisites Check

Run these commands to verify you're ready:

```bash
# Check Python version (need 3.10+)
python3 --version

# Check if Anthropic key is set
echo $ANTHROPIC_API_KEY

# Check GitHub CLI
gh auth status
```

## One-Command Setup (After Prerequisites)

```bash
cd /Users/admin/Dev/Crypto/BlockDAG/crewai && \
python3.11 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" > .env && \
python deploy_crew.py --crew phoenix-node
```

## What's Been Prepared

✅ All crew files configured for Claude  
✅ Workspace structure created  
✅ Specifications copied  
✅ Cost-optimized (Claude 3 Sonnet)  
✅ MVP simplified (single mining algorithm)  
✅ Anthropic API key configured

## Current Blockers

1. Python 3.10+ required (you have 3.9.6)

See NEXT_STEPS.md for detailed resolution.
