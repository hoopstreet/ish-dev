#!/usr/bin/env python3
import sys, os, time, threading, subprocess
from datetime import datetime

spinner_running = False
FAILED_PHASES = {}

def spinner(phase):
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    i = 0
    while spinner_running:
        sys.stdout.write(f"\r{chars[i%8]} Phase {phase} running...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def log(msg):
    with open("/root/ish-dev/logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

print("\n📦 ENTER CODE (END to finish)\n")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

code = "\n".join(lines)
if not code.strip():
    print("No code provided")
    sys.exit(1)

phases = []
buffer = []
phase_id = 0

for line in code.split("\n"):
    if "# Phase" in line:
        if buffer:
            phase_id += 1
            phases.append((phase_id, "\n".join(buffer)))
        buffer = [line]
    else:
        buffer.append(line)

if buffer:
    phase_id += 1
    phases.append((phase_id, "\n".join(buffer)))

print(f"\n📊 {len(phases)} phases detected\n")

for pid, pcode in phases:
    global spinner_running
    spinner_running = True

    t = threading.Thread(target=spinner, args=(pid,))
    t.daemon = True
    t.start()

    tmp = f"/tmp/p_{pid}.sh"
    with open(tmp, "w") as f:
        f.write(pcode)

    result = subprocess.call(["sh", tmp])
    os.remove(tmp)

    spinner_running = False
    time.sleep(0.2)
    sys.stdout.write("\r" + " " * 60 + "\r")

    if result != 0:
        log(f"PHASE {pid} FAILED - INIT DEBUG LOOP")

        FAILED_PHASES[pid] = pcode

        # AUTO FIX ATTEMPT (basic AI heuristic)
        fixed = pcode.replace("rm -rf /", "# blocked risky command")
        fixed = fixed.replace("sudo", "")

        tmp_fix = f"/tmp/p_{pid}_fix.sh"
        with open(tmp_fix, "w") as f:
            f.write(fixed)

        retry = subprocess.call(["sh", tmp_fix])
        os.remove(tmp_fix)

        if retry == 0:
            log(f"PHASE {pid} RECOVERED")
            print(f"🔧 Phase {pid} auto-fixed & recovered")
        else:
            log(f"PHASE {pid} FAILED PERMANENT")
            print(f"❌ Phase {pid} failed permanently")
    else:
        log(f"PHASE {pid} SUCCESS")
        print(f"✅ Phase {pid} complete")

    os.system("cd /root/ish-dev && git add .")

    if result != 0:
        os.system(f'cd /root/ish-dev && git commit -m "rollback phase {pid}"')
        os.system("cd /root/ish-dev && git reset --hard HEAD~1")
    else:
        os.system(f'cd /root/ish-dev && git commit -m "phase {pid} success"')

    try:
        import requests

        payload = {
            "phase": pid,
            "status": "FAILED" if result != 0 else "SUCCESS",
            "time": str(datetime.now())
        }

        requests.post(
            "https://YOUR_SUPABASE_URL/rest/v1/logs",
            headers={
                "apikey": "YOUR_KEY",
                "Authorization": "Bearer YOUR_KEY",
                "Content-Type": "application/json"
            },
            json=payload
        )
    except:
        pass

print("\n🚀 PIPELINE STATUS: COMPLETE")

if FAILED_PHASES:
    print("⚠️ Some phases failed + auto-recovery attempted")
else:
    print("🎉 ALL PHASES PASSED")

        if result != 0:
            log(f"PHASE {pid} FAILED - AI DEBUG START")

            error_log = "execution failed"

            try:
                from ai_debugger import fix_file
                fixed = fix_file(tmp, error_log)

                retry = subprocess.call(["sh", tmp])

                if retry == 0:
                    print(f"🧠 Phase {pid} AI FIXED")
                    log(f"PHASE {pid} AI RECOVERED")
                else:
                    print(f"❌ Phase {pid} AI FAILED")
                    log(f"PHASE {pid} PERMANENT FAILURE")

            except Exception as e:
                print(f"AI DEBUG ERROR: {e}")
