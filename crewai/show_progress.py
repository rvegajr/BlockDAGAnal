#!/usr/bin/env python3
import sys
sys.path.append('.')
from swarm_orchestrator import COMPONENTS
from datetime import datetime
import os

print("="*70)
print("🔥 PHOENIX SWARM - PROGRESS REPORT")
print("="*70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Check if swarm is running
if os.system("pgrep -f 'deploy_swarm' > /dev/null 2>&1") == 0:
    print("✅ Swarm Status: RUNNING")
else:
    print("⚠️  Swarm Status: NOT RUNNING")
print()

# Group by priority
priorities = {}
for name, comp in COMPONENTS.items():
    if comp.priority not in priorities:
        priorities[comp.priority] = []
    priorities[comp.priority].append(comp)

for priority in sorted(priorities.keys(), key=lambda x: x.value):
    print(f"{priority.name} Components:")
    for comp in sorted(priorities[priority], key=lambda x: x.name):
        status_icon = '✅' if comp.completion_percentage >= 90 else '🔧' if comp.completion_percentage > 0 else '⚠️'
        bar_length = int(comp.completion_percentage / 5)
        bar = '█' * bar_length + '░' * (20 - bar_length)
        print(f"  {status_icon} {comp.name:30} [{bar}] {comp.completion_percentage:3}%")
    print()

print("="*70)
