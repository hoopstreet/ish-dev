#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET SELF-IMPROVING AI AGENT v4.0
- Self-learning from past commands
- Auto-upgrading capabilities
- Handles any task autonomously
"""

import sys, os, time, subprocess, re, json, shutil
from datetime import datetime
from pathlib import Path

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

# ============ CONFIGURATION ============
DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
LEARNING_FILE = "/root/ish-dev/agents/learning_v4.json"
AGENT_VERSION = "4.0"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [SELF-AGENT] {msg}\n")
    with open(DNA_FILE, "a") as f: f.write(f"\n## {ts}\n🤖 SELF-AGENT: {msg}\n")

# ============ LEARNING DATABASE ============
class LearningDB:
    def __init__(self):
        self.data = self.load()
    
    def load(self):
        if os.path.exists(LEARNING_FILE):
            with open(LEARNING_FILE, 'r') as f:
                return json.load(f)
        return {
            "successful_commands": [],
            "failed_commands": [],
            "learned_patterns": [],
            "self_upgrades": [],
            "stats": {
                "total_executions": 0,
                "total_success": 0,
                "total_failed": 0,
                "self_heals": 0
            }
        }
    
    def save(self):
        with open(LEARNING_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def record_success(self, command, output):
        self.data["successful_commands"].append({
            "command": command[:200],
            "timestamp": str(datetime.now()),
            "output": output[:200]
        })
        self.data["stats"]["total_executions"] += 1
        self.data["stats"]["total_success"] += 1
        self.save()
    
    def record_failure(self, command, error):
        self.data["failed_commands"].append({
            "command": command[:200],
            "timestamp": str(datetime.now()),
            "error": error[:200]
        })
        self.data["stats"]["total_executions"] += 1
        self.data["stats"]["total_failed"] += 1
        self.save()
    

    def learn_pattern(self, pattern):
        if pattern not in self.data["learned_patterns"]:
            self.data["learned_patterns"].append(pattern)
            self.save()

learning = LearningDB()

# ============ INTELLIGENT COMMAND PARSER ============
class IntelligentParser:
    def __init__(self):
        self.intent_patterns = {
            # System intents
            r"(show|get|check).*(status|health)": "/root/ish-dev/core/status.sh",
            r"(fix|repair|heal).*": "/root/ish-dev/core/heal.sh",
            r"(sync|push|upload).*": "cd /root/ish-dev && git add -A && git commit -m 'Auto-sync' && git push",
            r"(pull|download|update).*": "cd /root/ish-dev && git pull",
            
            # File intents
            r"(list|show).*files": "ls -la",
            r"(show|display).*structure": "tree /root/ish-dev -L 2 2>/dev/null || ls -la /root/ish-dev",
            r"(show|list).*core": "ls -la /root/ish-dev/core",
            r"(show|list).*docs": "ls -la /root/ish-dev/docs",
            
            # System info
            r"(disk|storage).*space": "df -h",
            r"(memory|ram).*": "free -m",
            r"(time|date).*": "date",
            
            # Python/Dev
            r"(python|py).*version": "python3 --version",
            r"(install|setup).*pip": "python3 -m ensurepip",
            
            # Self improvement
            r"(upgrade|update|improve).*self": "__SELF_UPGRADE__",
            r"(learn|teach).*pattern": "__LEARN_PATTERN__",
            r"(stats|statistics|performance)": "__STATS__",
        }
    
    def parse(self, text):
        text_lower = text.lower()
        
        # Check for self-upgrade command
        if "upgrade" in text_lower or "improve" in text_lower:
            return "__SELF_UPGRADE__"
        
        # Match intents
        for pattern, command in self.intent_patterns.items():
            if re.search(pattern, text_lower):
                return command
        
        # Check learning database for similar commands
        for cmd in learning.data["successful_commands"][-10:]:
            if cmd["command"] in text_lower:
                return cmd["command"]
        
        # Return as-is for direct commands
        return text

parser = IntelligentParser()

# ============ CODE EXECUTOR WITH LEARNING ============
class SmartExecutor:
    def __init__(self):
        self.auto_fixes = 0
    
    def execute(self, command):
        print(f"\n📌 Executing: {command}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(result.stdout if result.stdout else "✅ SUCCESS")
                learning.record_success(command, result.stdout)
                log(f"SUCCESS: {command}")
                return True
            else:
                print(f"❌ ERROR: {result.stderr[:200]}")
                learning.record_failure(command, result.stderr)
                log(f"FAILED: {command}")
                return self.auto_heal(command, result.stderr)
                
        except subprocess.TimeoutExpired:
            print("❌ TIMEOUT (60s)")
            learning.record_failure(command, "Timeout")
            return False
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            learning.record_failure(command, str(e))
            return False
    
    def auto_heal(self, command, error):
        """Auto-heal common errors"""
        self.auto_fixes += 1
        
        # Fix: command not found -> install
        if "not found" in error:
            pkg = command.split()[0]
            print(f"🔧 Auto-healing: Installing {pkg}...")
            subprocess.run(f"pip install {pkg}", shell=True)
            return self.execute(command)
        
        # Fix: permission denied -> chmod +x
        if "Permission denied" in error:
            print(f"🔧 Auto-healing: Adding execute permission...")
            subprocess.run(f"chmod +x {command.split()[0]}", shell=True)
            return self.execute(command)
        
        # Fix: No such file -> create directory
        if "No such file" in error:
            print(f"🔧 Auto-healing: Creating directory...")
            subprocess.run(f"mkdir -p $(dirname {command.split()[-1]})", shell=True)
            return self.execute(command)
        
        return False

executor = SmartExecutor()

# ============ SELF-UPGRADE MODULE ============
class SelfUpgrader:
    def __init__(self):
        self.upgrade_count = 0
    
    def upgrade(self):
        print("\n🔄 SELF-UPGRADE INITIATED")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # 1. Pull latest from GitHub
        print("📥 Pulling latest updates...")
        os.system("cd /root/ish-dev && git pull")
        
        # 2. Run heal engine
        print("🔧 Running heal engine...")
        os.system("/root/ish-dev/core/heal.sh")
        
        # 3. Update learning patterns
        print("🧠 Updating learning patterns...")
        learning.learn_pattern("self_upgrade_triggered")
        
        # 4. Record upgrade
        self.upgrade_count += 1
        learning.data["self_upgrades"].append({
            "timestamp": str(datetime.now()),
            "version": AGENT_VERSION,
            "upgrade_number": self.upgrade_count
        })
        learning.save()
        # 5. Log to DNA
        log(f"Self-upgrade #{self.upgrade_count} completed")
        
        print("\n✅ SELF-UPGRADE COMPLETE!")
        print(f"   Upgrades performed: {self.upgrade_count}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        return True

upgrader = SelfUpgrader()

# ============ DISPLAY FUNCTIONS ============
def show_banner():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 HOOPSTREET SELF-IMPROVING AI AGENT v4.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CAPABILITIES:")
    print(" • 🧠 Learns from every command")
    print(" • 🔧 Auto-heals errors intelligently")
    print(" • 🔄 Self-upgrades automatically")
    print(" • 💾 Remembers successful patterns")
    print(" • 🐙 Full Git integration")
    print(" • 📁 File system mastery")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n👉 Type 'help' for commands, 'upgrade' to self-improve, 'exit' to quit")
    print("")

def show_help():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 SELF-IMPROVING AI AGENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 SYSTEM COMMANDS (Natural Language):
   "show status" or "check health"  → Status dashboard
   "fix everything" or "heal"       → Auto-heal engine
   "sync now" or "push to GitHub"   → Git sync

🔹 FILE COMMANDS:
   "list files" or "show structure" → Project structure
   "show core" or "list scripts"    → Core scripts
   "show docs"                      → Documentation

🔹 SELF-IMPROVEMENT:
   "upgrade" or "improve yourself"  → Self-upgrade agent
   "stats" or "show stats"          → Agent statistics
   "learn" or "teach"               → Record learning patterns

🔹 INFO COMMANDS:
   "disk space" or "storage"        → Disk usage
   "memory" or "ram"                → Memory usage
   "time" or "date"                 → Current time

🔹 AGENT COMMANDS:
   "help"      → Show this help
   "stats"     → Show agent statistics
   "exit"      → Return to main menu

📝 EXAMPLES (Just type naturally):
   🤖 Agent > show status
   🤖 Agent > fix everything and sync
   🤖 Agent > upgrade yourself
   🤖 Agent > list files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_stats():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 SELF-IMPROVING AGENT STATISTICS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Agent Version: {AGENT_VERSION}")
    print(f"   Total Executions: {learning.data['stats']['total_executions']}")
    print(f"   Success Rate: {learning.data['stats']['total_success']}/{learning.data['stats']['total_executions']}")
    print(f"   Self-Heals Performed: {learning.data['stats']['self_heals']}")
    print(f"   Learned Patterns: {len(learning.data['learned_patterns'])}")
    print(f"   Self-Upgrades: {len(learning.data['self_upgrades'])}")
    
    dna_lines = 0
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            dna_lines = len(f.readlines())
    print(f"   DNA.md Size: {dna_lines} lines")
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

# ============ MAIN LOOP ============
def main():
    show_banner()
    
    while True:
        try:
            user_input = input("🤖 Agent > ").strip()
            
            if not user_input:
                continue
            
            # Check for exit
            if user_input.lower() in ['exit', 'quit']:
                print("\n🔙 Returning to main menu...")
                break
            
            # Check for help
            if user_input.lower() in ['help', '?']:
                show_help()
                continue
            
            # Check for stats
            if user_input.lower() in ['stats', 'statistics']:
                show_stats()
                continue
            
            # Check for self-upgrade
            if user_input.lower() in ['upgrade', 'self-upgrade', 'improve']:
                upgrader.upgrade()
                continue
            
            # Parse and execute
            command = parser.parse(user_input)
            
            if command == "__SELF_UPGRADE__":
                upgrader.upgrade()
            elif command == "__STATS__":
                show_stats()
            else:
                executor.execute(command)
                
        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
