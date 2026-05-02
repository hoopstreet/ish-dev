#!/usr/bin/env python3
import os
import sys
import requests
import json

# Using a fresh key from your authenticated list
API_KEY = "AIzaSyDl3XCDiTlrLbKtHyMFNArFprdKNzFrz7E"

def run_gemini_cli(prompt):
    print(f"🤖 Gemini CLI Agent [v9.3.7] Analyzing...")
    
    # Try v1beta with the standard model name
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"{prompt}. Output only raw linux shell commands. No markdown, no explanations."}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        # If v1beta fails with a 404, fallback to v1/gemini-pro
        if response.status_code == 404:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()

        if 'candidates' in data:
            commands = data['candidates'][0]['content']['parts'][0]['text']
            clean_commands = commands.replace('
```bash', '').replace('```', '').strip()
            
            for line in clean_commands.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"🚀 Executing: {line}")
                    os.system(line)
        else:
            msg = data.get('error', {}).get('message', 'Check API Key or Model Access.')
            print(f"❌ API Error: {msg}")
            
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("👉 Enter task: ")
    if task:
        run_gemini_cli(task)
