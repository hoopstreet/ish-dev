import os, sys, requests, json, subprocess, time, re
from concurrent.futures import ThreadPoolExecutor

GH_TOKEN = "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"
OR_KEY = "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"
MODELS = ["deepseek/deepseek-chat", "anthropic/claude-3-haiku", "google/gemini-flash-1.5"]

def log(msg):
    with open('master.log', 'a') as f:
        f.write(f"[{time.ctime()}] {msg}\n")
    print(f"[{time.ctime()}] {msg}")

def ensure_context():
    os.chdir("/root/Ai-Coder")

def swarm_call(model, prompt):
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OR_KEY}"},
            json={"model": model, "messages": [
                {"role": "system", "content": "AUTONOMOUS RECOVERY UNIT. FIXED JSON ONLY. NO CHAT."},
                {"role": "user", "content": prompt}
            ]}, timeout=60)
        return res.json()['choices'][0]['message']['content']
    except: return None

def run_task(task):
    ensure_context()
    log(f"🧠 Autonomous Task: {task}")
    
    with open('dna.md', 'r') as f: dna = f.read()
    with open('RECOVERYLOGS.md', 'r') as f: logs = f.read()
    
    prompt = f"TASK: {task}\nCONTEXT: {dna}\nLOGS: {logs}\nMISSION: Fix and Merge. Output JSON: {{'dna_update': '...', 'recovery_entry': '...'}}"
    
    with ThreadPoolExecutor() as exec:
        results = list(exec.map(lambda m: swarm_call(m, prompt), MODELS))
    
    for r in results:
        if r and '{' in r:
            try:
                data = json.loads(re.search(r'(\{.*\})', r, re.DOTALL).group(1))
                with open('dna.md', 'a') as f: f.write(f"\n{data['dna_update']}")
                with open('RECOVERYLOGS.md', 'a') as f: f.write(f"\n\n### AUTO-FIX [{time.ctime()}]\n{data['recovery_entry']}")
                
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", f"auto-recovery: {time.ctime()}"], check=True)
                remote = f"https://{GH_TOKEN}@github.com/hoopstreet/Ai-Coder.git"
                subprocess.run(["git", "remote", "set-url", "origin", remote], check=True)
                subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
                log("✅ Self-Recovery Successful.")
                return
            except: continue
    log("❌ Autonomous Consensus Failed. Retrying in next heartbeat.")

if __name__ == "__main__":
    run_task(" ".join(sys.argv[1:]))
