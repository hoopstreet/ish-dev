import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    # Trialing the exact ID structure from Northflank API
    project = "ai-coder"
    service = "ai-coder"
    
    # Updated API route to specifically target Environment variables
    url = f"https://api.northflank.com/v1/projects/{project}/services/deployment/{service}/config"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    data = {
        "deployment": {
            "secrets": [
                {"key": "CHAT_ID", "value": os.getenv("CHAT_ID")},
                {"key": "TELEGRAM_TOKEN", "value": os.getenv("TELEGRAM_TOKEN")},
                {"key": "OR_KEY", "value": os.getenv("OR_KEY")},
                {"key": "SB_URL", "value": os.getenv("SB_URL")},
                {"key": "SB_KEY", "value": os.getenv("SB_KEY")}
            ]
        }
    }
    
    print(f"📡 Injecting Env to Northflank...")
    r = requests.put(url, headers=headers, json=data)
    if r.status_code < 300:
        print("✅ SUCCESS: Northflank updated.")
    else:
        # Fallback to secondary route if first fails
        url_alt = f"https://api.northflank.com/v1/projects/{project}/services/combined/{service}/config"
        r_alt = requests.put(url_alt, headers=headers, json=data)
        print(f"⚠️ Primary Failed ({r.status_code}). Alt Status: {r_alt.status_code}")
        if r_alt.status_code >= 400:
             print(f"❌ Detail: {r_alt.text}")

run()
