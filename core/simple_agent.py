#!/usr/bin/env python3
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
import urllib.request

class SimpleHealingAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or "YOUR-OPENAI-KEY"
        self.dna_file = Path("/root/DNA.md")
        self.attempts = 0
        
    def run_tests(self):
        result = subprocess.run(["pytest", "-v", "-x"], 
                               capture_output=True, text=True)
        return result.returncode == 0, result.stdout + result.stderr
    
    def ask_gpt_to_fix(self, code, error):
        """Call OpenAI API to fix code"""
        prompt = f"Fix this code. Return only fixed code.\n\n```python\n{code}\n```\n\nError:\n{error}\n\nFixed code:"
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.3
        }
        
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read())
                fixed = result['choices'][0]['message']['content']
                # Extract code from markdown
                if '```python' in fixed:
                    fixed = fixed.split('```python')[1].split('```')[0]
                return fixed.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def heal_file(self, filepath, max_attempts=3):
        """Attempt to heal a file"""
        for attempt in range(1, max_attempts + 1):
            print(f"\n🔧 Healing attempt {attempt}/{max_attempts}")
            
            # Read current code
            with open(filepath, 'r') as f:
                code = f.read()
            
            # Run tests
            passed, output = self.run_tests()
            if passed:
                print("✅ Tests passed!")
                self.log_success(filepath, attempt)
                return True
            
            print(f"❌ Tests failed:\n{output[:200]}")
            
            # Ask GPT to fix
            fixed_code = self.ask_gpt_to_fix(code, output)
            if fixed_code:
                # Backup original
                backup = filepath.with_suffix('.backup')
                with open(backup, 'w') as f:
                    f.write(code)
                
                # Write fixed code
                with open(filepath, 'w') as f:
                    f.write(fixed_code)
                
                print("📝 Applied fix, re-testing...")
            else:
                print("⚠️ Could not generate fix")
                return False
        
        print("💀 Max attempts reached")
        return False
    
    def log_success(self, filepath, attempt):
        """Log to DNA.md"""
        entry = f"""
## Version v0.0.{self.attempts} - {datetime.now().isoformat()}
- **File**: {filepath}
- **Fix Attempts**: {attempt}
- **Status**: ✅ Success
"""
        with open(self.dna_file, 'a') as f:
            f.write(entry)

if __name__ == "__main__":
    import sys
    agent = SimpleHealingAgent(api_key=os.environ.get("OPENAI_API_KEY"))
    
    if len(sys.argv) > 1:
        agent.heal_file(sys.argv[1])
    else:
        print("Usage: python simple_agent.py <file_to_heal.py>")
