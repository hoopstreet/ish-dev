import sys
import os
import json
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
DNA_PATH = "/root/ish-dev/docs/DNA.md"
LOG_PATH = "/root/ish-dev/docs/logs.txt"

def log_evolution(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DNA_PATH, "a") as f:
        f.write(f"\n[{timestamp}] [GENESIS-AGENT] {message}")
    with open(LOG_PATH, "a") as f:
        f.write(f"\n[{timestamp}] Agent Activity: {message}")

def run_cli():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 HOOPSTREET MASTER GEMINI AGENT v11.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("System: Online | Mode: Gemini-CLI Merge")
    
    while True:
        try:
            cmd = input("\n👉 Agent Command (or 'exit'): ").strip()
            if cmd.lower() in ['exit', 'quit', '0']:
                break
            
            # Here we wrap your task logic
            print(f"⚡ Processing: {cmd}")
            # Simulate Gemini interaction or trigger task engine
            os.system(f"task \"{cmd}\"")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    log_evolution("Master Agent v11.0 Initialized")
    run_cli()
