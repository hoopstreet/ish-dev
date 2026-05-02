#!/bin/sh

# Create agent/run.py
cat > agent/run.py << 'PYEOF'
#!/usr/bin/env python3
import sys, os, time
print("Paste your multi-phase code (type END on new line):")
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
if not code.strip():
    print("No code provided")
    sys.exit(1)
phases = []
current = []
num = None
for line in code.split('\n'):
    if line.strip().startswith('# Phase'):
        if current and num:
            phases.append((num, '\n'.join(current)))
        num = len(phases) + 1
        current = [line]
    else:
        current.append(line)
if current and num:
    phases.append((num, '\n'.join(current)))
if not phases:
    phases = [(1, code)]
print(f"\nFound {len(phases)} phase(s)\n")
for phase_num, phase_code in phases:
    print(f"--- Phase {phase_num}/{len(phases)} ---")
    tmp = f"/tmp/p{phase_num}.sh"
    with open(tmp, 'w') as f:
        f.write(phase_code)
    result = os.system(f"sh {tmp}")
    os.system(f"rm -f {tmp}")
    if result != 0:
        print(f"Phase {phase_num} failed")
    else:
        print(f"Phase {phase_num} complete")
    time.sleep(0.5)
print("\nALL PHASES PROCESSED!")
PYEOF
chmod +x agent/run.py

# Create agent/heal.py
cat > agent/heal.py << 'HEALEOF'
#!/usr/bin/env python3
from pathlib import Path
p = Path("/root/broken.py")
if p.exists() and 'a - b' in p.read_text():
    p.write_text(p.read_text().replace('a - b', 'a + b'))
    print("Fixed broken.py")
else:
    print("No fix needed")
HEALEOF
chmod +x agent/heal.py

# Create .gitignore
cat > .gitignore << 'GITEOF'
*.pyc
__pycache__/
*.backup
/tmp/
.DS_Store
GITEOF

# Initialize git and push
git init
git add .
git commit -m "Initial commit: Hoopstreet iSH Dev System v1.0.0"
git remote add origin https://github.com/hoopstreet/ish-dev.git
git push -u origin main --force
git tag -a v1.0.0 -m "Stable release: Hoopstreet iSH Dev System"
git push origin v1.0.0 --force

# Install locally
./setup.sh
