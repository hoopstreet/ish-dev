#!/usr/bin/env python3
import sys, os, time, subprocess
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [AGENT] {msg}\n")

def show_help():
    print("""
📚 AVAILABLE COMMANDS:
   • status   - Show system status
   • heal     - Run auto-heal
   • sync     - Sync to GitHub
   • stats    - Show agent statistics
   • help     - Show this help
   • exit     - Return to menu

📝 Examples:
   🤖 Agent > status
   🤖 Agent > heal
   🤖 Agent > sync
""")

def show_banner():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 HOOPSTREET UNIFIED AI AGENT v2.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CAPABILITIES:")
    print(" • 🧠 Natural language commands")
    print(" • 🔧 Auto-error detection")
    print(" • 💾 Learning from history")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n👇 Type 'help' for commands, 'exit' to quit")
    print("")

def main():
    show_banner()
    
    while True:
        try:
            cmd = input("🤖 Agent > ").strip().lower()
            
            if cmd in ['exit', 'quit']:
                print("\n🔙 Returning to main menu...")
                break
            elif cmd == 'help':
                show_help()
            elif cmd == 'status':
                log("Running status command")
                os.system("/root/ish-dev/core/status.sh")
            elif cmd == 'heal':
                log("Running heal command")
                os.system("/root/ish-dev/core/heal.sh")
            elif cmd == 'sync':
                log("Running sync command")
                os.system("/root/ish-dev/core/sync.sh")
            elif cmd == 'stats':
                dna_lines = 0
                if os.path.exists(DNA_FILE):
                    with open(DNA_FILE, 'r') as f:
                        dna_lines = len(f.readlines())
                log_lines = 0
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, 'r') as f:
                        log_lines = len(f.readlines())
                print(f"\n📊 AGENT STATISTICS:")
                print(f"   DNA.md lines: {dna_lines}")
                print(f"   Logs.txt entries: {log_lines}")
                print(f"   Agent version: 2.0")
            elif cmd == '':
                continue
            else:
                print(f"📌 Executing: {cmd}")
                log(f"Executing: {cmd}")
                os.system(cmd)
                
        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
