"""
Deploy Crew - Main deployment script for all Phoenix crews

Usage:
    python deploy_crew.py --crew phoenix-node
    python deploy_crew.py --deploy-all
    python deploy_crew.py --crew phoenix-node --phase 1
"""

import argparse
import sys
import os
from pathlib import Path

# Add crews directory to path
sys.path.append(str(Path(__file__).parent))

def deploy_phoenix_node():
    """Deploy Phoenix Node development crew"""
    print("\n🚀 Deploying Phoenix Node Crew...")
    
    from crews.phoenix_node_crew import phoenix_node_crew
    
    try:
        result = phoenix_node_crew.kickoff()
        print("\n✅ Phoenix Node Crew completed successfully!")
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def deploy_phoenix_sdk_js():
    """Deploy Phoenix SDK JS development crew (minimal MVP version)"""
    print("\n🚀 Deploying Phoenix SDK JS Crew (Minimal)...")
    
    from crews.phoenix_sdk_minimal import phoenix_sdk_minimal_crew
    
    try:
        result = phoenix_sdk_minimal_crew.kickoff()
        print("\n✅ Phoenix SDK JS Crew completed successfully!")
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def deploy_phoenix_explorer():
    """Deploy Phoenix Explorer development crew (minimal MVP version)"""
    print("\n🚀 Deploying Phoenix Explorer Crew (Minimal)...")
    
    from crews.phoenix_explorer_minimal import phoenix_explorer_minimal_crew
    
    try:
        result = phoenix_explorer_minimal_crew.kickoff()
        print("\n✅ Phoenix Explorer Crew completed successfully!")
        return result
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def deploy_phoenix_docs():
    """Deploy Phoenix Documentation crew"""
    print("\n🚀 Deploying Phoenix Docs Crew...")
    print("⚠️  Not yet implemented - create crews/phoenix_docs_crew.py")
    return None

CREWS = {
    "phoenix-node": deploy_phoenix_node,
    "phoenix-sdk-js": deploy_phoenix_sdk_js,
    "phoenix-explorer": deploy_phoenix_explorer,
    "phoenix-docs": deploy_phoenix_docs,
    # Add more as you implement them
}

def main():
    parser = argparse.ArgumentParser(
        description="Deploy AI crews to develop Phoenix repositories"
    )
    parser.add_argument(
        "--crew",
        choices=list(CREWS.keys()),
        help="Specific crew to deploy"
    )
    parser.add_argument(
        "--deploy-all",
        action="store_true",
        help="Deploy all crews"
    )
    parser.add_argument(
        "--phase",
        type=int,
        help="Deploy specific phase only (1-3)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without deploying"
    )
    
    args = parser.parse_args()
    
    # Validate .env exists
    if not os.path.exists(".env"):
        print("❌ Error: .env file not found")
        print("Create .env file with your API keys:")
        print("  ANTHROPIC_API_KEY=your-key-here")
        print("  GITHUB_TOKEN=your-token-here (optional)")
        sys.exit(1)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY not set in .env")
        print("Get your API key from: https://console.anthropic.com/")
        sys.exit(1)
    
    print("=" * 70)
    print("Phoenix Crew Deployment System")
    print("=" * 70)
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No crews will be deployed\n")
    
    if args.deploy_all:
        print("\n📦 Deploying all crews...\n")
        for crew_name, deploy_func in CREWS.items():
            if args.dry_run:
                print(f"Would deploy: {crew_name}")
            else:
                print(f"\n{'='*70}")
                print(f"Deploying: {crew_name}")
                print(f"{'='*70}")
                result = deploy_func()
                if result:
                    print(f"✅ {crew_name} completed")
                else:
                    print(f"⚠️  {crew_name} not implemented or failed")
    
    elif args.crew:
        crew_name = args.crew
        deploy_func = CREWS[crew_name]
        
        if args.dry_run:
            print(f"\nWould deploy: {crew_name}")
            print(f"Phase: {args.phase if args.phase else 'All'}")
        else:
            print(f"\n{'='*70}")
            print(f"Deploying: {crew_name}")
            if args.phase:
                print(f"Phase: {args.phase}")
            print(f"{'='*70}\n")
            
            result = deploy_func()
            
            if result:
                print(f"\n✅ {crew_name} deployment complete!")
            else:
                print(f"\n⚠️  {crew_name} deployment failed or not implemented")
    
    else:
        parser.print_help()
        print("\nAvailable crews:")
        for crew_name in CREWS.keys():
            print(f"  - {crew_name}")
        print("\nExample usage:")
        print("  python deploy_crew.py --crew phoenix-node")
        print("  python deploy_crew.py --deploy-all")
        print("  python deploy_crew.py --crew phoenix-node --dry-run")

if __name__ == "__main__":
    main()






