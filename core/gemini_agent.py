#!/usr/bin/env python3
import os
import sys
import requests
import json

# Configuration from your provided environment
API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = "https://ixdukafvxqermhgoczou.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk"

def get_context():
    """Retrieves builder memory from Supabase public schema."""
    url = f"{SUPABASE_URL}/rest/v1/builder_memory?select=*"
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    try:
        r = requests.get(url, headers=headers)
        return r.json()[-1]['content'] if r.json() else "No recent memory found."
    except:
        return "Memory sync offline."

def execute_phase(prompt):
    """Sends prompt to Gemini and executes returned CLI blocks."""
    print(f"[*] Analyzing Project DNA...")
    context = get_context()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": f"Context: {context}\nTask: {prompt}\nOutput only the raw shell commands to execute."}]
        }]
    }
    
    response = requests.post(url, json=payload)
    commands = response.json()['candidates'][0]['content']['parts'][0]['text']
    
    # Clean and Execute
    for line in commands.split('\n'):
        if line.strip() and not line.startswith('```'):
            print(f"🚀 Executing: {line}")
            os.system(line)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_phase(" ".join(sys.argv[1:]))
    else:
        task = input("🤖 Gemini Agent > Enter task/roadmap phase: ")
        execute_phase(task)
