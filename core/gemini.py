import os, sys, requests, json, time, subprocess

class SwarmSupreme:
    def __init__(self):
        self.repo = "/root/Ai-Coder"
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"
        self.keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas", "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA", "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY", "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg", "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]

    def log(self, msg):
        print(f"🛰️ [v5.1.0] {msg}")
        with open(f"{self.repo}/swarm_status.log", "a") as f: f.write(f"[{time.ctime()}] {msg}\n")

    def sync(self):
        try:
            ts = int(time.time())
            tag = f"v5-lockdown-{ts}"
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"Final v5 Integration: Roadmap 1-10 Restore {tag}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            subprocess.run(["git", "tag", tag], cwd=self.repo)
            subprocess.run(["git", "push", "origin", tag], cwd=self.repo)
            self.log(f"Synced & Tagged: {tag}")
        except: pass

    def ask_head(self, prompt):
        # Using Paid Claude 3.5 for complex roadmap restoration
        headers = {"Authorization": f"Bearer {self.or_key}"}
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers,
                json={"model": "anthropic/claude-3.5-sonnet", "messages": [{"role": "system", "content": "You are the Head Agent. Focus: Reconstruct Roadmap 1-10, Supabase, Telegram, and Northflank."}, {"role": "user", "content": prompt}]}, timeout=50)
            return r.json()['choices'][0]['message']['content']
        except: return None

if __name__ == "__main__":
    swarm = SwarmSupreme()
    if len(sys.argv) > 1 and sys.argv[1] == "AUTO_SYNC":
        swarm.sync()
    else:
        task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Restore Roadmap 1-10"
        res = swarm.ask_head(task)
        if res:
            with open(f"{swarm.repo}/RECOVERYLOGS.md", "a") as f:
                f.write(f"\n\n### [SUPREME MERGE {time.ctime()}]\n{res}")
            swarm.sync()
