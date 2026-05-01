#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET DEVELOPER & CODER AGENT v11.0
- Writes and executes code
- Fixes errors automatically
- Self-improves by learning from failures
- Professional development assistant
"""

import sys, os, subprocess, json, requests, tempfile, re
from datetime import datetime
from pathlib import Path

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class DeveloperAgent:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.workspace = "/root/ish-dev/workspace"
        os.makedirs(self.workspace, exist_ok=True)
        self.history_file = f"{self.workspace}/dev_history.json"
        self.load_history()
    
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
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {"tasks": [], "successful_code": [], "failed_attempts": []}
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def call_api(self, prompt, system_prompt=None):
        if not self.api_key:
            return "❌ No API key found"
        
        default_system = """You are Hoopstreet Developer Agent + a professional coder.
You write working code, fix errors automatically, and help developers build software.
Respond with code in ```language blocks and execute commands with [EXECUTE].

When asked to write code, always provide COMPLETE, WORKING code with error handling.
When there's an error, analyze it and provide the FIXED code immediately.
Never just explain + always PROVIDE THE SOLUTION."""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system_prompt or default_system},
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
        """Extract code blocks from AI response"""
        code_blocks = []
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        for lang, code in matches:
            code_blocks.append({"language": lang, "code": code.strip()})
        return code_blocks
    
    def extract_commands(self, response):
        """Extract commands to execute"""
        commands = []
        pattern = r'\[EXECUTE\]\s*(.+)'
        matches = re.findall(pattern, response)
        commands.extend(matches)
        return commands
    
    def save_and_run_code(self, code, language="python"):
        """Save code and run it"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if language == "python":
            filename = f"{self.workspace}/script_{timestamp}.py"
            with open(filename, 'w') as f:
                f.write(code)
            os.chmod(filename, 0o755)
            
            print(f"\n📁 Saved: {filename}")
            print("🚀 Running code...")
            print("━" * 50)
            
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
            
            print(f"\n📁 Saved: {filename}")
            print("🚀 Running script...")
            print("━" * 50)
            
            result = subprocess.run(["bash", filename], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Output:\n{result.stdout}")
                return True, result.stdout
            else:
                print(f"❌ Error:\n{result.stderr}")
                return False, result.stderr
        
        return False, "Unsupported language"
    
    def auto_fix_error(self, code, error, language):
        """Auto-fix code using AI"""
        prompt = f"""The following {language} code has an error:

CODE:
{code}

ERROR:
{error}

Please provide the COMPLETE FIXED code. Only return the code block."""
        
        response = self.call_api(prompt, system_prompt="You are a code debugger. Return ONLY the fixed code in a code block.")
        fixed_blocks = self.extract_code(response)
        if fixed_blocks:
            return fixed_blocks[0]["code"]
        return None
    
    def execute_task(self, user_request):
        """Main execution flow for developer tasks"""
        print(f"\n📋 Task: {user_request}")
        print("━" * 60)
        
        # Check if it's a file operation command
        if user_request.startswith('/exec '):
            cmd = user_request[6:]
            print(f"🔧 Executing: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            print(result.stdout if result.stdout else result.stderr)
            return
        
        # Check if it's a workspace command
        if user_request.startswith('/workspace'):
            print(f"📁 Workspace: {self.workspace}")
            subprocess.run(f"ls -la {self.workspace}", shell=True)
            return
        
        # Get AI response with code
        print("🤖 Generating solution...")
        response = self.call_api(user_request)
        print(f"\n{response}\n")
        
        # Extract and run code blocks
        code_blocks = self.extract_code(response)
        
        for block in code_blocks:
            print(f"\n📝 Found {block['language']} code block")
            print("━" * 50)
            print(block['code'][:500])
            print("━" * 50)
            
            user_choice = input("\n❓ Run this code? (y/n/e to edit): ").strip().lower()
            
            if user_choice == 'y':
                success, output = self.save_and_run_code(block['code'], block['language'])
                if not success and "fix" in user_request.lower():
                    print("\n🔧 Attempting auto-fix...")
                    fixed_code = self.auto_fix_error(block['code'], output, block['language'])
                    if fixed_code:
                        print("✅ Auto-fix applied!")
                        self.save_and_run_code(fixed_code, block['language'])
                        
            elif user_choice == 'e':
                print("\n📝 Edit code (Ctrl+D to finish):")
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                edited_code = '\n'.join(lines)
                if edited_code:
                    self.save_and_run_code(edited_code, block['language'])
        
        # Execute commands
        commands = self.extract_commands(response)
        for cmd in commands:
            print(f"\n🔧 Executing command: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            print(result.stdout if result.stdout else result.stderr)
    
    def interactive(self):
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET DEVELOPER & CODER AGENT v11.0")
        print("━" * 60)
        print("📋 CAPABILITIES:")
        print("   • Write and execute code")
        print("   • Auto-fix errors")
        print("   • Self-improve from failures")
        print("   • File operations (/exec, /workspace)")
        print("━" * 60)
        print(f"📁 Workspace: {self.workspace}")
        print(f"🔑 API: {'✅ Connected' if self.api_key else '❌ Missing'}")
        print("━" * 60)
        print("\n💬 Describe what you want me to CODE:")
        print("   • 'Create a Python script to download a file'")
        print("   • 'Fix this error: [error message]'")
        print("   • '/exec ls -la'")
        print("   • '/workspace'")
        print("")
        
        while True:
            try:
                user_input = input("💻 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['/exit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                self.execute_task(user_input)
                self.save_history()
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    agent = DeveloperAgent()
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        agent.execute_task(prompt)
    else:
        agent.interactive()

if __name__ == "__main__":
    main()
