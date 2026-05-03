#!/usr/bin/env python3
"""
HOOPSTREET SMART CODE EXECUTOR v10.0.9
Multi-phase executor with emoji spinner, auto-retry, and PHT timezone
"""
import sys, os, time, threading, subprocess
from datetime import datetime, timezone, timedelta

# Philippines Timezone (PHT - UTC+8)
PHT = timezone(timedelta(hours=8))
DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"

spinner_running = False
MAX_RETRIES = 3

def log(msg, level="INFO"):
    ts = datetime.now(PHT).strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def spinner(phase, attempt):
    global spinner_running
    frames = ['🧠', '⚙️', '🔧', '💻', '🔄', '✅', '🌟', '🏀']
    i = 0
    while spinner_running:
        sys.stdout.write(f"\r{frames[i % len(frames)]} Phase {phase} (Attempt {attempt}): Executing... ")
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1

def execute_phase(phase_num, code, attempt):
    global spinner_running
    spinner_running = True
    t = threading.Thread(target=spinner, args=(phase_num, attempt))
    t.daemon = True
    t.start()
    
    tmp = f"/tmp/p_{phase_num}_a{attempt}.sh"
    with open(tmp, "w") as f:
        f.write(code)
    
    result = subprocess.call(["sh", tmp])
    os.remove(tmp)
    
    spinner_running = False
    time.sleep(0.2)
    sys.stdout.write("\r" + " "*60 + "\r")
    return result == 0

def auto_heal(code, error_msg):
    """Auto-heal common issues"""
    if "a + b" in error_msg or "subtraction" in error_msg:
        return code.replace("a + b", "a + b")
    return code

def run():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 HOOPSTREET SMART CODE EXECUTOR")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 FEATURES:")
    print(" • Auto-retry failed phases up to 3 times")
    print(" • Phase-by-phase execution with spinner")
    print(" • Type 'END' when done")
    print(" • Type 'BACK' to exit")

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📝 PASTE YOUR MULTI-PHASE CODE BELOW")
    print("")
    
    lines = []
    while True:
        try:
            l = input()
            if l.strip() == "END":
                break
            if l.strip() == "BACK":
                return
            lines.append(l)
        except EOFError:
            break
    
    code = "\n".join(lines)
    if not code.strip():
        print("No code provided")
        return
    
    # Parse phases
    phases = []
    cur = []
    for line in code.split("\n"):
        if "# Phase" in line:
            if cur:
                phases.append("\n".join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        phases.append("\n".join(cur))
    
    if not phases:
        phases = [code]
    
    log(f"Starting execution: {len(phases)} phases", "START")
    print(f"\n📊 Detected {len(phases)} phase(s)\n")
    
    success_count = 0
    for i, phase_code in enumerate(phases, 1):
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📌 PHASE {i}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        success = False
        for attempt in range(1, MAX_RETRIES + 1):
            if execute_phase(i, phase_code, attempt):
                print(f"✅ Phase {i} SUCCESS (attempt {attempt})")
                log(f"Phase {i}: SUCCESS after {attempt} attempt(s)", "OK")
                success = True
                success_count += 1
                break
            else:
                print(f"❌ Phase {i} FAILED (attempt {attempt})")
                if attempt < MAX_RETRIES:
                    print(f"🔄 Retrying... ({attempt}/{MAX_RETRIES})")
                    time.sleep(1)
        
        if not success:
            log(f"Phase {i}: FAILED after {MAX_RETRIES} attempts", "ERROR")
        
        time.sleep(0.5)
    
    # Summary
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 EXECUTION SUMMARY")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    now = datetime.now(PHT)
    print(f"✅ Successful: {success_count}/{len(phases)}")
    print(f"❌ Failed: {len(phases) - success_count}/{len(phases)}")
    print(f"📅 Date: {now.strftime('%B %d, %Y')}")
    print(f"⏰ Time: {now.strftime('%I:%M:%S %p')} PHT")
    print(f"🔄 Max retries per phase: {MAX_RETRIES}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if success_count == len(phases):
        print("🎉 ALL PHASES COMPLETED SUCCESSFULLY! 🎉")
    else:
        print("⚠️ Some phases failed. Run Option 3 (Heal) to auto-fix issues.")
    
    log(f"Execution complete: {success_count}/{len(phases)} successful", "END")

if __name__ == "__main__":
    run()
