"""
Phoenix Explorer Minimal Crew - MVP Version

This crew forks Blockscout and makes minimal configuration changes
"""

from crewai import Agent, Task, Crew, Process
from langchain_anthropic import ChatAnthropic
from crewai_tools import FileReadTool, FileWriterTool
import os

# Initialize Claude LLM
llm = ChatAnthropic(
    model="claude-3-opus-20240229",
    temperature=0.1,
    max_tokens=4000,
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Define workspace
WORKSPACE = "../phoenix-workspace/phoenix-explorer"

# Initialize tools
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()

# ============================================================================
# AGENTS (Minimal - Just 1 agent)
# ============================================================================

explorer_dev = Agent(
    role="Block Explorer Developer",
    goal="Fork Blockscout and configure for Phoenix",
    backstory="""You are an expert in block explorers, particularly Blockscout. 
    You can quickly configure Blockscout to work with new blockchain networks 
    by updating configuration files.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool, file_writer_tool],
    llm=llm
)

# ============================================================================
# TASKS (Minimal - Just 2 tasks)
# ============================================================================

task_fork_blockscout = Task(
    description="""Fork Blockscout repository and set up for Phoenix.
    
    Steps:
    1. Clone Blockscout from https://github.com/blockscout/blockscout
    2. Update configuration files:
       - Change chain name to "Phoenix"
       - Update RPC endpoint to Phoenix RPC
       - Update chain ID to 888
    3. Update branding (minimal - just name changes)
    
    Output: Configured Blockscout instance""",
    agent=explorer_dev,
    expected_output="Blockscout configured for Phoenix network"
)

task_update_config = Task(
    description="""Update Blockscout configuration for Phoenix.
    
    Update:
    - config/chains/phoenix.json
    - Docker configuration
    - Environment variables
    
    Output: Working explorer configuration""",
    agent=explorer_dev,
    expected_output="Phoenix-specific configuration files",
    context=[task_fork_blockscout]
)

# ============================================================================
# CREW
# ============================================================================

phoenix_explorer_minimal_crew = Crew(
    agents=[explorer_dev],
    tasks=[task_fork_blockscout, task_update_config],
    process=Process.sequential,
    verbose=True,
    memory=True,
    cache=True,
)

if __name__ == "__main__":
    print("=" * 70)
    print("Phoenix Explorer Minimal Crew - MVP Version")
    print("=" * 70)
    result = phoenix_explorer_minimal_crew.kickoff()
    print(result)

