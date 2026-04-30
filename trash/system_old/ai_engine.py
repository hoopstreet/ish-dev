#!/usr/bin/env python3
import os, requests, random
from dotenv import load_dotenv

load_dotenv("/root/.hoopstreet/creds/.env")

GEMINI_KEYS = os.getenv("GEMINI_KEYS","").split(",")
OPENROUTER_KEYS = os.getenv("OPENROUTER_KEYS","").split(",")

def gemini_fix(code, error):
    for key in GEMINI_KEYS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
            payload = {
                "contents":[{"parts":[{"text": f"Fix this shell script:\nERROR:\n{error}\nCODE:\n{code}"}]}]
            }
            r = requests.post(url, json=payload, timeout=20)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return None

def openrouter_fix(code, error):
    for key in OPENROUTER_KEYS:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages":[{"role":"user","content":f"Fix:\n{error}\n{code}"}]
                },
                timeout=20
            )
            return r.json()["choices"][0]["message"]["content"]
        except:
            continue
    return None

def fix_code(code, error):
    print("🤖 Trying Gemini pool...")
    result = gemini_fix(code, error)

    if result:
        return result

    print("🔁 Falling back to OpenRouter...")
    return openrouter_fix(code, error)
