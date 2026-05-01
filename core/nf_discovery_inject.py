import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Discover Projects
    p_res = requests.get("https://api.northflank.com/v1/projects", headers=headers)
    if p_res.status_code != 200:
        print(f"❌ Auth Error: {p_res.text}")
        return

    projects = p_res.json().get('projects', [])
    if not projects:
        print("❌ No projects found.")
        return

    # Use the first project found
    proj_id = projects[0]['id']
    print(f"📂 Found Project: {proj_id}")

    # 2. Discover Services
    s_res = requests.get(f"https://api.northflank.com/v1/projects/{proj_id}/services", headers=headers)
    services = s_res.json().get('services', [])
    if not services:
        print(f"❌ No services found in {proj_id}")
        return

    # Use the first service found (likely ai-coder)
    svc_id = services[0]['id']
    print(f"🚀 Found Service: {svc_id}")

    # 3. Inject Config
    url = f"https://api.northflank.com/v1/projects/{proj_id}/services/deployment/{svc_id}/config"
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
    
    print(f"📡 Injecting Env...")
    r = requests.put(url, json=data, headers=headers)
    if r.status_code < 300:
        print("✅ SUCCESS: Northflank Config Updated.")
    else:
        print(f"❌ Injection Failed: {r.status_code} - {r.text}")

run()
