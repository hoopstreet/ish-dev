#!/usr/bin/env python3
import sys, os, time, threading, re, subprocess
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
spinner_running = False
first_run = True

def show_spinner(phase, attempt):
    global spinner_running
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    i = 0
    while spinner_running:
        sys.stdout.write(f'\r{chars[i%8]} Phase {phase}: Executing (attempt {attempt})... ')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] {msg}\n")
    with open(DNA_FILE, "a") as f: f.write(f"\n## {ts}\n{msg}\n")

def detect_phases(code):
    phases, current, phase_num = [], [], 0
    for line in code.split('\n'):
        if re.match(r'^\s*#\s*Phase\s*\d+', line, re.IGNORECASE):
            if current:
                phase_num += 1
                phases.append((phase_num, '\n'.join(current)))
            current = [line]
        else:
            current.append(line)
    if current:
        phase_num += 1
        phases.append((phase_num, '\n'.join(current)))
    return phases if phases else [(1, code)]

def execute_phase(phase_num, phase_code, max_retries=3):
    global spinner_running
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📌 PHASE {phase_num}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for attempt in range(1, max_retries + 1):
        spinner_running = True
        t = threading.Thread(target=show_spinner, args=(phase_num, attempt))
        t.daemon = True
        t.start()
        tmp = f"/tmp/phase_{phase_num}.sh"
        with open(tmp, 'w') as f: f.write(phase_code)
        result = subprocess.call(["sh", tmp])
        os.remove(tmp)
        spinner_running = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' ' * 70 + '\r')
        if result == 0:
            print(f"✅ Phase {phase_num} SUCCESS (attempt {attempt})")
            log(f"Phase {phase_num}: SUCCESS after {attempt} attempt(s)")
            return True
        else:
            print(f"❌ Phase {phase_num} FAILED (attempt {attempt})")
            if attempt < max_retries:
                print(f"🔄 Retrying Phase {phase_num}...")
                time.sleep(1)
            else:
                print(f"💀 Phase {phase_num} FAILED after {max_retries} attempts")
                log(f"Phase {phase_num}: FAILED after {max_retries} attempts")
    return False
def main():
    global first_run
    while True:
        if first_run:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("🤖 HOOPSTREET SMART CODE EXECUTOR")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("📋 FEATURES:")
            print("   • Auto-retry failed phases up to 3 times")
            print("   • Phase-by-phase execution with spinner")
            print("   • Type 'END' when done")
            print("   • Type 'BACK' to exit")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("📝 PASTE YOUR MULTI-PHASE CODE BELOW")
            print("")
            print("# Phase 1")
            print("echo \"Testing Philippines timezone\"")
            print("")
            print("# Phase 2")
            print("echo \"Current PHT time: \$(date)\"")
            print("")
            print("# Phase 3")
            print("echo \"Done!\"")
            print("END")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("")
            print("👇 Paste Below")
            print("")
            first_run = False
        else:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("Ready for next code. Type BACK to exit.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("")
            print("👇 Paste Below")
            print("")
        
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == "END":
                    break
                if line.strip().upper() in ["BACK", "EXIT", "QUIT", "CANCEL"]:
                    print("\n🔙 Returning to main menu...")
                    return
                lines.append(line)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n\n🔙 Returning to menu...")
                return


        
        full_code = "\n".join(lines)
        if not full_code.strip():
            print("❌ No code provided")
            continue
        
        phases = detect_phases(full_code)
        total = len(phases)
        log(f"Starting execution: {total} phases detected")
        print(f"\n📊 Detected {total} phase(s)\n")
        
        success_count = 0
        for phase_num, phase_code in phases:
            if execute_phase(phase_num, phase_code):
                success_count += 1
            time.sleep(0.5)
        
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📊 EXECUTION SUMMARY")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"✅ Successful: {success_count}/{total}")
        print(f"❌ Failed: {total - success_count}/{total}")
        print(f"📅 Date: {date_str}")
        print(f"⏰ Time: {time_str} PHT")
        print(f"🔄 Max retries per phase: 3")
        print(f"🔧 Auto-healing: Enabled")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        if success_count == total:
            print(f"\n🎉 ALL PHASES COMPLETED SUCCESSFULLY! 🎉")
            print(f"   Completed on {date_str} at {time_str} PHT")
        else:
            print(f"\n⚠️ {total - success_count} phase(s) failed after 3 retries")
        
        log(f"Execution complete: {success_count}/{total} successful")

if __name__ == "__main__":
    main()
