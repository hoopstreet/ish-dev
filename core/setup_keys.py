#!/usr/bin/env python3
import re

print("🔑 MULTI-MODEL KEY CONFIGURATOR")
print("="*50)

# Update multi_agent.py with your keys
with open('/root/multi_agent.py', 'r') as f:
    content = f.read()

# Replace Gemini keys placeholder
gemini_keys_input = input("\nEnter Gemini keys (comma-separated, at least 1): ")
gemini_keys = [k.strip() for k in gemini_keys_input.split(',')]

# Replace OpenRouter free keys  
or_free_input = input("Enter OpenRouter free keys (comma-separated): ")
or_free_keys = [k.strip() for k in or_free_input.split(',')] if or_free_input else []

# Replace OpenRouter paid keys
or_paid_input = input("Enter OpenRouter paid keys (optional): ")
or_paid_keys = [k.strip() for k in or_paid_input.split(',')] if or_paid_input else []

# Update the file
content = re.sub(r'self\.gemini_keys = \[.*?\]', f'self.gemini_keys = {gemini_keys}', content, flags=re.DOTALL)
content = re.sub(r'self\.openrouter_free_keys = \[.*?\]', f'self.openrouter_free_keys = {or_free_keys}', content, flags=re.DOTALL)
content = re.sub(r'self\.openrouter_paid_keys = \[.*?\]', f'self.openrouter_paid_keys = {or_paid_keys}', content, flags=re.DOTALL)

with open('/root/multi_agent.py', 'w') as f:
    f.write(content)

print(f"\n✅ Configured: {len(gemini_keys)} Gemini keys, {len(or_free_keys)} OpenRouter free, {len(or_paid_keys)} OpenRouter paid")
print("\nRun: python3 /root/multi_agent.py")
