#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        self.repo = "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        # STRICT FORBIDDEN LIST - Do not move these into core
        self.forbidden = ['shutil.py', 'queue.py', '_ssl.py', 'functools.py', 'warnings.py', 'types.py', 'glob.py', 'inspect.py', 'six.py', 'tarfile.py', 'token.py', 'traceback.py', 'subprocess.py', 'logging.py', 'datetime.py', 're.py', 'enum.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_ish_dev(self):
        self.log("Deep Scanning /recovery for Project DNA...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                # ONLY adopt files that are NOT in the forbidden list
                if f.endswith(('.py', '.sh', '.json')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Merged Project File: {f}")

    def sync_to_github(self):
        self.log("Pushing Clean ish-dev Setup to GitHub...")
        # Running without capture_output so you can see any real Git errors
        os.chdir(self.target)
        os.system("git init")
        os.system(f"git remote add origin {self.repo} || git remote set-url origin {self.repo}")
        os.system("git add .")
        os.system("git commit -m '🤖 [v20.0.0] Final Clean Merge - Project DNA Only'")
        os.system("git push origin main --force")
        self.log("✅ GitHub Sync Attempt Finished.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_ish_dev()
    arch.sync_to_github()
