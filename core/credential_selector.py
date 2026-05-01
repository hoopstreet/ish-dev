#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET REAL-TIME CREDENTIAL SELECTOR
- Tests each API key in real-time
- Automatically picks working keys
- Maintains fallback chain
- Updates key status dynamically
"""

import sys, os, json, requests, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

KEYS_FILE = "/root/.hoopstreet/creds/ai_keys.json"
CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"
STATUS_FILE = "/root/ish-dev/.key_status.json"

class CredentialSelector:
    def __init__(self):
        self.keys = self.load_keys()
        self.key_status = self.load_status()
        self.working_provider = None
        self.working_key = None
        
    def load_keys(self):
        """Load all API keys"""
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
                    for provider in ["gemini", "openrouter", "github"]:
                        if provider in data:
                            keys[provider] = data[provider]
            except:
                pass
        
        # Also load from plain text
        if os.path.exists(CREDS_FILE):
            with open(CREDS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if "sk-or-v1" in line:
                        key = line.split("=", 1)[1] if "=" in line else line
                        keys["openrouter"].append({"key": key, "priority": len(keys["openrouter"])+1})
                    elif "AIzaSy" in line:
                        key = line.split("=", 1)[1] if "=" in line else line
                        keys["gemini"].append({"key": key, "priority": len(keys["gemini"])+1})
        
        return keys
    
    def load_status(self):
        """Load saved key status"""
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {"gemini": {}, "openrouter": {}, "last_updated": None}
        return {"gemini": {}, "openrouter": {}, "last_updated": None}

    
    def save_status(self):
        """Save key status"""
        self.key_status["last_updated"] = str(datetime.now())
        with open(STATUS_FILE, 'w') as f:
            json.dump(self.key_status, f, indent=2)
    
    def test_gemini_key(self, key_data):
        """Test a single Gemini key"""
        key = key_data.get("key")
        priority = key_data.get("priority", 999)
        
        if not key or not key.startswith("AIzaSy"):
            return None
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return {
                    "provider": "gemini",
                    "key": key,
                    "priority": priority,
                    "status": "working",
                    "test_time": str(datetime.now())
                }
            else:
                return {
                    "provider": "gemini",
                    "key": key[:20] + "...",
                    "priority": priority,
                    "status": f"failed (HTTP {response.status_code})"
                }
        except Exception as e:
            return {
                "provider": "gemini",
                "key": key[:20] + "...",
                "priority": priority,
                "status": f"failed ({str(e)[:30]})"
            }
    
    def test_openrouter_key(self, key_data):
        """Test a single OpenRouter key"""
        key = key_data.get("key")
        priority = key_data.get("priority", 999)
        
        if not key or not key.startswith("sk-or-v1"):
            return None
        
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "provider": "openrouter",
                    "key": key[:20] + "...",
                    "priority": priority,
                    "status": "working",
                    "test_time": str(datetime.now())
                }
            else:
                return {
                    "provider": "openrouter",
                    "key": key[:20] + "...",
                    "priority": priority,
                    "status": f"failed (HTTP {response.status_code})"
                }
        except Exception as e:
            return {
                "provider": "openrouter",
                "key": key[:20] + "...",
                "priority": priority,
                "status": f"failed ({str(e)[:30]})"
            }
    
    def test_free_openrouter(self):
        """Test free OpenRouter endpoints"""
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
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 5
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    return {
                        "provider": "openrouter_free",
                        "model": model,
                        "status": "working",
                        "test_time": str(datetime.now())
                    }
            except:
                continue
        return None
    
    def scan_all_keys(self):
        """Scan and test all API keys"""
        print("\n🔍 SCANNING API KEYS...")
        print("━" * 50)
        
        results = {
            "gemini": [],
            "openrouter": [],
            "free": None
        }
        
        # Test Gemini keys
        print("📡 Testing Gemini keys...")
        for key_data in self.keys.get("gemini", []):
            result = self.test_gemini_key(key_data)
            if result:
                results["gemini"].append(result)
                status_icon = "✅" if "working" in result.get("status", "") else "❌"
                print(f"   {status_icon} Gemini (p{result['priority']}): {result.get('status', 'unknown')}")
        
        # Test OpenRouter keys
        print("📡 Testing OpenRouter keys...")
        for key_data in self.keys.get("openrouter", []):
            result = self.test_openrouter_key(key_data)
            if result:
                results["openrouter"].append(result)
                status_icon = "✅" if "working" in result.get("status", "") else "❌"
                print(f"   {status_icon} OpenRouter (p{result['priority']}): {result.get('status', 'unknown')}")

        
        # Test free models
        print("📡 Testing free OpenRouter models...")
        free_result = self.test_free_openrouter()
        if free_result:
            results["free"] = free_result
            print(f"   ✅ Free models: {free_result.get('model', 'unknown')}")
        else:
            print(f"   ❌ Free models: not available")
        
        # Save results
        self.key_status = results
        self.save_status()
        
        return results
    
    def get_best_working_key(self):
        """Get the best working key based on scan"""
        # If we have cached working key that's recent (< 1 hour), use it
        if self.working_provider and self.working_key:
            return self.working_provider, self.working_key
        
        # Scan for working keys
        results = self.scan_all_keys()
        
        # Priority order: Gemini > OpenRouter > Free
        for gemini in results.get("gemini", []):
            if "working" in gemini.get("status", ""):
                self.working_provider = "gemini"
                self.working_key = gemini["key"]
                return "gemini", gemini["key"]
        
        for openrouter in results.get("openrouter", []):
            if "working" in openrouter.get("status", ""):
                self.working_provider = "openrouter"
                self.working_key = openrouter["key"]
                return "openrouter", openrouter["key"]
        
        if results.get("free"):
            self.working_provider = "free"
            self.working_key = results["free"].get("model", "")
            return "free", self.working_key
        
        return None, None


    
    def list_all_models(self):
        """List all available AI models"""
        models = {
            "gemini": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
            "openrouter_paid": [
                "openai/gpt-4-turbo", "openai/gpt-3.5-turbo",
                "anthropic/claude-3-opus", "anthropic/claude-3-sonnet",
                "google/gemini-pro", "meta-llama/llama-3-70b-instruct",
                "deepseek/deepseek-chat", "mistralai/mistral-large"
            ],
            "openrouter_free": [
                "meta-llama/llama-3-8b-instruct:free",
                "microsoft/phi-3-mini-4k-instruct:free"
            ]
        }
        return models

def main():
    selector = CredentialSelector()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "scan":
            selector.scan_all_keys()
        elif cmd == "list":
            models = selector.list_all_models()
            print("\n📋 AVAILABLE AI MODELS:")
            print("━" * 50)
            print("\n🔥 Gemini Models:")
            for m in models["gemini"]:
                print(f"   • {m}")
            print("\n💰 OpenRouter Paid Models:")
            for m in models["openrouter_paid"]:
                print(f"   • {m}")
            print("\n🎁 OpenRouter Free Models:")
            for m in models["openrouter_free"]:
                print(f"   • {m}")
        elif cmd == "status":
            if os.path.exists(STATUS_FILE):
                with open(STATUS_FILE, 'r') as f:
                    data = json.load(f)
                    print("\n📊 KEY STATUS:")
                    print("━" * 50)
                    for provider in ["gemini", "openrouter"]:
                        print(f"\n{provider.upper()}:")
                        for key in data.get(provider, []):
                            print(f"   P{key.get('priority', '?')}: {key.get('status', 'unknown')}")
            else:
                print("No status available. Run: python3 credential_selector.py scan")
        else:
            print("Commands: scan, list, status")
    else:
        # Interactive test
        print("\n🔑 HOOPSTREET CREDENTIAL SELECTOR")
        print("━" * 50)
        provider, key = selector.get_best_working_key()
        if provider:
            print(f"\n✅ Best working provider: {provider}")
            print(f"🔑 Key: {key[:30]}...")
        else:
            print("\n❌ No working API keys found")

if __name__ == "__main__":
    main()
