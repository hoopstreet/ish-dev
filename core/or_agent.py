#!/usr/bin/env python3
import subprocess, json, time, sys, os, re, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

class HealingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.dna_file = Path("/root/DNA.md")
        if not self.api_key:
            print("⚠️  NO API KEY - Run: export OPENROUTER_API_KEY='sk-or-v1-...'")
    
    def run_tests(self):
        try:
            r = subprocess.run(["pytest", "-v", "--tb=short"], 
                              capture_output=True, text=True, timeout=30)
            return r.returncode == 0, (r.stdout + r.stderr)[-800:]
        except: 
            return False, "pytest error"
    
    def fix_code(self, code, error):
        if not self.api_key: 
            return None
        prompt = f"Fix this Python code. Return ONLY corrected code.\n\nCODE:\n{code}\n\nERROR:\n{error[:800]}\n\nFIXED CODE:"
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
                return fixed.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def heal(self, filepath, max_attempts=3):
        filepath = Path(filepath)
        if not filepath.exists(): 
            return False
        for attempt in range(1, max_attempts+1):
            print(f"\nAttempt {attempt}/{max_attempts}")
            with open(filepath) as f: 
                code = f.read()
            passed, err = self.run_tests()
            if passed: 
                print("PASSED!")
                self._log(filepath.name, "success", attempt)
                return True
            print(f"Failed: {err[:200]}")
            if attempt == max_attempts: 
                return False
            fixed = self.fix_code(code, err)
            if fixed:
                Path(f"{filepath}.backup").write_text(code)
                filepath.write_text(fixed)
                print("Fix applied, retesting...")
                time.sleep(2)
        return False
    
    def watch(self, filepath, interval=5):
        filepath = Path(filepath)
        print(f"Watching {filepath.name} (Ctrl+C to stop)")
        last = filepath.stat().st_mtime if filepath.exists() else 0
        while True:
            time.sleep(interval)
            if filepath.exists() and filepath.stat().st_mtime != last:
                last = filepath.stat().st_mtime
                print(f"\nChange at {datetime.now().strftime('%H:%M:%S')}")
                passed, _ = self.run_tests()
                if passed: 
                    print("Tests passed")
                else: 
                    self.heal(filepath)
    
    def _log(self, filename, status, attempt):
        with open(self.dna_file, 'a') as f:
            f.write(f"\n## {datetime.now().isoformat()} - {filename}\n")
            f.write(f"Status: {status} (attempt {attempt})\n---\n")

def setup():
    Path("/root/broken.py").write_text('def add(a, b):\n    return a + b')
    Path("/root/test_broken.py").write_text('from broken import add\ndef test_add():\n    assert add(2, 3) == 5\n    assert add(10, 5) == 15')
    print("Demo files created")

if __name__ == "__main__":
    setup()
    agent = HealingAgent()
    if len(sys.argv) > 1:
        agent.watch(sys.argv[1])
    else:
        print("\n" + "="*40)
        print("iSH Self-Healing Agent (OpenRouter)")
        print("="*40)
        print("\nCommands:")
        print("  export OPENROUTER_API_KEY='sk-or-v1-...'")
        print("  python3 or_agent.py broken.py")
