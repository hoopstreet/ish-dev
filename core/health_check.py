import subprocess
import time
import os
import sys

# Try to import supabase, if missing, log to console
try:
    from supabase import create_client
except ImportError:
    print("⚠️ Supabase library missing. Running in limited health mode.")

# Configuration
URL = "https://ixdukafvxqermhgoczou.supabase.co/"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M iOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91 Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3M iwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1 LF3RJnQNacBc-dHk"

def heal():
    print("🛡️ [v2.2.0] Checking System Vitals...")
    
    # Check processes using 'ps'
    try:
        ps_output = subprocess.check_output(["ps", "-w"]).decode()
    except:
        ps_output = ""

    # 1. Restart Bot if offline
    if "bot.py" not in ps_output:
        print("🚑 Bot Offline. Restarting...")
        subprocess.Popen(["python3", "/root/Ai-Coder/bot.py"])

    # 2. Restart Sentinel if offline
    if "sentinel.py" not in ps_output:
        print("🚑 Sentinel Offline. Restarting...")
        subprocess.Popen(["python3", "/root/Ai-Coder/core/sentinel.py"])

if __name__ == "__main__":
    while True:
        heal()
        time.sleep(300)
