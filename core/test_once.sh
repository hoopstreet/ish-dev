#!/bin/sh
echo "Running one-time test and heal..."
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, '/root')
from agent import HealingAgent
agent = HealingAgent()
if agent.heal('broken.py'):
    print('✅ Successfully healed!')
else:
    print('❌ Could not heal')
"
