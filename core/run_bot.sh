#!/bin/sh
cd /root/Ai-Coder
export PYTHONPATH=$PYTHONPATH:/root/Ai-Coder

python3 - << 'PYEOF'
import os
def load_env():
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()

# Map your .env names to what the bot expects
if "TELEGRAM_BOT_TOKEN" in os.environ:
    os.environ["TELEGRAM_TOKEN"] = os.environ["TELEGRAM_BOT_TOKEN"]

if not os.environ.get("TELEGRAM_TOKEN"):
    print("❌ ERROR: TELEGRAM_TOKEN or TELEGRAM_BOT_TOKEN not found in .env")
    exit(1)

print(f"✅ Environment Loaded. Starting Bot...")
os.system("python3 /root/Ai-Coder/bot/main.py")
PYEOF
