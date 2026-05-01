#!/usr/bin/env python3
import os, sys, json, time, subprocess, requests

class HoopstreetOS:
    def __init__(self):
        self.version = "10.5.0-PRO"
        self.root = "/root/ish-dev"
        self.vault_path = "/root/.hoopstreet/creds/master_vault.json"
        self.load_creds()

    def load_creds(self):
        try:
            with open(self.vault_path, "r") as f:
                self.vault = json.load(f)
            self.keys = self.vault.get("gemini_pool", [])
            self.current_key_index = 0
        except:
            self.vault = {}; self.keys = []

    def get_active_key(self):
        return self.keys[self.current_key_index] if self.keys else None

    def rotate_key(self):
        if self.keys:
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)

    def ai_query(self, prompt):
        key = self.get_active_key()
        if not key: return "❌ No API Keys found."
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            self.rotate_key()
            return "🔄 Key rotated. Retrying..."

    def run_agent(self):
        os.system('clear')
        print("🤖 GEMINI CLI AGENT - AUTONOMOUS MODE")
        print(f"📡 Using Key Slot: {self.current_key_index}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        while True:
            cmd = input("Hoopstreet-AI > ")
            if cmd.lower() in ['exit', 'quit', '0']: break
            print("🧠 Thinking...")
            response = self.ai_query(f"Context: TikTok Affiliate Automation. Task: {cmd}")
            print(f"\n✨ Response:\n{response}\n")

    def sync_247(self):
        print("🔄 Syncing DNA to GitHub...")
        os.system(f"cd {self.root} && git add . && git commit -m '🤖 Auto-Sync' && git push")
        time.sleep(1)

    def system_heal(self):
        print("🔧 Repairing iSH environment...")
        os.system(f"sh {self.root}/core/heal.sh")
        print("✅ Healthy.")
        time.sleep(1)

    def menu(self):
        while True:
            os.system('clear')
            print("═══════════════════════════════════════════════════════")
            print(f"  📋 HOOPSTREET iSH AUTO HEALING AGENT v{self.version}")
            print("═══════════════════════════════════════════════════════")
            print("  1. 🤖 Agent       - Gemini CLI (Automated)")
            print("  2. 🔄 Sync        - Git push/pull with auto-version")
            print("  3. 🔧 Heal        - Auto-fix common bugs / DNA Restore")
            print("  4. 📊 Status      - View DNA, roadmap, logs")
            print("  5. 🔗 Remote      - GitHub Projects Manager")
            print("  6. 🔐 Credentials - Secure Token Storage")
            print("  7. 🤖 AI Sync     - Trigger GitHub Actions")
            print("  0. 🚪 Exit        - Exit to shell")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            choice = input("👉 Choose (0-7): ")
            if choice == '1': self.run_agent()
            elif choice == '2': self.sync_247()
            elif choice == '3': self.system_heal()
            elif choice == '0': break

if __name__ == "__main__":
    HoopstreetOS().menu()
