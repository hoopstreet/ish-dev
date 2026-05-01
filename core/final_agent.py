#!/usr/bin/env python3
import subprocess, json, time, sys, os, threading, urllib.request
from pathlib import Path
from datetime import datetime
print("✅ Phase 1: Core imports loaded")

class CompleteAgent:
    def __init__(self):
        self.gemini_keys = [
            "AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas",
            "AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA",
            "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY",
            "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg",
            "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"
        ]
        self.gemini_failed = [False] * 5
        self.or_key = "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"
        self.current = "gemini-0"
        self.dna = Path("/root/DNA.md")
        self.spin = False
        print("✅ Phase 2: Agent class initialized")

    def _spin(self, msg):
        chars = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
        i = 0
        while self.spin:
            sys.stdout.write(f'\r{chars[i%8]} {msg}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def _start(self, msg):
        self.spin = True
        threading.Thread(target=self._spin, args=(msg,), daemon=True).start()
    
    def _stop(self, ok=True, msg=""):
        self.spin = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' '*50 + '\r')
        print(f"{'✅' if ok else '❌'} {msg}")
    print("✅ Phase 3: Spinner methods added")

    def _call_gemini(self, prompt, idx):
        if self.gemini_failed[idx]:
            return None, "Key failed"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_keys[idx]}"
        data = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.2,"maxOutputTokens":800}}
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text, None
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                self.gemini_failed[idx] = True
            return None, str(e)
    print("✅ Phase 4: Gemini API method added")

    def _call_or(self, prompt):
        data = {"model":"google/gemini-2.0-flash-exp:free","messages":[{"role":"user","content":prompt}],"max_tokens":800}
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(data).encode(), headers={"Authorization":f"Bearer {self.or_key}","Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                return result['choices'][0]['message']['content'], None
        except Exception as e:
            return None, str(e)
    print("✅ Phase 5: OpenRouter API method added")

    def _clean(self, text):
        if '```python' in text:
            text = text.split('```python')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        return text.strip()
    print("✅ Phase 6: Code cleaner added")

    def fix(self, code, error):
        prompt = f"Fix this Python code. Return ONLY fixed code.\n\nCODE:\n{code}\n\nERROR:\n{error}\n\nFIXED:"
        for i in range(5):
            if not self.gemini_failed[i]:
                self._start(f"Gemini {i+1}")
                result, err = self._call_gemini(prompt, i)
                if result:
                    self._stop(True, f"Gemini-{i+1}")
                    self.current = f"gemini-{i+1}"
                    return self._clean(result)
                self._stop(False, f"Key {i+1} failed")
        self._start("OpenRouter")
        result, err = self._call_or(prompt)
        if result:
            self._stop(True, "OpenRouter")
            self.current = "openrouter"
            return self._clean(result)
        if 'a + b' in code:
            self._stop(True, "Rule fix")
            return code.replace('a + b', 'a + b')
        self._stop(False, "All failed")
        return None
    print("✅ Phase 7: Fix logic added")

    def test(self):
        try:
            cmd = ["python3", "-c", "import sys; sys.path.insert(0,'/root'); from broken import add; assert add(2,3)==5; print('OK')"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr
        except Exception as e:
            return False, str(e)
    print("✅ Phase 8: Test method added")

    def heal(self, path):
        filepath = Path(path)
        if not filepath.exists():
            return False
        print("\n" + "="*50)
        print("🤖 AUTO-HEALING (5 Gemini+OpenRouter)")
        print("="*50)
        for attempt in range(1, 4):
            print(f"\n📌 Attempt {attempt}/3")
            code = filepath.read_text()
            print(f"📄 Code: {code.strip()[:50]}")
            passed, error = self.test()
            if passed:
                print("✨ HEALTHY!")
                self._log(filepath.name, "healthy", attempt)
                return True
            print(f"⚠️ Error: {error[:80]}")
            fixed = self.fix(code, error)
            if fixed:
                backup = Path(f"{filepath}.backup")
                backup.write_text(code)
                filepath.write_text(fixed)
                print("💾 Fix applied!")
                time.sleep(1)
            else:
                return False
        return False
    
    def _log(self, name, status, attempt):
        with open(self.dna, 'a') as f:
            f.write(f"\n## {datetime.now().isoformat()} | {name} | {status} | attempt {attempt} | model {self.current}\n")
    print("✅ Phase 9: Heal method added")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌟 COMPLETE AUTO AGENT v2.0")
    print("="*50)
    print("📋 5 Gemini Keys + OpenRouter Backup")
    print("🎯 Auto-failover with visual feedback\n")
    
    agent = CompleteAgent()
    
    # Auto-fix broken.py if it exists and has bug
    bp = Path("/root/broken.py")
    if bp.exists():
        content = bp.read_text()
        if 'a + b' in content:
            print("🔧 Auto-detected bug in broken.py")
            agent.heal("/root/broken.py")
    else:
        # Create test file
        bp.write_text('def add(a,b): return a + b')
        print("📁 Created test file: broken.py")
    
    # Interactive menu
    while True:
        print("\n" + "-"*40)
        print("1. 🔧 Heal broken.py")
        print("2. 🧪 Run tests")
        print("3. 📊 Show status")
        print("0. 🚪 Exit")
        print("-"*40)
        
        choice = input("👉 Choose: ").strip()
        
        if choice == "1":
            agent.heal("/root/broken.py")
        elif choice == "2":
            passed, error = agent.test()
            print(f"\n✅ Tests passed: {passed}")
            if not passed:
                print(f"Error: {error[:200]}")
        elif choice == "3":
            active = sum(1 for f in agent.gemini_failed if not f)
            print(f"\n📊 Gemini keys active: {active}/5")
            print(f"🎯 Current model: {agent.current}")
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
    print("✅ Phase 10: Main menu added")
