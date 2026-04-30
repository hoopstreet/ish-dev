#!/usr/bin/env python3
import os, subprocess, time

def run():
    print("\nHOOPSTREET AGENT v8 SAFE MODE\n")
    print("Paste code. Type END to execute:\n")

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

    tmp = "/tmp/run.sh"
    with open(tmp, "w") as f:
        f.write(code)

    print("\n[EXECUTING]\n")
    subprocess.call(["sh", tmp])

    os.remove(tmp)
    print("\n[DONE]\n")

if __name__ == "__main__":
    run()
