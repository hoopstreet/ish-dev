#!/usr/bin/env python3
import os, sys, json, time, subprocess, requests, glob
from datetime import datetime

class IshOmniEvolution:
    def __init__(self):
        self.version = "20.0.0-OMNI"
        self.root = "/root/ish-dev"
        self.recovery_dir = f"{self.root}/recovery"
        self.vault = {
            "gh_token": "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",
            "repo_url": "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git",
            "gemini_keys": ["AIzaSyDHhh5zkL6NnEBD9SI-sLfl9Ur8yNA6PxA", "AIzaSyDpuZ5pFlQd0ezHxNJfoWHos_XiegAiV14", "AIzaSyA5BU2mk6o2HHJMq1pqydwFeJUpd36akHU"]
        }

    def shell(self, cmd):
        return subprocess.getoutput(f"cd {self.root} && {cmd}")

    def log(self, action, status):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{self.root}/logs/evolution.log", "a") as l:
            l.write(f"[{ts}] v{self.version} | {action} | {status}\n")

    def bootstrap_git(self):
        if not os.path.exists(f"{self.root}/.git"):
            self.shell("git init")
        self.shell(f"git remote remove origin 2>/dev/null")
        self.shell(f"git remote add origin {self.vault['repo_url']}")
        self.shell("git config --global user.email 'hoopstreet143@gmail.com' && git config --global user.name 'hoopstreet'")

    def deep_recursive_adoption(self):
        # Scan all recovery tarballs or folders for code blocks
        snapshots = glob.glob(f"{self.recovery_dir}/**/*", recursive=True)
        for snap in snapshots:
            if os.path.isfile(snap) and snap.endswith(('.py', '.sh', '.md')):
                target_path = snap.replace(self.recovery_dir, f"{self.root}/core")
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                # Analyze if target exists, if not, or if older, adopt it.
                self.shell(f"cp -u {snap} {target_path}")
        self.log("RECOVERY_ADOPTION", "SUCCESS - All versions merged to Core")

    def self_heal_and_upgrade(self):
        # Fix permissions and missing headers for all v20 scripts
        self.shell("chmod +x core/*.sh core/*.py 2>/dev/null")
        self.shell("find . -name '*.py' -exec sed -i '1i #!/usr/bin/env python3' {} + 2>/dev/null")
        self.log("INFRA_HEALING", "SUCCESS - Permissions & Shebangs restored")

    def auto_commit_push(self):
        status = self.shell("git status --porcelain")
        if status:
            self.shell("git add .")
            self.shell(f"git commit -m '🤖 [v20-OMNI] Auto-Evolution: Merge Recovery & Self-Heal'")
            res = self.shell("git push origin master --force")
            self.log("GITHUB_SYNC", f"PUSHED - {res}")
        else:
            self.log("GITHUB_SYNC", "SKIPPED - No changes detected")

    def run_loop(self):
        while True:
            os.system('clear')
            print("═══════════════════════════════════════════════════════")
            print(f"🧬 ISH-DEV OMNI-AGENT v{self.version} [AUTOPILOT]")
            print("═══════════════════════════════════════════════════════")
            print("⚡ STATUS: Active Exploration & Adoption...")
            
            self.bootstrap_git()
            self.deep_recursive_adoption()
            self.self_heal_and_upgrade()
            self.auto_commit_push()

            print("✅ CYCLE COMPLETE. Sleeping for 300s...")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            time.sleep(300) # Re-analyze every 5 minutes

if __name__ == "__main__":
    IshOmniEvolution().run_loop()
