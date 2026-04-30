import requests
import os
import base64
from security.loader import secrets

def fetch_structure(owner, repo, path=""):
    """Recursively fetches the file tree and content."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {secrets.github}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error: {response.status_code}"

    items = response.json()
    output = ""
    
    for item in items:
        if item['type'] == 'dir':
            output += f"\n--- DIR: {item['path']} ---\n"
            output += fetch_structure(owner, repo, item['path'])
        else:
            # Skip binary files/images to save tokens
            ext = item['name'].split('.')[-1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'gif', 'ico', 'zip', 'pyc']:
                continue
                
            file_response = requests.get(item['url'], headers=headers)
            content = base64.b64decode(file_response.json()['content']).decode('utf-8', errors='ignore')
            output += f"\nFILE: {item['path']}\n"
            output += "```\n" + content + "\n```\n"
            
    return output

if __name__ == "__main__":
    owner = "charles-tanauan" # Change if your username is different
    repo = input("Enter Repo Name (e.g., Hoopstreet-V12): ")
    print(f"🚀 Ingesting {repo}...")
    full_code = fetch_structure(owner, repo)
    
    with open(f"{repo}_full_dump.txt", "w") as f:
        f.write(full_code)
    
    print(f"✅ Success! Data saved to {repo}_full_dump.txt")
    print("Run: cat " + repo + "_full_dump.txt")
