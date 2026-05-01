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
