import subprocess
def run_code(code):
    with open("/tmp/exec_v16.py", "w") as f:
        f.write(code)
    p = subprocess.run(["python3", "/tmp/exec_v16.py"], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr
