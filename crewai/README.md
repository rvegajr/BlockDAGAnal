# CrewAI Setup for BlockDAG Phoenix

**Purpose**: Deploy AI agents (Crews) to develop each repository in parallel  
**Framework**: CrewAI - Multi-agent orchestration framework  
**Status**: Ready to deploy

---

## 🎯 Overview

This setup enables you to deploy specialized AI agent crews to work on each repository. Each crew has:
- **Agents**: Specialized AI workers (e.g., Backend Developer, Frontend Developer)
- **Tasks**: Specific goals to accomplish
- **Process**: Workflow coordination (sequential or hierarchical)
- **Tools**: Access to code, git, terminal, etc.

---

## 📦 Installation

### 1. Install CrewAI

```bash
# Install CrewAI and dependencies
pip install crewai crewai-tools

# Install optional tools
pip install langchain langchain-openai
```

### 2. Set Up Environment

```bash
# Create .env file
cat > /Users/xcode/Documents/BlockDAG/crewai/.env << 'EOF'
# OpenAI API Key (required)
OPENAI_API_KEY=your-api-key-here

# GitHub Token (for repo access)
GITHUB_TOKEN=your-github-token

# OpenAI Model Configuration
OPENAI_MODEL_NAME=gpt-4
OPENAI_API_BASE=https://api.openai.com/v1

# CrewAI Configuration
CREWAI_TELEMETRY=false
EOF
```

### 3. Verify Installation

```bash
cd /Users/xcode/Documents/BlockDAG/crewai
python -c "import crewai; print(f'CrewAI version: {crewai.__version__}')"
```

---

## 🏗️ Directory Structure

```
crewai/
├── README.md                    # This file
├── .env                         # API keys and config
├── requirements.txt             # Python dependencies
├── crews/
│   ├── phoenix_node_crew.py    # Core blockchain development
│   ├── phoenix_sdk_crew.py     # SDK development
│   ├── phoenix_explorer_crew.py # Explorer development
│   ├── phoenix_wallet_crew.py  # Wallet development
│   └── phoenix_docs_crew.py    # Documentation
├── agents/
│   ├── blockchain_developer.py # Core blockchain agent
│   ├── smart_contract_dev.py   # Solidity/EVM agent
│   ├── frontend_developer.py   # React/TypeScript agent
│   ├── devops_engineer.py      # Infrastructure agent
│   └── technical_writer.py     # Documentation agent
├── tasks/
│   ├── core_tasks.py           # Blockchain tasks
│   ├── sdk_tasks.py            # SDK tasks
│   ├── frontend_tasks.py       # Frontend tasks
│   └── docs_tasks.py           # Documentation tasks
├── tools/
│   ├── git_tools.py            # Git operations
│   ├── code_tools.py           # Code generation/editing
│   └── testing_tools.py        # Testing utilities
├── deploy_crew.py              # Main deployment script
└── monitor_crews.py            # Monitoring dashboard
```

---

## 🤖 Agent Architecture

### Agent Hierarchy

```
Crew Manager (Orchestrator)
├── Core Blockchain Crew
│   ├── Go Backend Developer
│   ├── Consensus Engineer
│   └── Testing Engineer
├── SDK Crew
│   ├── TypeScript Developer
│   ├── Python Developer
│   └── Go Developer
├── Frontend Crew
│   ├── React Developer
│   ├── UI/UX Designer
│   └── Web3 Integration Specialist
├── Infrastructure Crew
│   ├── DevOps Engineer
│   ├── Security Engineer
│   └── Monitoring Specialist
└── Documentation Crew
    ├── Technical Writer
    └── Tutorial Creator
```

---

## 🚀 Quick Start

### Deploy All Crews

```bash
cd /Users/xcode/Documents/BlockDAG/crewai
python deploy_crew.py --deploy-all
```

### Deploy Specific Crew

```bash
# Deploy core blockchain crew
python deploy_crew.py --crew phoenix-node

# Deploy SDK crew
python deploy_crew.py --crew phoenix-sdk-js

# Deploy explorer crew
python deploy_crew.py --crew phoenix-explorer
```

### Monitor Progress

```bash
# Start monitoring dashboard
python monitor_crews.py
```

