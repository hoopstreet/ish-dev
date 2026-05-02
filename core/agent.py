#!/usr/bin/env python3
import os, sys, requests, json

# Using your OpenRouter key for better model availability
API_KEY = "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"
MODEL = "google/gemini-flash-1.5"

def run_gemini_cli(prompt):
    print(f"🤖 Hoopstreet OS Agent [v9.3.9] Analyzing...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": f"{prompt}. Output only raw linux shell commands. No markdown."}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'choices' in data:
            raw_text = data['choices'][0]['message']['content']
            clean_lines = [line for line in raw_text.split('\n') if '```' not in line and line.strip()]
            
            for cmd in clean_lines:
                print(f"🚀 Executing: {cmd}")
                os.system(cmd)
        else:
            print(f"❌ API Error: {data.get('error', {}).get('message', 'Unknown Error')}")
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("👉 Enter task: ")
    if task: run_gemini_cli(task)
