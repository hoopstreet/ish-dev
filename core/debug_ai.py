#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load the specific path we created
load_dotenv("/root/.hoopstreet/creds/.env")

gemini_keys = [k for k in os.getenv("GEMINI_KEYS", "").split(",") if k]
open_keys = [k for k in os.getenv("OPENROUTER_KEYS", "").split(",") if k]

print(f"Checking Gemini Keys: {len(gemini_keys)} found")
print(f"Checking OpenRouter Keys: {len(open_keys)} found")

if gemini_keys:
    from ai.router import ai
    print("Testing Gemini Connection...")
    res = ai.ask("Status check: Reply with 'Hoopstreet Online'")
    print(f"Response: {res}")
else:
    print("Skipping test: No keys available.")
