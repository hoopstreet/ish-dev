import sys, os, time
from datetime import datetime

CONFIG = {
    "VERSION": "12.1-MASTER",
    "ROOT": "/root/ish-dev",
    "DNA": "/root/ish-dev/docs/DNA.md"
}

def execute(cmd, label):
    print(f"⚡ [Gemini CLI] Initiating {label}...")
    return os.system(cmd)

def main():
    os.system("clear")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🤖 HOOPSTREET MASTER GEMINI CLI v{CONFIG['VERSION']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("System Status: CONNECTED | GitHub: READY")
    
    while True:
        cmd = input("\n👉 Command: ").strip().lower()
        if cmd in ['exit', '0', 'quit']: break
        
        # Priority 1: GitHub & Merge Logic
        if "sync" in cmd or "push" in cmd or "merge" in cmd:
            execute("sh /root/ish-dev/core/sync.sh", "GitHub Sync")
        
        # Priority 2: Recovery & Heal
        elif "fix" in cmd or "heal" in cmd or "recover" in cmd:
            execute("sh /root/ish-dev/core/heal.sh", "System Recovery")
            
        # Priority 3: Adoption of New Files
        elif "adopt" in cmd or "upgrade" in cmd:
            print("🚀 Adopting new mutations and merging history...")
            execute("git pull origin main", "Adoption")
            
        else:
            # Fallback to general system task
            os.system(f"task \"{cmd}\"")

if __name__ == "__main__":
    main()
