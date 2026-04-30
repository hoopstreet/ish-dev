#!/usr/bin/env python3
import subprocess, os, time
from ai_engine import fix_code

def run_script(code):
    tmp = "/tmp/run.sh"
    with open(tmp, "w") as f:
        f.write(code)

    result = subprocess.run(
        ["sh", tmp],
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr

def git_sync():
    try:
        os.chdir("/root/ish-dev")
        subprocess.call(["git","add","."])
        subprocess.call(["git","commit","-m","auto"])
        subprocess.call(["git","push"])
        print("🔄 Synced")
    except:
        print("⚠️ Git skipped")

def main():
    print("\n💎 HOOPSTREET V12 AI SYSTEM\n")
    print("Paste code (END to run):")

    lines = []
    while True:
        l = input()
        if l.strip() == "END":
            break
        lines.append(l)

    code = "\n".join(lines)

    for attempt in range(5):
        print(f"\n⚙️ Attempt {attempt+1}")

        rc, out, err = run_script(code)

        if rc == 0:
            print("✅ SUCCESS")
            print(out)
            git_sync()
            return

        print("❌ ERROR:")
        print(err)

        fixed = fix_code(code, err)

        if not fixed:
            print("⚠️ AI failed")
            return

        print("🤖 Applying AI fix...")
        code = fixed

    print("❌ FAILED AFTER RETRIES")
