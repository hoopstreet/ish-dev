#!/usr/bin/env python3
"""
HOOPSTREET AI ORCHESTRATOR v1.0
Intent-driven AI that controls all system modules
"""
import sys, os, subprocess, json, requests, re
from datetime import datetime, timezone, timedelta

PHT = timezone(timedelta(hours=8))
CREDS_FILE = "/root/.hoopstreet/creds/credentials.txt"

# ============================================================
# SYSTEM CONTEXT BUILDER
# ============================================================
def get_system_context():
    """Gather full system state for AI"""
    context = {
        "timestamp": datetime.now(PHT).strftime("%Y-%m-%d %H:%M:%S"),
        "version": "v10.1.0",
        "modules": ["agent", "sync", "heal", "status", "remote", "credentials"],
        "available_commands": {
            "sync": ["push", "pull", "commit", "tag"],
            "heal": ["scan", "fix", "recover", "snapshot"],
            "status": ["show", "metrics", "health"],
            "remote": ["list", "connect", "load"],
            "credentials": ["add", "get", "delete"]
        }
    }
    
    # Try to get recent logs
    logs_file = "/root/ish-dev/docs/logs.txt"
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            context["recent_logs"] = f.readlines()[-30:]
    
    # Get status
    status_file = "/root/ish-dev/docs/status.json"
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                context["status"] = json.load(f)
        except: pass
    
    return context

# ============================================================
# GEMINI INTENT PARSER
# ============================================================
def get_gemini_key():
    if not os.path.exists(CREDS_FILE): return None
    with open(CREDS_FILE, 'r') as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                return line.split('=',1)[1].strip()
    return None

