# Update agent to use OpenRouter
import re

# Read current agent
with open('/root/agent.py', 'r') as f:
    content = f.read()

# Replace the fix_code method with OpenRouter version
old_method = r'''    def fix_code\(self, code, error\):
        if not self\.api_key: 
            return None
        prompt = f"Fix this Python code\. Return ONLY corrected code\.\n\nCODE:\n\{code\}\n\nERROR:\n\{error\}\n\nFIXED CODE:"
        data = \{"model":"gpt-3\.5-turbo","messages":\[\{"role":"user","content":prompt\}\],"max_tokens":500\}
        req = urllib\.request\.Request\("https://api\.openai\.com/v1/chat/completions", 
            data=json\.dumps\(data\)\.encode\(\), 
            headers=\{"Authorization":f"Bearer \{self\.api_key\}","Content-Type":"application/json"\}\)
        try:
            resp = json\.loads\(urllib\.request\.urlopen\(req, timeout=45\)\.read\(\)\)
            fixed = resp\['choices'\]\[0\]\['message'\]\['content'\]
            if '```python' in fixed: 
                fixed = fixed\.split\('```python'\)\[1\]\.split\('```'\)\[0\]
            return fixed\.strip\(\)
        except: 
            return None'''

new_method = '''    def fix_code(self, code, error):
        if not self.api_key: 
            return None
        prompt = f"Fix this Python code. Return ONLY corrected code.\\n\\nCODE:\\n{code}\\n\\nERROR:\\n{error}\\n\\nFIXED CODE:"
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ish.iphone.local",
                "X-Title": "iSH Self-Healing Agent"
            }
        )
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=45).read())
            fixed = resp['choices'][0]['message']['content']
            if '```python' in fixed:
                fixed = fixed.split('```python')[1].split('```')[0]
            if '```' in fixed and '```python' not in fixed:
                fixed = fixed.split('```')[1].split('```')[0]
            return fixed.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return None'''

# Simple replacement using string replace
content = content.replace(
    "def fix_code(self, code, error):",
    "def fix_code(self, code, error):\n        if not self.api_key: \n            return None"
)
# Write the OpenRouter version directly
