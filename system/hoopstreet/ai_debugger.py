#!/usr/bin/env python3
import os, json, subprocess, requests

# NOTE: replace with your model endpoint (OpenAI / local / proxy)
AI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = "YOUR_KEY"

def run_llm_debug(code, error):
    prompt = f"""
You are a senior DevOps engineer.

Fix this broken shell/python code.

RULES:
- Only return corrected code
- Do not explain
- Keep same intent

CODE:
{code}

ERROR:
{error}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    r = requests.post(AI_ENDPOINT, headers=headers, json=payload)
    return r.json()["choices"][0]["message"]["content"]

def fix_file(path, error):
    with open(path, "r") as f:
        code = f.read()

    fixed = run_llm_debug(code, error)

    with open(path, "w") as f:
        f.write(fixed)

    return fixed
