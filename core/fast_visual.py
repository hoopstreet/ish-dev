#!/usr/bin/env python3
import subprocess, json, time, sys, os, threading
from pathlib import Path
from datetime import datetime
from itertools import cycle

class FastVisualAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
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
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
    
    def run_tests(self):
        try:
            self.start_spinner("Testing")
            # Use python directly instead of pytest for speed
            result = subprocess.run(
                ["python3", "-c", "import sys; sys.path.insert(0,'/root'); from broken import add; assert add(2,3)==5; print('OK')"],
                capture_output=True, text=True, timeout=10
            )
            self.stop_spinner(True, "Tests done")
            return result.returncode == 0, result.stderr
        except subprocess.TimeoutExpired:
            self.stop_spinner(False, "Test timeout")
            return False, "Timeout"
        except Exception as e:
            self.stop_spinner(False, f"Error: {e}")
            return False, str(e)
    
    def fix_with_api(self, code, error):
        if not self.api_key:
            return None
        self.start_spinner("Contacting AI")
        prompt = f"Fix this Python code. Return ONLY fixed code.\n\nCODE:\n{code}\n\nERROR:\n{error}\n\nFIXED:"
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                fixed = json.loads(resp.read())['choices'][0]['message']['content']
                if '```' in fixed:
                    fixed = fixed.split('```')[1].split('```')[0]
                    if fixed.startswith('python'):
                        fixed = fixed[6:]
                self.stop_spinner(True, "AI response received")
                return fixed.strip()
        except Exception as e:
            self.stop_spinner(False, f"API error: {e}")
            return None
    
    def heal(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ Not found: {filepath}")
            return False
        
        print("\n" + "="*50)
        print("🤖 SELF-HEALING ACTIVE 🤖")
        print("="*50)
        
        for attempt in range(1, 4):
            print(f"\n▶️ Attempt {attempt}/3")
            
            with open(filepath) as f:
                code = f.read()
            
            print("📖 Current code:")
            print(f"   {code.strip()}")
            
            print("\n🔍 Running tests...")
            passed, error = self.run_tests()
            
            if passed:
                print("✨ NO ISSUES FOUND ✨")
                self._log(filepath.name, "healthy", attempt)
                return True
            
            print(f"⚠️  Test failed: {error[:100]}")
            
            if attempt == 3:
                print("💀 Max attempts - manual fix needed")
                return False
            
            print("🔧 Attempting to fix...")
            
            # Try API fix first
            fixed = self.fix_with_api(code, error)
            
            # Fallback to simple rule-based fix
            if not fixed and 'a + b' in code:
                fixed = code.replace('a + b', 'a + b')
                print("⚙️ Applied rule-based fix (changed '-' to '+')")
            
            if fixed:
                backup = Path(f"{filepath}.backup")
                backup.write_text(code)
                filepath.write_text(fixed)
                print("💾 Fix saved, re-testing...")
                time.sleep(1)
            else:
                print("❌ Could not generate fix")
                return False
        
        return False
    
    def watch(self, filepath):
        filepath = Path(filepath)
        print("\n" + "="*50)
        print("👁️ WATCH MODE ACTIVE")
        print("="*50)
        print(f"📁 Watching: {filepath.name}")
        print("Press Ctrl+C to stop\n")
        
        last = filepath.stat().st_mtime if filepath.exists() else 0
        
        while True:
            time.sleep(2)
            if filepath.exists() and filepath.stat().st_mtime != last:
                last = filepath.stat().st_mtime
                print(f"\n🔔 [{datetime.now().strftime('%H:%M:%S')}] File changed!")
                self.heal(filepath)
    
    def _log(self, name, status, attempt):
        with open(self.dna_file, 'a') as f:
            f.write(f"\n## {datetime.now().isoformat()} - {name}\n")
            f.write(f"Status: {status} (attempt {attempt})\n---\n")
        print("📝 Logged to DNA.md")

def setup():
    Path("/root/broken.py").write_text('def add(a,b): return a + b')
    Path("/root/test.py").write_text('from broken import add\nassert add(2,3)==5\nprint("OK")')
    print("📁 Demo ready: broken.py has bug (a + b instead of a + b)")

def menu():
    print("\n" + "="*50)
    print("🎨 FAST VISUAL HEALING AGENT")
    print("="*50)
    print("1. 🔧 One-time heal")
    print("2. 👁️ Watch mode")
    print("3. 🧪 Quick test")
    print("0. Exit")
    return input("\n👉 Choose: ").strip()

if __name__ == "__main__":
    setup()
    agent = FastVisualAgent()
    
    # Need urllib for API calls
    import urllib.request
    
    while True:
        choice = menu()
        if choice == "1":
            agent.heal("/root/broken.py")
        elif choice == "2":
            agent.watch("/root/broken.py")
        elif choice == "3":
            passed, err = agent.run_tests()
            print(f"\nTests passed: {passed}")
            if not passed:
                print(f"Error: {err}")
        elif choice == "0":
            print("\n👋 Bye!")
            break
        else:
            print("❌ Invalid choice")
