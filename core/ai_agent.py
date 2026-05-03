#!/usr/bin/env python3
import sys, os, subprocess, json, requests, re, time
from datetime import datetime

CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"
MEM_FILE = "/root/ish-dev/memory/ai_memory.json"

def get_key():
    if not os.path.exists(CREDS_FILE): return None
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                return line.split('=',1)[1].strip()
    return None

def call_gemini(prompt):
    key = get_key()
    if not key: return None
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    data = {"contents": [{"parts": [{"text": prompt[:2000]}]}]}
    try:
        r = requests.post(f"{url}?key={key}", json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except: pass
    return None

def exec_action(action):
    if action == "heal":
        return os.popen("sh /root/ish-dev/core/heal.sh 2>&1").read()
    if action == "sync":
        return os.popen("sh /root/ish-dev/core/sync.sh 2>&1").read()
    if action == "status":
        return os.popen("cat /root/ish-dev/docs/status.json 2>/dev/null").read()
    if action == "github":
        try:
            r = requests.get("https://api.github.com/repos/hoopstreet/ish-dev", timeout=10)
            if r.status_code == 200:
                d = r.json()
                return f"Repo: {d['name']}\nStars: {d['stargazers_count']}\nForks: {d['forks_count']}"
        except: pass
        return "GitHub API error"
    return None

def save_mem(user, resp):
    mem = {"conversations": []}
    if os.path.exists(MEM_FILE):
        try:
            with open(MEM_FILE, 'r') as f: mem = json.load(f)
        except: pass
    mem["conversations"].append({"time": str(datetime.now()), "user": user[:200], "ai": resp[:200]})
    with open(MEM_FILE, 'w') as f: json.dump(mem, f, indent=2)

def show_help():
    print("""
📋 COMMANDS:
   heal      - Auto-fix system issues
   sync      - Push to GitHub
   status    - Show system status
   github    - Analyze GitHub repo
   ask <q>   - Ask Gemini AI
   help      - This menu
   menu      - Exit to main menu
""")

def main():
    os.system('clear')
    print("\n" + "="*50)
    print("🧠 HOOPSTREET AI AGENT v6.0")
    print("="*50)
    if get_key():
        print("✅ Gemini API: Ready")
    else:
        print("⚠️ No API key. Add via Option 6")
    print("💡 Type 'help' for commands")
    print("="*50)
    
    while True:
        try:
            user = input("\n⚡ ").strip().lower()
            if not user: continue
            
            if user == 'menu':
                print("👋 Goodbye!")
                break
            elif user == 'help':
                show_help()
            elif user == 'heal':
                print("\n🔧 Running heal...")
                print(exec_action('heal')[:500])
            elif user == 'sync':
                print("\n🔄 Syncing...")
                print(exec_action('sync')[:500])
            elif user == 'status':
                print("\n📊 Status:")
                print(exec_action('status')[:500])
            elif user == 'github':
                print("\n🐙 GitHub Analysis:")
                print(exec_action('github')[:500])
            elif user.startswith('ask '):
                q = user[4:]
                print("\n🤖 Thinking...")
                resp = call_gemini(q)
                print(resp if resp else "No response")
            else:
                # Try to understand natural language
                if 'fix' in user or 'heal' in user:
                    print("\n🔧 Running heal...")
                    print(exec_action('heal')[:300])
                elif 'sync' in user or 'push' in user:
                    print("\n🔄 Syncing...")
                    print(exec_action('sync')[:300])
                elif 'status' in user:
                    print("\n📊 Status")
                    print(exec_action('status')[:300])
                elif 'github' in user or 'repo' in user:
                    print("\n🐙 GitHub Analysis")
                    print(exec_action('github')[:300])
                else:
                    print(f"\n🤔 Try: heal, sync, status, github, or ask <question>")
            
            save_mem(user, "processed")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
