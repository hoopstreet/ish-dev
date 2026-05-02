#!/usr/bin/env python3
import os, sys, requests, json

API_KEY = "AIzaSyDl3XCDiTlrLbKtHyMFNArFprdKNzFrz7E"

def run_gemini_cli(prompt):
    print(f"🤖 Gemini CLI Agent [v9.3.8] Analyzing...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": f"{prompt}. Output only raw linux shell commands. No markdown."}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'candidates' in data:
            raw_text = data['candidates'][0]['content']['parts'][0]['text']
            # Robust cleaning of markdown blocks
            clean_lines = [line for line in raw_text.split('\n') if '```' not in line and line.strip()]
            
            for cmd in clean_lines:
                print(f"🚀 Executing: {cmd}")
                os.system(cmd)
        else:
            msg = data.get('error', {}).get('message', 'Check API Access')
            print(f"❌ API Error: {msg}")
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("👉 Enter task: ")
    if task: run_gemini_cli(task)
