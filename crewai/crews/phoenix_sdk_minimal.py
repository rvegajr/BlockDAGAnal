"""
Phoenix SDK Minimal Crew - MVP Version

This crew creates a minimal JavaScript SDK (100 lines max) that wraps ethers.js
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
WORKSPACE = "../phoenix-workspace/phoenix-sdk-js"

# Initialize tools
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()

# ============================================================================
# AGENTS (Minimal - Just 2 agents)
# ============================================================================

typescript_dev = Agent(
    role="TypeScript SDK Developer",
    goal="Create minimal Phoenix SDK that wraps ethers.js",
    backstory="""You are an expert TypeScript developer who specializes in 
    creating minimal, efficient SDKs. You understand ethers.js deeply and can 
    create a simple wrapper that works with Phoenix RPC endpoints.""",
    verbose=True,
    allow_delegation=False,
    tools=[file_read_tool, file_writer_tool],
    llm=llm
)

# ============================================================================
# TASKS (Minimal - Just 3 tasks)
# ============================================================================

task_provider = Task(
    description="""Create a minimal provider that connects to Phoenix RPC.
    
    Requirements:
    - Wrap ethers.JsonRpcProvider
    - Default endpoint: http://localhost:8545
    - Support custom RPC URLs
    
    Output: src/provider.ts (max 30 lines)""",
    agent=typescript_dev,
    expected_output="Provider class that connects to Phoenix RPC"
)

task_wallet = Task(
    description="""Create minimal wallet utilities.
    
    Requirements:
    - Re-export ethers.Wallet
    - Add Phoenix-specific helpers if needed
    
    Output: src/wallet.ts (max 20 lines)""",
    agent=typescript_dev,
    expected_output="Wallet utilities",
    context=[task_provider]
)

task_contract = Task(
    description="""Create minimal contract interaction.
    
    Requirements:
    - Re-export ethers.Contract
    - Ensure compatibility with Phoenix
    
    Output: src/contract.ts (max 20 lines)""",
    agent=typescript_dev,
    expected_output="Contract interaction utilities",
    context=[task_wallet]
)

# ============================================================================
# CREW
# ============================================================================

phoenix_sdk_minimal_crew = Crew(
    agents=[typescript_dev],
    tasks=[task_provider, task_wallet, task_contract],
    process=Process.sequential,
    verbose=True,
    memory=True,
    cache=True,
)

if __name__ == "__main__":
    print("=" * 70)
    print("Phoenix SDK Minimal Crew - MVP Version")
    print("=" * 70)
    result = phoenix_sdk_minimal_crew.kickoff()
    print(result)

