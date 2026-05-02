#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Notice: {result.stderr.strip()}")
    return result.stdout.strip()

def get_pht_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S PHT")

def start_auto_merge():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔄 HOOPSTREET AUTO-MERGE & SYNC ENGINE v9.3.2")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Identity & State Prep
    run_command("git config --global user.email 'hoopstreet143@gmail.com'")
    run_command("git config --global user.name 'hoopstreet'")
    
    # 2. Force Pull/Rebase with Stash
    print("[*] Syncing with Remote...")
    run_command("git stash")
    run_command("git pull origin main --rebase")
    run_command("git stash pop")

    # 3. Versioning & DNA Update
    new_version = "v9.3.2"
    print(f"[*] Incrementing System DNA to {new_version}...")
    
    # 4. Commit & Tag
    run_command("git add .")
    run_command(f'git commit -m "{new_version}: Mobile-optimized merge"')
    run_command(f"git tag -d {new_version}") # Delete local if exists
    run_command(f"git tag {new_version}")

    # 5. Authenticated Push
    print("[*] Pushing updates to GitHub...")
    # Remote URL already contains the token from Step 1
    push_op = subprocess.run("git push origin main --tags --force", shell=True)
    
    if push_op.returncode == 0:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("✅ FULL AUTOMATED MERGE SUCCESSFUL!")
        print(f"📌 Version: {new_version}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    else:
        print("❌ Push failed. Verify token permissions.")

if __name__ == "__main__":
    start_auto_merge()
