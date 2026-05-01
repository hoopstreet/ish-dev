#!/usr/bin/env python3
#!/usr/bin/env python3
import sys, os, time, threading, subprocess
from datetime import datetime

spinner_running = False

DNA_FILE = "/root/ish-dev/DNA.md"
LOG_FILE = "/root/ish-dev/logs.txt"
ROADMAP_FILE = "/root/ish-dev/ROADMAP.md"

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    open(LOG_FILE, "a").write(entry + "\n")
    open(DNA_FILE, "a").write("\n" + entry + "\n")

def spinner(phase):
    global spinner_running
    chars = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
    i = 0
    while spinner_running:
        sys.stdout.write(f"\r{chars[i%8]} Phase {phase} running...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

def execute_phase(n, code):
    global spinner_running

    spinner_running = True
    t = threading.Thread(target=spinner, args=(n,))
    t.start()

    tmp = f"/tmp/p_{n}.sh"
    open(tmp,"w").write(code)

    result = subprocess.call(["sh", tmp])
    os.remove(tmp)

    spinner_running = False
    time.sleep(0.2)
    sys.stdout.write("\r" + " "*60 + "\r")

    if result == 0:
        log(f"PHASE {n} SUCCESS", "OK")
        print(f"✅ Phase {n} OK")
        return True

    log(f"PHASE {n} FAILED", "ERROR")

    # AUTO HEAL LOOP
    fixed = code.replace("rm -rf /","echo blocked").replace("sudo ","")
    tmp2 = f"/tmp/p_{n}_fix.sh"
    open(tmp2,"w").write(fixed)

    retry = subprocess.call(["sh", tmp2])
    os.remove(tmp2)

    if retry == 0:
        log(f"PHASE {n} AUTO-FIXED", "FIX")
        print(f"🔧 Phase {n} auto-fixed")
        return True

    return False

def run():
    print("\nPaste code (END to finish)\n")

    lines = []
    while True:
        try:
            l = input()
            if l.strip() == "END":
                break
            lines.append(l)
        except:
            break

    code = "\n".join(lines)

    phases = []
    cur = []
    n = 0

    for line in code.split("\n"):
        if "# Phase" in line:
            if cur:
                n += 1
                phases.append((n, "\n".join(cur)))
            cur = [line]
        else:
            cur.append(line)

    if cur:
        n += 1
        phases.append((n, "\n".join(cur)))

    if not phases:
        phases = [(1, code)]

    print(f"\n📦 {len(phases)} phases detected\n")

    success = 0
    for n, p in phases:
        if execute_phase(n, p):
            success += 1
        time.sleep(0.5)

    print(f"\n✔ {success}/{len(phases)} completed")

if __name__ == "__main__":
    run()
