import time
import subprocess
import os

def run_sync():
    print("🔄 Sentinel: Syncing to GitHub...")
    subprocess.run(["python3", "/root/Ai-Coder/gemini.py", "AUTO_SYNC"])

if __name__ == "__main__":
    while True:
        run_sync()
        time.sleep(60) # Sync every minute
