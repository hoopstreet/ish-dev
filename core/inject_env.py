import requests, os

def inject():
    token = os.getenv("NF_TOKEN")
    # Using the exact IDs from your Northflank URL structure
    project_id = "ai-coder"
    service_id = "ai-coder"
    
    # Correct API endpoint for secret variables in a deployment service
    url = f"https://api.northflank.com/v1/projects/{project_id}/services/deployment/{service_id}/config"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "deployment": {
            "secrets": [
                {"key": "CHAT_ID", "value": "8296776401"},
                {"key": "TELEGRAM_TOKEN", "value": "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"},
                {"key": "OR_KEY", "value": "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"},
                {"key": "SB_URL", "value": "https://ixdukafvxqermhgoczou.supabase.co/"},
                {"key": "SB_KEY", "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk"}
            ]
        }
    }
    
    print(f"📡 Sending configuration to Northflank...")
    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in [200, 201, 204]:
        print("✅ SUCCESS: Environment variables injected. Container restarting.")
    else:
        print(f"❌ FAILED: {r.status_code} - {r.text}")

if __name__ == "__main__":
    inject()
