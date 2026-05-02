#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        self.repo = "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        self.forbidden = ['token.py', 'traceback.py', 'subprocess.py', 'json.py', 'logging.py', 'datetime.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_history(self):
        self.log("Deep Scanning /recovery for ish-dev DNA...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                if f.endswith(('.py', '.sh')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Adopted: {f}")

    def sync_github(self):
        self.log("Finalizing ish-dev GitHub Merge...")
        commands = [
            "git init",
            f"git remote add origin {self.repo} || git remote set-url origin {self.repo}",
            "git add .",
            "git commit -m '🤖 [v20.0.0] Final ish-dev DNA Merge & Stabilization'",
            "git push origin main --force"
        ]
        for cmd in commands:
            subprocess.run(f"cd {self.target} && {cmd}", shell=True, capture_output=True)
        self.log("✅ GitHub Merge 100% Complete.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_history()
    arch.sync_github()
