#!/usr/bin/env python3
import os, sys, json, time, subprocess, glob
from datetime import datetime

class IshOmniEvolution:
    def __init__(self):
        self.version = "20.0.0-OMNI"
        self.root = "/root/ish-dev"
        self.recovery_dir = f"{self.root}/recovery"
        self.vault = {
            "gh_token": "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",
            "repo_url": "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        }

    def shell(self, cmd):
        return subprocess.getoutput(f"cd {self.root} && {cmd}")

    def log(self, action, status):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        os.makedirs(f"{self.root}/logs", exist_ok=True)
        with open(f"{self.root}/logs/evolution.log", "a") as l:
            l.write(f"[{ts}] v{self.version} | {action} | {status}\n")

    def sync_remote(self):
        """Pull from GitHub first to catch remote changes/duplicates."""
        if not os.path.exists(f"{self.root}/.git"):
            self.shell("git init")
            self.shell(f"git remote add origin {self.vault['repo_url']}")
        
        # Fetch and merge remote changes
        self.shell("git fetch --all")
        res = self.shell("git merge origin/master -X theirs --allow-unrelated-histories")
        self.log("REMOTE_SYNC", f"PULL/MERGE: {res}")

    def deep_recursive_adoption(self):
        """Adopts files from /recovery and resolves duplicates."""
        snapshots = glob.glob(f"{self.recovery_dir}/**/*", recursive=True)
        for snap in snapshots:
            if os.path.isfile(snap) and snap.endswith(('.py', '.sh', '.md', '.json')):
                # Logic: If it exists in recovery but missing in core, move it.
                # If duplicate, 'cp -u' only updates if recovery is newer.
                target_path = snap.replace(self.recovery_dir, f"{self.root}/core")
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                self.shell(f"cp -u '{snap}' '{target_path}'")
        self.log("DNA_ADOPTION", "RECOVERY MERGED TO CORE")

    def self_heal(self):
        """Fixes permissions and environment issues."""
        self.shell("chmod +x core/*.sh core/*.py 2>/dev/null")
        self.log("SELF_HEAL", "INFRASTRUCTURE STABILIZED")

    def auto_push(self):
        """Commits all local merges/adoptions and pushes to GitHub."""
        self.shell("git config user.email 'hoopstreet143@gmail.com'")
        self.shell("git config user.name 'hoopstreet'")
        status = self.shell("git status --porcelain")
        if status:
            self.shell("git add .")
            self.shell(f"git commit -m '🤖 [v20-OMNI] Auto-Pilot: Merge, Adopt & Evolution'")
            res = self.shell("git push origin master --force")
            self.log("GITHUB_PUSH", f"RESULT: {res}")

    def run_loop(self):
        while True:
            os.system('clear')
            print("═══════════════════════════════════════════════════════")
            print(f"🧬 ISH-DEV OMNI-AGENT v{self.version} [FAST-AUTOPILOT]")

            print("═══════════════════════════════════════════════════════")
            print(f"🕒 Last Run: {datetime.now().strftime('%I:%M:%S %p')}")
            print("⚡ STATUS: Pulling Remote > Merging Recovery > Pushing Evolution...")
            
            self.sync_remote()
            self.deep_recursive_adoption()
            self.self_heal()
            self.auto_push()

            print("✅ CYCLE COMPLETE. Next run in 8 seconds...")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            time.sleep(8)

if __name__ == "__main__":
    IshOmniEvolution().run_loop()
