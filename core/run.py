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
