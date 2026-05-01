#!/usr/bin/env python3
#!/usr/bin/env python3
import sys, re, os, time
from pathlib import Path

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        if line.strip() == "END":
            break
        lines.append(line)
    
    code = "\n".join(lines)
    if not code.strip():
        # Try reading interactively
        print("📝 Enter your code (type END on new line):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            except EOFError:
                break
        code = "\n".join(lines)
    
    if not code.strip():
        print("❌ No code provided")
        return
    
    # Detect phases
    phases = []
    current = []
    num = None
    
    for line in code.split('\n'):
        match = re.match(r'^\s*#\s*phase\s*(\d+)\s*:?', line, re.IGNORECASE)
        if match:
            if current and num:
                phases.append((num, '\n'.join(current)))
            num = int(match.group(1))
            current = [line]
        else:
            current.append(line)
    
    if current and num:
        phases.append((num, '\n'.join(current)))
    
    if not phases:
        phases = [(1, code)]
    
    print(f"\n📊 Found {len(phases)} phase(s)\n")
    
    for phase_num, phase_code in phases:
        print(f"▶️ Executing Phase {phase_num}...")
        temp_file = Path(f"/tmp/p{phase_num}.sh")
        temp_file.write_text(phase_code)
        
        try:
            result = os.system(f"sh {temp_file}")
            if result != 0:
                print(f"❌ Phase {phase_num} failed (code: {result})")
                temp_file.unlink()
                return
            print(f"✅ Phase {phase_num} complete\n")
        except Exception as e:
            print(f"❌ Error: {e}")
            temp_file.unlink()
            return
        finally:
            if temp_file.exists():
                temp_file.unlink()
        
        time.sleep(0.5)
    
    print("🎉 ALL PHASES COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