---

## 📋 Crew Definitions

### 1. Phoenix Node Crew (Priority: P0)

**Goal**: Develop core blockchain node (fork Kaspa, add EVM)

**Agents**:
- **Go Backend Developer**: Implements blockchain logic
- **Consensus Engineer**: Works on GHOSTDAG and canonicalization
- **EVM Integration Specialist**: Integrates BSC EVM layer
- **Mining Engineer**: Implements dual algorithm mining
- **Testing Engineer**: Writes comprehensive tests

**Tasks** (see `crews/phoenix_node_crew.py`):
1. Fork and rebrand Kaspa
2. Configure genesis block
3. Implement SHA-3 mining
4. Create DAG→Linear canonicalization
5. Integrate EVM execution
6. Build JSON-RPC server

**Success Criteria**:
- `bdpd` compiles and runs
- Genesis block created
- Both mining algorithms work
- Smart contracts deployable
- RPC endpoints functional

---

### 2. Phoenix SDK Crew (Priority: P1)

**Goal**: Create SDKs for JavaScript, Python, and Go

**Agents**:
- **TypeScript Developer**: Builds @phoenix/sdk
- **Python Developer**: Builds phoenix-sdk
- **Go Developer**: Builds phoenix-sdk-go
- **API Designer**: Designs consistent API
- **Documentation Writer**: Creates API docs

**Tasks**:
1. Design unified SDK API
2. Implement provider interface
3. Implement wallet management
4. Implement contract interaction
5. Write comprehensive tests
6. Create usage examples

---

### 3. Phoenix Explorer Crew (Priority: P1)

**Goal**: Build block explorer with DAG visualization

**Agents**:
- **Backend Developer**: Forks and customizes Blockscout
- **Frontend Developer**: Builds DAG visualization UI
- **Database Engineer**: Optimizes indexing
- **UI/UX Designer**: Designs explorer interface

**Tasks**:
1. Fork Blockscout
2. Customize for Phoenix
3. Add DAG visualization
4. Integrate with Phoenix RPC
5. Deploy to production

---

### 4. Additional Crews

- **Phoenix Wallet Crew**: Mobile + Browser extension
- **Phoenix DevTools Crew**: Hardhat, Foundry, Remix
- **Phoenix Pool Crew**: Mining pool software
- **Phoenix Infrastructure Crew**: DevOps and monitoring
- **Phoenix Docs Crew**: Technical documentation

---

## 🔧 Configuration

### Crew Configuration File

Each crew has a configuration file that defines:

```yaml
# crews/config/phoenix_node.yaml
crew_name: "Phoenix Node Development Crew"
repository: "BlockDAGPhoenix/phoenix-node"
workspace: "../phoenix-workspace/phoenix-node"

agents:
  - name: "Go Backend Developer"
    role: "Senior Go Developer"
    goal: "Implement core blockchain functionality"
    backstory: "Expert in Go, blockchain, and distributed systems"
    tools:
      - git_tool
      - code_editor_tool
      - terminal_tool
      - testing_tool
    
  - name: "Consensus Engineer"
    role: "Blockchain Consensus Expert"
    goal: "Implement and optimize GHOSTDAG consensus"
    backstory: "Deep expertise in DAG-based consensus mechanisms"
    tools:
      - git_tool
      - code_editor_tool
      - simulation_tool

tasks:
  - description: "Fork Kaspa and rebrand to Phoenix"
    agent: "Go Backend Developer"
    expected_output: "Rebranded codebase that compiles"
    
  - description: "Implement DAG to linear canonicalization"
    agent: "Consensus Engineer"
    expected_output: "Deterministic ordering algorithm"

process: "sequential"  # or "hierarchical"
verbose: true
```

---

## 📊 Monitoring & Coordination

### Dashboard Features

```bash
# Start monitoring dashboard
python monitor_crews.py

# Features:
- Real-time crew status
- Task completion tracking
- Git commit history
- PR status
- Error logs
- Performance metrics
```

### Crew Coordination

Crews coordinate through:
1. **Shared Issues**: GitHub issues with `[crew-coordination]` tag
2. **Daily Sync**: Each crew reports progress to central hub
3. **Dependency Management**: Crews wait for dependencies
4. **Human Review**: Critical decisions flagged for review

