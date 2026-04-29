import requests
from security.loader import secrets

def gemini(prompt):
    for k in secrets.gemini_keys:
        try:
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={k}",
                json={"contents":[{"parts":[{"text":prompt}]}]},
                timeout=20
            )
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return None

def openrouter(prompt):
    for k in secrets.openrouter_keys:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization":f"Bearer {k}"},
                json={
                    "model":"openai/gpt-4o-mini",
                    "messages":[{"role":"user","content":prompt}]
                },
                timeout=20
            )
            return r.json()["choices"][0]["message"]["content"]
        except:
            continue
    return None

def ask(prompt):
    return gemini(prompt) or openrouter(prompt)
