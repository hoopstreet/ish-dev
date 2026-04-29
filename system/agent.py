#!/usr/bin/env python3
import os, subprocess, time, datetime

MEMORY = "/root/ish-dev/memory/history.log"
REPO = "/root/ish-dev"

def save_memory(code):
    with open(MEMORY, "a") as f:
        f.write("\n==== " + str(datetime.datetime.now()) + " ====\n")
        f.write(code + "\n")

def git_sync():
    try:
        os.chdir(REPO)
        subprocess.call(["git", "add", "."])
        subprocess.call(["git", "commit", "-m", "auto-sync " + str(time.time())])
        subprocess.call(["git", "push"])
        print("🔄 Auto Git Sync Complete")
    except:
        print("⚠️ Git sync skipped")

def split_phases(code):
    phases, current = [], []
    for line in code.split("\n"):
        if line.lower().startswith("# phase"):
            if current:
                phases.append("\n".join(current))
                current = []
        current.append(line)
    if current:
        phases.append("\n".join(current))
    return phases

def run():
    print("\n🚀 HOOPSTREET V10\n")
    print("Paste code (END to run):\n")

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

    save_memory(code)

    phases = split_phases(code)
    print(f"\n📊 {len(phases)} phase(s)\n")

    for i, p in enumerate(phases, 1):
        print(f"\n=== PHASE {i} ===\n")

        tmp = f"/tmp/p{i}.sh"
        with open(tmp, "w") as f:
            f.write(p)

        result = subprocess.call(["sh", tmp])

        if result != 0:
            print(f"\n❌ Phase {i} failed\n")
            print("🤖 Attempting auto-fix...")

            # simple AI debug (basic fallback)
            fixed = p.replace("pip install", "pip3 install")
            with open(tmp, "w") as f:
                f.write(fixed)

            retry = subprocess.call(["sh", tmp])

            if retry != 0:
                print("❌ Auto-fix failed. Stopping.")
                return

        os.remove(tmp)

    print("\n✅ DONE\n")
    git_sync()

if __name__ == "__main__":
    run()
