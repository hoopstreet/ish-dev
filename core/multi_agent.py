#!/usr/bin/env python3
import subprocess, json, time, sys, os, threading, urllib.request
from pathlib import Path
from datetime import datetime
from itertools import cycle

class MultiModelAgent:
    def __init__(self):
        # Gemini free API keys (rotating)
        self.gemini_keys = ['AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas']
        self.current_gemini_idx = 0
        self.gemini_failed = [False] * len(self.gemini_keys)
        
        # OpenRouter backup keys (free then paid)
        self.openrouter_free_keys = ['AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA']
        self.openrouter_paid_keys = ['AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY']  # Add paid keys here
        
        self.current_model = "gemini"
        self.dna_file = Path("/root/DNA.md")
        self.spinner_running = False
        
    def spinner(self, message):
        chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        i = 0
        while self.spinner_running:
            sys.stdout.write(f'\r{chars[i % len(chars)]} {message}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def start_spinner(self, msg):
        self.spinner_running = True
        threading.Thread(target=self.spinner, args=(msg,), daemon=True).start()
    
    def stop_spinner(self, success=True, msg=""):
        self.spinner_running = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        print(f"{'✅' if success else '❌'} {msg}")
    
    def call_gemini(self, prompt, key_idx=None):
        """Call Gemini free API with key rotation"""
        if key_idx is None:
            key_idx = self.current_gemini_idx
        
        if self.gemini_failed[key_idx]:
            return None, f"Key {key_idx} marked as failed"
        
        api_key = self.gemini_keys[key_idx]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 800
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text, None
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                self.gemini_failed[key_idx] = True
                return None, f"QUOTA_EXCEEDED"
            return None, error_msg
    
    def get_next_gemini_key(self):
        """Find next working Gemini key"""
        for i in range(len(self.gemini_keys)):
            if not self.gemini_failed[i]:
                self.current_gemini_idx = i
                return i
        return None
    
    def call_openrouter(self, prompt, use_paid=False):
        """Call OpenRouter API (free or paid)"""
        keys = self.openrouter_paid_keys if use_paid else self.openrouter_free_keys
        
        if not keys:
            return None, "No keys available"
        
        model = "google/gemini-2.0-flash-exp:free" if not use_paid else "openai/gpt-4o-mini"
        
        for api_key in keys:
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 800,
                "temperature": 0.2
            }
            
            try:
                req = urllib.request.Request(
                    "https://openrouter.ai/api/v1/chat/completions",
                    data=json.dumps(data).encode(),
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode())
                    text = result['choices'][0]['message']['content']
                    return text, None
            except Exception as e:
                continue
        
        return None, "All OpenRouter keys failed"
    
    def fix_code_with_failover(self, code, error):
        """Auto-switch between models with failover"""
        prompt = f"Fix this Python code. Return ONLY fixed code.\n\nCODE:\n{code}\n\nERROR:\n{error}\n\nFIXED:"
        
        # Strategy 1: Try Gemini free (with key rotation)
        self.start_spinner("Trying Gemini Free")
        working_key = self.get_next_gemini_key()
        
        if working_key is not None:
            result, err = self.call_gemini(prompt, working_key)
            if result:
                self.stop_spinner(True, "Gemini fixed it!")
                self.current_model = f"gemini-key{working_key}"
                return self._clean_code(result)
            elif err == "QUOTA_EXCEEDED":
                print(f"\n⚠️ Gemini key {working_key} quota exceeded, switching...")
        
        # Strategy 2: Try all Gemini keys
        self.start_spinner("Trying all Gemini keys")
        for i in range(len(self.gemini_keys)):
            if not self.gemini_failed[i]:
                result, err = self.call_gemini(prompt, i)
                if result:
                    self.stop_spinner(True, f"Gemini key {i} worked!")
                    self.current_gemini_idx = i
                    return self._clean_code(result)
        
        # Strategy 3: Try OpenRouter free tier
        self.start_spinner("Trying OpenRouter Free")
        result, err = self.call_openrouter(prompt, use_paid=False)
        if result:
            self.stop_spinner(True, "OpenRouter Free fixed it!")
            self.current_model = "openrouter-free"
            return self._clean_code(result)
        
        # Strategy 4: Try OpenRouter paid tier (if available)
        if self.openrouter_paid_keys:
            self.start_spinner("Trying OpenRouter Paid")
            result, err = self.call_openrouter(prompt, use_paid=True)
            if result:
                self.stop_spinner(True, "OpenRouter Paid fixed it!")
                self.current_model = "openrouter-paid"
                return self._clean_code(result)
        
        self.stop_spinner(False, "All models failed")
        return None
    
    def _clean_code(self, text):
        """Extract clean code from response"""
        if '```python' in text:
            text = text.split('```python')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        return text.strip()
    
    def run_tests(self):
        try:
            self.start_spinner("Testing code")
            result = subprocess.run(
                ["python3", "-c", "import sys; sys.path.insert(0,'/root'); from broken import add; assert add(2,3)==5; print('OK')"],
                capture_output=True, text=True, timeout=10
            )
            self.stop_spinner(True, "Tests done")
            return result.returncode == 0, result.stderr
        except Exception as e:
            self.stop_spinner(False, f"Test error")
            return False, str(e)
    
    def heal(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ Not found: {filepath}")
            return False
        
        print("\n" + "="*60)
        print("🤖 MULTI-MODEL HEALING AGENT 🤖")
        print("="*60)
        print(f"📋 Strategy: Gemini Free → Gemini Keys → OpenRouter Free → OpenRouter Paid")
        print(f"🎯 Current: {self.current_model}")
        
        for attempt in range(1, 4):
            print(f"\n📌 Attempt {attempt}/3")
            
            with open(filepath) as f:
                code = f.read()
            
            print(f"📄 Code: {code.strip()[:60]}")
            passed, error = self.run_tests()
            
            if passed:
                print("✨ CODE IS HEALTHY! ✨")
                self._log(filepath.name, "healthy", attempt, self.current_model)
                return True
            
            print(f"⚠️  Failure: {error[:100]}")
            
            if attempt == 3:
                print("💀 All attempts exhausted")
                return False
            
            print("🔧 Generating fix...")
            fixed = self.fix_code_with_failover(code, error)
            
            if fixed:
                backup = Path(f"{filepath}.backup")
                backup.write_text(code)
                filepath.write_text(fixed)
                print("💾 Fix applied, re-testing...")
                time.sleep(1)
            else:
                print("❌ No fix generated")
                return False
        
        return False
    
    def watch(self, filepath):
        filepath = Path(filepath)
        print("\n" + "="*60)
        print("👁️ MULTI-MODEL WATCH MODE")
        print("="*60)
        print(f"📁 Monitoring: {filepath.name}")
        print("🔄 Auto-switch between: Gemini → OpenRouter\n")
        
        last = filepath.stat().st_mtime if filepath.exists() else 0
        while True:
            time.sleep(2)
            if filepath.exists() and filepath.stat().st_mtime != last:
                last = filepath.stat().st_mtime
                print(f"\n🔔 [{datetime.now().strftime('%H:%M:%S')}] Change!")
                self.heal(filepath)
    
    def _log(self, name, status, attempt, model):
        with open(self.dna_file, 'a') as f:
            f.write(f"\n## {datetime.now().isoformat()} - {name}\n")
            f.write(f"Status: {status} | Model: {model} | Attempt: {attempt}\n---\n")
        print(f"📝 Logged to DNA.md (Model: {model})")

def setup():
    Path("/root/broken.py").write_text('def add(a,b): return a + b')
    Path("/root/test.py").write_text('from broken import add\nassert add(2,3)==5\nprint("OK")')
    print("📁 Demo: broken.py has bug (a + b)")

def show_status(agent):
    print("\n" + "="*50)
    print("📊 MODEL STATUS")
    print("="*50)
    print(f"🎯 Current: {agent.current_model}")
    print(f"🔑 Gemini keys: {len([k for k, f in zip(agent.gemini_keys, agent.gemini_failed) if not f])}/{len(agent.gemini_keys)} active")
    print(f"🆓 OpenRouter Free: {len(agent.openrouter_free_keys)} key(s)")
    print(f"💎 OpenRouter Paid: {len(agent.openrouter_paid_keys)} key(s)")

def menu():
    print("\n" + "="*50)
    print("🎯 MULTI-MODEL HEALING AGENT")
    print("="*50)
    print("1. 🔧 Heal (auto failover)")
    print("2. 👁️ Watch mode")
    print("3. 📊 Show model status")
    print("4. 🧪 Quick test")
    print("0. Exit")
    return input("\n👉 Choose: ").strip()

if __name__ == "__main__":
    setup()
    agent = MultiModelAgent()
    
    # Configure your Gemini keys here
    print("\n⚙️ CONFIGURATION:")
    print("Please add your Gemini API keys to the script")
    print("Edit: /root/multi_agent.py - line 15-17")
    
    while True:
        choice = menu()
        if choice == "1":
            agent.heal("/root/broken.py")
        elif choice == "2":
            agent.watch("/root/broken.py")
        elif choice == "3":
            show_status(agent)
        elif choice == "4":
            passed, err = agent.run_tests()
            print(f"\n✅ Tests passed: {passed}")
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
