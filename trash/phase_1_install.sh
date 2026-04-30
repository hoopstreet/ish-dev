#!/bin/sh

echo "🚀 Installing Phase 1: Infrastructure & Modules..."

mkdir -p ai core logs dashboard security

########################################
# 1. LOGGER
########################################
cat > ai/logger.py << 'EOL'
import json, time, os

LOG_FILE = "logs/ai_log.jsonl"

def log(event, data):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "time": time.time(),
        "event": event,
        "data": data
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
EOL

########################################
# 2. KEY ROTATION
########################################
cat > ai/keys.py << 'EOL'
from security.loader import secrets

class KeyManager:
    def __init__(self):
        self.gemini_keys = secrets.gemini
        self.openrouter_keys = secrets.openrouter
        self.g_index = 0
        self.o_index = 0

    def next_gemini(self):
        if not self.gemini_keys:
            return None
        key = self.gemini_keys[self.g_index % len(self.gemini_keys)]
        self.g_index += 1
        return key

    def next_openrouter(self):
        if not self.openrouter_keys:
            return None
        key = self.openrouter_keys[self.o_index % len(self.openrouter_keys)]
        self.o_index += 1
        return key

keys = KeyManager()
EOL

########################################
# 3. MODEL DETECTION
########################################
cat > ai/models.py << 'EOL'
import requests
from ai.keys import keys

def list_gemini_models(api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return [m["name"].split("/")[-1] for m in r.json().get("models", [])]
    except:
        pass
    return ["gemini-1.5-flash"]
EOL

########################################
# 4. HEALTH SCORING
########################################
cat > ai/health.py << 'EOL'
import time

class Health:
    def __init__(self):
        self.score = {
            "gemini": 100,
            "openrouter": 100
        }

    def success(self, provider):
        self.score[provider] = min(100, self.score[provider] + 1)

    def fail(self, provider):
        self.score[provider] = max(0, self.score[provider] - 5)

health = Health()
EOL

########################################
# 5. OFFLINE FALLBACK
########################################
cat > ai/offline.py << 'EOL'
def offline_response(prompt):
    return "⚠️ OFFLINE MODE: AI services unavailable. Try again later."
EOL

echo "✅ Phase 1 Modules Ready"
