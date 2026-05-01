#!/usr/bin/env python3
import os
import sys

# Use your NEW key here
os.environ['OPENROUTER_API_KEY'] = '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'

from or_agent import HealingAgent

agent = HealingAgent()

print("="*50)
print("Fixing broken.py")
print("="*50)

# Show current code
print("\nCurrent code:")
with open('/root/broken.py', 'r') as f:
    print(f.read())

# Attempt to fix
print("\nAttempting to fix...")
result = agent.heal('/root/broken.py', max_attempts=1)

if result:
    print("\n✅ FIXED! New code:")
    with open('/root/broken.py', 'r') as f:
        print(f.read())
else:
    print("\n❌ Could not fix - check API key")
    
# Run tests
print("\nRunning tests:")
os.system('cd /root && python3 -m pytest test_broken.py -v 2>/dev/null || echo "Tests failed"')
