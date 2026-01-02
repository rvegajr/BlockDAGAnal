#!/usr/bin/env python3
"""
Phoenix Network - Quick Swarm Deployment Script
===============================================
Simplified script to deploy the CrewAI swarm for parallel development.
"""

import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Import the orchestrator
from swarm_orchestrator import SwarmOrchestrator, Priority, COMPONENTS

# ============================================================================
# ANSI Color Codes
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================================
# DEPLOYMENT FUNCTIONS
# ============================================================================

def print_banner():
    """Print the Phoenix Network banner"""
    banner = f"""
{Colors.CYAN}{'='*80}
{Colors.BOLD}🔥 PHOENIX NETWORK - CREWAI SWARM DEPLOYMENT 🔥{Colors.ENDC}
{Colors.CYAN}{'='*80}{Colors.ENDC}

{Colors.GREEN}Building the future of DAG blockchain with AI-powered development{Colors.ENDC}
    """
    print(banner)

def check_environment():
    """Check environment setup"""
    print(f"\n{Colors.BLUE}Checking environment...{Colors.ENDC}")
    
    issues = []
    
    # Check API keys
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        issues.append("❌ No API keys found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")
    else:
        if os.getenv("ANTHROPIC_API_KEY"):
            print(f"{Colors.GREEN}✅ Claude API key found{Colors.ENDC}")
        if os.getenv("OPENAI_API_KEY"):
            print(f"{Colors.GREEN}✅ OpenAI API key found{Colors.ENDC}")
    
    # Check workspace directories
    workspace_base = "/Users/admin/Dev/Crypto/phoenix-workspace"
    if not os.path.exists(workspace_base):
        issues.append(f"❌ Workspace not found: {workspace_base}")
    else:
        print(f"{Colors.GREEN}✅ Workspace found{Colors.ENDC}")
    
    # Check log directory
    log_dir = Path(__file__).parent / "logs"
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"{Colors.GREEN}✅ Created logs directory{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}✅ Logs directory exists{Colors.ENDC}")
    
    if issues:
        print(f"\n{Colors.RED}Environment issues found:{Colors.ENDC}")
        for issue in issues:
            print(f"  {issue}")
        return False
    
    return True

def show_status():
    """Show current status of all components"""
    print(f"\n{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}COMPONENT STATUS{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*80}{Colors.ENDC}")
    
    # Group by priority
    priorities = {}
    for name, comp in COMPONENTS.items():
        if comp.priority not in priorities:
            priorities[comp.priority] = []
        priorities[comp.priority].append(comp)
    
    # Display by priority
    for priority in sorted(priorities.keys(), key=lambda x: x.value):
        print(f"\n{Colors.CYAN}{priority.name} Components:{Colors.ENDC}")
        for comp in priorities[priority]:
            status_icon = "✅" if comp.completion_percentage >= 90 else "🔧" if comp.completion_percentage > 0 else "⚠️"
            status_color = Colors.GREEN if comp.completion_percentage >= 90 else Colors.WARNING if comp.completion_percentage > 0 else Colors.RED
            print(f"  {status_icon} {comp.name:25} {status_color}[{comp.completion_percentage:3}%]{Colors.ENDC} - {comp.estimated_hours}h estimated")

