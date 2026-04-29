import requests, time, random, json
from security.loader import secrets

LOG_FILE = "logs/router.jsonl"

def log(data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass

class Router:
    def __init__(self):
        self.g_index = 0
        self.o_index = 0

    def next_key(self, pool, index):
        if not pool: return None
        return pool[index % len(pool)]

    def rotate_gemini(self):
        key = self.next_key(secrets.gemini, self.g_index)
        self.g_index += 1
        return key

    def rotate_openrouter(self):
        key = self.next_key(secrets.openrouter, self.o_index)
        self.o_index += 1
        return key

    def backoff(self, attempt):
        time.sleep(min(2 ** attempt, 8))

    def gemini(self, prompt, key):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            r = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}]
            }, timeout=20)
            log({"provider": "gemini", "status": r.status_code})
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            log({"gemini_error": str(e)})
        return None
    def get_models(self, key):
        try:
            r = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {key}"},
                timeout=10
            )
            if r.status_code == 200:
                return [m["id"] for m in r.json().get("data", [])]
        except:
            pass
        return ["google/gemini-1.5-flash", "openai/gpt-4o-mini"]

    def openrouter(self, prompt, key, model):
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "AgentOS-v2"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=20
            )
            log({"provider": "openrouter", "model": model, "status": r.status_code})
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            log({"openrouter_error": str(e)})
        return None

    def ask(self, prompt):
        for i in range(len(secrets.gemini)):
            key = self.rotate_gemini()
            if not key: continue
            for attempt in range(3):
                result = self.gemini(prompt, key)
                if result: return result
                self.backoff(attempt)
        for i in range(len(secrets.openrouter)):
            key = self.rotate_openrouter()
            if not key: continue
            models = self.get_models(key)
            for model in models[:3]:
                for attempt in range(2):
                    result = self.openrouter(prompt, key, model)
                    if result: return result
                    self.backoff(attempt)
        return "⚠️ OFFLINE MODE: All AI providers failed."

ai = Router()
