#!/usr/bin/env python3
"""
HOOPSTREET GEMINI AI AGENT v10.1.0
Reads API key from credentials
"""
import sys, os, subprocess, json, requests
from datetime import datetime, timezone, timedelta

PHT = timezone(timedelta(hours=8))
CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"

def get_gemini_key():
    """Get Gemini API key from credentials"""
    if not os.path.exists(CREDS_FILE):
        return None
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('GEMINI_API_KEY='):
                return line.split('=', 1)[1].strip()
            if line.startswith('GEMINI_KEY='):
                return line.split('=', 1)[1].strip()
    return None

def test_key(key):
    """Test if key works"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    try:
        r = requests.post(
            f"{url}?key={key}",
            json={"contents": [{"parts": [{"text": "test"}]}]},
            timeout=10
        )
        if r.status_code == 200:
            return True, "Working"
        elif r.status_code == 403:
            return False, "Invalid/Expired key"
        elif r.status_code == 429:
            return False, "Rate limited"
        else:
            return False, f"Error {r.status_code}"
    except Exception as e:
        return False, str(e)[:50]

def ask_gemini(prompt, key):
    """Ask Gemini API"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    data = {
        "contents": [{"parts": [{"text": prompt[:2000]}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
    }
    try:
        r = requests.post(f"{url}?key={key}", json=data, timeout=60)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return None
    except:
        return None

def execute_code(code, lang="bash"):
    tmp = f"/tmp/code.{'py' if lang=='python' else 'sh'}"
    with open(tmp, 'w') as f:
        f.write(code)
    result = os.popen(f"{'python3' if lang=='python' else 'sh'} {tmp} 2>&1").read()
    os.remove(tmp)
    return result[:2000]

def analyze_project():
    core_dir = "/root/ish-dev/core/"
    info = ["📁 **Project Analysis**\n"]
    if os.path.exists(core_dir):
        scripts = [f for f in os.listdir(core_dir) if f.endswith(('.sh','.py'))]
        info.append(f"📂 Core Scripts: {len(scripts)}")
        info.append(f"   • menu.sh, agent.py, sync.sh, heal.sh")
    return "\n".join(info)

def main():
    os.system('clear')
    print("\n" + "="*50)
    print("🤖 HOOPSTREET GEMINI AI AGENT")
    print("="*50)
    
    # Get and test key
    api_key = get_gemini_key()
    WORKING_KEY = None
    
    if api_key:
        print(f"🔑 Testing key: {api_key[:20]}...")
        valid, msg = test_key(api_key)
        if valid:
            WORKING_KEY = api_key
            print("✅ Key is WORKING!")
        else:
            print(f"❌ Key invalid: {msg}")
    else:
        print("⚠️ No API key found in credentials")
    if WORKING_KEY:
        print("\n✅ Gemini AI: ACTIVE")
        print("💡 You can ask anything naturally!")
    else:
        print("\n⚠️ Gemini AI: INACTIVE")
        print("\n📝 To add a working API key:")
        print("   1. Go to: https://aistudio.google.com/app/apikey")
        print("   2. Click 'Create API Key'")
        print("   3. Copy the new key")
        print("   4. Run this command (replace YOUR_KEY):")
        print("")
        print("      echo 'GEMINI_API_KEY=YOUR_KEY' >> /root/.hoopstreet/creds/credentials.txt")
        print("")
    
    print("\n" + "="*50)
    print("💬 Type 'help' for commands, 'menu' to exit")
    print("="*50)
    
    while True:
        try:
            user = input("\n💬 You: ").strip()
            if not user: continue
            if user.lower() in ['menu', 'exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            if user.lower() == 'help':
                print("""
📋 **Available Commands:**
• Ask anything naturally
• "analyze" - Scan project
• "status" - System status
• # Phase 1... END - Multi-phase code
• python print("hi") - Run Python
• run echo "hi" - Run shell
""")
                continue
            
            if user.lower() == 'analyze':
                print(analyze_project())
                continue
            
            if user.lower() == 'status':
                print(os.popen("cat /root/ish-dev/docs/status.json 2>/dev/null").read() or "No status")
                continue
            
            if user.strip().startswith('# Phase'):
                lines = [user]
                print("📝 Type 'END' when done:")
                while True:
                    l = input()
                    if l.strip().upper() == 'END':
                        break
                    lines.append(l)
                print("\n⚡ Executing...")
                print(execute_code('\n'.join(lines)))
                continue
            
            if user.startswith('python '):
                print(execute_code(user[7:], 'python'))
                continue
            
            if user.startswith('run '):
                print(execute_code(user[4:], 'bash'))
                continue
            
            # Natural language
            if WORKING_KEY:
                print("\n🤖 Thinking...")
                response = ask_gemini(user, WORKING_KEY)
                if response:
                    print(f"\n{response}")
                else:
                    print("\n⚠️ API error - please try again")
            else:
                print(f"\n🤖 I see: {user[:100]}")
                print("\n💡 Add a valid Gemini API key first (see instructions above)")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
