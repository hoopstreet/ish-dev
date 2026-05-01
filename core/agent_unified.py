#!/usr/bin/env python3
import sys, os, time, subprocess, re
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [AGENT] {msg}\n")

# Bundle command mappings
BUNDLE_COMMANDS = {
    # System commands
    "status": "/root/ish-dev/core/status.sh",
    "heal": "/root/ish-dev/core/heal.sh", 
    "sync": "/root/ish-dev/core/sync.sh",
    "menu": "/root/menu",
    
    # File operations
    "list files": "ls -la",
    "show structure": "ls -la /root/ish-dev",
    "show core": "ls -la /root/ish-dev/core",
    "show docs": "ls -la /root/ish-dev/docs",
    
    # Git commands
    "push": "cd /root/ish-dev && git add -A && git commit -m 'Update' && git push",
    "pull": "cd /root/ish-dev && git pull",
    "commit": "cd /root/ish-dev && git add -A && git commit -m 'Update'",
    
    # Python commands
    "install pip": "python3 -m ensurepip",
    "check python": "python3 --version",
    
    # System info
    "disk space": "df -h",
    "memory": "free -m",
    "time": "date",
    
    # Agent commands
    "help": "__HELP__",
    "stats": "__STATS__",
    "exit": "__EXIT__",
}

def show_help():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 AI AGENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 SYSTEM COMMANDS:
   status     - Show system status dashboard
   heal       - Run auto-heal engine
   sync       - Sync to GitHub with backup

🔹 FILE COMMANDS:
   list files     - List current directory
   show structure - Show project structure
   show core      - Show core scripts
   show docs      - Show documentation

🔹 GIT COMMANDS:
   push     - Commit and push to GitHub
   pull     - Pull latest from GitHub
   commit   - Commit changes only

🔹 INFO COMMANDS:
   disk space - Show disk usage
   memory     - Show memory usage
   time       - Show current time
   check python - Show Python version

🔹 AGENT COMMANDS:
   help   - Show this help
   stats  - Show agent statistics
   exit   - Return to main menu

📝 EXAMPLES:
   🤖 Agent > status
   🤖 Agent > show structure
   🤖 Agent > push
   🤖 Agent > disk space
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_banner():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 HOOPSTREET UNIFIED AI AGENT v3.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CAPABILITIES:")
    print(" • 🧠 Natural language bundle commands")
    print(" • 🔧 Auto-error detection and fixing")
    print(" • 💾 Learning from history")
    print(" • 📁 File system navigation")
    print(" • 🐙 Git operations")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n👉 Type 'help' for commands, 'exit' to quit")
    print("")

def show_stats():
    dna_lines = 0
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            dna_lines = len(f.readlines())
    log_lines = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_lines = len(f.readlines())
    
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 AGENT STATISTICS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   DNA.md lines: {dna_lines}")
    print(f"   Logs.txt entries: {log_lines}")
    print(f"   Agent version: 3.0")
    print(f"   Bundle commands: {len(BUNDLE_COMMANDS)}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def process_natural_language(text):
    """Convert natural language to commands"""
    text_lower = text.lower()

    
    # Check for bundle matches
    for keyword, command in BUNDLE_COMMANDS.items():
        if keyword in text_lower:
            if command == "__HELP__":
                return "help"
            elif command == "__STATS__":
                return "stats"
            elif command == "__EXIT__":
                return "exit"
            return command
    
    # Handle "show me the status" type phrases
    if "show" in text_lower and "status" in text_lower:
        return "/root/ish-dev/core/status.sh"
    if "fix" in text_lower or "repair" in text_lower:
        return "/root/ish-dev/core/heal.sh"
    if "sync" in text_lower or "push" in text_lower:
        return "cd /root/ish-dev && git add -A && git commit -m 'Update' && git push"
    
    # Return as-is for direct commands
    return text

def main():
    show_banner()
    
    while True:
        try:
            user_input = input("🤖 Agent > ").strip()
            
            if not user_input:
                continue
            
            # Process natural language
            command = process_natural_language(user_input)
            
            if command == "exit":
                print("\n🔙 Returning to main menu...")
                break
            elif command == "help":
                show_help()
            elif command == "stats":
                show_stats()
            else:
                log(f"Executing: {user_input} -> {command}")
                print(f"\n📌 Executing: {user_input}")
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                os.system(command)
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                
        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
