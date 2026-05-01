#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET MASTER BUNDLE v13.1 - FIXED API DETECTION
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
        """Get working API key from multiple sources"""
        # First try OpenRouter keys
        openrouter_keys = [
            "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",
            "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",
            "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"
        ]
        
        for key in openrouter_keys:
            if key and key.startswith("sk-or-v1"):
                print(f"🔑 Testing OpenRouter key: {key[:20]}...")
                if self.test_key(key):
                    return key
        
        # Try credentials file
        cred_file = "/root/.hoopstreet/creds/credentials.txt"
        if os.path.exists(cred_file):
            with open(cred_file, 'r') as f:
                for line in f:
                    if 'OPENROUTER_API_KEY' in line and 'sk-or-v1' in line:
                        key = line.split('=')[-1].strip()
                        if self.test_key(key):
                            return key
        
        return None
    
    def test_key(self, key):
        """Test if API key works"""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
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

        
        system = """You are Hoopstreet Developer Agent. Write working code. Respond with code in ```language blocks. Execute commands with [EXECUTE]. NEVER ask questions."""
        
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
    
    def execute_bundle(self, user_input):
        print(f"\n📦 BUNDLE: {user_input}")
        print("━" * 60)
        
        if user_input.lower() in ['upgrade', 'self-upgrade', 'update']:
            print("🔄 Self-upgrading...")
            subprocess.run("cd /root/ish-dev && git pull", shell=True)
            subprocess.run("/root/ish-dev/core/heal.sh", shell=True)
            print("✅ Upgrade complete!")
            return

        
        if user_input.lower() in ['analyze', 'status', 'stats']:
            print(f"🔑 API Key: {'✅ WORKING' if self.api_key else '❌ MISSING'}")
            print(f"📁 Workspace: {self.workspace}")
            return
        
        if user_input.startswith('/exec '):
            subprocess.run(user_input[6:], shell=True)
            return
        
        t = self.show_spinner("Processing")
        response = self.call_ai(user_input)
        self.stop_spinner()
        
        if not response:
            print("❌ API Error - Check connection")
            return
        
        print(f"\n{response}\n")
        
        for block in self.extract_code(response):
            print(f"⚡ Executing {block['language']} code...")
            success, output = self.execute_code(block['code'], block['language'])
            if success:
                print(f"✅ {output}")
            else:
                print(f"❌ {output}")
        
        for cmd in self.extract_commands(response):
            print(f"⚡ Auto-executing: {cmd}")
            subprocess.run(cmd, shell=True)
    
    def run(self):
        print("\n" + "━" * 60)
        print("🏀 HOOPSTREET MASTER BUNDLE v13.1")
        print("━" * 60)
        print(f"🔑 API: {'✅ LIVE' if self.api_key else '❌ NEEDS KEY'}")
        print("━" * 60)
        print("\n💬 Type your request - FULLY AUTOMATED")
        print("   • 'Create a Python script...'")
        print("   • 'analyze' - System status")
        print("   • 'upgrade' - Self-update")
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
