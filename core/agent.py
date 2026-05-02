#!/usr/bin/env python3
import os
import sys
import requests
import json

API_KEY = "AIzaSyDHhh5zkL6NnEBD9SI-sLfl9Ur8yNA6PxA"

def run_gemini_cli(prompt):
    print(f"🤖 Gemini CLI Agent [v9.3.3] Analyzing...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"{prompt}. Output only raw linux shell commands. No markdown, no explanations."}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'candidates' in data:
            commands = data['candidates'][0]['content']['parts'][0]['text']
            # Clean markdown code blocks if AI included them
            clean_commands = commands.replace('```bash', '').replace('```', '').strip()
            
            for line in clean_commands.split('\n'):
                line = line.strip()
                if line:
                    print(f"🚀 Executing: {line}")
                    os.system(line)
        else:
            print(f"❌ API Error: {json.dumps(data)}")
            
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("👉 Enter task: ")
    if task:
        run_gemini_cli(task)
