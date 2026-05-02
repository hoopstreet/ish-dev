#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        self.token = "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"
        self.repo_url = "https://github.com/hoopstreet/ish-dev.git"
        self.forbidden = ['shutil.py', 'queue.py', '_ssl.py', 'functools.py', 'warnings.py', 'types.py', 'glob.py', 'inspect.py', 'six.py', 'tarfile.py', 'token.py', 'traceback.py', 'subprocess.py', 'logging.py', 'datetime.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_dna(self):
        self.log("Adopting ish-dev DNA...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                if f.endswith(('.py', '.sh', '.json')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Recovered: {f}")

    def push_to_github(self):
        self.log("Forcing Push to ish-dev via Credential Helper...")
        os.chdir(self.target)
        os.system("git config user.email 'hoopstreet143@gmail.com'")
        os.system("git config user.name 'hoopstreet'")
        
        # Setup credential injection
        cmd = f"git remote set-url origin https://hoopstreet:{self.token}@github.com/hoopstreet/ish-dev.git"
        os.system(cmd)
        
        os.system("git add .")
        os.system("git commit -m '🤖 [v20.0.0] Production Ready - Final DNA Merge'")
        
        # Force push using the injected credentials
        result = os.system("git push origin main --force")
        
        if result == 0:
            self.log("🚀 SUCCESS: ish-dev updated at https://github.com/hoopstreet/ish-dev")
        else:
            self.log("❌ FAILED: Token Rejected. Generate a new PAT with 'repo' scope.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_dna()
    arch.push_to_github()
