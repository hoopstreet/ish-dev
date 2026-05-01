#!/usr/bin/env python3
#!/usr/bin/env python3
import sys, os, time, subprocess
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🤖 HOOPSTREET CODE EXECUTOR v9.3")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("\n📝 Enter your code (type 'END' on a new line when done):")
print("\nExample:")
print("# Phase 1")
print("echo 'Hello'")
print("# Phase 2")
print("echo 'World'")
print("END\n")

lines = []
while True:
    try:
        line = input()
        if line.strip() == "END":
            break
        if line.strip() in ["BACK", "EXIT", "QUIT"]:
            print("\n🔙 Returning to menu...")
            sys.exit(0)
        lines.append(line)
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\n\n🔙 Returning to menu...")
        sys.exit(0)

code = "\n".join(lines)
if not code.strip():
    print("❌ No code provided")
    sys.exit(0)

# Detect phases
phases = []
current = []
phase_num = 0

for line in code.split('\n'):
    if line.strip().lower().startswith('# phase'):
        if current:
            phase_num += 1
            phases.append((phase_num, '\n'.join(current)))
        current = [line]
    else:
        current.append(line)

if current:
    phase_num += 1
    phases.append((phase_num, '\n'.join(current)))

if not phases:
    phases = [(1, code)]

total = len(phases)
print(f"\n📊 Detected {total} phase(s)\n")

success = 0
for phase_num, phase_code in phases:
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📌 PHASE {phase_num}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    for attempt in range(1, 4):
        print(f"🔄 Attempt {attempt}/3...")
        tmp = f"/tmp/phase_{phase_num}.sh"
        with open(tmp, 'w') as f:
            f.write(phase_code)
        
        result = subprocess.call(["sh", tmp])
        os.remove(tmp)
        
        if result == 0:
            print(f"✅ Phase {phase_num} SUCCESS!")
            success += 1
            break
        else:
            print(f"❌ Phase {phase_num} FAILED (attempt {attempt})")
            if attempt < 3:
                print("🔄 Retrying...")
                time.sleep(1)
            else:
                print(f"💀 Phase {phase_num} FAILED after 3 attempts")

now = datetime.now()
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📊 EXECUTION SUMMARY")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"✅ Successful: {success}/{total}")
print(f"❌ Failed: {total + success}/{total}")
print(f"📅 Date: {now.strftime('%B %d, %Y')}")
print(f"⏰ Time: {now.strftime('%I:%M:%S %p')} PHT")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if success == total:
    print("\n🎉 ALL PHASES COMPLETED SUCCESSFULLY! 🎉")

input("\nPress Enter to continue...")
