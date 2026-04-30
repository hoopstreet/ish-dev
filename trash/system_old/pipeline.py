#!/usr/bin/env python3
import os, time, subprocess

QUEUE = "/root/ish-dev/queue"

while True:
    files = os.listdir(QUEUE)
    for f in files:
        path = QUEUE + "/" + f
        print("Running:", f)
        subprocess.call(["sh", path])
        os.remove(path)
    time.sleep(5)
