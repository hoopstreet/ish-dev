#!/usr/bin/env python3
import os, subprocess, shutil
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.target = "/root/ish-dev"
        self.token = "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"
        self.repo_url = f"https://hoopstreet:{self.token}@github.com/hoopstreet/ish-dev.git"
        self.forbidden = ['shutil.py', 'queue.py', '_ssl.py', 'functools.py', 'warnings.py', 'types.py', 'glob.py', 'inspect.py', 'six.py', 'tarfile.py', 'token.py', 'traceback.py', 'subprocess.py', 'logging.py', 'datetime.py']

    def log(self, msg):
        print(f"[{datetime.now().strftime('%I:%M:%S %p')}] 🧬 {msg}")

    def merge_dna(self):
        self.log("Merging Project DNA from Recovery...")
        rec_path = f"{self.target}/recovery"
        if os.path.exists(rec_path):
            for f in os.listdir(rec_path):
                if f.endswith(('.py', '.sh', '.json')) and f not in self.forbidden:
                    shutil.copy2(os.path.join(rec_path, f), f"{self.target}/core/{f}")
                    self.log(f"Adopted: {f}")

    def push_to_github(self):
        self.log("Forcing GitHub Sync with Credential Injection...")
        os.chdir(self.target)
        
        # 1. Reset Git Config locally
        os.system("git config user.email 'hoopstreet143@gmail.com'")
        os.system("git config user.name 'hoopstreet'")
        
        # 2. Force-set the remote with the token
        os.system("git remote remove origin 2>/dev/null")
        os.system(f"git remote add origin {self.repo_url}")
        
        # 3. Add and Commit
        os.system("git add .")
        os.system("git commit -m '🤖 [v20.0.0] Final Project DNA Merge'")
        
        # 4. Use GIT_ASKPASS=true to prevent interactive prompts
        # and force the push to the main branch
        self.log("Pushing to remote...")
        result = os.system(f"git -c core.askPass=true push origin main --force")
        
        if result == 0:
            self.log("🚀 SUCCESS: ish-dev is now live on GitHub!")
        else:
            self.log("❌ CRITICAL: GitHub rejected the token. Verify token permissions.")

if __name__ == "__main__":
    arch = OmniArchitect()
    arch.merge_dna()
    arch.push_to_github()
