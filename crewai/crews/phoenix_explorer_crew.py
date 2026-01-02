"""
Phoenix Explorer Development Crew
==================================
Builds the block explorer with DAG visualization based on Blockscout.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
    SerperDevTool
)
import os

# Get LLM configuration
USE_CLAUDE = os.getenv("USE_CLAUDE", "true").lower() == "true"

if USE_CLAUDE:
    from langchain_anthropic import ChatAnthropic
    claude_model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    llm = ChatAnthropic(
        model=claude_model,
        temperature=0.1,
        max_tokens=4000,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# Workspace configuration
WORKSPACE = "/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-explorer"
SPECS_DIR = f"{WORKSPACE}/docs/specs"

# Initialize tools
file_read = FileReadTool()
file_write = FileWriterTool()
dir_read = DirectoryReadTool(directory=WORKSPACE)
# GitHub search tool not available in current version
# github_search = GitHubSearchTool(
#     github_token=os.getenv("GITHUB_TOKEN"),
#     gh_search_query="blockscout"
# )
web_search = SerperDevTool()

# ============================================================================
# AGENTS
# ============================================================================

elixir_developer = Agent(
    role="Senior Elixir Backend Developer",
    goal="Fork and customize Blockscout for Phoenix Network",
    backstory="""You are an expert Elixir developer with deep knowledge of 
    Blockscout, Phoenix Framework, and blockchain indexing. You've customized 
    Blockscout for multiple chains and understand how to adapt it for DAG 
    structures.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write, dir_read],  # github_search removed
    llm=llm
)

frontend_developer = Agent(
    role="React/TypeScript Frontend Developer",
    goal="Build DAG visualization and modern UI for the explorer",
    backstory="""You are a frontend expert specializing in React, TypeScript, 
    and data visualization. You've built complex blockchain explorers and know 
    how to visualize DAG structures using libraries like D3.js or vis.js.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write, dir_read],
    llm=llm
)

database_engineer = Agent(
    role="Database and Indexing Specialist",
    goal="Optimize database schema and indexing for DAG structure",
    backstory="""You are a PostgreSQL expert who understands blockchain data 
    models. You know how to efficiently index and query DAG structures, handle 
    high-volume writes, and optimize for explorer query patterns.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write],
    llm=llm
)

ui_ux_designer = Agent(
    role="UI/UX Designer",
    goal="Design intuitive and beautiful explorer interface",
    backstory="""You are a UI/UX designer with experience in blockchain 
    products. You understand how to make complex data accessible and create 
    interfaces that both technical and non-technical users can navigate 
    easily.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write],
    llm=llm
)

devops_engineer = Agent(
    role="DevOps and Infrastructure Engineer",
    goal="Set up deployment, monitoring, and scaling infrastructure",
    backstory="""You are a DevOps expert who has deployed Blockscout and 
    similar applications. You know Docker, Kubernetes, monitoring tools, 
    and how to ensure high availability for blockchain infrastructure.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read, file_write, dir_read],
    llm=llm
)

# ============================================================================
# TASKS
# ============================================================================

task_analyze_blockscout = Task(
    description="""Analyze Blockscout architecture and Phoenix requirements.
    
    1. Study Blockscout repository structure
    2. Read Phoenix explorer specifications in docs/specs/
    3. Identify customization points needed for DAG support
    4. Create CUSTOMIZATION_PLAN.md with:
       - Required Blockscout modifications
       - DAG-specific features to add
       - API endpoints needed
       - Database schema changes
    """,
    agent=elixir_developer,
    expected_output="Detailed customization plan for Blockscout adaptation"
)

task_fork_blockscout = Task(
    description="""Fork and set up Blockscout for Phoenix.
    
    1. Fork Blockscout v5.3.0 (latest stable)
    2. Update configuration for Phoenix Network:
       - Network name and branding
       - Chain ID and network parameters
       - RPC endpoint configuration
    3. Set up development environment:
       - Docker compose configuration
       - Environment variables
       - Database setup
    4. Verify basic compilation and startup
    """,
    agent=elixir_developer,
    expected_output="Forked and configured Blockscout instance",
    context=[task_analyze_blockscout]
)

