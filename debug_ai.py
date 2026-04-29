import requests
from security.loader import secrets

print(f"Checking Gemini Keys: {len(secrets.gemini)} found")
print(f"Checking OpenRouter Keys: {len(secrets.openrouter)} found")

# Test Gemini First Key
k = secrets.gemini[0]
try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={k}"
    r = requests.post(url, json={"contents":[{"parts":[{"text":"hi"}]}]}, timeout=10)
    print(f"Gemini Status: {r.status_code}")
    if r.status_code != 200:
        print(f"Gemini Error: {r.text}")
except Exception as e:
    print(f"Gemini Connection Failed: {e}")

# Test OpenRouter First Key
k2 = secrets.openrouter[0]
try:
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {k2}"},
        json={"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "hi"}]},
        timeout=10
    )
    print(f"OpenRouter Status: {r.status_code}")
    if r.status_code != 200:
        print(f"OpenRouter Error: {r.text}")
except Exception as e:
    print(f"OpenRouter Connection Failed: {e}")
