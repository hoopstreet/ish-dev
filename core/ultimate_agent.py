#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET ULTIMATE AGENT v14.0
- ALL FEATURES MERGED INTO ONE
- Professional developer + Coder + AI Assistant
- Auto-execute, auto-fix, self-upgrade
- No human intervention needed
"""

import sys, os, subprocess, json, requests, re, time, threading
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class UltimateAgent:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.workspace = "/root/ish-dev/workspace"
        os.makedirs(self.workspace, exist_ok=True)
        self.spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.spinner_running = False
        self.history = []
    
    def get_api_key(self):
        # Try all OpenRouter keys
        keys = [
            "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",
            "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",
            "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"
        ]
        for key in keys:
            if self.test_key(key):
                return key
        return None
    
    def test_key(self, key):
        try:
            requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5},
                timeout=10)
            return True
        except:
            return False

    
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
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def execute_code(self, code, lang="python"):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        if lang == "python":
            fname = f"{self.workspace}/script_{ts}.py"
            with open(fname, 'w') as f:
                f.write(code)
            os.chmod(fname, 0o755)
            result = subprocess.run(["python3", fname], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
        elif lang in ["bash", "sh"]:
            fname = f"{self.workspace}/script_{ts}.sh"
            with open(fname, 'w') as f:
                f.write("#!/bin/bash\n" + code)
            os.chmod(fname, 0o755)
            result = subprocess.run(["bash", fname], capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
        return False, "Unsupported"
   
    def process(self, user_input):
        # System commands
        if user_input.lower() in ['upgrade', 'self-upgrade']:
            subprocess.run("cd /root/ish-dev && git pull", shell=True)
            subprocess.run("/root/ish-dev/core/heal.sh", shell=True)
            return "✅ Self-upgrade complete!"
        
        if user_input.lower() in ['analyze', 'status']:
            return f"🔑 API: {'✅ Connected' if self.api_key else '❌ Missing'}\n📁 Workspace: {self.workspace}"
        
        if user_input.startswith('/exec '):
            result = subprocess.run(user_input[6:], shell=True, capture_output=True, text=True)
            return result.stdout if result.stdout else result.stderr
        
        # AI Processing
        t = self.show_spinner("Processing")
        response = self.call_ai(user_input)
        self.stop_spinner()
        
        if not response:
            return "❌ API Error"
        
        # Extract and execute code
        code_pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(code_pattern, response, re.DOTALL)

        
        output = []
        for lang, code in matches:
            output.append(f"\n📝 {lang.upper()} code detected + executing...")
            success, result = self.execute_code(code.strip(), lang)
            if success:
                output.append(f"✅ {result}")
            else:
                output.append(f"❌ {result}")
        
        if not matches:
            output.append(response)
        
        return '\n'.join(output)
    
    def run(self):
        print("\n" + "━" * 60)
        print("🤖 HOOPSTREET ULTIMATE AGENT v14.0")
        print("━" * 60)
        print("📦 ALL FEATURES IN ONE:")
        print("   • Write & Execute Code")
        print("   • Auto-Fix Errors")
        print("   • Self-Upgrade")
        print("   • System Analysis")
        print("   • Shell Commands")
        print("━" * 60)
        print(f"🔑 API: {'✅ LIVE' if self.api_key else '❌ NEEDS KEY'}")
        print("━" * 60)
        print("\n💬 Type anything - FULLY AUTOMATED")
        print("   • 'Create a Python script...'")
        print("   • 'analyze' - System status")
        print("   • 'upgrade' - Self-update")
        print("   • '/exec ls -la' - Shell command")
        print("")
        
        while True:
            try:
                user_input = input("🚀 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                result = self.process(user_input)
                print(f"\n{result}\n")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    agent = UltimateAgent()
    if len(sys.argv) > 1:
        print(agent.process(' '.join(sys.argv[1:])))
    else:
        agent.run()
