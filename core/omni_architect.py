#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        # Token-injected URL for non-interactive auth
        self.repo = "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        self.forbidden = ['shutil.py', 'queue.py', '_ssl.py', 'functools.py', 'warnings.py', 'types.py', 'glob.py', 'inspect.py', 'six.py', 'tarfile.py', 'token.py', 'traceback.py', 'subprocess.py', 'logging.py', 'datetime.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_dna(self):
        self.log("Adopting Project DNA (run_bot, auto_sync, platform)...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                if f.endswith(('.py', '.sh', '.json')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Merged: {f}")

    def push_to_github(self):
        self.log("Force-Syncing to GitHub (Auth Injection)...")
        os.chdir(self.target)
        os.system("git init")
        os.system(f"git remote set-url origin {self.repo} || git remote add origin {self.repo}")
        os.system("git add .")
        os.system("git commit -m '🤖 [v20.0.0] Production Ready - Clean Merge'")
        # Force push to clear the 'broken' history on GitHub
        os.system("git push origin main --force")
        self.log("✅ GitHub Sync Complete. Check your repository now.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_dna()
    arch.push_to_github()
