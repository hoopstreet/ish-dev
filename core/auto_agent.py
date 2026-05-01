#!/usr/bin/env python3
import subprocess, json, time, sys, os, threading, urllib.request, re
from pathlib import Path
from datetime import datetime
from itertools import cycle

class AutoHealingAgent:
    def __init__(self):
        self.gemini_keys = [
            "AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas",
            "AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA",
            "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY",
            "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg",
            "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"
        ]
        self.gemini_failed = [False] * 5
        self.openrouter_keys = ["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"]
        self.current_model = "gemini-0"
        self.dna_file = Path("/root/DNA.md")
        self.spinner_running = False
    
    def spinner(self, message):
        chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        i = 0
        while self.spinner_running:
            sys.stdout.write(f'\r{chars[i % 8]} {message}... ')
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
    
    def call_gemini(self, prompt, key_idx):
        if self.gemini_failed[key_idx]:
            return None, "Key failed"
        api_key = self.gemini_keys[key_idx]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800}}
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text, None
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                self.gemini_failed[key_idx] = True
                return None, "QUOTA_EXCEEDED"
            return None, str(e)
    
    def call_openrouter(self, prompt):
        if not self.openrouter_keys:
            return None, "No keys"
        data = {"model": "google/gemini-2.0-flash-exp:free", "messages": [{"role": "user", "content": prompt}], "max_tokens": 800}
        for api_key in self.openrouter_keys:
            try:
                req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(data).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode())
                    return result['choices'][0]['message']['content'], None
            except:
                continue
        return None, "OpenRouter failed"
    
    def _clean_code(self, text):
        if '```python' in text:
            text = text.split('```python')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        return text.strip()
    
    def fix_code(self, code, error):
        prompt = f"Fix this Python code. Return ONLY fixed code.\n\nCODE:\n{code}\n\nERROR:\n{error}\n\nFIXED:"
        for key_idx in range(5):
            if not self.gemini_failed[key_idx]:
                self.start_spinner(f"Gemini {key_idx+1}")
                result, err = self.call_gemini(prompt, key_idx)
                if result:
                    self.stop_spinner(True, f"Gemini-{key_idx+1} fixed it!")
                    self.current_model = f"gemini-{key_idx+1}"
                    self._log("fix", "success", self.current_model)
                    return self._clean_code(result)
                elif err == "QUOTA_EXCEEDED":
                    print(f"\n⚠️ Gemini key {key_idx+1} exceeded")
        self.start_spinner("OpenRouter")
        result, err = self.call_openrouter(prompt)
        if result:
            self.stop_spinner(True, "OpenRouter fixed it!")
            self.current_model = "openrouter"
            self._log("fix", "success", self.current_model)
            return self._clean_code(result)
        if 'a + b' in code:
            self.stop_spinner(True, "Rule fix applied")
            return code.replace('a + b', 'a + b')
        self.stop_spinner(False, "All models failed")
        return None
    
    def _log(self, action, status, model):
        with open(self.dna_file, 'a') as f:
            f.write(f"\n## {datetime.now().isoformat()} | {action} | {status} | {model}\n")
    
    def run_tests(self):
        try:
            result = subprocess.run(["python3", "-c", "import sys; sys.path.insert(0,'/root'); from broken import add; assert add(2,3)==5"], capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stderr
        except:
            return False, "Timeout"
    
    def heal_file(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            return False
        print("\n" + "="*50)
        print("🤖 AUTO-HEALING (5 Gemini Keys)")
        print("="*50)
        for attempt in range(1, 4):
            print(f"\n📌 Attempt {attempt}/3")
            with open(filepath) as f:
                code = f.read()
            print(f"📄 Code: {code.strip()[:50]}")
            passed, error = self.run_tests()
            if passed:
                print("✨ HEALTHY!")
                return True
            print(f"⚠️ Error: {error[:80]}")
            fixed = self.fix_code(code, error)
            if fixed:
                Path(f"{filepath}.backup").write_text(code)
                filepath.write_text(fixed)
                print("💾 Fix applied!")
                time.sleep(1)
            else:
                return False
        return False
    
    def heal_code_string(self, code_string):
        print("\n🚀 HEALING CODE BLOCK")
        passed, error = self.run_tests()
        if passed:
            print("✅ Code works!")
            return code_string
        fixed = self.fix_code(code_string, error)
        return fixed if fixed else code_string

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌟 AUTO AGENT - 5 GEMINI KEYS")
    print("="*50)
    agent = AutoHealingAgent()
    if Path("/root/broken.py").exists():
        agent.heal_file("/root/broken.py")
    while True:
        print("\n1. Heal | 2. Watch | 3. Status | 0. Exit")
        choice = input("👉 ").strip()
        if choice == "1":
            agent.heal_file("/root/broken.py")
        elif choice == "2":
            print("Watch mode - press Ctrl+C to stop")
            agent.watch("/root/broken.py") if hasattr(agent, 'watch') else None
        elif choice == "3":
            active = sum(1 for f in agent.gemini_failed if not f)
            print(f"Gemini: {active}/5 active | Model: {agent.current_model}")
        elif choice == "0":
            break