task_database_schema = Task(
    description="""Design and implement DAG-optimized database schema.
    
    1. Extend Blockscout schema for DAG structure:
       - Add parent_blocks table for multiple parents
       - Add blue_score and DAG-specific fields
       - Create canonical_chain view
    2. Design efficient indexes for:
       - DAG traversal queries
       - Blue/red block filtering
       - Canonical chain queries
    3. Create migration scripts
    4. Document schema in DATABASE_SCHEMA.md
    """,
    agent=database_engineer,
    expected_output="DAG-optimized database schema with migrations",
    context=[task_fork_blockscout]
)

task_dag_visualization = Task(
    description="""Build DAG visualization component.
    
    1. Create React component for DAG visualization:
       - Use D3.js or vis.js for graph rendering
       - Show block relationships and paths
       - Color code blue/red blocks
       - Interactive zoom and navigation
    2. Integrate with Blockscout frontend:
       - Add DAG view tab
       - Link from block details
       - Real-time updates via WebSocket
    3. Optimize performance for large graphs
    4. Create responsive mobile view
    """,
    agent=frontend_developer,
    expected_output="Interactive DAG visualization component",
    context=[task_database_schema]
)

task_phoenix_api = Task(
    description="""Implement Phoenix-specific API endpoints.
    
    1. Add DAG-specific endpoints:
       - /api/dag/tips - Current DAG tips
       - /api/dag/blue-blocks - Blue block list
       - /api/dag/canonical - Canonical chain
       - /api/dag/graph/:block - DAG subgraph around block
    2. Extend existing endpoints:
       - Add DAG fields to block responses
       - Include blue score and confirmation data
    3. Implement efficient caching
    4. Add API documentation
    """,
    agent=elixir_developer,
    expected_output="Phoenix-specific API endpoints implementation",
    context=[task_dag_visualization]
)

task_ui_design = Task(
    description="""Design Phoenix explorer user interface.
    
    1. Create design mockups:
       - Homepage with network stats
       - Block explorer with DAG view
       - Transaction details
       - Address pages
       - Mining statistics
    2. Design Phoenix branding integration
    3. Create responsive layouts
    4. Design dark/light theme
    5. Create UI component library
    """,
    agent=ui_ux_designer,
    expected_output="Complete UI design system and mockups",
    context=[task_phoenix_api]
)

task_deployment_setup = Task(
    description="""Set up production deployment infrastructure.
    
    1. Create Docker configuration:
       - Multi-stage Dockerfile
       - docker-compose.yml for services
       - Environment configuration
    2. Set up Kubernetes manifests:
       - Deployment configurations
       - Service definitions
       - Ingress rules
    3. Configure monitoring:
       - Prometheus metrics
       - Grafana dashboards
       - Log aggregation
    4. Create deployment scripts
    5. Document in DEPLOYMENT.md
    """,
    agent=devops_engineer,
    expected_output="Production-ready deployment configuration",
    context=[task_ui_design]
)

task_integration_testing = Task(
    description="""Comprehensive integration testing.
    
    1. Test Phoenix node integration:
       - RPC connection
       - Block indexing
       - Real-time updates
    2. Test DAG visualization:
       - Large graph performance
       - Real-time updates
       - Mobile responsiveness
    3. API testing:
       - Endpoint validation
       - Performance benchmarks
       - Error handling
    4. Create test documentation
    """,
    agent=elixir_developer,
    expected_output="Complete test suite with passing tests",
    context=[task_deployment_setup]
)

# ============================================================================
# CREW
# ============================================================================

phoenix_explorer_crew = Crew(
    agents=[
        elixir_developer,
        frontend_developer,
        database_engineer,
        ui_ux_designer,
        devops_engineer
    ],
    tasks=[
        task_analyze_blockscout,
        task_fork_blockscout,
        task_database_schema,
        task_dag_visualization,
        task_phoenix_api,
        task_ui_design,
        task_deployment_setup,
        task_integration_testing
    ],
    process=Process.sequential,
    verbose=True,
    memory=True,
    cache=True,
    output_log_file="logs/phoenix_explorer_crew.log"
)

# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PHOENIX EXPLORER DEVELOPMENT CREW")
    print("=" * 70)
    print("\nStarting Blockscout customization for Phoenix Network...")
    print(f"Using LLM: {'Claude' if USE_CLAUDE else 'GPT-4'}")
    print(f"Workspace: {WORKSPACE}\n")
    
    result = phoenix_explorer_crew.kickoff()
    
    print("\n" + "=" * 70)
    print("EXPLORER CREW EXECUTION COMPLETE")
    print("=" * 70)
    print("\nResults:", result)
