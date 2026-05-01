#!/usr/bin/env python3
import subprocess, json, time, sys, os, re, threading
import urllib.request, urllib.error
from pathlib import Path
from datetime import datetime
from itertools import cycle

class VisualHealingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.dna_file = Path("/root/DNA.md")
        self.spinner_running = False
        self.spinner_thread = None
        
    def spinner(self, message="Processing"):
        """Show animated spinner"""
        spinner_cycle = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while self.spinner_running:
            sys.stdout.write(f'\r{" " * 50}\r')
            sys.stdout.write(f'\r{next(spinner_cycle)} {message}...')
            sys.stdout.flush()
            time.sleep(0.1)
    
    def start_spinner(self, message):
        self.spinner_running = True
        self.spinner_thread = threading.Thread(target=self.spinner, args=(message,))
        self.spinner_thread.daemon = True
        self.spinner_thread.start()
    
    def stop_spinner(self, success=True, result=""):
        self.spinner_running = False
        if self.spinner_thread:
            self.spinner_thread.join(timeout=0.5)
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        if success:
            print(f"✅ {result}")
        else:
            print(f"❌ {result}")
    
    def run_tests(self):
        try:
            self.start_spinner("Running tests")
            r = subprocess.run(["pytest", "-v", "--tb=line"], 
                              capture_output=True, text=True, timeout=30)
            self.stop_spinner(True, "Tests complete")
            return r.returncode == 0, (r.stdout + r.stderr)[-800:]
        except Exception as e:
            self.stop_spinner(False, f"Test error: {e}")
            return False, str(e)
    
    def fix_code(self, code, error):
        if not self.api_key:
            return None
        self.start_spinner("Contacting OpenRouter AI")
        prompt = f"Fix this Python code. Return ONLY corrected code.\n\nCODE:\n{code}\n\nERROR:\n{error[:600]}\n\nFIXED CODE:"
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.2
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ish.iphone.local",
                "X-Title": "iSH Self-Healing Agent"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                resp = json.loads(response.read().decode())
                fixed = resp['choices'][0]['message']['content']
                if '```python' in fixed:
                    fixed = fixed.split('```python')[1].split('```')[0]
                elif '```' in fixed:
                    fixed = fixed.split('```')[1].split('```')[0]
                self.stop_spinner(True, "AI fix received")
                return fixed.strip()
        except Exception as e:
            self.stop_spinner(False, f"API error: {e}")
            return None
    
    def heal(self, filepath, max_attempts=3):
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"❌ File not found: {filepath}")
            return False
        
        print("\n" + "="*60)
        print("🤖 SELF-HEALING AGENT ACTIVE 🤖")
        print("="*60)
        
        for attempt in range(1, max_attempts+1):
            print(f"\n📌 Attempt {attempt}/{max_attempts}")
            
            with open(filepath) as f:
                code = f.read()
            
            print("🔍 Analyzing code...")
            passed, err = self.run_tests()
            
            if passed:
                print("\n✨ No issues detected! ✨")
                self._log(filepath.name, "healthy", attempt)
                return True
            
            print(f"\n⚠️  Issues detected:")
            error_lines = err.split('\n')[:5]
            for line in error_lines:
                if 'Error' in line or 'assert' in line:
                    print(f"   {line[:80]}")
            
            if attempt == max_attempts:
                print("\n💀 Max attempts reached - manual intervention needed")
                return False
            
            print("\n🔧 Generating fix...")
            fixed = self.fix_code(code, err)
            
            if fixed:
                backup = Path(f"{filepath}.backup")
                backup.write_text(code)
                filepath.write_text(fixed)
                print("📝 Fix applied successfully!")
                print("🔄 Re-running tests...")
                time.sleep(1)
            else:
                print("⚠️ Could not generate fix")
                return False
        
        return False
    
    def watch(self, filepath, interval=3):
        filepath = Path(filepath)
        print("\n" + "="*60)
        print("👁️  VISUAL MONITORING MODE ACTIVE")
        print("="*60)
        print(f"📁 Target: {filepath.name}")
        print(f"⏱️  Interval: {interval}s")
        print("⌨️  Press Ctrl+C to stop\n")
        
        last = filepath.stat().st_mtime if filepath.exists() else 0
        
        while True:
            time.sleep(interval)
            if filepath.exists() and filepath.stat().st_mtime != last:
                last = filepath.stat().st_mtime
                print(f"\n🔔 [{datetime.now().strftime('%H:%M:%S')}] Change detected!")
                passed, _ = self.run_tests()
                if passed:
                    print("🎉 All tests passing!")
                else:
                    print("⚠️ Test failures detected - initiating heal")
                    self.heal(filepath)
    
    def _log(self, filename, status, attempt):
        timestamp = datetime.now().isoformat()
        with open(self.dna_file, 'a') as f:
            f.write(f"\n## {timestamp} - {filename}\n")
            f.write(f"Status: {status} (attempt {attempt})\n")
            f.write(f"---\n")
        print(f"\n📋 Logged to DNA.md")

def setup():
    Path("/root/broken.py").write_text('def add(a, b):\n    return a + b')
    Path("/root/test_broken.py").write_text('''from broken import add

def test_add():
    assert add(2, 3) == 5
    assert add(10, 5) == 15

def test_negative():
    assert add(-1, 1) == 0
''')
    print("📁 Demo files created")
    print("   - broken.py (contains bug: a + b)")
    print("   - test_broken.py (expects addition)\n")

def interactive_menu():
    print("\n" + "="*50)
    print("🎨 VISUAL SELF-HEALING AGENT")
    print("="*50)
    print("\nOptions:")
    print("  1. 🔧 One-time heal (fix broken.py)")
    print("  2. 👁️  Watch mode (monitor for changes)")
    print("  3. 🧪 Run tests only")
    print("  0. ❌ Exit")
    
    choice = input("\n👉 Choose (0-3): ").strip()
    return choice

if __name__ == "__main__":
    setup()
    agent = VisualHealingAgent()
    
    # Check command line args
    if len(sys.argv) > 1:
        if sys.argv[1] == "heal":
            agent.heal("/root/broken.py")
        elif sys.argv[1] == "watch":
            agent.watch("/root/broken.py")
        else:
            agent.heal(sys.argv[1])
    else:
        # Interactive mode
        while True:
            choice = interactive_menu()
            if choice == "1":
                agent.heal("/root/broken.py")
            elif choice == "2":
                agent.watch("/root/broken.py")
            elif choice == "3":
                agent.run_tests()
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")
