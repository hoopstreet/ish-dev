import requests

class AI:

    def ask(self, prompt):
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization":"Bearer YOUR_KEY"},
                json={
                    "model":"openai/gpt-4o-mini",
                    "messages":[{"role":"user","content":prompt}]
                },
                timeout=20
            )
            return r.json()["choices"][0]["message"]["content"]
        except:
            return "ERROR: AI FAILED"

ai = AI()
