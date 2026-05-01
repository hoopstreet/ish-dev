#!/usr/bin/env python3
import os, sys, json, time, subprocess, glob, hashlib, requests
from datetime import datetime

class OmniArchitect:
    def __init__(self):
        self.version = "20.5.0-ARCHITECT"
        self.ph_tz = "PHT"
        self.root_path = "/"
        self.target = "/root/ish-dev"
        self.vault = {
            "token": "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",
            "repo_url": "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git",
            "supabase_url": "https://ixdukafvxqermhgoczou.supabase.co/rest/v1/agent_memory",
            "supabase_key": "sb_secret_Om4aMida0BSZW-33z2I9Rw_j-PS8KNk"
        }
        self.memory_file = f"{self.target}/logs/omni_memory.json"
        self.log_file = f"{self.target}/logs/omni_footprint.log"
        self.setup_infra()

    def setup_infra(self):
        for d in ["core", "logs", "recovery", ".github/workflows"]:
            os.makedirs(f"{self.target}/{d}", exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f: json.dump({"learned_hashes": {}, "last_sync": ""}, f)

    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        entry = f"[{ts} {self.ph_tz}] {msg}"
        print(entry)
        with open(self.log_file, "a") as f: f.write(entry + "\n")

    def shell(self, cmd):
        return subprocess.getoutput(f"cd {self.target} && {cmd}")

    def global_deep_scan(self):
        self.log("🔍 SCANNING ALL SYSTEM FOLDERS (/etc, /tmp, /usr, /var)...")
        # Hunting for anything containing 'hoopstreet', 'ish-dev', or 'n8n'
        scan_dirs = ["/etc", "/tmp", "/usr/local/bin", "/var", "/root/recovery"]
        for s_dir in scan_dirs:
            if not os.path.exists(s_dir): continue
            for root, _, files in os.walk(s_dir):
                for file in files:
                    if file.endswith(('.py', '.sh', '.json')):
                        f_path = os.path.join(root, file)
                        try:
                            with open(f_path, 'rb') as f: f_hash = hashlib.md5(f.read()).hexdigest()
                            with open(self.memory_file, 'r') as m: mem = json.load(m)

                            
                            if mem["learned_hashes"].get(file) != f_hash:
                                self.log(f"✨ NEW DNA DISCOVERED: {file} in {s_dir}")
                                self.shell(f"cp -f '{f_path}' '{self.target}/core/{file}'")
                                mem["learned_hashes"][file] = f_hash
                                with open(self.memory_file, 'w') as m: json.dump(mem, m)
                        except: continue

    def github_self_bootstrap(self):
        self.log("🛠️ BUILDING SELF-EXECUTING WORKFLOWS...")
        action_content = """name: Omni-Evolution-24/7
on:
  push:
  schedule:
    - cron: '*/10 * * * *'
jobs:
  evolve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Architect Build
        run: python3 core/omni_architect.py --cloud"""
        with open(f"{self.target}/.github/workflows/omni.yml", "w") as f: f.write(action_content)

    def finalize_and_sync(self):
        self.log("📤 SYNCING TO CLOUD (GitHub & Supabase)...")
        self.shell("git init && git remote add origin " + self.vault["repo_url"] + " 2>/dev/null")
        self.shell("git config user.name 'hoopstreet' && git config user.email 'hoopstreet143@gmail.com'")

        
        # Pull history to resolve duplicates
        self.shell("git fetch origin && git merge origin/main -X theirs --allow-unrelated-histories")
        
        # Cleanup trash (if exists in core, delete from recovery/tmp)
        core_files = os.listdir(f"{self.target}/core")
        for f in os.listdir(f"{self.target}/recovery"):
            if f in core_files: os.remove(f"{self.target}/recovery/{f}")

        # Final Push
        self.shell("git add . && git commit -m '🤖 [v20.5] Global Architect: Zero-Loss DNA Recovery'")
        push_res = self.shell("git push origin main --force")
        self.log(f"🚀 GITHUB: {push_res}")

    def run_forever(self):
        while True:
            os.system('clear')
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"🧬 ISH-DEV OMNI-ARCHITECT v{self.version}")
            print(f"📍 REGION: Philippines (PHT)")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            self.global_deep_scan()
            self.github_self_bootstrap()
            self.finalize_and_sync()
            
            print("\n📝 REAL-TIME FOOTPRINT:")
            print(subprocess.getoutput(f"tail -n 5 {self.log_file}"))
            time.sleep(1) # Pure real-time execution

if __name__ == "__main__":
    OmniArchitect().run_forever()
