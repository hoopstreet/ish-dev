#!/usr/bin/env python3
import os, sys, json, time, subprocess, glob, hashlib
from datetime import datetime

class IshDevFinalizer:
    def __init__(self):
        self.version = "20.2.0-FINALIZER"
        self.root = "/root"
        self.target = "/root/ish-dev"
        self.vault = {
            "token": "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",
            "repo": "https://hoopstreet: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@github.com/hoopstreet/ish-dev.git"
        }
        self.memory_file = f"{self.target}/logs/discovery_memory.json"
        self.load_memory()

    def shell(self, cmd):
        return subprocess.getoutput(f"cd {self.target} && {cmd}")

    def load_memory(self):
        os.makedirs(f"{self.target}/logs", exist_ok=True)
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f: self.memory = json.load(f)
        else: self.memory = {"hashes": {}, "processed_files": []}

    def save_memory(self):
        with open(self.memory_file, 'w') as f: json.dump(self.memory, f)

    def log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {msg}")
        with open(f"{self.target}/logs/omni_footprint.log", "a") as f:
            f.write(f"[{ts}] {msg}\n")

    def get_hash(self, file_path):
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def discover_and_merge(self):
        self.log("🔍 STARTING GLOBAL DISCOVERY (Searching /root)...")
        # Search for any .py, .sh, .md, .json related to ish-dev outside target
        search_patterns = [f"{self.root}/**/*.py", f"{self.root}/**/*.sh", f"{self.root}/recovery/**/*"]
        for pattern in search_patterns:
            for file_path in glob.glob(pattern, recursive=True):
                if self.target in file_path or "node_modules" in file_path: continue
                
                file_name = os.path.basename(file_path)
                file_hash = self.get_hash(file_path)

                
                # Check memory to see if we've already handled this exact file content
                if self.memory["hashes"].get(file_name) == file_hash:
                    continue 

                self.log(f"✨ FOUND NEW DNA: {file_name}")
                dest = f"{self.target}/core/{file_name}" if file_path.endswith('.py') else f"{self.target}/recovery/{file_name}"
                
                # Adopt/Merge Logic
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                self.shell(f"cp -f '{file_path}' '{dest}'")
                self.memory["hashes"][file_name] = file_hash
                self.log(f"📦 ADOPTED: {file_name} -> {dest}")

    def cleanup_trash(self):
        self.log("🧹 CLEANUP: Removing duplicates & temporary buffers...")
        # Remove files in recovery that already exist in core
        core_files = os.listdir(f"{self.target}/core")
        for rec_file in os.listdir(f"{self.target}/recovery"):
            if rec_file in core_files:
                os.remove(f"{self.target}/recovery/{rec_file}")
                self.log(f"🗑️ DELETED TRASH: Duplicated recovery {rec_file}")

    def finalize_github(self):
        self.log("📤 FINALIZING REPOSITORY: Matching local to GitHub...")
        if not os.path.exists(f"{self.target}/.git"):
            self.shell("git init")
            self.shell(f"git remote add origin {self.vault['repo']}")
        
        self.shell("git add .")
        diff = self.shell("git status --porcelain")
        if diff:
            commit_msg = f"🤖 [v20.2] Omni-Evolution: Global DNA Discovery & Cleanup"
            self.shell(f"git commit -m '{commit_msg}'")
            res = self.shell("git push origin master --force")
            self.log(f"🚀 GITHUB UPDATED: {res}")
        else:
            self.log("✅ GITHUB MATCHED: No new DNA found in this cycle.")

    def run(self):
        while True:
            os.system('clear')
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"🧬 ISH-DEV OMNI-AGENT v{self.version}")
            print(f"🕒 {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            self.discover_and_merge()
            self.cleanup_trash()
            self.finalize_github()
            self.save_memory()
            
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("💤 CYCLE COMPLETE. Sleeping for 8 seconds...")
            time.sleep(8)

if __name__ == "__main__":
    IshDevFinalizer().run()
