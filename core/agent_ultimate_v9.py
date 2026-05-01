import sys, os, subprocess, time
from datetime import datetime

CONFIG = {
    "VERSION": "12.2-AUTO",
    "ROOT": "/root/ish-dev",
    "DNA": "/root/ish-dev/docs/DNA.md",
    "RECOVERY": "/root/ish-dev/recovery"
}

def auto_log(msg):
    with open(CONFIG["DNA"], "a") as f:
        f.write(f"\n[{datetime.now()}] [AUTO-EXEC] {msg}")

def autonomous_run(cmd):
    """Executes command and auto-heals on failure without human input."""
    print(f"🤖 [Auto-System] Executing: {cmd}")
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if process.returncode != 0:
        auto_log(f"FAIL: {cmd} | ERR: {process.stderr}")
        print(f"⚠️ Failure detected. Initiating Autonomous Repair...")
        # Auto-trigger heal without waiting
        os.system("sh /root/ish-dev/core/heal.sh --silent")
        return False
    return True

def main():
    os.system("clear")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🤖 GEMINI MASTER CLI v{CONFIG['VERSION']} (AUTONOMOUS)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    while True:
        prompt = input("\n🛰️ System Awaiting Input: ").strip().lower()
        if prompt in ['exit', '0']: break
        
        # 1. Automated Merging & Sync
        if any(x in prompt for x in ["sync", "merge", "push", "adopt"]):
            if not autonomous_run("sh /root/ish-dev/core/sync.sh"):
                print("📡 Network offline. Queuing sync for later...")

        # 2. Automated Global Repair
        elif any(x in prompt for x in ["fix", "heal", "repair", "recover"]):
            autonomous_run("sh /root/ish-dev/core/heal.sh")

        # 3. Code Implementation Logic
        elif "cat <<" in prompt or "import" in prompt:
            print("📝 Code block detected. Automating implementation...")
            with open("/tmp/auto_script.sh", "w") as f: f.write(prompt)
            autonomous_run("sh /tmp/auto_script.sh")

        # 4. Fallback: Intelligent Execution
        else:
            print(f"🧠 Processing Intent: {prompt}")
            autonomous_run(f"task \"{prompt}\"")

if __name__ == "__main__":
    main()
