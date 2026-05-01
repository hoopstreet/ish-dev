#!/bin/sh
# MASTER PHASE EXECUTOR - Clean version

# Create phase executor Python script
cat > /tmp/phase_executor.py << 'PYEOF'
#!/usr/bin/env python3
import sys, re, os, time
from pathlib import Path

class PhaseExecutor:
    def __init__(self):
        self.phases = []
        
    def detect_phases(self, code):
        phases = []
        lines = code.split('\n')
        current = []
        num = None
        
        for line in lines:
            match = re.match(r'^\s*#\s*phase\s*(\d+)\s*:?', line, re.IGNORECASE)
            if match:
                if current and num:
                    phases.append({'num': num, 'code': '\n'.join(current)})
                num = int(match.group(1))
                current = [line]
            else:
                current.append(line)
        
        if current and num:
            phases.append({'num': num, 'code': '\n'.join(current)})
        return phases
    
    def execute(self, phase, total):
        print(f"\n--- Phase {phase['num']}/{total} ---")
        temp = Path(f"/tmp/p{phase['num']}.sh")
        temp.write_text(phase['code'])
        result = os.system(f"sh {temp}")
        temp.unlink()
        return result == 0
    
    def run(self, code):
        phases = self.detect_phases(code)
        if not phases:
            phases = [{'num': 1, 'code': code}]
        
        print(f"\nFound {len(phases)} phases")
        for p in phases:
            if not self.execute(p, len(phases)):
                print(f"\n❌ Phase {p['num']} failed")
                return False
            time.sleep(0.5)
        
        print(f"\n✅ All {len(phases)} phases completed!")
        return True

print("Paste your code (type END on new line):")
lines = []
while True:
    try:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    except:
        break

code = "\n".join(lines)
if code.strip():
    executor = PhaseExecutor()
    executor.run(code)
else:
    print("No code provided")
PYEOF

python3 /tmp/phase_executor.py
rm -f /tmp/phase_executor.py
