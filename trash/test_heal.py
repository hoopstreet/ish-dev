#!/usr/bin/env python3
import os
os.environ['OPENROUTER_API_KEY'] = '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'

from or_agent import HealingAgent
agent = HealingAgent()

print("="*50)
print("Testing self-healing agent")
print("="*50)

# Check broken.py before
print("\nBefore fix:")
with open('/root/broken.py', 'r') as f:
    print(f.read())

# Run the heal
print("\nAttempting to fix...")
result = agent.heal('/root/broken.py')

# Check after
print("\nAfter fix:")
with open('/root/broken.py', 'r') as f:
    print(f.read())

# Run tests
print("\nRunning final tests...")
os.system('cd /root && pytest test_broken.py -v')
