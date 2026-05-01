import os
import requests
from system.load_keys import load_keys

load_keys()

class AI:
    def __init__(self):
        self.gemini = os.getenv("GEMINI_KEYS")
        self.openrouter = os.getenv("OPENROUTER_KEYS")

    def ask(self, prompt):

        # ---------------- GEMINI ----------------
        if self.gemini:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini}"

                r = requests.post(url, json={
                    "contents": [{"parts": [{"text": prompt}]}]
                }, timeout=8)

                if r.status_code == 200:
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

            except:
                pass  # fallback

        # ---------------- OPENROUTER ----------------
        if self.openrouter:
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter}"
                    },
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=8
                )

                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"]

            except:
                pass

        # ---------------- OFFLINE MODE ----------------
        return "⚠️ OFFLINE MODE: No internet or APIs reachable. Task queued."

ai = AI()
