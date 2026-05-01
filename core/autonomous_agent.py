#!/usr/bin/env python3
"""
HOOPSTREET AUTONOMOUS AI AGENT v10.0
- Multi-layer API failover (Gemini → OpenRouter Free → OpenRouter Paid)
- Self-healing credential rotation
- Automatic agent recovery
- No human intervention required
"""

import sys, os, json, requests, time, subprocess
from datetime import datetime
from typing import Optional, Dict, List, Tuple

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

# ============ CONFIGURATION ============
KEYS_FILE = "/root/.hoopstreet/creds/ai_keys.json"
LOG_FILE = "/root/ish-dev/docs/agent.log"
LOCK_FILE = "/root/ish-dev/.agent_lock"
PRIMARY_AGENT = None  # Will be set to working provider

class AutonomousAIAgent:
    def __init__(self):
        self.keys = self.load_keys()
        self.working_provider = None
        self.failover_history = []
        self.conversation = []
        self.load_lock()
    
    def load_keys(self):
        """Load all API keys from secure storage"""
        try:
            with open(KEYS_FILE, 'r') as f:
                return json.load(f)
        except:
            return self.create_default_keys()
    
    def create_default_keys(self):
        """Create default key structure if missing"""
        default = {
            "gemini": [{"key": "", "priority": 1, "status": "unknown"}],
            "openrouter": [{"key": "", "priority": 1, "status": "unknown"}],
            "github": [{"key": "", "priority": 1, "status": "unknown"}],
            "supabase": {"url": "", "anon_key": ""},
            "telegram": {"bot_token": ""}
        }
        return default
    
    def save_lock(self):
        """Save current working provider to lock file"""
        with open(LOCK_FILE, 'w') as f:
            json.dump({
                "working_provider": self.working_provider,
                "timestamp": str(datetime.now()),
                "failover_history": self.failover_history[-10:]
            }, f)
    
    def load_lock(self):
        """Load last working provider from lock file"""
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE, 'r') as f:
                    data = json.load(f)
                    self.working_provider = data.get("working_provider")
            except:
                pass
    
    def test_gemini(self, api_key: str) -> bool:
        """Test if Gemini API key works"""
        if not api_key:
            return False
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(
                url,
                json={"contents": [{"parts": [{"text": "test"}]}]},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def test_openrouter(self, api_key: str) -> bool:
        """Test if OpenRouter API key works"""
        if not api_key:
            return False
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            return response.status_code in [200, 201]
        except:
            return False

    
    def test_free_model(self) -> bool:
        """Test free OpenRouter models"""
        free_models = [
            "openai/gpt-3.5-turbo",
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
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 10
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    return True
            except:
                continue
        return False
    
    def find_working_provider(self) -> Tuple[str, str]:
        """
        Auto-discover working API provider
        Returns: (provider_name, api_key)
        """
        print("\n🔍 Auto-discovering working AI provider...")
        
        # Layer 1: Try Gemini keys
        for gemini in self.keys.get("gemini", []):
            key = gemini.get("key", "")
            if key and self.test_gemini(key):
                print(f"✅ Gemini API working (priority {gemini.get('priority')})")
                return ("gemini", key)
        
        # Layer 2: Try OpenRouter keys
        for openrouter in self.keys.get("openrouter", []):
            key = openrouter.get("key", "")
            if key and self.test_openrouter(key):
                print(f"✅ OpenRouter API working (priority {openrouter.get('priority')})")
                return ("openrouter", key)
        
        # Layer 3: Try free OpenRouter models (no key)
        if self.test_free_model():
            print("✅ OpenRouter Free Models working")
            return ("openrouter_free", "none")
        
        # Layer 4: Fallback to local agent
        print("⚠️ No API working - Falling back to local agent")
        return ("local", "none")
    
    def ai_complete(self, prompt: str, max_tokens: int = 1000) -> str:
        """AI completion with automatic failover"""
        global PRIMARY_AGENT
        
        # If we have a working provider cached, use it
        if not self.working_provider:
            provider, key = self.find_working_provider()
            self.working_provider = provider
            self.save_lock()
        else:
            provider = self.working_provider
            key = self.get_key_for_provider(provider)
        
        # Route to appropriate provider
        if provider == "gemini":
            return self.call_gemini(prompt, key, max_tokens)
        elif provider == "openrouter":
            return self.call_openrouter(prompt, key, max_tokens)
        elif provider == "openrouter_free":
            return self.call_openrouter_free(prompt, max_tokens)
        else:
            return self.local_response(prompt)
    
    def get_key_for_provider(self, provider: str) -> str:
        """Get API key for specific provider"""
        if provider == "gemini":
            for g in self.keys.get("gemini", []):
                if g.get("status") == "active":
                    return g.get("key", "")
        elif provider == "openrouter":
            for o in self.keys.get("openrouter", []):
                if o.get("status") == "active":
                    return o.get("key", "")
        return ""
    
    def call_gemini(self, prompt: str, api_key: str, max_tokens: int) -> str:
        """Call Gemini API"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
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
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
            else:
                # Key may have failed, reset provider
                self.working_provider = None
                return self.ai_complete(prompt, max_tokens)
        except Exception as e:
            self.working_provider = None
            return self.ai_complete(prompt, max_tokens)
    
    def call_openrouter(self, prompt: str, api_key: str, max_tokens: int) -> str:
        """Call OpenRouter API"""
        models = ["openai/gpt-3.5-turbo", "anthropic/claude-3-haiku", "google/gemini-flash"]
        
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
        
        self.working_provider = None
        return self.ai_complete(prompt, max_tokens)
    def call_openrouter_free(self, prompt: str, max_tokens: int) -> str:
        """Call free OpenRouter models"""
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
        
        return self.local_response(prompt)
    
    def local_response(self, prompt: str) -> str:
        """Fallback local response when no API works"""
        return f"""⚠️ AI API temporarily unavailable.

Your request: "{prompt[:100]}..."

💡 To fix:
1. Check API keys: /root/.hoopstreet/creds/ai_keys.json
2. Run: /heal
3. Or use: interpreter (local mode)

The system will auto-recover when APIs are available."""

    def execute_command(self, cmd: str) -> str:
        """Execute shell command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.stdout else result.stderr
        except:
            return "Command execution failed"

    def interactive_mode(self):
        """Main interactive loop"""
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET AUTONOMOUS AI AGENT v10.0")
        print("━" * 60)
        print(f"📡 Provider: {self.working_provider or 'Auto-discovery'}")
        print("🔄 Auto-failover: Enabled")
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
                elif user_input == '/status':
                    print(f"\n📡 Provider: {self.working_provider}")
                    print(f"📊 Failover history: {len(self.failover_history)} events")
                else:
                    print("\n🤖 Thinking...")
                    response = self.ai_complete(user_input)
                    print(f"\n{response}\n")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    agent = AutonomousAIAgent()
    
    # Command line mode
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        response = agent.ai_complete(prompt)
        print(response)
    else:
        agent.interactive_mode()

if __name__ == "__main__":
    main()
