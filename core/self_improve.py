#!/usr/bin/env python3
#!/usr/bin/env python3
import os, time, json

LOG = "/root/ish-dev/logs.txt"
DNA = "/root/ish-dev/DNA.md"

def analyze_failures():
    if not os.path.exists(LOG):
        return []

    with open(LOG) as f:
        lines = f.readlines()

    fails = [l for l in lines if "FAILED" in l]
    return fails[-10:]

def improve_system():
    fails = analyze_failures()

    if len(fails) > 3:
        with open("/root/ish-dev/ROADMAP.md", "a") as f:
            f.write("\n## AUTO-IMPROVEMENT TRIGGERED\n")
            f.write("- Detected repeated failures\n")
            f.write("- System suggests refactor\n")

        print("🧬 Self-improvement triggered")

if __name__ == "__main__":
    while True:
        improve_system()
        time.sleep(30)
