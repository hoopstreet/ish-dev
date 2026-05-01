#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET MULTI-AGENT SYSTEM
- Gemini CLI Mode
- Open Interpreter Mode
- OpenRouter AI Mode
- Unified Interface
"""

import sys, os, requests
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try:
    import time
    time.tzset()
except:
    pass

# Configuration
CRED_FILE = "/root/.hoopstreet/creds/credentials.txt"

def get_api_key():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r') as f:
            for line in f:
                if 'OPENROUTER_API_KEY' in line:
                    return line.split('=')[1].strip()
    return None

API_KEY = get_api_key()
CURRENT_MODEL = "gpt-3.5-turbo"

def ai_complete(prompt, max_tokens=1000):
    """Send to OpenRouter AI"""
    if not API_KEY:
        return "⚠️ OpenRouter API key not found.\n\nRun: echo 'OPENROUTER_API_KEY=your_key' >> /root/.hoopstreet/creds/credentials.txt"
  
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": CURRENT_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"❌ API Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def show_banner():
    print("\n" + "━" * 60)
    print("🚀 HOOPSTREET MULTI-AGENT SYSTEM")
    print("━" * 60)
    print("📋 AVAILABLE AGENTS:")
    print("")
    print("   1. gemini 'question'  - Quick AI query (Gemini style)")
    print("   2. interpreter        - Interactive AI chat")
    print("   3. agent              - Full AI agent with code execution")
    print("   4. menu               - Main menu (6 options)")
    print("")
    print(f"   🤖 AI Status: {'✅ Connected' if API_KEY else '❌ No API Key'}")
    print("   🧠 Current Model: GPT-3.5 Turbo")
    print("━" * 60 + "\n")

def gemini_mode():
    """Gemini CLI style + single command"""
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        print(f"\n🤖 Processing: {prompt}")
        print("━" * 50)
        response = ai_complete(prompt)
        print(f"\n{response}\n")
        return True
    return False
 

def interpreter_mode():
    """Open Interpreter style + interactive"""
    print("\n" + "━" * 60)
    print("🚀 Open Interpreter Mode (via Hoopstreet AI)")
    print("━" * 60)
    print("📝 Type your commands naturally. Type 'exit' to quit.")
    print("━" * 60 + "\n")
    
    while True:
        try:
            user_input = input("🔷 > ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Exiting Interpreter Mode...")
                break
            if not user_input:
                continue
            
            print("\n🤖 Thinking...")
            response = ai_complete(user_input)
            print(f"\n{response}\n")
            
            if "```" in response:
                print("💡 Code detected! Copy and run manually.\n")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break

def main():
    if len(sys.argv) > 1:
        if gemini_mode():
            return
    
    print("\n" + "━" * 60)
    print("🏀 HOOPSTREET MULTI-AGENT READY")
    print("━" * 60)
    print("")
    print("  💬 Type 'agent' for full AI chat")
    print("  🔷 Type 'interpreter' for Open Interpreter mode")
    print("  ⚡ Type 'gemini <question>' for quick query")
    print("  📊 Type 'status' for system info")
    print("  🔧 Type 'menu' for main menu")
    print("  ❌ Type 'exit' to quit")
    print("")
    
    while True:
        try:
            cmd = input("🚀 > ").strip().lower()
            
            if cmd in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break
            elif cmd == 'agent':
                os.system("python3 /root/ish-dev/core/agent_ultimate_v9.py")
            elif cmd == 'interpreter':
                interpreter_mode()
            elif cmd.startswith('gemini '):
                prompt = cmd[7:]
                response = ai_complete(prompt)
                print(f"\n🤖 {response}\n")
            elif cmd == 'status':
                os.system("/root/ish-dev/core/status.sh")
            elif cmd == 'menu':
                os.system("/root/menu")
                break
            elif cmd == 'help':
                show_banner()
            elif cmd:
                print("\n🤖 Thinking...")
                response = ai_complete(cmd)
                print(f"\n{response}\n")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_banner()
        print("💡 Quick tips:")
        print("   • gemini 'your question' - Quick AI query")
        print("   • interpreter - Interactive AI chat")
        print("   • agent - Full AI agent with code execution")
        print("")
        main()
    else:
        gemini_mode()
