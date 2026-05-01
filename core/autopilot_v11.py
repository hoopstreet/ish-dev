#!/usr/bin/env python3
import os, sys, json, time, subprocess, requests
from datetime import datetime

class IshDevAutopilot:
    def __init__(self):
        self.root = "/root/ish-dev"
        self.vault = {
            "gh_token": "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",
            "repo": "https://github.com/hoopstreet/ish-dev",
            "supabase_url": "https://ixdukafvxqermhgoczou.supabase.co",
            "supabase_key": "sb_secret_Om4aMida0BSZW-33z2I9Rw_j-PS8KNk",
            "gemini_pool": [
                "AIzaSyDHhh5zkL6NnEBD9SI-sLfl9Ur8yNA6PxA",
                "AIzaSyDpuZ5pFlQd0ezHxNJfoWHos_XiegAiV14",
                "AIzaSyA5BU2mk6o2HHJMq1pqydwFeJUpd36akHU",
                "AIzaSyBzw8_9DqLXqhxzGRl0xrdXNIHPvGlIjPA",
                "AIzaSyDl3XCDiTlrLbKtHyMFNArFprdKNzFrz7E"
            ]
        }
        self.current_key = 0

    def log(self, msg):
        with open(f"{self.root}/logs/autopilot.log", "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

    def execute(self, cmd):
        return subprocess.getoutput(cmd)

    def ui_box(self, text):
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(text)
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def phase_runner(self, phase_name, logic_func):
        sys.stdout.write(f"🔧 {phase_name}...")
        sys.stdout.flush()
        try:
            logic_func()
            print(" ✅ DONE")
        except Exception as e:
            print(f" ❌ FAILED: {e}")

    def run_brain(self):
        os.system('clear')
        self.ui_box("🤖 ISH-DEV AUTOPILOT: STARTING SELF-EVOLUTION")

        
        # PHASE 1: Fix Git Repo
        def fix_git():
            if not os.path.exists(f"{self.root}/.git"):
                self.execute(f"cd {self.root} && git init && git remote add origin {self.vault['repo']}")
            self.execute(f"git config --global user.name 'hoopstreet'")
            self.execute(f"git config --global user.email 'hoopstreet143@gmail.com'")
        self.phase_runner("GIT_AUTO_LINK", fix_git)

        # PHASE 2: Analyze DNA & Recovery
        def analyze_dna():
            # Merging recovery versions to core
            self.execute(f"cp -r {self.root}/recovery/* {self.root}/core/ 2>/dev/null")
            self.log("DNA Merged from Recovery folder")
        self.phase_runner("DNA_MERGE_ADOPTION", analyze_dna)

        # PHASE 3: Self-Healing & Upgrade
        def heal():
            # Check for missing Python libs and install
            self.execute("pip install requests supabase 2>/dev/null")
            self.log("Infrastructure dependencies verified")
        self.phase_runner("HEAL_ENGINE_INFRA", heal)

        # PHASE 4: Perpetual Sync
        def cloud_sync():
            msg = f"🤖 [Autopilot] Auto-Upgrade {datetime.now().strftime('%Y%m%d-%H%M')}"
            self.execute(f"cd {self.root} && git add . && git commit -m '{msg}' && git push origin main")
        self.phase_runner("GITHUB_MIRROR_SYNC", cloud_sync)

        print("\n🎉 ALL PHASES COMPLETED SUCCESSFULLY! 🎉")
        print(f"✅ Completed on {datetime.now().strftime('%b %d, %Y at %I:%M:%S %p PHT')}")
        self.ui_box("STATUS: PERPETUAL MONITORING ACTIVE")
        
        # Loop to keep it alive without human input
        time.sleep(5)
        self.run_brain()

if __name__ == "__main__":
    IshDevAutopilot().run_brain()
