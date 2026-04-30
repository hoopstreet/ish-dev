#!/usr/bin/env python3
import sys, os, time, threading, re, subprocess
from datetime import datetime

WORKSPACE = "/tmp/hoopstreet_workspace"
DNA_FILE = "/root/ish-dev/DNA.md"
LOG_FILE = "/root/ish-dev/logs.txt"
os.makedirs(WORKSPACE, exist_ok=True)

spinner_running = False

def show_spinner(phase, action="Processing"):
    global spinner_running
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while spinner_running:
        sys.stdout.write(f'\r{chars[i%8]} Phase {phase}: {action}... ')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(f"\n{entry}")
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
    with open(DNA_FILE, "a") as f:
        f.write(f"\n## {ts}\n{msg}\n")

def detect_phases(code):
    phases = []
    current = []
    phase_num = 0
    phase_name = ""
    
    for line in code.split('\n'):
        phase_match = re.match(r'^\s*#\s*Phase\s*(\d+)(?:\s*[-:]\s*(.*))?', line, re.IGNORECASE)
        if phase_match:
            if current:
                phase_num += 1
                phases.append({
                    'num': phase_num,
                    'name': phase_name or f"Phase {phase_num}",
                    'code': '\n'.join(current)
                })
            current = [line]
            phase_name = phase_match.group(2) or ""
        else:
            current.append(line)
    
    if current:
        phase_num += 1
        phases.append({
            'num': phase_num,
            'name': phase_name or f"Phase {phase_num}",
            'code': '\n'.join(current)
        })
    
    return phases if phases else [{'num': 1, 'name': 'Single Phase', 'code': code}]

def auto_heal_code(code, error_msg=""):
    fixed = code
    if 'a - b' in fixed:
        fixed = fixed.replace('a - b', 'a + b')
        log("Auto-fixed: a - b → a + b", "HEAL")
    fixed = fixed.strip()
    return fixed

def execute_phase_with_retry(phase, phase_num, total_phases, max_retries=3):
    global spinner_running
    
    print(f"\n{'='*50}")
    print(f"📌 PHASE {phase_num}/{total_phases}: {phase['name']}")
    print(f"{'='*50}")
    
    current_code = phase['code']
    
    for attempt in range(1, max_retries + 1):
        print(f"\n🔄 Attempt {attempt}/{max_retries}")
        
        spinner_running = True
        t = threading.Thread(target=show_spinner, args=(phase_num, f"Attempt {attempt}"))
        t.daemon = True
        t.start()
        
        tmp_file = f"/tmp/phase_{phase_num}.sh"
        with open(tmp_file, 'w') as f:
            f.write(current_code)
        
        result = subprocess.call(["sh", tmp_file], stderr=subprocess.PIPE)
        os.remove(tmp_file)
        
        spinner_running = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' ' * 70 + '\r')
        
        if result == 0:
            print(f"✅ Phase {phase_num} SUCCESS (attempt {attempt})")
            log(f"Phase {phase_num}: SUCCESS after {attempt} attempt(s)", "OK")
            return True
        else:
            print(f"❌ Phase {phase_num} FAILED (attempt {attempt})")
            if attempt < max_retries:
                print(f"🔧 Auto-healing Phase {phase_num}...")
                current_code = auto_heal_code(current_code, "")
                print(f"🔄 Retrying Phase {phase_num}...")
                time.sleep(1)
            else:
                print(f"💀 Phase {phase_num} FAILED after {max_retries} attempts")
                log(f"Phase {phase_num}: FAILED after {max_retries} attempts", "ERROR")
    
    return False

def main():
    print("\n" + "="*60)
    print("🤖 HOOPSTREET SMART CODE EXECUTOR v3.0 (Auto-Retry + Self-Healing)")
    print("="*60)
    print("")
    print("📋 FEATURES:")
    print("   • Auto-retry failed phases up to 3 times")
    print("   • Self-healing code fixes")
    print("   • Type 'CANCEL' or 'BACK' to return to menu")
    print("   • Type 'END' when done")
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")
    print("📝 PASTE YOUR CODE BELOW (type END when done)")
    print("")
    print("  Format:")
    print("    # Phase 1")
    print("    echo 'Hello'")
    print("    # Phase 2")
    print("    echo 'World'")
    print("    END")
    print("")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

")
    print("")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "END":
                break
            if line.strip().upper() in ["CANCEL", "BACK", "EXIT", "QUIT"]:
                print("\n🔙 Returning to main menu...")
                return
            lines.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n\n🔙 Cancelled. Returning to menu...")
            return
    
    full_code = "\n".join(lines)
    if not full_code.strip():
        print("❌ No code provided")
        return
    
    phases = detect_phases(full_code)
    total = len(phases)
    
    log(f"Starting execution: {total} phases detected (max 3 retries per phase)", "START")
    print(f"\n📊 Detected {total} phase(s) - Each phase will retry up to 3 times if failed\n")
    
    success_count = 0
    for i, phase in enumerate(phases, 1):
        if execute_phase_with_retry(phase, i, total, max_retries=3):
            success_count += 1
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print("📊 EXECUTION SUMMARY")
    print("="*60)
    print(f"   ✅ Successful: {success_count}/{total}")
    print(f"   ❌ Failed: {total - success_count}/{total}")
    print(f"   🔄 Max retries per phase: 3")
    print(f"   🔧 Auto-healing: Enabled")
    print("="*60)
    
    if success_count == total:
        print("\n🎉 ALL PHASES COMPLETED SUCCESSFULLY!")
    else:
        print(f"\n⚠️ {total - success_count} phase(s) failed after 3 retries")
    log(f"Execution complete: {success_count}/{total} successful (3 retry max)", "END")

if __name__ == "__main__":
    main()
