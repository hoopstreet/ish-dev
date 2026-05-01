#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET ALL-IN-ONE AI AGENT v8.0
- Developer, Coder, Prompt, Executor, Automated Setup
- ChatGPT-like conversation
- Code generation and execution
- System management
- Self-improving
"""

import sys, os, subprocess, re, json, requests, time
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try:
    time.tzset()
except:
    pass

# ============ CONFIGURATION ============
DNA_FILE = "/root/ish-dev/docs/DNA.md"
LOG_FILE = "/root/ish-dev/docs/logs.txt"
CRED_FILE = "/root/.hoopstreet/creds/credentials.txt"
HISTORY_FILE = "/root/ish-dev/agents/chat_history.json"
AGENT_VERSION = "8.0"

def get_api_key():
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r') as f:
            for line in f:
                if 'OPENROUTER_API_KEY' in line:
                    return line.split('=')[1].strip()
    return None

API_KEY = get_api_key()

AI_MODELS = {
    "1": ("gpt4", "openai/gpt-4-turbo", "GPT-4 (Best)"),
    "2": ("gpt35", "openai/gpt-3.5-turbo", "GPT-3.5 (Fast)"),
    "3": ("claude", "anthropic/claude-3-opus", "Claude 3 (Smart)"),
    "4": ("gemini", "google/gemini-pro", "Gemini Pro"),
    "5": ("deepseek", "deepseek/deepseek-chat", "DeepSeek"),
    "6": ("llama", "meta-llama/llama-3-70b-instruct", "Llama 3")
}
CURRENT_MODEL = "openai/gpt-3.5-turbo"
CURRENT_MODEL_NAME = "GPT-3.5"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] [AIO] {msg}\n")

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def ai_chat(prompt, history=[]):
    if not API_KEY:
        return "⚠️ OpenRouter API key not found. Add OPENROUTER_API_KEY to credentials."

    messages = [{"role": "system", "content": """You are Hoopstreet AI Agent, an all-in-one assistant for developers.
You can:
- Write and execute code in any language
- Answer questions like ChatGPT
- Help with system tasks
- Generate shell commands
- Be professional and helpful

When asked to execute code, respond with:
[EXECUTE] command_here

