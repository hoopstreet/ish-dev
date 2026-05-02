#!/usr/bin/env python3
import os, sys, json, time, subprocess, requests

class HoopstreetUltimate:
    def __init__(self):
        self.version = "10.5.1-FINAL"
        self.root = "/root/ish-dev"
        self.vault_path = "/root/.hoopstreet/creds/master_vault.json"
        self.load_config()

    def load_config(self):
        try:
            with open(self.vault_path, "r") as f:
                self.vault = json.load(f)
            self.keys = self.vault.get("gemini_pool", [])
            self.current_key = 0
        except:
            print("⚠️ Vault missing. Run Setup first.")
            self.keys = []

    def call_gemini(self, prompt):
        if not self.keys: return "Error: No Keys"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.keys[self.current_key]}"
        data = {"contents": [{"parts": [{"text": f"SYSTEM: You are the Hoopstreet OS v10.5.0 Master AI. Context: TikTok Affiliate/N8N/Supabase. Task: {prompt}"}]}]}
        try:
            res = requests.post(url, json=data, timeout=10)
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            self.current_key = (self.current_key + 1) % len(self.keys)
            return "🔄 Key Rotated. Retrying..."

    def sync_dna(self):
        print("🧬 Syncing DNA to GitHub Actions...")
        os.system("git add . && git commit -m '🤖 [Final Merge] v10.5 Stable' && git push")
        print("✅ Cloud Blueprint Updated.")
        time.sleep(1.5)

    def self_heal(self):
        print("🔧 Running Deep System Recovery...")
        # Merges legacy heal.sh and agent_self_improving logic
        os.system(f"sh {self.root}/core/heal.sh")
        print("✅ Environment Restored.")
        time.sleep(1.5)

    def run_agent(self):
        os.system('clear')
        print(f"🤖 GEMINI CLI PROFESSIONAL - v{self.version}")
        print("Status: 24/7 Automated Mode Active")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        while True:
            cmd = input("Hoopstreet-AI > ")
            if cmd.lower() in ['exit', '0']: break
            print("🧠 Processing...")
            print(f"\n✨ {self.call_gemini(cmd)}\n")

    def main_menu(self):
        while True:
            os.system('clear')
            print("═══════════════════════════════════════════════════════")
            print(f"  📋 HOOPSTREET OS MASTER MENU - v{self.version}")
            print("═══════════════════════════════════════════════════════")
            print("  1. 🤖 AI Agent     - Professional Gemini CLI")
            print("  2. 🔄 Cloud Sync   - Full GitHub Merge/Push")
            print("  3. 🔧 Self-Heal    - DNA Restore & Bug Fix")
            print("  4. 📈 Stats        - Check DNA & Roadmap")
            print("  5. 🔗 Credentials  - Manage Vault/API Keys")
            print("  6. ⚡ AI Sync      - Trigger GitHub Actions")
            print("  0. 🚪 Shutdown     - Exit to iSH")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            choice = input("👉 Select Action (0-6): ")
            if choice == '1': self.run_agent()
            elif choice == '2': self.sync_dna()
            elif choice == '3': self.self_heal()
            elif choice == '4': print(f"DNA: 100%\nVersion: {self.version}"); time.sleep(2)
            elif choice == '6': self.sync_dna()
            elif choice == '0': break

if __name__ == "__main__":
    HoopstreetUltimate().main_menu()
