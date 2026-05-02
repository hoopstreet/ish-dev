import subprocess

def run(code):
    path = "/tmp/v16.py"

    with open(path,"w") as f:
        f.write(code)

    p = subprocess.run(["python3", path], capture_output=True, text=True)

    return p.returncode, p.stderr
