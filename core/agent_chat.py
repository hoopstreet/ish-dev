#!/usr/bin/env python3
import sys, os, subprocess, re, json, requests
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
CRED_FILE = "/root/.hoopstreet/creds/credentials.txt"
CHAT_HISTORY_FILE = "/root/ish-dev/agents/chat_history.json"
AGENT_VERSION = "7.0"

def get_api_key():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r') as f:
            for line in f:
                if 'OPENROUTER_API_KEY' in line:
                    return line.split('=')[1].strip()
    return None

API_KEY = get_api_key()

AI_MODELS = {
    "gpt4": "openai/gpt-4-turbo",
    "gpt35": "openai/gpt-3.5-turbo",
    "claude": "anthropic/claude-3-opus",
    "gemini": "google/gemini-pro",
    "deepseek": "deepseek/deepseek-chat",
    "llama": "meta-llama/llama-3-70b-instruct"
}
CURRENT_MODEL = "openai/gpt-3.5-turbo"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f: f.write(f"[{ts}] [CHAT] {msg}\n")

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def ai_chat(prompt, conversation_history=[]):
    if not API_KEY:
        return "⚠️ OpenRouter API key not found. Add OPENROUTER_API_KEY to credentials."
    
    messages = [
        {"role": "system", "content": "You are Hoopstreet AI Agent, a friendly assistant. Answer naturally like ChatGPT. When asked to execute code, respond with [EXECUTE] followed by the command."}
    ]
    for msg in conversation_history[-10:]:
        messages.append(msg)
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": CURRENT_MODEL, "messages": messages, "max_tokens": 1000, "temperature": 0.7},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ AI Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def execute_command(cmd):
    print(f"\n📌 Executing: {cmd}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    result = os.system(cmd)
    print("✅ SUCCESS" if result == 0 else "❌ FAILED")
    return result

def show_banner():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("💬 HOOPSTREET CHAT AI AGENT v7.0")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CAPABILITIES:")
    print(" • 💬 Chat like ChatGPT/DeepSeek/Claude/Gemini")
    print(" • 📝 Generate and execute code")
    print(" • 🔧 Auto-heal errors")
    print(" • 🧠 Switch AI models")
    print(" • 💾 Remembers conversation")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("\n👉 Just type naturally! Type 'help' for commands, 'exit' to quit")
    print("")

def show_help():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 CHAT AI AGENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 CHAT COMMANDS (Natural Language):
   Just type anything! Like talking to ChatGPT.
   Examples:
   • "Write a Python script to download a webpage"
   • "What's the weather like?"
   • "How do I install a package in Alpine?"

🔹 SYSTEM COMMANDS:
   /status   - Show system status
   /heal     - Run auto-heal
   /sync     - Git sync
   /stats    - Agent statistics
   /clear    - Clear conversation history
   /model    - Show/change AI model
   /help     - Show this help
   /exit     - Exit to menu

🔹 AVAILABLE MODELS: gpt4, gpt35, claude, gemini, deepseek, llama

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_stats():
    dna_lines = 0
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            dna_lines = len(f.readlines())
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 CHAT AGENT STATISTICS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Agent Version: {AGENT_VERSION}")
    print(f"   Current Model: {CURRENT_MODEL.split('/')[-1]}")
    print(f"   AI Status: {'✅ Connected' if API_KEY else '❌ API Key needed'}")
    print(f"   DNA.md: {dna_lines} lines")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
def main():
    show_banner()
    conversation = load_chat_history()
    
    while True:
        try:
            user_input = input("💬 > ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ['/exit', 'exit', '/quit']:
                print("\n🔙 Returning to main menu...")
                save_chat_history(conversation)
                break
            elif user_input.lower() in ['/help', 'help', '?']:
                show_help()
                continue
            elif user_input.lower() in ['/stats', 'stats']:
                show_stats()
                continue
            elif user_input.lower() == '/clear':
                conversation = []
                save_chat_history(conversation)
                print("✅ Conversation history cleared")
                continue
            elif user_input.lower() == '/status':
                execute_command("/root/ish-dev/core/status.sh")
                continue
            elif user_input.lower() == '/heal':
                execute_command("/root/ish-dev/core/heal.sh")
                continue
            elif user_input.lower() == '/sync':
                execute_command("/root/ish-dev/core/sync.sh")
                continue
            elif user_input.lower().startswith('/model'):
                parts = user_input.split()
                if len(parts) > 1:
                    model_key = parts[1].lower()
                    if model_key in AI_MODELS:
                        global CURRENT_MODEL
                        CURRENT_MODEL = AI_MODELS[model_key]
                        print(f"✅ Switched to model: {model_key}")
                    else:
                        print(f"❌ Model not found. Available: {', '.join(AI_MODELS.keys())}")
                else:
                    print(f"📌 Current model: {CURRENT_MODEL.split('/')[-1]}")
                continue
            
            print("\n🤖 Thinking...")
            response = ai_chat(user_input, conversation)
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "assistant", "content": response})
            save_chat_history(conversation)
            print(f"\n🤖 Assistant:\n{response}\n")
            
            if "[EXECUTE]" in response:
                cmd_match = re.search(r'\[EXECUTE\](.*?)(?:\n|$)', response)
                if cmd_match:
                    cmd = cmd_match.group(1).strip()
                    print(f"\n🔧 Auto-executing: {cmd}")
                    execute_command(cmd)
                    
        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
