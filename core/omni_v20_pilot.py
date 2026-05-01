#!/usr/bin/env python3
import os, sys, json, time, subprocess, glob
from datetime import datetime

class IshOmniEvolution:
    def __init__(self):
        self.version = "20.1.0-INSIGHT"
        self.root = "/root/ish-dev"
        self.recovery_dir = f"{self.root}/recovery"
        self.vault = {
            "gh_token": "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",
            "repo_url": "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        }
        self.current_action = "Initializing..."

    def shell(self, cmd):
        return subprocess.getoutput(f"cd {self.root} && {cmd}")

    def log_activity(self, msg):
        self.current_action = msg
        ts = datetime.now().strftime("%H:%M:%S")
        with open(f"{self.root}/logs/live_footprint.log", "a") as f:
            f.write(f"[{ts}] {msg}\n")

    def sync_remote(self):
        self.log_activity("🔍 CHECKING GITHUB: Fetching remote updates...")
        if not os.path.exists(f"{self.root}/.git"):
            self.shell("git init")
            self.shell(f"git remote add origin {self.vault['repo_url']}")
        
        self.shell("git fetch --all")
        res = self.shell("git merge origin/master -X theirs --allow-unrelated-histories")
        if "Already up to date" in res:
            self.log_activity("☁️ GITHUB: Local matches Remote (No changes).")
        else:
            self.log_activity("📥 GITHUB: Pulled new recovery data from Cloud.")

    def deep_recursive_adoption(self):
        self.log_activity("🧬 DNA SCAN: Searching /recovery for missing versions...")
        snapshots = glob.glob(f"{self.recovery_dir}/**/*", recursive=True)
        count = 0
        for snap in snapshots:
            if os.path.isfile(snap) and snap.endswith(('.py', '.sh', '.md', '.json')):
                target_path = snap.replace(self.recovery_dir, f"{self.root}/core")
                if not os.path.exists(target_path):

                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    self.shell(f"cp -u '{snap}' '{target_path}'")
                    self.log_activity(f"✨ ADOPTED: {os.path.basename(snap)} (New Logic Found)")
                    count += 1
        if count == 0:
            self.log_activity("✅ DNA: Core is 100% complete. No missing files.")

    def self_heal(self):
        self.log_activity("🔧 HEALING: Fixing permissions & environment...")
        self.shell("chmod +x core/*.sh core/*.py 2>/dev/null")
        self.log_activity("🩹 HEALING: Environment stabilized.")

    def auto_push(self):
        self.log_activity("📤 SYNC: Committing local evolution to GitHub...")
        self.shell("git config user.email 'hoopstreet143@gmail.com'")
        self.shell("git config user.name 'hoopstreet'")
        status = self.shell("git status --porcelain")
        if status:
            self.shell("git add .")
            self.shell(f"git commit -m '🤖 [v20.1] Auto-Pilot Evolution'")
            self.shell("git push origin master --force")
            self.log_activity("🚀 SUCCESS: Cloud Repository Updated.")
        else:
            self.log_activity("😴 IDLE: No new improvements to push.")

    def run_loop(self):
        while True:
            os.system('clear')
            print("═══════════════════════════════════════════════════════")
            print(f"🧬 ISH-DEV OMNI-AGENT v{self.version}")
            print("═══════════════════════════════════════════════════════")
            print(f"🕒 TIME: {datetime.now().strftime('%I:%M:%S %p')}")
            print(f"📡 CURRENT TASK: {self.current_action}")
            print("═══════════════════════════════════════════════════════")
            
            # Show the last 5 activities for "Footprint"
            if os.path.exists(f"{self.root}/logs/live_footprint.log"):
                print("📝 RECENT FOOTPRINT:")
                tail = subprocess.getoutput(f"tail -n 5 {self.root}/logs/live_footprint.log")
                print(tail)
            
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            self.sync_remote()
            self.deep_recursive_adoption()
            self.self_heal()
            self.auto_push()

            time.sleep(8)

if __name__ == "__main__":
    IshOmniEvolution().run_loop()
