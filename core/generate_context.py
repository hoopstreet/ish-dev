#!/usr/bin/env python3
import os
import json
import requests
from security.loader import secrets

# Configuration
TARGET_DIRS = ['/root/ish-dev', '/root/.hoopstreet', '/etc/network']
GITHUB_REPO = "hoopstreet/ish-dev"

def get_local_structure(path):
    structure = []
    for root, dirs, files in os.walk(path):
        # Skip hidden git and cache folders to save space
        if '.git' in dirs: dirs.remove('.git')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # We only read text-based files
                if file.endswith(('.py', '.sh', '.env', '.md', '.json', '.js')):
                    with open(file_path, 'r') as f:
                        content = f.read()
                    structure.append({
                        "path": file_path,
                        "content": content
                    })
            except Exception as e:
                structure.append({"path": file_path, "content": f"Error reading: {str(e)}"})
    return structure

def get_github_metadata():
    url = f"https://api.github.com/repos/{GITHUB_REPO}"
    headers = {"Authorization": f"token {secrets.github}"}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else {"error": "Could not fetch GitHub metadata"}

if __name__ == "__main__":
    print("🧠 Mapping iSH Local Files & Root Context...")
    full_data = {
        "metadata": {
            "project": "Hoopstreet iSH-Dev Automation",
            "github_info": get_github_metadata(),
            "environment": "iPhone iSH (Alpine x86)"
        },
        "files": []
    }

    for d in TARGET_DIRS:
        if os.path.exists(d):
            full_data["files"].extend(get_local_structure(d))

    with open("ai_master_setup.json", "w") as f:
        json.dump(full_data, f, indent=2)

    print("\n✅ DONE! File created: ai_master_setup.json")
    print("👉 Next: Upload this file or copy-paste its content to Gemini.")
