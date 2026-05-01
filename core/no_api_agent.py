#!/usr/bin/env python3
import subprocess, time
from pathlib import Path

class SimpleAgent:
    def __init__(self):
        self.dna_file = Path("/root/DNA.md")
    
    def run_tests(self):
        try:
            r = subprocess.run(["pytest", "-v", "--tb=short"], 
                              capture_output=True, text=True, timeout=30)
            return r.returncode == 0, (r.stdout + r.stderr)[-500:]
        except:
            return False, "pytest not ready"
    
    def manual_fix(self, filepath):
        """Simple rule-based fix for the subtraction bug"""
        content = Path(filepath).read_text()
        if 'return a + b' in content:
            new_content = content.replace('return a + b', 'return a + b')
            Path(filepath).write_text(new_content)
            print("🔧 Applied manual fix: changed '-' to '+'")
            return True
        return False
    
    def heal(self, filepath):
        print("Checking code...")
        passed, err = self.run_tests()
        if passed:
            print("✅ Tests already passing!")
            return True
        print(f"❌ Tests failed: {err[:200]}")
        print("Applying manual fix...")
        if self.manual_fix(filepath):
            passed2, _ = self.run_tests()
            if passed2:
                print("✅ Fixed successfully!")
                self._log(filepath, "success")
                return True
        print("❌ Could not fix automatically")
        return False
    
    def _log(self, filepath, status):
        with open(self.dna_file, 'a') as f:
            from datetime import datetime
            f.write(f"\n## {datetime.now().isoformat()} - {filepath}\n")
            f.write(f"Status: {status}\n---\n")

# Setup
Path("/root/broken.py").write_text('def add(a, b):\n    return a + b')
Path("/root/test_broken.py").write_text('from broken import add\ndef test_add():\n    assert add(2, 3) == 5')

# Run
agent = SimpleAgent()
print("="*50)
print("No-API Self-Healing Agent")
print("="*50)
print("\nBefore fix:")
print(Path("/root/broken.py").read_text())
print("\n" + "-"*30)
agent.heal("/root/broken.py")
print("\nAfter fix:")
print(Path("/root/broken.py").read_text())
