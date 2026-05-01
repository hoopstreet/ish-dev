#!/usr/bin/env python3
"""
HOOPSTREET UNIFIED AI AGENT v2.0
Merged: Code Executor + AI Assistant + Bundle Handler + Auto-Healer
"""

import sys, os, time, threading, re, subprocess, json, shlex
from datetime import datetime
from pathlib import Path

# Environment setup
os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

# Paths
DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
LEARNING_FILE = "/root/ish-dev/agents/learning.json"

# Global state
spinner_running = False
first_run = True

# Spinner characters
SPINNER = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [AGENT] {msg}\n")
    with open(DNA_FILE, "a") as f: f.write(f"\n## {ts}\n🤖 {msg}\n")

def show_spinner(phase, attempt):
    global spinner_running
    i = 0
    while spinner_running:
        sys.stdout.write(f'\r{SPINNER[i%8]} Phase {phase}: Executing (attempt {attempt})... ')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def clear_line():
    sys.stdout.write('\r' + ' ' * 70 + '\r')
    sys.stdout.flush()

def load_learning():
    if os.path.exists(LEARNING_FILE):
        with open(LEARNING_FILE, 'r') as f:
            return json.load(f)
    return {"successful": [], "failed": [], "fixes": [], "patterns": []}

def save_learning(data):
    with open(LEARNING_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class ErrorFixer:
    def __init__(self):
        self.fix_patterns = {
            "No such file": self.fix_missing_file,
            "permission denied": self.fix_permission,
            "command not found": self.fix_missing_command,
            "syntax error": self.fix_syntax,
            "indentation": self.fix_indentation,
            "connection refused": self.fix_network,
            "ModuleNotFoundError": self.fix_module,
            "pip not found": self.fix_pip,
        }
    
    def fix_missing_file(self, cmd):
        return f"ls -la {cmd.split()[-1] if cmd.split() else '.'}"
    
    def fix_permission(self, cmd):
        file = cmd.split()[-1] if cmd.split() else ""
        return f"chmod +x {file}\n{cmd}"
    
    def fix_missing_command(self, cmd):
        pkg = cmd.split()[0]
        return f"pip install {pkg}\n{cmd}"
    
    def fix_syntax(self, cmd):
        return cmd.replace("'", '"')
    
    def fix_indentation(self, cmd):
        lines = cmd.split('\n')
        return '\n'.join(["    " + l if l.strip() and not l.startswith(' ') else l for l in lines])
    
    def fix_network(self, cmd):
        return f"ping -c 1 github.com\n{cmd}"
    
    def fix_module(self, cmd):
        module = cmd.split()[-1] if 'import' in cmd else ''
        return f"pip install {module}\n{cmd}"
    
    def fix_pip(self, cmd):
        return "python3 -m ensurepip --upgrade\n" + cmd
    
    def analyze_and_fix(self, error_msg, command):
        for pattern, fix_func in self.fix_patterns.items():
            if pattern in error_msg:
                fixed = fix_func(command)
                log(f"Auto-fixed: {pattern} → {fixed[:50]}...")
                return fixed, f"✅ Fixed: {pattern}"
        return command, "❌ No auto-fix available"

error_fixer = ErrorFixer()

class BundleParser:
    def __init__(self):
        self.bundles = {
            # System commands
            "status": "/root/ish-dev/core/status.sh",
            "heal": "/root/ish-dev/core/heal.sh",
            "sync": "/root/ish-dev/core/sync.sh",
            "menu": "/root/menu",
            
            # Development
            "install python": "pip install python",
            "install pip": "python3 -m ensurepip",
            "setup project": "mkdir -p project && cd project",
            "git init": "git init && git add . && git commit -m 'Initial'",
            
            # GitHub
            "push all": "git add . && git commit -m 'Update' && git push",
            "pull latest": "git pull origin main",
            "clone repo": "git clone $URL",
            
            # Docker
            "build docker": "docker build -t hoopstreet/agent .",
            "run docker": "docker run -it hoopstreet/agent",
            
            # Testing
            "run tests": "/root/ish-dev/tests/test_all.sh",
            "benchmark": "/root/ish-dev/tests/benchmark.sh",
            
            # Cleanup
            "clean cache": "find . -type d -name __pycache__ -exec rm -rf {} +",
            "clean logs": "find /root/ish-dev/docs -name '*.log.*' -mtime +7 -delete",
        }
    
    def parse(self, text):
        text_lower = text.lower()
        commands = []
        
        # Check for bundle matches
        for keyword, cmd in self.bundles.items():
            if keyword in text_lower:
                commands.append(cmd)
        
        # Parse multi-phase code
        if '# Phase' in text:
            return self.parse_phases(text)
        
        # Parse multiple commands separated by AND
        if ' and ' in text_lower:
            parts = text_lower.split(' and ')
            for part in parts:
                for keyword, cmd in self.bundles.items():
                    if keyword in part:
                        commands.append(cmd)
        
        return commands if commands else None
    
    def parse_phases(self, code):
        phases = []
        current = []
        phase_num = 0
        
        for line in code.split('\n'):
            if re.match(r'^\s*#\s*Phase\s*\d+', line, re.IGNORECASE):
                if current:
                    phase_num += 1
                    phases.append((phase_num, '\n'.join(current)))
                current = [line]
            else:
                current.append(line)
        
        if current:
            phase_num += 1
            phases.append((phase_num, '\n'.join(current)))
        
        return phases

bundle_parser = BundleParser()

class CodePredictor:
    def __init__(self):
        self.predictions = {
            'echo': '🔮 echo "Your message"',
            'python': '🔮 python3 script.py',
            'pip': '🔮 pip install package_name',
            'git add': '🔮 git commit -m "message"',
            'git commit': '🔮 git push origin main',
            'mkdir': '🔮 cd new_directory',
            'cd': '🔮 ls -la',
            '# Phase': '🔮 # Phase N\necho "command"',
            'import': '🔮 from module import function',
            'def ': '🔮 return value',
            'class ': '🔮 def __init__(self):',
        }
    
    def predict(self, line):
        for trigger, prediction in self.predictions.items():
            if line.strip().startswith(trigger):
                return prediction
        return None
    
    def suggest_completion(self, history):
        if not history:
            return None
        last = history[-1]
        if 'pip install' in last:
            return "🔮 Next: Run the installed package"
        if 'git add' in last:
            return "🔮 Next: git commit -m 'message'"
        if 'mkdir' in last:
            return "🔮 Next: cd into new directory"
        return None

predictor = CodePredictor()

class UnifiedAgent:
    def __init__(self):
        self.learning = load_learning()
        self.history = []
        self.total_success = 0
        self.total_failed = 0
    
    def execute_command(self, cmd, phase_num=1, max_retries=3):
        global spinner_running
        
        for attempt in range(1, max_retries + 1):
            spinner_running = True
            t = threading.Thread(target=show_spinner, args=(phase_num, attempt))
            t.daemon = True
            t.start()
            
            tmp = f"/tmp/agent_cmd_{phase_num}.sh"
            with open(tmp, 'w') as f:
                f.write(cmd)
            
            result = subprocess.run(["sh", tmp], capture_output=True, text=True)
            os.remove(tmp)
            
            spinner_running = False
            clear_line()
            
            if result.returncode == 0:
                print(f"✅ Phase {phase_num} SUCCESS (attempt {attempt})")
                log(f"SUCCESS: {cmd[:100]}")
                self.total_success += 1
                return True, result.stdout
            else:
                print(f"❌ Phase {phase_num} FAILED (attempt {attempt})")
                error_msg = result.stderr[:200]
                
                if attempt < max_retries:
                    fixed_cmd, fix_msg = error_fixer.analyze_and_fix(error_msg, cmd)
                    if fixed_cmd != cmd:
                        print(f"🔧 {fix_msg}")
                        cmd = fixed_cmd
                        print(f"🔄 Retrying with fix...")
                        time.sleep(1)
                        continue
                else:
                    print(f"💀 Phase {phase_num} FAILED after {max_retries} attempts")
                    log(f"FAILED: {cmd[:100]} - {error_msg[:100]}")
                    self.total_failed += 1
                    return False, error_msg
        
        return False, "Max retries exceeded"
    
    def execute_bundle(self, bundle):
        parsed = bundle_parser.parse(bundle)
        
        if parsed is None:
            print("\n❌ Could not parse command. Use natural language or # Phase format.")
            print("📝 Examples: 'check status', 'heal everything', # Phase 1... END")
            return
        
        # Handle multi-phase code
        if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], tuple):
            print(f"\n📊 Detected {len(parsed)} phase(s)")
            for phase_num, phase_cmd in parsed:
                success, output = self.execute_command(phase_cmd, phase_num)
                if output:
                    print(f"📤 Output: {output[:200]}")
        # Handle regular commands
        elif isinstance(parsed, list):
            print(f"\n📊 Executing {len(parsed)} command(s)")
            for i, cmd in enumerate(parsed, 1):
                print(f"\n📌 Command {i}/{len(parsed)}: {cmd[:50]}...")
                success, output = self.execute_command(cmd, i)
                if output:
                    print(f"📤 {output[:200]}")
        else:
            print("❌ Invalid command format")
        
        # Show summary
        print(f"\n📊 EXECUTION SUMMARY")
        print(f"✅ Successful: {self.total_success}")
        print(f"❌ Failed: {self.total_failed}")
        
        # Save learning
        self.learning['successful'].append({"commands": self.history[-5:]})
        save_learning(self.learning)
    
    def interactive_mode(self):
        global first_run
        
        while True:
            if first_run:
                self.show_welcome()
                first_run = False
            else:
                print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print("Ready for next command. Type 'exit' to quit.")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            print("\n🤖 Agent > ", end="")
            try:
                user_input = input().strip()
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() in ['exit', 'quit', 'back']:
                print("\n🔙 Returning to main menu...")
                break
            elif user_input.lower() == 'help':
                self.show_help()
                continue
            elif user_input.lower() == 'stats':
                self.show_stats()
                continue
            
            # Show prediction while typing (simulated)
            pred = predictor.predict(user_input)
            if pred:
                print(pred)
            
            self.history.append(user_input)
            self.execute_bundle(user_input)
    
    def show_welcome(self):
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🤖 HOOPSTREET UNIFIED AI AGENT v2.0")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 CAPABILITIES:")
        print(" • 🧠 Natural language bundle commands")
        print(" • 📝 Multi-phase code execution (# Phase 1... END)")
        print(" • 🔧 Auto-error detection and fixing")
        print(" • 🔮 Smart code predictions")
        print(" • 💾 Learning from history")
        print(" • 🌀 Visual spinner feedback")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\n📝 EXAMPLES:")
        print("   • check status")
        print("   • heal everything")
        print("   • install python and git")
        print("   • # Phase 1\necho 'Hello'\n# Phase 2\necho 'World'\nEND")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\n👇 Type your command below")
    
    def show_help(self):
        print("\n📚 AVAILABLE COMMANDS:")
        print("   🔹 System: status, heal, sync, menu")
        print("   🔹 Git: push all, pull latest, clone repo")
        print("   🔹 Python: install python, install pip")
        print("   🔹 Docker: build docker, run docker")
        print("   🔹 Testing: run tests, benchmark")
        print("   🔹 Cleanup: clean cache, clean logs")
        print("   🔹 Multi-phase: # Phase 1... # Phase N... END")
        print("")
    
    def show_stats(self):
        print(f"\n📊 AGENT STATISTICS:")
        print(f"   ✅ Successful commands: {self.total_success}")
        print(f"   ❌ Failed commands: {self.total_failed}")
        print(f"   📚 Learned patterns: {len(self.learning.get('successful', []))}")
        print(f"   🔧 Auto-fixes applied: {len(self.learning.get('fixes', []))}")

if __name__ == "__main__":
    agent = UnifiedAgent()
    agent.interactive_mode()
