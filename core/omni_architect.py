#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        # Using the direct token URL format
        self.token = "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"
        self.repo_url = f"https://hoopstreet:{self.token}@github.com/hoopstreet/ish-dev.git"
        self.forbidden = ['shutil.py', 'queue.py', '_ssl.py', 'functools.py', 'warnings.py', 'types.py', 'glob.py', 'inspect.py', 'six.py', 'tarfile.py', 'token.py', 'traceback.py', 'subprocess.py', 'logging.py', 'datetime.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_dna(self):
        self.log("Merging /recovery files into Core...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                if f.endswith(('.py', '.sh', '.json')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Adopted: {f}")

    def push_to_github(self):
        self.log("Initiating Force-Push to GitHub...")
        os.chdir(self.target)
        
        # Configure Git Identity
        os.system("git config --global user.email 'hoopstreet143@gmail.com'")
        os.system("git config --global user.name 'hoopstreet'")
        
        # Reset Remote and Push
        os.system("git init")
        os.system(f"git remote remove origin 2>/dev/null")
        os.system(f"git remote add origin {self.repo_url}")
        os.system("git add .")
        os.system("git commit -m '🤖 [v20.0.0] Production Ready - Final DNA Merge'")
        
        # CAPTURING THE PUSH RESULT
        result = os.system("git push origin main --force")
        if result == 0:
            self.log("🚀 SUCCESS: GitHub is now updated!")
        else:
            self.log("❌ FAILED: Still having Auth issues. Check token validity.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_dna()
    arch.push_to_github()
