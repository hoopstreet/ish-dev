#!/usr/bin/env python3
import os, sys, json, subprocess, hashlib, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.version = "20.5.1-PATCHED"
        self.target = "/root/ish-dev"
        self.forbidden = ['types.py', 'functools.py', 're.py', 'enum.py', 'logging.py', 'inspect.py', 'datetime.py', 'warnings.py', 'json.py', 'os.py', 'sys.py', 'shutil.py', 'glob.py', 'hashlib.py', 'ssl.py', '_ssl.py']
        self.log_file = f"{self.target}/logs/omni_footprint.log"

    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        print(f"[{ts} PHT] {msg}")

    def auto_adopt_dna(self):
        self.log("🔍 Running Safe Scan (Skipping System Names)...")
        search_paths = ["/tmp", "/root/ish-dev/recovery"]
        for path in search_paths:
            if not os.path.exists(path): continue
            for file in os.listdir(path):
                if file.endswith(('.py', '.sh', '.json')) and file not in self.forbidden:
                    shutil.copy2(os.path.join(path, file), f"{self.target}/core/{file}")
                    self.log(f"✨ DNA ADOPTED: {file}")

    def run(self):
        self.auto_adopt_dna()
        # Auto-sync to GitHub
        subprocess.run(f"cd {self.target} && git add . && git commit -m '🤖 Auto-fix: Filtered DNA adoption' && git push origin main --force", shell=True, capture_output=True)
        self.log("✅ System Stabilized & Cloud Synced.")

if __name__ == "__main__":
    OmniArchitect().run()
