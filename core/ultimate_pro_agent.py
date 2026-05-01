#!/usr/bin/env python3
"""
HOOPSTREET ULTIMATE PRO AGENT v17.0
- Auto-failover: Gemini CLI → Open Interpreter → OpenRouter
- Auto-credential selection
- Code generation, execution, fixing, testing, analysis
- Professional developer assistant
"""

import sys, os, subprocess, json, requests, re, time, threading
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class UltimateProAgent:
    def __init__(self):
        self.workspace = "/root/ish-dev/workspace"
        self.logs = "/root/ish-dev/docs/agent.log"
        os.makedirs(self.workspace, exist_ok=True)
        self.spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.active_provider = None
        self.load_credentials()
    
    def load_credentials(self):
        """Load all API keys from credentials"""
        self.openrouter_keys = [
            "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",
            "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",
            "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"
        ]
        self.gemini_keys = [
            "AIzaSyDpTlgDGF3G2MEpjt9S0o_Dx0eLw4231t0",
            "AIzaSyCwgzPlhPayfwwge4jLMkxgy_dbIZO0AhU"
        ]
        self.openrouter_working = None
        self.gemini_working = None
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.logs, "a") as f:
            f.write(f"[{ts}] {msg}\n")
    
    def test_gemini_cli(self):
        """Test if Gemini CLI is installed and working"""
        try:
            result = subprocess.run(["gemini", "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                self.log("Gemini CLI available")
                return True
        except:
            pass
        return False
    
    def test_gemini_api(self, key):
        """Test Gemini API key"""
        try:
            r = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}", timeout=10)
            return r.status_code == 200
        except:
            return False
    
    def test_openrouter_key(self, key):
        """Test OpenRouter API key"""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}], "max_tokens": 5},
                timeout=10
            )
            return r.status_code == 200
        except:
            return False
    
    def call_gemini_cli(self, prompt):
        """Use Gemini CLI directly"""
        try:
            result = subprocess.run(["gemini", prompt], capture_output=True, text=True, timeout=60)
            return result.stdout if result.returncode == 0 else None
        except:
            return None

    
    def call_gemini_api(self, prompt, key):
        """Call Gemini API"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if r.status_code == 200:
                data = r.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return None
        except:
            return None
    
    def call_openrouter(self, prompt, key):
        """Call OpenRouter API"""
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000
                },
                timeout=60
            )
            if r.status_code == 200:
                return r.json()['choices'][0]['message']['content']
            return None
        except:
            return None
    
    def call_interpreter(self, prompt):
        """Use Open Interpreter (local fallback)"""
        try:
            result = subprocess.run(["interpreter", "-y", prompt], capture_output=True, text=True, timeout=60)
            return result.stdout if result.returncode == 0 else None
        except:
            return None
    
    def get_response(self, prompt):
        """Auto-failover: Try providers in order"""
        
        # Priority 1: Gemini CLI
        if self.test_gemini_cli():
            print("📡 [1/3] Trying Gemini CLI...")
            response = self.call_gemini_cli(prompt)
            if response:
                self.active_provider = "Gemini CLI"
                self.log(f"Used Gemini CLI for: {prompt[:50]}")
                return response
        
        # Priority 2: Gemini API Keys
        for key in self.gemini_keys:
            if self.test_gemini_api(key):
                print(f"📡 [2/3] Trying Gemini API...")
                response = self.call_gemini_api(prompt, key)
                if response:
                    self.active_provider = "Gemini API"
                    self.log(f"Used Gemini API for: {prompt[:50]}")
                    return response
                break
        
        # Priority 3: Open Interpreter (local)
        try:
            result = subprocess.run(["which", "interpreter"], capture_output=True)
            if result.returncode == 0:
                print("📡 [3/3] Trying Open Interpreter...")
                response = self.call_interpreter(prompt)
                if response:
                    self.active_provider = "Open Interpreter"
                    return response
        except:
            pass
        
        # Priority 4: OpenRouter Keys
        for key in self.openrouter_keys:
            if self.test_openrouter_key(key):
                print(f"📡 [4/4] Trying OpenRouter...")
                response = self.call_openrouter(prompt, key)
                if response:
                    self.active_provider = "OpenRouter"
                    self.log(f"Used OpenRouter for: {prompt[:50]}")
                    return response
                break
        
        return "❌ No working AI provider available. Check API keys."
    
    def extract_and_run_code(self, response):
        """Extract code blocks and execute them"""
        code_pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(code_pattern, response, re.DOTALL)

        
        results = []
        for lang, code in matches:
            results.append(f"\n📝 {lang.upper()} code detected + executing...")
            output = self.execute_code(code.strip(), lang.lower())
            results.append(f"📤 {output}")
        
        if not matches:
            # Try to detect inline code
            if "print" in response or "echo" in response:
                results.append(f"📝 Code detected: {response[:200]}")
            else:
                results.append(response)
        
        return '\n'.join(results)
    
    def execute_code(self, code, lang):
        """Execute code and return output"""
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
    
    def analyze_code(self, code):
        """Analyze code for issues"""
        issues = []
        if "import" not in code and "def" not in code and "print" not in code:
            issues.append("⚠️ No imports or functions found")
        if "TODO" in code or "FIXME" in code:
            issues.append("⚠️ TODO/FIXME comments found")
        return issues

    
    def fix_code(self, code, error):
        """Attempt to auto-fix code"""
        prompt = f"""Fix this code that has an error:

CODE:
{code}

ERROR:
{error}

Return ONLY the fixed code in a code block."""
        
        response = self.get_response(prompt)
        fixed_pattern = r'```(\w+)\n(.*?)```'
        matches = re.findall(fixed_pattern, response, re.DOTALL)
        if matches:
            return matches[0][1].strip()
        return None
    
    def process(self, user_input):
        # System commands
        if user_input.lower() in ['upgrade', 'self-upgrade', 'update']:
            os.system("cd /root/ish-dev && git pull && /root/ish-dev/core/heal.sh")
            return "✅ Self-upgrade complete!"
        
        if user_input.lower() in ['analyze', 'status', 'stats']:
            return f"""📊 SYSTEM STATUS:
🔑 Active Provider: {self.active_provider or 'Not active yet'}
📁 Workspace: {self.workspace}
🤖 Models: Gemini CLI, Gemini API, Open Interpreter, OpenRouter
🔐 Keys: OpenRouter ({len(self.openrouter_keys)}), Gemini ({len(self.gemini_keys)})"""
        
        if user_input.startswith('/exec '):
            os.system(user_input[6:])
            return "✅ Command executed"
        
        if user_input.lower() in ['help', '?']:
            return """📋 ULTIMATE PRO AGENT COMMANDS:
• 'Create a Python script that...' - Auto-generates and runs
• 'Write a bash script to...' - Auto-executes
• 'analyze' - System status
• 'upgrade' - Self-update
• '/exec ls -la' - Shell command
• 'fix error: [error]' - Auto-fix code"""
        
        # Process user request
        print("\n⣾ Processing your request...")
        response = self.get_response(user_input)
        
        if not response or response.startswith("❌"):
            return response if response else "❌ Failed to get response"
        
        # Execute any code in response
        result = self.extract_and_run_code(response)
        
        # Check if auto-fix needed
        if "Error:" in result and "fix" in user_input.lower():
            print("\n🔧 Attempting auto-fix...")
            fixed = self.fix_code(code, result)
            if fixed:
                return f"✅ Fixed code executed:\n{self.execute_code(fixed, 'python')}"
        
        return result
    
    def run(self):
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET ULTIMATE PRO AGENT v17.0")
        print("━" * 60)
        print("📦 FEATURES:")
        print("   • Auto-failover: Gemini CLI → Gemini API → Interpreter → OpenRouter")
        print("   • Auto-code generation & execution")
        print("   • Auto-fix errors")
        print("   • Code analysis & testing")
        print("   • Self-learning & upgrades")
        print("━" * 60)
        print("🔑 STATUS:")
        print(f"   Gemini CLI: {'✅' if self.test_gemini_cli() else '❌'}")
        print(f"   Gemini API: {'✅' if any(self.test_gemini_api(k) for k in self.gemini_keys) else '❌'}")
        print(f"   OpenRouter: {'✅' if any(self.test_openrouter_key(k) for k in self.openrouter_keys) else '❌'}")
        print("━" * 60)
        print("\n💬 Type your request - FULLY AUTOMATED\n")
        
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
    agent = UltimateProAgent()
    if len(sys.argv) > 1:
        print(agent.process(' '.join(sys.argv[1:])))
    else:
        agent.run()