def deploy_phase(phase: Priority, orchestrator: SwarmOrchestrator, dry_run: bool = False):
    """Deploy a specific phase"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Deploying {phase.name} Components{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
    
    # Get components for this phase
    phase_components = [
        comp for comp in COMPONENTS.values() 
        if comp.priority == phase and comp.completion_percentage < 90
    ]
    
    if not phase_components:
        print(f"{Colors.GREEN}✅ No components to deploy in {phase.name}{Colors.ENDC}")
        return
    
    print(f"\nComponents to deploy:")
    for comp in phase_components:
        print(f"  • {comp.name} ({comp.estimated_hours}h)")
    
    if dry_run:
        print(f"\n{Colors.WARNING}DRY RUN - Skipping actual deployment{Colors.ENDC}")
        return
    
    # Deploy
    print(f"\n{Colors.GREEN}Starting deployment...{Colors.ENDC}")
    orchestrator.run_swarm(phases=[phase])

def interactive_menu():
    """Interactive deployment menu"""
    while True:
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}DEPLOYMENT OPTIONS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print("\n1. Show component status")
        print("2. Deploy P0 (Critical) components")
        print("3. Deploy P1 (High) components")
        print("4. Deploy P2 (Medium) components")
        print("5. Deploy P3 (Low) components")
        print("6. Deploy all phases")
        print("7. Monitor progress (real-time)")
        print("8. Generate report")
        print("9. Exit")
        
        choice = input(f"\n{Colors.BOLD}Select option (1-9): {Colors.ENDC}")
        
        if choice == "1":
            show_status()
        elif choice == "2":
            orchestrator = SwarmOrchestrator(max_parallel_crews=3)
            deploy_phase(Priority.P0_CRITICAL, orchestrator)
        elif choice == "3":
            orchestrator = SwarmOrchestrator(max_parallel_crews=5)
            deploy_phase(Priority.P1_HIGH, orchestrator)
        elif choice == "4":
            orchestrator = SwarmOrchestrator(max_parallel_crews=3)
            deploy_phase(Priority.P2_MEDIUM, orchestrator)
        elif choice == "5":
            orchestrator = SwarmOrchestrator(max_parallel_crews=2)
            deploy_phase(Priority.P3_LOW, orchestrator)
        elif choice == "6":
            orchestrator = SwarmOrchestrator(max_parallel_crews=5)
            orchestrator.run_swarm()
        elif choice == "7":
            orchestrator = SwarmOrchestrator()
            try:
                orchestrator.monitor_progress()
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Monitoring stopped{Colors.ENDC}")
        elif choice == "8":
            orchestrator = SwarmOrchestrator()
            orchestrator.generate_report()
        elif choice == "9":
            print(f"\n{Colors.GREEN}Goodbye! 🔥{Colors.ENDC}")
            break
        else:
            print(f"{Colors.RED}Invalid option{Colors.ENDC}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Deploy Phoenix Network CrewAI Swarm")
    parser.add_argument("--quick", action="store_true", help="Quick deployment of critical components")
    parser.add_argument("--all", action="store_true", help="Deploy all components")
    parser.add_argument("--phase", choices=["P0", "P1", "P2", "P3"], help="Deploy specific phase")
    parser.add_argument("--status", action="store_true", help="Show component status")
    parser.add_argument("--dry-run", action="store_true", help="Simulation mode")
    parser.add_argument("--max-crews", type=int, default=5, help="Maximum parallel crews")
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check environment
    if not check_environment():
        print(f"\n{Colors.RED}Please fix environment issues before proceeding{Colors.ENDC}")
        sys.exit(1)
    
    # Handle command-line options
    if args.status:
        show_status()
    elif args.quick:
        print(f"\n{Colors.GREEN}Quick deployment mode - P0 and P1 components{Colors.ENDC}")
        orchestrator = SwarmOrchestrator(max_parallel_crews=args.max_crews)
        deploy_phase(Priority.P0_CRITICAL, orchestrator, args.dry_run)
        deploy_phase(Priority.P1_HIGH, orchestrator, args.dry_run)
    elif args.all:
        print(f"\n{Colors.GREEN}Deploying all components{Colors.ENDC}")
        orchestrator = SwarmOrchestrator(max_parallel_crews=args.max_crews)
        if args.dry_run:
            print(f"{Colors.WARNING}DRY RUN MODE{Colors.ENDC}")
        orchestrator.run_swarm()
    elif args.phase:
        phase_map = {
            "P0": Priority.P0_CRITICAL,
            "P1": Priority.P1_HIGH,
            "P2": Priority.P2_MEDIUM,
            "P3": Priority.P3_LOW
        }
        phase = phase_map[args.phase]
        orchestrator = SwarmOrchestrator(max_parallel_crews=args.max_crews)
        deploy_phase(phase, orchestrator, args.dry_run)
    else:
        # Interactive menu
        interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Deployment cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)
