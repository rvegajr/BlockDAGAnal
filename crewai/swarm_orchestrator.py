"""
Phoenix Network - CrewAI Swarm Orchestrator
============================================
Master orchestration system for parallel development of all Phoenix components.

This orchestrator manages multiple specialized crews working in parallel to build
the entire Phoenix Network ecosystem.
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from enum import Enum

from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
    DirectoryReadTool,
    SerperDevTool
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/swarm_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

class Priority(Enum):
    """Component development priority levels"""
    P0_CRITICAL = 0  # Must have for testnet
    P1_HIGH = 1      # Essential for usability
    P2_MEDIUM = 2    # Important but not blocking
    P3_LOW = 3       # Nice to have

class ComponentStatus(Enum):
    """Current status of each component"""
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    STUB = "stub"
    NOT_STARTED = "not_started"

@dataclass
class Component:
    """Represents a Phoenix Network component"""
    name: str
    directory: str
    priority: Priority
    status: ComponentStatus
    dependencies: List[str] = field(default_factory=list)
    crew_file: Optional[str] = None
    agents_needed: List[str] = field(default_factory=list)
    estimated_hours: int = 0
    completion_percentage: int = 0

# ============================================================================
# COMPONENT REGISTRY
# ============================================================================

COMPONENTS = {
    "phoenix-node": Component(
        name="phoenix-node",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-node",
        priority=Priority.P0_CRITICAL,
        status=ComponentStatus.IN_PROGRESS,
        dependencies=[],
        crew_file="crews/phoenix_node_crew_claude.py",
        agents_needed=["go_developer", "consensus_engineer", "evm_specialist"],
        estimated_hours=40,
        completion_percentage=90
    ),
    "phoenix-explorer": Component(
        name="phoenix-explorer",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-explorer",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_explorer_crew.py",
        agents_needed=["elixir_developer", "frontend_developer", "ui_designer"],
        estimated_hours=60,
        completion_percentage=0
    ),
    "phoenix-sdk-js": Component(
        name="phoenix-sdk-js",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-sdk-js",
        priority=Priority.P0_CRITICAL,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_sdk_js_crew.py",
        agents_needed=["typescript_developer", "web3_expert"],
        estimated_hours=30,
        completion_percentage=10
    ),
    "phoenix-sdk-python": Component(
        name="phoenix-sdk-python",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-sdk-python",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_sdk_python_crew.py",
        agents_needed=["python_developer", "web3_expert"],
        estimated_hours=30,
        completion_percentage=0
    ),
    "phoenix-sdk-go": Component(
        name="phoenix-sdk-go",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-sdk-go",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_sdk_go_crew.py",
        agents_needed=["go_developer", "api_designer"],
        estimated_hours=30,
        completion_percentage=0
    ),
    "phoenix-wallet-mobile": Component(
        name="phoenix-wallet-mobile",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-wallet-mobile",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-sdk-js"],
        crew_file="crews/phoenix_wallet_mobile_crew.py",
        agents_needed=["react_native_developer", "mobile_ui_designer", "security_expert"],
        estimated_hours=80,
        completion_percentage=0
    ),
    "phoenix-wallet-extension": Component(
        name="phoenix-wallet-extension",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-wallet-extension",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-sdk-js"],
        crew_file="crews/phoenix_wallet_extension_crew.py",
        agents_needed=["extension_developer", "frontend_developer", "security_expert"],
        estimated_hours=60,
        completion_percentage=0
    ),
    "phoenix-pool": Component(
        name="phoenix-pool",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-pool",
        priority=Priority.P1_HIGH,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_pool_crew.py",
        agents_needed=["go_developer", "mining_expert", "protocol_engineer"],
        estimated_hours=50,
        completion_percentage=0
    ),
    "phoenix-devtools": Component(
        name="phoenix-devtools",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-devtools",
        priority=Priority.P2_MEDIUM,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-sdk-js"],
        crew_file="crews/phoenix_devtools_crew.py",
        agents_needed=["tooling_developer", "plugin_developer"],
        estimated_hours=40,
        completion_percentage=0
    ),
    "phoenix-infrastructure": Component(
        name="phoenix-infrastructure",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-infrastructure",
        priority=Priority.P2_MEDIUM,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-node"],
        crew_file="crews/phoenix_infrastructure_crew.py",
        agents_needed=["devops_engineer", "cloud_architect", "monitoring_specialist"],
        estimated_hours=30,
        completion_percentage=0
    ),
    "phoenix-website": Component(
        name="phoenix-website",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-website",
        priority=Priority.P3_LOW,
        status=ComponentStatus.STUB,
        dependencies=["phoenix-brand"],
        crew_file="crews/phoenix_website_crew.py",
        agents_needed=["nextjs_developer", "web_designer", "content_writer"],
        estimated_hours=40,
        completion_percentage=0
    ),
    "phoenix-brand": Component(
        name="phoenix-brand",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-brand",
        priority=Priority.P3_LOW,
        status=ComponentStatus.STUB,
        dependencies=[],
        crew_file="crews/phoenix_brand_crew.py",
        agents_needed=["brand_designer", "ui_ux_designer"],
        estimated_hours=20,
        completion_percentage=30
    ),
    "phoenix-docs": Component(
        name="phoenix-docs",
        directory="/Users/admin/Dev/Crypto/phoenix-workspace/phoenix-docs",
        priority=Priority.P0_CRITICAL,
        status=ComponentStatus.COMPLETE,
        dependencies=[],
        crew_file=None,
        agents_needed=[],
        estimated_hours=0,
        completion_percentage=100
    )
}

# ============================================================================
# SWARM ORCHESTRATOR
# ============================================================================

class SwarmOrchestrator:
    """Manages multiple CrewAI crews working in parallel"""
    
    def __init__(self, max_parallel_crews: int = 5, use_claude: bool = True):
        self.components = COMPONENTS
        self.max_parallel_crews = max_parallel_crews
        self.use_claude = use_claude
        self.active_crews: Dict[str, Any] = {}
        self.completed_components: List[str] = []
        self.failed_components: List[str] = []
        self.start_time = datetime.now()
        
        # Initialize LLM based on preference
        if use_claude:
            from langchain_anthropic import ChatAnthropic
            # Allow model to be configured via environment variable
            claude_model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
            self.llm = ChatAnthropic(
                model=claude_model,
                temperature=0.1,
                max_tokens=4000,
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.1,
                max_tokens=4000,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def get_ready_components(self) -> List[Component]:
        """Get components ready for development (dependencies met)"""
        ready = []
        for name, component in self.components.items():
            if component.status in [ComponentStatus.STUB, ComponentStatus.NOT_STARTED]:
                # Check if all dependencies are complete
                deps_ready = all(
                    self.components[dep].status == ComponentStatus.COMPLETE
                    or self.components[dep].completion_percentage >= 80
                    for dep in component.dependencies
                )
                if deps_ready and name not in self.active_crews:
                    ready.append(component)
        # Sort by priority
        return sorted(ready, key=lambda x: (x.priority.value, -x.estimated_hours))
    
    def deploy_crew(self, component: Component) -> Optional[Any]:
        """Deploy a crew for a specific component"""
        try:
            logger.info(f"Deploying crew for {component.name} (Priority: {component.priority.name})")
            
            # Import and execute the crew module dynamically
            if component.crew_file and os.path.exists(f"/Users/admin/Dev/Crypto/BlockDAG/crewai/{component.crew_file}"):
                import importlib.util
                spec = importlib.util.spec_from_file_location(
                    f"{component.name}_crew",
                    f"/Users/admin/Dev/Crypto/BlockDAG/crewai/{component.crew_file}"
                )
                crew_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(crew_module)
                
                # Get the crew instance
                crew = getattr(crew_module, f"{component.name.replace('-', '_')}_crew", None)
                if crew:
                    self.active_crews[component.name] = crew
                    return crew
                else:
                    logger.warning(f"No crew found in {component.crew_file}")
                    return None
            else:
                logger.warning(f"Crew file not found for {component.name}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to deploy crew for {component.name}: {str(e)}")
            self.failed_components.append(component.name)
            return None
    
    def execute_crew(self, component: Component, crew: Any) -> Dict[str, Any]:
        """Execute a crew and return results"""
        try:
            logger.info(f"Executing crew for {component.name}")
            result = crew.kickoff()
            
            # Update component status
            component.status = ComponentStatus.IN_PROGRESS
            component.completion_percentage = min(component.completion_percentage + 20, 100)
            
            return {
                "component": component.name,
                "status": "success",
                "result": result,
                "completion": component.completion_percentage
            }
        except Exception as e:
            logger.error(f"Crew execution failed for {component.name}: {str(e)}")
            return {
                "component": component.name,
                "status": "failed",
                "error": str(e),
                "completion": component.completion_percentage
            }
    
    def run_swarm(self, phases: List[Priority] = None):
        """Run the swarm orchestrator"""
        if phases is None:
            phases = [Priority.P0_CRITICAL, Priority.P1_HIGH, Priority.P2_MEDIUM, Priority.P3_LOW]
        
        logger.info("=" * 80)
        logger.info("PHOENIX NETWORK - CREWAI SWARM ORCHESTRATOR")
        logger.info("=" * 80)
        logger.info(f"Starting swarm with {len(self.components)} components")
        logger.info(f"Max parallel crews: {self.max_parallel_crews}")
        logger.info(f"Using LLM: {'Claude' if self.use_claude else 'GPT-4'}")
        logger.info("=" * 80)
        
        for phase in phases:
            logger.info(f"\n{'='*60}")
            logger.info(f"PHASE: {phase.name}")
            logger.info(f"{'='*60}")
            
            # Get components for this phase
            phase_components = [
                c for c in self.components.values() 
                if c.priority == phase and c.status != ComponentStatus.COMPLETE
            ]
            
            if not phase_components:
                logger.info(f"No components to process in {phase.name}")
                continue
            
            # Process components in parallel
            with ThreadPoolExecutor(max_workers=self.max_parallel_crews) as executor:
                futures = {}
                
                for component in phase_components:
                    # Check if dependencies are met
                    ready_components = self.get_ready_components()
                    if component in ready_components:
                        crew = self.deploy_crew(component)
                        if crew:
                            future = executor.submit(self.execute_crew, component, crew)
                            futures[future] = component
                
                # Process completed futures
                for future in as_completed(futures):
                    component = futures[future]
                    result = future.result()
                    
                    if result["status"] == "success":
                        logger.info(f"✅ {component.name} - Progress: {result['completion']}%")
                        if result["completion"] >= 100:
                            self.completed_components.append(component.name)
                            component.status = ComponentStatus.COMPLETE
                    else:
                        logger.error(f"❌ {component.name} - Failed: {result.get('error', 'Unknown error')}")
                        self.failed_components.append(component.name)
                    
                    # Remove from active crews
                    if component.name in self.active_crews:
                        del self.active_crews[component.name]
        
        # Final report
        self.generate_report()
    
    def generate_report(self):
        """Generate final execution report"""
        elapsed_time = datetime.now() - self.start_time
        
        report = f"""
{"="*80}
PHOENIX NETWORK SWARM EXECUTION REPORT
{"="*80}

