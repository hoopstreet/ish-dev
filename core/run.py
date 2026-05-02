import sys, re, os, time
from pathlib import Path

def read_code():
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except:
            break
    return "\n".join(lines)

def detect_phases(code):
    phases = []
    current = []
    num = None
    for line in code.split('\n'):
        m = re.match(r'^\s*#\s*phase\s*(\d+)', line, re.I)
        if m:
            if current and num:
                phases.append((num, '\n'.join(current)))
            num = int(m.group(1))
            current = [line]
        else:
            current.append(line)
    if current and num:
        phases.append((num, '\n'.join(current)))
    return phases if phases else [(1, code)]

def run_phase(num, code):
    print(f"\n--- Phase {num} ---")
    tmp = Path(f"/tmp/p{num}.sh")
    tmp.write_text(code)
    r = os.system(f"sh {tmp}")
    tmp.unlink()
    return r == 0

def main():
    code = read_code()
    if not code.strip():
        print("No code")
        return
    phases = detect_phases(code)
    print(f"\nFound {len(phases)} phases")
    for num, ph in phases:
        if not run_phase(num, ph):
            print(f"Phase {num} FAILED")
            return
        time.sleep(0.3)
    print("\n✅ DONE!")

if __name__ == "__main__":
    main()
