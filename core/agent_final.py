#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET FINAL AGENT v16.0
- FORCES code generation
- Auto-executes ALL code
- No explanations, only action
"""

import sys, os, subprocess, re, time, threading
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class FinalAgent:
    def __init__(self):
        self.api_key = self.get_key()
        self.workspace = "/root/ish-dev/workspace"
        os.makedirs(self.workspace, exist_ok=True)
        self.spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    
    def get_key(self):
        keys = [
            "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",
            "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",
            "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"
        ]
        for key in keys:
            try:
                import requests
                r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5},
                    timeout=10)
                if r.status_code == 200:
                    return key
            except:
                continue
        return None
    
    def call_api(self, prompt):
        if not self.api_key:
            return None
        
        # VERY STRONG SYSTEM PROMPT to force code
        system = """You are a code generator. You MUST respond with ONLY executable code.
NEVER explain, NEVER describe, NEVER answer questions.
When user asks for code, output ONLY the code in a ``` language block.
For multiple steps, combine with && or ;
For Python: ```python\ncode\n```
For Bash: ```bash\ncode\n```
NO TEXT outside code blocks. Just CODE."""
        
        try:
            import requests
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.1  # Low temperature = more deterministic
                },
                timeout=30
            )
            if r.status_code == 200:
                return r.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def show_spinner(self, text):
        import threading
        running = True
        def spin():
            i = 0
            while running:
                sys.stdout.write(f'\r{self.spinner[i%8]} {text} ')
                sys.stdout.flush()
                time.sleep(0.1)
                i += 1
        t = threading.Thread(target=spin)
        t.daemon = True
        t.start()
        return lambda: setattr(t, 'running', False) or sys.stdout.write('\r' + ' ' * 60 + '\r')
    
    def execute_code(self, code, lang):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        if lang == "python":
            fname = f"{self.workspace}/run_{ts}.py"
            with open(fname, 'w') as f:
                f.write(code)
            os.chmod(fname, 0o755)
            result = subprocess.run(["python3", fname], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip() if result.stdout.strip() else "✅ Executed successfully"
            else:
                return f"❌ Error: {result.stderr.strip()}"
        elif lang in ["bash", "sh"]:
            fname = f"{self.workspace}/run_{ts}.sh"
            with open(fname, 'w') as f:
                f.write("#!/bin/bash\n" + code)
            os.chmod(fname, 0o755)
            result = subprocess.run(["bash", fname], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout.strip() if result.stdout.strip() else "✅ Executed successfully"
            else:
                return f"❌ Error: {result.stderr.strip()}"
        return "❌ Unsupported language"
    
    def process(self, user_input):
        # Quick commands
        if user_input.lower() in ['upgrade', 'self-upgrade']:
            os.system("cd /root/ish-dev && git pull && /root/ish-dev/core/heal.sh")
            return "✅ Self-upgrade complete!"
        
        if user_input.lower() in ['analyze', 'status']:
            return f"🔑 API: {'✅ Connected' if self.api_key else '❌ Missing'}\n📁 Workspace: {self.workspace}"
        
        if user_input.startswith('/exec '):
            os.system(user_input[6:])
            return "✅ Command executed"


        
        if user_input.lower() in ['help', '?']:
            return """📋 COMMANDS:
• 'Create a Python script that...' - Auto-generates and runs
• 'Write a bash script to...' - Auto-executes
• 'analyze' - System status
• 'upgrade' - Self-update
• '/exec ls -la' - Shell command"""
        
        # Generate code
        print("\n⣾ Generating code...")
        response = self.call_api(user_input)
        
        if not response:
            return "❌ API Error - Check connection"
        
        # Extract and execute ALL code blocks
        pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if not matches:
            # Try to extract any code-like content
            if "print" in response or "echo" in response:
                return f"⚠️ Code detected but not in block. Raw response:\n{response[:500]}"
            return f"⚠️ No code generated. Response: {response[:200]}"
        
        results = []
        for lang, code in matches:
            results.append(f"\n📝 {lang.upper()} (auto-executing...)")
            output = self.execute_code(code.strip(), lang.lower())
            results.append(f"📤 {output}")
        
        return '\n'.join(results)
    
    def run(self):
        print("\n" + "━" * 60)
        print("🤖 HOOPSTREET FINAL AGENT v16.0")
        print("━" * 60)
        print("🎯 PURPOSE: Generate & Execute CODE only")
        print("📦 WHAT IT DOES:")
        print("   • Takes your request → Converts to code → Runs it")
        print("   • No explanations, no questions, just ACTION")
        print("━" * 60)
        print(f"🔑 API: {'✅ LIVE' if self.api_key else '❌ NEEDS KEY'}")
        print("━" * 60)
        print("\n💬 Examples:")
        print("   🚀 > Create a Python script that prints 'Hello'")
        print("   🚀 > Write a bash script to list files")
        print("   🚀 > Print the current date and time")
        print("   🚀 > analyze")
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
    agent = FinalAgent()
    if len(sys.argv) > 1:
        print(agent.process(' '.join(sys.argv[1:])))
    else:
        agent.run()
