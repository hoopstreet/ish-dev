#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET MASTER BUNDLE v13.0
- Professional end-to-end automation
- Auto-detects task type
- Executes code, fixes errors, upgrades self
- No human intervention needed
"""

import sys, os, subprocess, json, requests, re, time
from datetime import datetime
import threading

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class MasterBundle:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.workspace = "/root/ish-dev/workspace"
        self.bundle_log = "/root/ish-dev/docs/bundle.log"
        os.makedirs(self.workspace, exist_ok=True)
        self.spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.spinner_running = False
    
    def get_api_key(self):
        cred_files = ["/root/.hoopstreet/creds/ai_keys.json", "/root/.hoopstreet/creds/credentials.txt"]
        for file in cred_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                        if 'sk-or-v1' in content:
                            for line in content.split('\n'):
                                if 'sk-or-v1' in line:
                                    return line.split('=')[-1].strip()
                except:
                    pass
        return None
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.bundle_log, 'a') as f:
            f.write(f"[{ts}] {msg}\n")
    
    def show_spinner(self, text):
        self.spinner_running = True
        def spin():
            i = 0
            while self.spinner_running:
                sys.stdout.write(f'\r{self.spinner[i%8]} {text} ')
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        t = threading.Thread(target=spin)
        t.daemon = True
        t.start()
        return t
    
    def stop_spinner(self):
        self.spinner_running = False
        sys.stdout.write('\r' + ' ' * 60 + '\r')
        sys.stdout.flush()
    
    def call_ai(self, prompt):
        if not self.api_key:
            return None

        
        system = """You are Hoopstreet Master Developer Agent.
You write working code and execute it immediately.
Respond with code in ```language blocks.
Execute commands with [EXECUTE].
NEVER ask questions + just provide the solution.
For upgrades, provide the upgrade code."""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.3
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def extract_code(self, response):
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        return [{"language": lang, "code": code.strip()} for lang, code in matches]
    
    def extract_commands(self, response):
        pattern = r'\[EXECUTE\]\s*(.+)'
        return re.findall(pattern, response)
    
    def execute_code(self, code, lang):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if lang == "python":
            filename = f"{self.workspace}/bundle_{ts}.py"
            with open(filename, 'w') as f:
                f.write(code)
            os.chmod(filename, 0o755)
            result = subprocess.run(["python3", filename], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
        
        elif lang in ["bash", "sh"]:
            filename = f"{self.workspace}/bundle_{ts}.sh"
            with open(filename, 'w') as f:
                f.write("#!/bin/bash\n" + code)
            os.chmod(filename, 0o755)
            result = subprocess.run(["bash", filename], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr

        
        return False, "Unsupported"
    
    def self_upgrade(self):
        print("\n🔄 SELF-UPGRADING MASTER BUNDLE...")
        self.log("Self-upgrade initiated")
        
        # Pull latest
        subprocess.run("cd /root/ish-dev && git pull", shell=True, capture_output=True)
        
        # Run heal
        subprocess.run("/root/ish-dev/core/heal.sh", shell=True)
        
        # Update this script
        self.log("Self-upgrade completed")
        print("✅ Master Bundle upgraded!")
        return True
    
    def analyze_system(self):
        print("\n🔍 ANALYZING SYSTEM...")
        print("━" * 60)
        
        stats = {
            "version": "v10.0.9",
            "api_status": "✅ Connected" if self.api_key else "❌ Missing",
            "workspace": self.workspace,
            "python": subprocess.run(["python3", "--version"], capture_output=True, text=True).stdout.strip(),
            "disk": subprocess.run(["df", "-h", "/"], capture_output=True, text=True).stdout.split('\n')[1].split()[3] if os.name != 'nt' else "N/A"
        }
        
        for k, v in stats.items():
            print(f"   {k}: {v}")
        
        print("━" * 60)
        return stats
    
    def execute_bundle(self, user_input):
        print(f"\n📦 BUNDLE: {user_input}")
        print("━" * 60)
        
        # Command handlers
        if user_input.lower() in ['upgrade', 'self-upgrade', 'update']:
            self.self_upgrade()
            return

        
        if user_input.lower() in ['analyze', 'status', 'stats']:
            self.analyze_system()
            return
        
        if user_input.startswith('/exec '):
            cmd = user_input[6:]
            print(f"🔧 Running: {cmd}")
            subprocess.run(cmd, shell=True)
            return
        
        if user_input.startswith('/workspace'):
            subprocess.run(f"ls -la {self.workspace}", shell=True)
            return
        
        # AI Processing
        t = self.show_spinner("Processing request")
        response = self.call_ai(user_input)
        self.stop_spinner()
        
        if not response:
            print("❌ No response from AI. Check API key.")
            return
        
        print(f"\n{response}\n")
        
        # Auto-execute code blocks
        code_blocks = self.extract_code(response)
        for block in code_blocks:
            print(f"⚡ Executing {block['language']} code...")
            success, output = self.execute_code(block['code'], block['language'])
            if success:
                print(f"✅ Output:\n{output}")
                self.log(f"Success: {user_input[:50]}")
            else:
                print(f"❌ Error: {output}")
                self.log(f"Failed: {user_input[:50]} - {output[:50]}")
        
        # Execute commands
        commands = self.extract_commands(response)
        for cmd in commands:
            print(f"⚡ Auto-executing: {cmd}")
            subprocess.run(cmd, shell=True)
    
    def run(self):
        print("\n" + "━" * 60)
        print("🏀 HOOPSTREET MASTER BUNDLE v13.0")
        print("━" * 60)
        print("📦 PROFESSIONAL END-TO-END AUTOMATION")
        print("━" * 60)
        print("   • Write code → Auto-execute → Auto-fix")
        print("   • type 'upgrade' → Self-update")
        print("   • type 'analyze' → System status")
        print("   • /exec <cmd> → Shell commands")
        print("━" * 60)
        print(f"🔑 API: {'✅ LIVE' if self.api_key else '❌ NEEDS KEY'}")
        print(f"📁 Workspace: {self.workspace}")
        print("━" * 60)
        print("\n💬 Just type your request - FULLY AUTOMATED")
        print("")
        
        while True:
            try:
                user_input = input("🎯 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                self.execute_bundle(user_input)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    bundle = MasterBundle()
    if len(sys.argv) > 1:
        bundle.execute_bundle(' '.join(sys.argv[1:]))
    else:
        bundle.run()
