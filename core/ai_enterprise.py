#!/usr/bin/env python3
import sys, os, subprocess, json, requests, time
from datetime import datetime

CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"

def get_cred(name):
    """Read credential from Option 6 storage"""
    if not os.path.exists(CREDS_FILE):
        return None
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            if line.startswith(f"{name}="):
                return line.split('=',1)[1].strip()
    return None

def get_all_creds():
    """Get all credentials as dict"""
    creds = {}
    if not os.path.exists(CREDS_FILE):
        return creds
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=',1)
                creds[k.strip()] = v.strip()
    return creds

def call_ai(prompt):
    """Call AI using available keys from credentials"""
    creds = get_all_creds()
    
    # Try OpenRouter first
    or_key = creds.get("OPENROUTER_KEY") or creds.get("OR_KEY")
    if or_key:
        return call_openrouter(or_key, prompt)
    
    # Try Gemini
    gem_key = creds.get("GEMINI_API_KEY") or creds.get("GEMINI_KEY")
    if gem_key:
        return call_gemini(gem_key, prompt)
    
    return "⚠️ No AI key found. Add OPENROUTER_KEY or GEMINI_API_KEY via Option 6"

def call_openrouter(key, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt[:2000]}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    try:
        r = requests.post(url, headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"OpenRouter Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return f"Error: {str(e)[:100]}"

def call_gemini(key, prompt):
    models = ["gemini-1.5-flash", "gemini-pro"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        data = {"contents": [{"parts": [{"text": prompt[:2000]}]}]}
        try:
            r = requests.post(f"{url}?key={key}", json=data, timeout=30)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return "Gemini API failed"

def analyze_project():
    results = ["📁 PROJECT ANALYSIS\n"]
    core_dir = "/root/ish-dev/core"
    if os.path.exists(core_dir):
        scripts = [f for f in os.listdir(core_dir) if f.endswith(('.sh','.py'))]
        results.append(f"📂 Core Scripts: {len(scripts)} files")
        for s in scripts[:10]:
            results.append(f"   • {s}")
    return '\n'.join(results)

def analyze_github():
    try:
        r = requests.get("https://api.github.com/repos/hoopstreet/ish-dev", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return f"""📦 {d['name']}
⭐ Stars: {d['stargazers_count']}
🍴 Forks: {d['forks_count']}
📝 {d.get('description', 'N/A')[:100]}"""
        return "GitHub API error"
    except:
        return "Cannot reach GitHub"

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return r.stdout[:500] if r.stdout else r.stderr[:200]
    except:
        return "Command failed"

def main():
    os.system('clear')
    print("\n" + "="*55)
    print("🏢 HOOPSTREET AI AGENT v7.6")
    print("="*55)
    
    # Show credentials status
    creds = get_all_creds()
    has_ai = False
    if creds.get("OPENROUTER_KEY") or creds.get("OR_KEY"):
        print("✅ OpenRouter API: READY (from Option 6)")
        has_ai = True
    elif creds.get("GEMINI_API_KEY") or creds.get("GEMINI_KEY"):
        print("✅ Gemini API: READY (from Option 6)")
        has_ai = True
    else:
        print("⚠️ No API key found in credentials")
        print("💡 Add via Option 6:")
        print("   Name: OPENROUTER_KEY")
        print("   Value: sk-or-v1-...")
    
    print("="*55)
    print("📋 COMMANDS: analyze | github | status | heal | sync")
    print("💡 Or just ask a question naturally!")
    print("💡 Type 'menu' to exit")
    print("="*55)
    
    while True:
        try:
            u = input("\n⚡ ").strip()
            if not u: continue
            if u.lower() == 'menu':
                print("👋 Goodbye!")
                break
            
            low = u.lower()
            
            # Handle commands
            if low == 'analyze':
                print(analyze_project())
            elif low == 'github':
                print(analyze_github())
            elif low == 'status':
                print(run_cmd("cat /root/ish-dev/docs/status.json 2>/dev/null || echo 'No status file'"))
            elif low == 'heal':
                print(run_cmd("sh /root/ish-dev/core/heal.sh 2>/dev/null || echo 'Heal script not found'"))
            elif low == 'sync':
                print(run_cmd("sh /root/ish-dev/core/sync.sh 2>/dev/null || echo 'Sync script not found'"))
            else:
                # Natural language - use AI
                if has_ai:
                    print("\n🤔 Thinking...")
                    resp = call_ai(u)
                    print(f"\n💬 {resp}")
                else:
                    print("🤔 Try: analyze, github, status, heal, sync")
                    print("💡 Or add an AI key via Option 6 first")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
