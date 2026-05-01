#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET AUTOMATED DEVELOPER AGENT v12.0
- NO human interaction + fully automated
- Auto-executes code immediately
- Auto-fixes errors without asking
- Bundle package execution
"""

import sys, os, subprocess, json, requests, re, time
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class AutoDeveloperAgent:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.workspace = "/root/ish-dev/workspace"
        os.makedirs(self.workspace, exist_ok=True)
        self.spinner_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.spinner_idx = 0
        self.spinner_running = False
    
    def get_api_key(self):
        cred_files = ["/root/.hoopstreet/creds/ai_keys.json", "/root/.hoopstreet/creds/credentials.txt"]
        for file in cred_files:
            if os.path.exists(file):
                try:
                    if file.endswith('.json'):
                        with open(file, 'r') as f:
                            data = json.load(f)
                            for key in data.get("openrouter", []):
                                if key.get("key"):
                                    return key.get("key")
                    else:
                        with open(file, 'r') as f:
                            for line in f:
                                if 'sk-or-v1' in line:
                                    return line.split('=')[-1].strip()
                except:
                    pass
        return None
    
    def show_spinner(self, phase, attempt):
        self.spinner_running = True
        import threading
        def spin():
            i = 0
            while self.spinner_running:
                sys.stdout.write(f'\r{self.spinner_chars[i%8]} Phase {phase}: Executing (attempt {attempt})... ')
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
    
    def call_api(self, prompt):
        if not self.api_key:
            return "❌ No API key found"
        
        system = """You are Hoopstreet Automated Developer Agent.
You write working code and execute it immediately.
Respond with code in ```language blocks.
When asked to write code, provide COMPLETE, WORKING code.
Execute commands with [EXECUTE].
NEVER ask questions + just provide the solution."""
        
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
            return f"❌ API Error: {response.status_code}"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def extract_code(self, response):
        code_blocks = []
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        for lang, code in matches:
            code_blocks.append({"language": lang, "code": code.strip()})
        return code_blocks
    
    def extract_commands(self, response):
        commands = []
        pattern = r'\[EXECUTE\]\s*(.+)'
        matches = re.findall(pattern, response)
        commands.extend(matches)
        return commands
    
    def execute_code(self, code, language="python"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if language == "python":
            filename = f"{self.workspace}/script_{timestamp}.py"
            with open(filename, 'w') as f:
                f.write(code)
            os.chmod(filename, 0o755)
            
            print(f"📁 Saved: {filename}")
            
            result = subprocess.run(["python3", filename], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Output:\n{result.stdout}")
                return True, result.stdout
            else:
                print(f"❌ Error:\n{result.stderr}")
                return False, result.stderr

                
        elif language in ["bash", "sh"]:
            filename = f"{self.workspace}/script_{timestamp}.sh"
            with open(filename, 'w') as f:
                f.write("#!/bin/bash\n" + code)
            os.chmod(filename, 0o755)
            
            print(f"📁 Saved: {filename}")
            
            result = subprocess.run(["bash", filename], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Output:\n{result.stdout}")
                return True, result.stdout
            else:
                print(f"❌ Error:\n{result.stderr}")
                return False, result.stderr
        
        return False, "Unsupported language"
    
    def auto_fix_and_retry(self, code, error, language, max_retries=3):
        for attempt in range(1, max_retries + 1):
            print(f"\n🔧 Auto-fix attempt {attempt}/{max_retries}...")
            prompt = f"""Fix this {language} code error:

CODE:
{code}

ERROR:
{error}

Return ONLY the COMPLETE FIXED code in a code block."""
            
            response = self.call_api(prompt)
            fixed_blocks = self.extract_code(response)
            if fixed_blocks:
                fixed_code = fixed_blocks[0]["code"]
                print("📝 Attempting fixed code...")
                success, output = self.execute_code(fixed_code, language)
                if success:
                    print("✅ Auto-fix successful!")
                    return True
        return False
    
    def execute_bundle(self, user_input):
        """Execute bundle commands automatically"""
        print(f"\n📋 Executing: {user_input}")
        print("━" * 60)
        
        # Direct shell commands
        if user_input.startswith('/exec '):
            cmd = user_input[6:]
            print(f"🔧 Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            print(result.stdout if result.stdout else result.stderr)
            return

        
        # Workspace commands
        if user_input.startswith('/workspace'):
            subprocess.run(f"ls -la {self.workspace}", shell=True)
            return
        
        # Upgrade self
        if user_input.lower() in ['upgrade', 'self-upgrade', 'update']:
            print("🔄 Self-upgrading agent...")
            subprocess.run("cd /root/ish-dev && git pull", shell=True)
            subprocess.run("/root/ish-dev/core/heal.sh", shell=True)
            print("✅ Upgrade complete!")
            return
        
        # API call for code generation
        print("🤖 Generating code...")
        t = self.show_spinner(1, 1)
        response = self.call_api(user_input)
        self.stop_spinner()
        print(f"\n{response}\n")
        
        # Find and execute code blocks automatically
        code_blocks = self.extract_code(response)
        
        for block in code_blocks:
            print(f"📝 Found {block['language']} code + executing automatically...")
            success, output = self.execute_code(block['code'], block['language'])
            
            if not success:
                print("🔧 Auto-fixing error...")
                self.auto_fix_and_retry(block['code'], output, block['language'])
        
        # Execute any commands
        commands = self.extract_commands(response)
        for cmd in commands:
            print(f"🔧 Auto-executing: {cmd}")
            subprocess.run(cmd, shell=True)


    
    def run(self):
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET AUTOMATED DEVELOPER AGENT v12.0")
        print("━" * 60)
        print("📋 FEATURES:")
        print("   • NO human interaction needed")
        print("   • Auto-executes code immediately")
        print("   • Auto-fixes errors automatically")
        print("   • Bundle package execution")
        print("   • Type 'upgrade' to self-update")
        print("━" * 60)
        print(f"📁 Workspace: {self.workspace}")
        print(f"🔑 API: {'✅ Connected' if self.api_key else '❌ Missing'}")
        print("━" * 60)
        print("\n💬 Just type your request + code will run automatically!")
        print("   • 'Create a Python script to download a file'")
        print("   • 'Write a bash backup script'")
        print("   • 'upgrade' - Self-update")
        print("   • '/exec ls -la' - Run shell command")
        print("")
        
        while True:
            try:
                user_input = input("🚀 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Goodbye!")
                    break
                self.execute_bundle(user_input)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    agent = AutoDeveloperAgent()
    if len(sys.argv) > 1:
        agent.execute_bundle(' '.join(sys.argv[1:]))
    else:
        agent.run()
