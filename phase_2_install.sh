#!/bin/sh

echo "🚀 Installing Phase 2: Production Router & Dashboard..."

########################################
# 6. MAIN ROUTER (PRODUCTION CORE)
########################################
cat > ai/router.py << 'EOL'
import requests, time
from ai.keys import keys
from ai.logger import log
from ai.health import health
from ai.offline import offline_response

class AI:

    def ask(self, prompt):

        # ---------------------------
        # GEMINI ROUTING
        # ---------------------------
        for _ in range(3):  # retry cycles
            key = keys.next_gemini()
            if not key:
                break

            try:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + key

                r = requests.post(url, json={
                    "contents": [{"parts": [{"text": prompt}]}]
                }, timeout=20)

                log("gemini_response", {"status": r.status_code})

                if r.status_code == 200:
                    health.success("gemini")
                    return r.json()["candidates"][0]["content"]["parts"][0]["text"]

                health.fail("gemini")

            except Exception as e:
                log("gemini_error", str(e))
                time.sleep(1)

        # ---------------------------
        # OPENROUTER ROUTING
        # ---------------------------
        for _ in range(3):
            key = keys.next_openrouter()
            if not key:
                break

            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}"},
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=20
                )

                log("openrouter_response", {"status": r.status_code})

                if r.status_code == 200:
                    health.success("openrouter")
                    return r.json()["choices"][0]["message"]["content"]

                health.fail("openrouter")

            except Exception as e:
                log("openrouter_error", str(e))
                time.sleep(1)

        # ---------------------------
        # OFFLINE MODE
        # ---------------------------
        return offline_response(prompt)

ai = AI()
EOL

########################################
# 7. DASHBOARD
########################################
cat > dashboard/cli.py << 'EOL'
import json

def show_logs():
    try:
        with open("logs/ai_log.jsonl") as f:
            lines = f.readlines()[-10:]
            for l in lines:
                print(json.loads(l))
    except:
        print("No logs found")

if __name__ == "__main__":
    print("📊 AI ROUTER DASHBOARD")
    print("======================")
    show_logs()
EOL

echo "✅ INSTALL COMPLETE"
echo "👉 Run test: python3 -c 'from ai.router import ai; print(ai.ask(\"hello\"))'"