---

## 🎯 Deployment Workflow

### Phase 1: Deploy Core Crews (Week 1)

```bash
# Deploy phoenix-node crew (P0)
python deploy_crew.py --crew phoenix-node --phase 1

# Deploy phoenix-sdk-js crew (P1)
python deploy_crew.py --crew phoenix-sdk-js --phase 1

# Deploy phoenix-docs crew (P1)
python deploy_crew.py --crew phoenix-docs --phase 1

# Monitor
python monitor_crews.py
```

**Expected Results**:
- Day 1-2: Crews analyze specs and create plans
- Day 3-7: Crews implement Phase 1 tasks
- End of Week 1: First PRs created

### Phase 2: Deploy Infrastructure Crews (Week 2)

```bash
# Deploy remaining crews
python deploy_crew.py --crew phoenix-explorer
python deploy_crew.py --crew phoenix-devtools
python deploy_crew.py --crew phoenix-pool
```

### Phase 3: Deploy User-Facing Crews (Week 3)

```bash
python deploy_crew.py --crew phoenix-wallet-mobile
python deploy_crew.py --crew phoenix-wallet-extension
python deploy_crew.py --crew phoenix-infrastructure
```

---

## 🛠️ Tools Available to Agents

### Code Tools
- `read_file`: Read source files
- `write_file`: Create/edit files
- `search_code`: Search codebase
- `analyze_code`: Static analysis

### Git Tools
- `git_clone`: Clone repository
- `git_commit`: Commit changes
- `git_push`: Push to remote
- `create_pr`: Create pull request
- `review_pr`: Review existing PRs

### Terminal Tools
- `run_command`: Execute shell commands
- `run_tests`: Run test suites
- `build_project`: Build/compile
- `check_logs`: View logs

### Documentation Tools
- `read_spec`: Read technical specs
- `search_docs`: Search documentation
- `generate_docs`: Generate API docs

---

## 🔐 Security Considerations

### Access Control
- Crews have **read/write** access to their assigned repos
- Crews **cannot**:
  - Merge PRs (requires human approval)
  - Delete branches
  - Access secrets (except via env vars)
  - Modify protected branches

### Code Review
- All code changes go through PR review
- Critical changes require human approval
- Security-sensitive code flagged automatically

---

## 📈 Success Metrics

### Per Crew
- [ ] Tasks completed
- [ ] PRs created
- [ ] Tests passing
- [ ] Code coverage
- [ ] Documentation complete

### Overall Project
- [ ] All 13 repos have active development
- [ ] Commits happening daily
- [ ] PRs being reviewed and merged
- [ ] CI/CD passing
- [ ] Progress toward testnet launch

---

## 🆘 Troubleshooting

### Crew Not Starting
```bash
# Check logs
python monitor_crews.py --crew phoenix-node --logs

# Restart crew
python deploy_crew.py --crew phoenix-node --restart
```

### Agent Stuck
```bash
# Intervene manually
python deploy_crew.py --crew phoenix-node --debug

# Review agent's current task
python monitor_crews.py --crew phoenix-node --current-task
```

### API Rate Limits
```bash
# Slow down crew
python deploy_crew.py --crew phoenix-node --rate-limit 10

# Use different model
# Edit .env: OPENAI_MODEL_NAME=gpt-3.5-turbo
```

---

## 📚 Resources

- **CrewAI Docs**: https://docs.crewai.com
- **Your Specs**: `/Users/xcode/Documents/BlockDAG/docs/specs/`
- **Agent Instructions**: Each repo's `AGENT_INSTRUCTIONS.md`
- **Coordination Hub**: https://github.com/BlockDAGPhoenix/phoenix-node/issues/1

---

## 🚀 Next Steps

1. **Install CrewAI**: `pip install crewai crewai-tools`
2. **Configure API Keys**: Edit `.env` file
3. **Deploy First Crew**: `python deploy_crew.py --crew phoenix-node`
4. **Monitor Progress**: `python monitor_crews.py`
5. **Review PRs**: Check GitHub daily
6. **Iterate**: Improve crew configurations based on results

---

**Ready to deploy AI agents! 🤖**






