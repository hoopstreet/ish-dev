import urllib.request
import json

# Your new key
api_key = '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'

print("Testing OpenRouter key...")
print(f"Key: {api_key[:20]}...")

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Say 'OK'"}],
    "max_tokens": 10
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(data).encode(),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        print("✅ Key is VALID!")
        print(f"Response: {result['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ Key is INVALID: {e}")