Execution Time: {elapsed_time}
Total Components: {len(self.components)}
Completed: {len(self.completed_components)}
Failed: {len(self.failed_components)}
In Progress: {len([c for c in self.components.values() if c.status == ComponentStatus.IN_PROGRESS])}

COMPONENT STATUS:
{"="*80}
"""
        for name, component in sorted(self.components.items(), key=lambda x: x[1].priority.value):
            status_icon = "✅" if component.status == ComponentStatus.COMPLETE else "🔧" if component.status == ComponentStatus.IN_PROGRESS else "⚠️"
            report += f"{status_icon} {name:30} | Priority: {component.priority.name:12} | Progress: {component.completion_percentage:3}%\n"
        
        report += f"""
{"="*80}
NEXT STEPS:
1. Review completed components in their respective directories
2. Run integration tests between components
3. Deploy failed components individually for debugging
4. Monitor crew logs in logs/crew_*.log files
{"="*80}
"""
        
        logger.info(report)
        
        # Save report to file
        with open("logs/swarm_execution_report.txt", "w") as f:
            f.write(report)
    
    def monitor_progress(self):
        """Real-time monitoring dashboard"""
        import curses
        
        def draw_dashboard(stdscr):
            curses.curs_set(0)
            stdscr.clear()
            
            while True:
                stdscr.addstr(0, 0, "PHOENIX NETWORK - SWARM MONITOR", curses.A_BOLD)
                stdscr.addstr(1, 0, "=" * 80)
                
                row = 3
                for name, component in self.components.items():
                    status_char = "✓" if component.status == ComponentStatus.COMPLETE else "→" if component.status == ComponentStatus.IN_PROGRESS else "·"
                    progress_bar = "█" * (component.completion_percentage // 10) + "░" * (10 - component.completion_percentage // 10)
                    
                    stdscr.addstr(row, 0, f"{status_char} {name:25} [{progress_bar}] {component.completion_percentage:3}%")
                    row += 1
                
                stdscr.addstr(row + 2, 0, f"Active Crews: {len(self.active_crews)}")
                stdscr.addstr(row + 3, 0, f"Completed: {len(self.completed_components)}")
                stdscr.addstr(row + 4, 0, f"Failed: {len(self.failed_components)}")
                
                stdscr.refresh()
                curses.napms(1000)  # Update every second
        
        try:
            curses.wrapper(draw_dashboard)
        except KeyboardInterrupt:
            pass

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for the swarm orchestrator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Phoenix Network CrewAI Swarm Orchestrator")
    parser.add_argument("--max-crews", type=int, default=5, help="Maximum parallel crews")
    parser.add_argument("--use-claude", action="store_true", help="Use Claude instead of GPT-4")
    parser.add_argument("--monitor", action="store_true", help="Launch monitoring dashboard")
    parser.add_argument("--phases", nargs="+", choices=["P0", "P1", "P2", "P3"], 
                      help="Specific phases to run")
    parser.add_argument("--dry-run", action="store_true", help="Simulation mode without actual execution")
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = SwarmOrchestrator(
        max_parallel_crews=args.max_crews,
        use_claude=args.use_claude
    )
    
    # Parse phases
    phases = None
    if args.phases:
        phase_map = {
            "P0": Priority.P0_CRITICAL,
            "P1": Priority.P1_HIGH,
            "P2": Priority.P2_MEDIUM,
            "P3": Priority.P3_LOW
        }
        phases = [phase_map[p] for p in args.phases]
    
    # Run or monitor
    if args.monitor:
        orchestrator.monitor_progress()
    elif args.dry_run:
        logger.info("DRY RUN MODE - Simulating execution")
        ready = orchestrator.get_ready_components()
        logger.info(f"Ready components: {[c.name for c in ready]}")
    else:
        orchestrator.run_swarm(phases=phases)

if __name__ == "__main__":
    main()
