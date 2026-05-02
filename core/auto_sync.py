#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return None

def get_pht_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S PHT")

def start_auto_merge():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔄 HOOPSTREET AUTO-MERGE & SYNC ENGINE")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Identity Verification
    print("[*] Configuring GitHub Identity...")
    run_command("git config --global user.email 'hoopstreet@ish-dev.com'")
    run_command("git config --global user.name 'Hoopstreet-AI'")

    # 2. Pull & Rebase
    print("[*] Fetching latest changes (Rebase)...")
    run_command("git pull origin main --rebase")

    # 3. Versioning (v9.3.0 -> v9.3.1)
    new_version = "v9.3.1"
    print(f"[*] Incrementing System DNA to {new_version}...")
    
    # 4. Stage & Commit
    print("[*] Staging core updates...")
    run_command("git add .")
    commit_msg = f"[{new_version}] Automated System Merge - {get_pht_time()}"
    run_command(f'git commit -m "{commit_msg}"')

    # 5. Tagging
    print(f"[*] Creating release tag: {new_version}...")
    run_command(f"git tag -a {new_version} -m 'Automated Release'")

    # 6. Push
    print("[*] Pushing to GitHub Repository...")
    push_res = run_command("git push origin main --tags --force")
    
    if push_res is not None:
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("✅ FULL AUTOMATED MERGE COMPLETE!")
        print(f"📌 Version: {new_version}")
        print(f"⏰ Timestamp: {get_pht_time()}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    else:
        print("❌ Sync Failed. Check Credentials/Token.")

if __name__ == "__main__":
    start_auto_merge()
