#!/usr/bin/env python3
#!/usr/bin/env python3
import time, os, subprocess

WATCH = "/root/ish-dev/remote.txt"

last = ""

while True:
    if os.path.exists(WATCH):
        data = open(WATCH).read()
        if data != last:
            print("📡 Remote trigger detected")
            subprocess.call(["python3", "/root/ish-dev/system/agent.py"])
            last = data
    time.sleep(3)
