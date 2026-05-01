#!/usr/bin/env python3
"""
HOOPSTREET AUTONOMOUS AI AGENT v10.1 - FIXED
- Proper API key loading from credentials
- Multi-layer failover
- Automatic provider detection
"""

import sys, os, json, requests, time, subprocess
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

# ============ CONFIGURATION ============
KEYS_FILE = "/root/.hoopstreet/creds/ai_keys.json"
CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"

class AutonomousAIAgent:
    def __init__(self):
        self.api_keys = self.load_all_keys()
        self.working_provider = None
        self.current_model = None
        
    def load_all_keys(self):
        """Load keys from both JSON and plain text credentials"""
        keys = {
            "gemini": [],
            "openrouter": [],
            "github": []
        }
        
        # Load from JSON
        if os.path.exists(KEYS_FILE):
            try:
                with open(KEYS_FILE, 'r') as f:
                    data = json.load(f)
                    if "gemini" in data:
                        keys["gemini"] = data["gemini"]
                    if "openrouter" in data:
                        keys["openrouter"] = data["openrouter"]
                    if "github" in data:
                        keys["github"] = data["github"]
            except:
                pass
        
        # Also load from plain text credentials
        if os.path.exists(CREDS_FILE):
            with open(CREDS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1]
                        keys["openrouter"].append({"key": key, "priority": len(keys["openrouter"])+1, "status": "active"})
                    elif line.startswith("GEMINI_API_KEY=") or "AIzaSy" in line:
                        key = line.split("=", 1)[1] if "=" in line else line
                        if "AIzaSy" in key:
                            keys["gemini"].append({"key": key, "priority": len(keys["gemini"])+1, "status": "active"})
        
        return keys
    
    def test_gemini(self, api_key):
        """Test Gemini API key"""
        if not api_key or not api_key.startswith("AIzaSy"):
            return False
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False

    
    def test_openrouter(self, api_key):
        """Test OpenRouter API key"""
        if not api_key or not api_key.startswith("sk-or-v1"):
            return False
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def call_gemini(self, prompt, api_key, max_tokens=1000):
        """Call Gemini API"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            response = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": max_tokens}
                },
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "No response")
            return None
        except Exception as e:
            return None
    
    def call_openrouter(self, prompt, api_key, max_tokens=1000):
        """Call OpenRouter API"""
        models = ["openai/gpt-3.5-turbo", "meta-llama/llama-3-8b-instruct:free"]
        for model in models:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except:
                continue
        return None

    
    def call_openrouter_free(self, prompt, max_tokens=1000):
        """Call free OpenRouter endpoints (no key needed)"""
        free_models = [
            "meta-llama/llama-3-8b-instruct:free",
            "microsoft/phi-3-mini-4k-instruct:free"
        ]
        for model in free_models:
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": max_tokens
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except:
                continue
        return None
    
    def get_response(self, prompt):
        """Get response with automatic failover"""
        # Try Gemini keys first
        for gemini in self.api_keys.get("gemini", []):
            key = gemini.get("key", "")
            if key:
                print(f"🔄 Trying Gemini (priority {gemini.get('priority', '?')})...")
                response = self.call_gemini(prompt, key)
                if response:
                    self.working_provider = "gemini"
                    return response
        
        # Try OpenRouter keys
        for openrouter in self.api_keys.get("openrouter", []):
            key = openrouter.get("key", "")
            if key:
                print(f"🔄 Trying OpenRouter (priority {openrouter.get('priority', '?')})...")
                response = self.call_openrouter(prompt, key)
                if response:
                    self.working_provider = "openrouter"
                    return response
        
        # Try free OpenRouter
        print("🔄 Trying free OpenRouter models...")
        response = self.call_openrouter_free(prompt)
        if response:
            self.working_provider = "openrouter_free"
            return response
        
        return "⚠️ No AI providers available. Please check your API keys."
    
    def execute_command(self, cmd):
        """Execute shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Error: {e}"

    
    def interactive_mode(self):
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET AUTONOMOUS AI AGENT v10.1")
        print("━" * 60)
        print("📡 Auto-failover: Enabled")
        print("🔑 Gemini API: {} keys".format(len(self.api_keys.get("gemini", []))))
        print("🔑 OpenRouter API: {} keys".format(len(self.api_keys.get("openrouter", []))))
        print("━" * 60)
        print("\n💬 Type naturally | /exit to quit\n")
        
        while True:
            try:
                user_input = input("🚀 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['/exit', 'exit']:
                    print("\n👋 Goodbye!")
                    break
                elif user_input.startswith('/exec '):
                    cmd = user_input[6:]
                    output = self.execute_command(cmd)
                    print(f"\n{output}\n")
                else:
                    print("\n🤖 Thinking...")
                    response = self.get_response(user_input)
                    print(f"\n{response}\n")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    agent = AutonomousAIAgent()
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        response = agent.get_response(prompt)
        print(response)
    else:
        agent.interactive_mode()

if __name__ == "__main__":
    main()
