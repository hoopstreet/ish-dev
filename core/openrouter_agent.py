#!/usr/bin/env python3
"""
HOOPSTREET OPENROUTER AGENT - Fixed Authentication
"""

import sys, os, json, requests, subprocess
from datetime import datetime

os.environ['TZ'] = 'Asia/Manila'
try: time.tzset()
except: pass

class OpenRouterAgent:
    def __init__(self):
        self.api_key = self.get_api_key()
        
    def get_api_key(self):
        """Get OpenRouter API key from credentials"""
        cred_files = [
            "/root/.hoopstreet/creds/ai_keys.json",
            "/root/.hoopstreet/creds/credentials.txt"
        ]
        
        for file in cred_files:
            if os.path.exists(file):
                try:
                    if file.endswith('.json'):
                        with open(file, 'r') as f:
                            data = json.load(f)
                            for key in data.get("openrouter", []):
                                if key.get("key"):
                                    return key.get("key")
                    else:
                        with open(file, 'r') as f:
                            for line in f:
                                if 'sk-or-v1' in line:
                                    return line.split('=')[-1].strip()
                except:
                    pass
        return None
    
    def call_api(self, prompt, model="openai/gpt-3.5-turbo"):
        """Call OpenRouter API with proper auth"""
        if not self.api_key:
            return "❌ No OpenRouter API key found. Add to credentials."
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/hoopstreet/ish-dev",
                    "X-Title": "Hoopstreet AI Agent"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 401:
                return "❌ Invalid API key. Please check your OpenRouter key."
            else:
                return f"❌ API Error: {response.status_code} - {response.text[:100]}"

                
        except Exception as e:
            return f"❌ Connection error: {e}"
    
    def interactive(self):
        print("\n" + "━" * 60)
        print("🚀 HOOPSTREET OPENROUTER AGENT")
        print("━" * 60)
        print(f"🔑 API Key: {'✅ Configured' if self.api_key else '❌ Missing'}")
        print("━" * 60)
        print("\n💬 Type your questions | /exit to quit\n")
        
        while True:
            try:
                user_input = input("🔷 > ").strip()
                if user_input.lower() in ['/exit', 'exit']:
                    break
                if not user_input:
                    continue
                
                print("\n🤖 Thinking...")
                response = self.call_api(user_input)
                print(f"\n{response}\n")
                
            except KeyboardInterrupt:
                break

def main():
    agent = OpenRouterAgent()
    
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        print(agent.call_api(prompt))
    else:
        agent.interactive()

if __name__ == "__main__":
    main()
