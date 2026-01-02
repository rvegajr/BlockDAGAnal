# CrewAI Setup Notes

## Python Version Requirement

**IMPORTANT**: CrewAI requires Python 3.10 or higher. Your current Python version is 3.9.6.

### Solutions:

1. **Upgrade Python** (Recommended):
   ```bash
   # Using Homebrew on macOS
   brew install python@3.11
   
   # Create new venv with Python 3.11
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Use pyenv**:
   ```bash
   pyenv install 3.11.0
   pyenv local 3.11.0
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## API Key Configuration

The `.env` file has been created and should have your Anthropic API key:

```bash
# Edit .env and add:
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

Or set it in your environment:
```bash
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

Get your API key from: https://console.anthropic.com/

## Current Configuration

- Model: Claude 3 Sonnet (cost-optimized, excellent for coding)
- Phoenix-node crew: Configured for MVP (single SHA-3 mining algorithm)
- Workspace: ../phoenix-workspace/phoenix-node

## Next Steps

1. Upgrade Python to 3.10+
2. Verify Anthropic API key in .env (should already be set)
3. Install dependencies: `pip install -r requirements.txt`
4. Run repository setup: `cd .. && ./scripts/RUN-ALL-SETUP.sh`
5. Deploy crew: `python deploy_crew.py --crew phoenix-node`