def parse_intent(user_input, context):
    """Send to Gemini and get structured JSON response"""
    api_key = get_gemini_key()
    if not api_key:
        return fallback_parse(user_input)
    
    system_prompt = f"""You are an AI DevOps Controller for Hoopstreet iSH system.
Available modules: {', '.join(context['modules'])}
System version: {context['version']}

User request: {user_input}

RESPOND ONLY IN VALID JSON FORMAT:
{{
  "intent": "brief description",
  "actions": [
    {{"module": "module_name", "command": "command", "params": {{}}}}
  ],
  "code": "optional bash/python code to execute",
  "message": "response to user"
}}

Rules:
- For "fix/recover": use heal module
- For "push/commit/sync": use sync module
- For "status/info": use status module
- For "connect/clone/repo": use remote module
- For "add key/credential": use credentials module
- For "build/create code": use agent module with code generation
- Combine multiple actions when needed

Example:
Input: "fix bugs and push to github"
Output: {{
  "intent": "Auto-heal and sync",
  "actions": [
    {{"module": "heal", "command": "scan_and_fix", "params": {{}}}},
    {{"module": "sync", "command": "push", "params": {{"message": "Auto-fixed"}}}}
  ],
  "code": "",
  "message": "Running heal then sync"
}}"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    data = {
        "contents": [{"parts": [{"text": system_prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1000}
    }
    
    try:
        r = requests.post(f"{url}?key={api_key}", json=data, timeout=30)
        if r.status_code == 200:
            result = r.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
    except:
        pass
    return fallback_parse(user_input)

def fallback_parse(user_input):
    """Rule-based fallback when AI unavailable"""
    low = user_input.lower()
    
    if any(w in low for w in ['fix', 'repair', 'heal', 'bug']):
        return {"intent": "heal", "actions": [{"module": "heal", "command": "scan", "params": {}}], "code": "", "message": "Running system heal"}
    if any(w in low for w in ['push', 'sync', 'commit', 'github']):
        return {"intent": "sync", "actions": [{"module": "sync", "command": "push", "params": {}}], "code": "", "message": "Syncing to GitHub"}
    if any(w in low for w in ['status', 'health', 'info']):
        return {"intent": "status", "actions": [{"module": "status", "command": "show", "params": {}}], "code": "", "message": "Fetching system status"}
    if any(w in low for w in ['connect', 'repo', 'github', 'clone']):
        return {"intent": "remote", "actions": [{"module": "remote", "command": "list", "params": {}}], "code": "", "message": "Checking remote projects"}
    return {"intent": "chat", "actions": [], "code": "", "message": f"I understand: {user_input[:100]}"}

# ============================================================
# ACTION EXECUTOR
# ============================================================
def execute_action(action):
    """Execute a single action on a module"""
    module = action.get("module")
    command = action.get("command", "")
    
    if module == "heal":
        return os.popen("sh /root/ish-dev/core/heal.sh 2>&1").read()
    elif module == "sync":
        return os.popen("sh /root/ish-dev/core/sync.sh 2>&1").read()
    elif module == "status":
        return os.popen("cat /root/ish-dev/docs/status.json 2>/dev/null").read() or "No status"
    elif module == "remote":
        return os.popen("sh /root/ish-dev/core/remote.sh 2>&1").read()
    elif module == "credentials":
        return os.popen("sh /root/ish-dev/core/creds.sh 2>&1").read()
    elif module == "agent" and action.get("code"):
        return execute_code(action["code"])
    return f"Unknown module: {module}"

def execute_code(code):
    tmp = "/tmp/orchestrator_code.sh"
    with open(tmp, 'w') as f:
        f.write(code)
    result = os.popen(f"sh {tmp} 2>&1").read()
    os.remove(tmp)
    return result[:2000]


    

# ============================================================
# MAIN ORCHESTRATOR LOOP
# ============================================================
def main():
    os.system('clear')
    print("\n" + "="*60)
    print("🧠 HOOPSTREET AI ORCHESTRATOR v1.0")
    print("="*60)
    print("🎯 I CONTROL YOUR ENTIRE SYSTEM")
    print("💬 Just describe what you want")
    print("📋 Examples:")
    print("   • 'Fix bugs and push to GitHub'")
    print("   • 'Show system status and suggest upgrades'")
    print("   • 'Connect new repository'")
    print("   • 'Heal all errors'")
    print("="*60)
    print("💡 Type 'menu' to exit")
    print("="*60)
    
    while True:
        try:
            user = input("\n💬 You: ").strip()
            if not user: continue
            if user.lower() in ['menu', 'exit', 'quit']:
                print("👋 Returning to menu...")
                break
            
            print("\n🧠 Analyzing intent...")
            context = get_system_context()
            plan = parse_intent(user, context)
            
            print(f"\n📋 Intent: {plan.get('intent', 'unknown')}")
            print(f"💬 AI: {plan.get('message', 'Processing...')}")
            
            # Execute actions
            actions = plan.get('actions', [])
            if actions:
                print("\n⚡ Executing actions:")
                for action in actions:
                    module = action.get('module', 'unknown')
                    print(f"   🔧 {module}...")
                    result = execute_action(action)
                    if result and len(result) < 500:
                        print(f"   📝 {result[:200]}")
            
            # Execute generated code if present
            code = plan.get('code', '')
            if code:
                print("\n⚙️ Executing AI-generated code...")
                result = execute_code(code)
                if result:
                    print(f"📝 {result[:500]}")
            
            # After actions, offer suggestions
            if actions:
                print("\n💡 Next suggestions:")
                print("   • 'analyze logs' - Review recent activity")
                print("   • 'suggest upgrades' - Get improvement ideas")
                print("   • 'show status' - Check system health")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
# ============================================================
# SELF-LEARNING MEMORY SYSTEM
# ============================================================
MEMORY_FILE = "/root/ish-dev/.orchestrator_memory.json"

def learn_from_interaction(user_input, plan, result):
    """Store learning for future improvements"""
    memory = {}
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                memory = json.load(f)
        except: pass
    
    if "history" not in memory:
        memory["history"] = []
    
    memory["history"].append({
        "input": user_input[:200],
        "intent": plan.get("intent"),
        "actions": plan.get("actions"),
        "timestamp": str(datetime.now(PHT))
    })
    
    # Keep last 100 interactions
    if len(memory["history"]) > 100:
        memory["history"] = memory["history"][-100:]
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

def suggest_upgrades():
    """Analyze history and suggest improvements"""
    if not os.path.exists(MEMORY_FILE):
        return "No history yet. Use the system more to get suggestions."
    
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    
    history = memory.get("history", [])
    if len(history) < 3:
        return "Need more interactions (at least 3) to generate suggestions."
    
    # Analyze patterns
    sync_count = sum(1 for h in history if "sync" in str(h.get("actions", [])))
    heal_count = sum(1 for h in history if "heal" in str(h.get("actions", [])))
    
    suggestions = []
    if heal_count > sync_count:
        suggestions.append("🔧 You fix issues often. Consider pre-emptive monitoring.")
    if sync_count > 5:
        suggestions.append("🔄 Frequent syncs detected. Auto-sync every hour?")
    
    suggestions.append("📊 Run 'analyze logs' for detailed insights")
    suggestions.append("🚀 Type 'suggest upgrades' anytime for recommendations")
    
    return "\n".join(suggestions)
