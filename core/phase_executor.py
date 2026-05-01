#!/usr/bin/env python3
#!/usr/bin/env python3
import sys, re, os, time
from pathlib import Path

class PhaseExecutor:
    def __init__(self):
        self.phases = []
        self.phase_results = []
        
    def detect_phases(self, code):
        phases = []
        lines = code.split('\n')
        current_phase = []
        phase_num = None
        
        for line in lines:
            match = re.match(r'^\s*#\s*phase\s*(\d+)\s*:?', line, re.IGNORECASE)
            if match:
                if current_phase and phase_num:
                    phases.append({'num': phase_num, 'code': '\n'.join(current_phase), 'type': 'marked'})
                phase_num = int(match.group(1))
                current_phase = [line]
            else:
                current_phase.append(line)
        
        if current_phase and phase_num:
            phases.append({'num': phase_num, 'code': '\n'.join(current_phase), 'type': 'marked'})
        return phases
    
    def execute_phase(self, phase, total):
        print(f"\n{'='*60}")
        print(f"📦 EXECUTING PHASE {phase['num']}/{total}")
        print(f"📋 Type: {phase['type']}")
        print(f"📏 Lines: {len(phase['code'].split(chr(10)))}")
        print(f"{'='*60}")
        
        temp_file = Path(f"/tmp/phase_{phase['num']}.sh")
        temp_file.write_text(phase['code'])
        
        try:
            result = os.system(f"sh {temp_file} 2>&1")
            if result == 0:
                print(f"\n✅ PHASE {phase['num']} SUCCESS!")
                return True
            else:
                print(f"\n❌ PHASE {phase['num']} FAILED (exit code: {result})")
                return False
        except Exception as e:
            print(f"\n❌ PHASE {phase['num']} ERROR: {e}")
            return False
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def run(self, code):
        print("\n🔍 ANALYZING CODE FOR PHASES...")
        phases = self.detect_phases(code)
        
        if not phases:
            print("⚠️ No phases detected, running as single block")
            phases = [{'num': 1, 'code': code, 'type': 'single'}]
        
        print(f"📊 Found {len(phases)} phase(s)")
        
        for phase in phases:
            success = self.execute_phase(phase, len(phases))
            self.phase_results.append((phase['num'], success))
            if not success:
                print(f"\n💀 Stopped at Phase {phase['num']}")
                return False
            time.sleep(0.5)
        
        print(f"\n{'🎉'*30}")
        print("✅ ALL PHASES EXECUTED SUCCESSFULLY!")
        print(f"{'🎉'*30}")
        return True

print("📝 Reading code... (type END on new line when done)")
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
    sys.exit(1)

executor = PhaseExecutor()
executor.run(code)
