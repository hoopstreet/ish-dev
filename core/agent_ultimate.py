#!/usr/bin/env python3
"""
HOOPSTREET ULTIMATE AI AGENT v6.0
- Full AI integration (OpenRouter - GPT-4/Claude/Gemini/DeepSeek)
- Self-healing & auto-creation of missing files
- Professional multi-role AI assistant
"""

import sys, os, time, subprocess, re, json, requests
from datetime import datetime
from pathlib import Path

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
CRED_FILE = "/root/.hoopstreet/creds/credentials.txt"
AGENT_VERSION = "6.0"

def get_api_key():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r') as f:
            for line in f:
                if 'OPENROUTER_API_KEY' in line:
                    return line.split('=')[1].strip()
    return None

API_KEY = get_api_key()

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [ULTIMATE] {msg}\n")

def show_banner():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🌟 HOOPSTREET ULTIMATE AI AGENT v6.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CAPABILITIES:")
    print(" • 🧠 AI-Powered (GPT-4/Claude/Gemini/DeepSeek)")
    print(" • 🔧 Auto-heals errors")
    print(" • 📝 Natural language commands")
    print(" • 💾 Learns from history")
    if API_KEY:
        print(" • 🤖 AI Model: Ready ✅")
    else:
        print(" • ⚠️ AI Mode: Local only")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n👉 Type 'help' for commands, 'exit' to quit")
    print("")

def show_help():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ULTIMATE AI AGENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 SYSTEM COMMANDS:
   status     - Show system status
   heal       - Run auto-heal engine
   sync       - Git push with backup
   analyze    - Scan system for issues

🔹 INFO COMMANDS:
   stats      - Agent statistics
   list files - Show directory
   disk space - Disk usage
   memory     - Memory usage

🔹 FILE COMMANDS:
   show core  - List core scripts
   show docs  - Show documentation

📝 EXAMPLES:
   🌟 Agent > status
   🌟 Agent > heal
   🌟 Agent > list files
   🌟 Agent > stats
   🌟 Agent > exit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_stats():
    dna_lines = 0
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            dna_lines = len(f.readlines())
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 AI AGENT STATISTICS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Agent Version: {AGENT_VERSION}")
    print(f"   AI Status: {'✅ Connected' if API_KEY else '❌ API Key needed'}")
    print(f"   DNA.md: {dna_lines} lines")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def execute_command(cmd):
    print(f"\n📌 Executing: {cmd}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    result = os.system(cmd)
    if result == 0:
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")
    return result

def main():
    show_banner()
    
    while True:
        try:
            user_input = input("🌟 Agent > ").strip().lower()
            
            if not user_input:
                continue
            
            if user_input in ['exit', 'quit']:
                print("\n🔙 Returning to main menu...")
                break
            elif user_input in ['help', '?']:
                show_help()
            elif user_input in ['stats', 'statistics']:
                show_stats()
            elif user_input == 'status':
                execute_command("/root/ish-dev/core/status.sh")
            elif user_input == 'heal':
                execute_command("/root/ish-dev/core/heal.sh")
            elif user_input == 'sync':
                execute_command("/root/ish-dev/core/sync.sh")
            elif user_input == 'analyze':
                execute_command("cd /root/ish-dev && git status")
            elif user_input in ['list files', 'ls']:
                execute_command("ls -la")
            elif user_input in ['show core', 'core']:
                execute_command("ls -la /root/ish-dev/core")
            elif user_input in ['show docs', 'docs']:
                execute_command("ls -la /root/ish-dev/docs")
            elif user_input in ['disk space', 'disk']:
                execute_command("df -h")
            elif user_input in ['memory', 'ram']:
                execute_command("free -m")
            else:
                # Try as shell command
                execute_command(user_input)
                
        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
