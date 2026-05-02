#!/usr/bin/env python3
import os
import sys
import requests

# Using your verified Gemini API Key
API_KEY = "AIzaSyDHhh5zkL6NnEBD9SI-sLfl9Ur8yNA6PxA"

def run_gemini_cli(prompt):
    print(f"🤖 Gemini CLI Agent [v9.3.2] Analyzing...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt + " \nOutput only raw shell commands."}]}]
    }
    try:
        r = requests.post(url, json=payload)
        commands = r.json()['candidates'][0]['content']['parts'][0]['text']
        for line in commands.split('\n'):
            if line.strip() and not line.startswith('```'):
                print(f"🚀 Executing: {line}")
                os.system(line)
    except Exception as e:
        print(f"❌ Gemini CLI Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_gemini_cli(" ".join(sys.argv[1:]))
    else:
        cmd = input("👉 Enter task for Gemini Agent: ")
        run_gemini_cli(cmd)