Otherwise, respond naturally."""}]

    for msg in history[-10:]:
        messages.append(msg)
    messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": CURRENT_MODEL, "messages": messages, "max_tokens": 1500, "temperature": 0.7},
            timeout=90
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"❌ AI Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def run_command(cmd):
    print(f"\n📌 Executing: {cmd}")
    print("━" * 60)
    result = os.system(cmd)
    print("✅ SUCCESS" if result == 0 else "❌ FAILED")
    return result

def show_banner():
    print("\n" + "━" * 60)
    print("🤖 HOOPSTREET ALL-IN-ONE AI AGENT v8.0")
    print("━" * 60)
    print("📋 CAPABILITIES:")
    print(" • 💬 Chat like ChatGPT/DeepSeek/Claude/Gemini")
    print(" • 📝 Generate and execute code")
    print(" • 🔧 Auto-heal and fix errors")
    print(" • 🧠 Multiple AI models")
    print(" • ⚡ System management commands")
    print(" • 💾 Remembers conversation")
    print("━" * 60)
    print("\n💬 Type naturally | /help for commands | /exit to quit\n")
def show_help():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ALL-IN-ONE AGENT COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 NATURAL LANGUAGE (Just type!):
   • "Write a Python script to..."
   • "How do I install X in Alpine?"
   • "Create a bash script that..."
   • "Fix this error: ..."

🔹 SYSTEM COMMANDS:
   /status     - Show system status
   /heal       - Run auto-heal engine
   /sync       - Git push with backup
   /stats      - Agent statistics
   /model      - Show/change AI model
   /clear      - Clear conversation
   /update     - Self-upgrade agent
   /help       - Show this help
   /exit       - Exit to menu

🔹 AVAILABLE MODELS:
   1. GPT-4 (Best, slower)
   2. GPT-3.5 (Fast, good)
   3. Claude 3 (Smart)
   4. Gemini Pro
   5. DeepSeek
   6. Llama 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def show_stats():
    dna_lines = 0
    if os.path.exists(DNA_FILE):
        with open(DNA_FILE, 'r') as f:
            dna_lines = len(f.readlines())
    log_lines = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_lines = len(f.readlines())

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 ALL-IN-ONE AGENT STATISTICS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Version: {AGENT_VERSION}")
    print(f"   AI Model: {CURRENT_MODEL_NAME}")
    print(f"   AI Status: {'✅ Connected' if API_KEY else '❌ API Key needed'}")
    print(f"   DNA.md: {dna_lines} lines")
    print(f"   Logs: {log_lines} entries")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def show_models():
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🤖 AVAILABLE AI MODELS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for key, (name, model, desc) in AI_MODELS.items():
        marker = "👉" if CURRENT_MODEL == model else "  "
        print(f"{marker} {key}. {name.upper()} - {desc}")
    print(f"\n👉 Current: {CURRENT_MODEL_NAME}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

def switch_model(choice):
    global CURRENT_MODEL, CURRENT_MODEL_NAME
    if choice in AI_MODELS:
        name, model, desc = AI_MODELS[choice]
        CURRENT_MODEL = model
        CURRENT_MODEL_NAME = name.upper()
        log(f"Switched to model: {CURRENT_MODEL_NAME}")
        return f"✅ Switched to {CURRENT_MODEL_NAME} - {desc}"
    return f"❌ Invalid. Choose 1-{len(AI_MODELS)}"

def self_upgrade():
    print("\n🔄 SELF-UPGRADING AGENT...")
    print("━" * 60)
    run_command("cd /root/ish-dev && git pull")
    run_command("/root/ish-dev/core/heal.sh")
    log("Self-upgrade completed")
    print("\n✅ SELF-UPGRADE COMPLETE!")

def main():
    show_banner()
    history = load_history()

    while True:
        try:
            user_input = input("💬 > ").strip()
            if not user_input:
                continue

            # Commands
            if user_input.lower() in ['/exit', 'exit', '/quit']:
                print("\n🔙 Returning to main menu...")
                save_history(history)
                break

            elif user_input.lower() in ['/help', 'help', '?']:
                show_help()
                continue

            elif user_input.lower() in ['/stats', 'stats']:
                show_stats()
                continue

            elif user_input.lower() == '/models':
                show_models()
                continue

            elif user_input.lower() == '/clear':
                history = []
                save_history(history)
                print("✅ Conversation cleared")
                continue


            elif user_input.lower() == '/status':
                run_command("/root/ish-dev/core/status.sh")
                continue

            elif user_input.lower() == '/heal':
                run_command("/root/ish-dev/core/heal.sh")
                continue

            elif user_input.lower() == '/sync':
                run_command("/root/ish-dev/core/sync.sh")
                continue

            elif user_input.lower() == '/update':
                self_upgrade()
                continue

            elif user_input.lower().startswith('/model'):
                parts = user_input.split()
                if len(parts) > 1:
                    result = switch_model(parts[1])
                    print(result)
                else:
                    show_models()
                continue

            # AI Chat
            print("\n🤖 Thinking...")
            response = ai_chat(user_input, history)

            # Save to history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response})
            save_history(history)

            # Display response
            print(f"\n🤖 Assistant:\n{response}\n")

            # Auto-execute if contains command marker
            if "[EXECUTE]" in response:
                import re
                cmd_match = re.search(r'\[EXECUTE\](.*?)(?:\n|$)', response)
                if cmd_match:
                    cmd = cmd_match.group(1).strip()
                    print(f"\n🔧 Auto-executing detected command...")
                    run_command(cmd)

        except KeyboardInterrupt:
            print("\n🔙 Returning to main menu...")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
