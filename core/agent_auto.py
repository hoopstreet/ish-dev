#!/usr/bin/env python3
"""
HOOPSTREET AUTONOMOUS AGENT with REAL-TIME CREDENTIAL SELECTION
"""

import sys, os, json, requests, subprocess
from credential_selector import CredentialSelector

class AutonomousAgent:
    def __init__(self):
        self.selector = CredentialSelector()
        self.provider, self.key = self.selector.get_best_working_key()
        
    def get_response(self, prompt):
        if not self.provider:
            return "❌ No working API keys found. Run: python3 credential_selector.py scan"
        
        if self.provider == "gemini":
            return self.call_gemini(prompt)
        elif self.provider == "openrouter":
            return self.call_openrouter(prompt)
        elif self.provider == "free":
            return self.call_free(prompt)
        return "No provider available"
    
    def call_gemini(self, prompt):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.key}"
            response = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}]
            }, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def call_openrouter(self, prompt):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

    
    def call_free(self, prompt):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def execute_command(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout if result.stdout else result.stderr

def main():
    agent = AutonomousAgent()
    
    print("\n" + "━" * 60)
    print("🚀 HOOPSTREET AUTONOMOUS AGENT (Real-time Credentials)")
    print("━" * 60)
    print(f"📡 Provider: {agent.provider or 'None'}")
    print(f"🔑 Key: {agent.key[:30] if agent.key else 'None'}...")
    print("━" * 60)
    
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[1:])
        if prompt.startswith('/exec '):
            print(agent.execute_command(prompt[6:]))
        else:
            print(agent.get_response(prompt))
    else:
        print("\n💬 Type naturally | /exec cmd | /exit\n")
        while True:
            try:
                cmd = input("🚀 > ").strip()
                if cmd in ['/exit', 'exit']:
                    break
                elif cmd.startswith('/exec '):
                    print(agent.execute_command(cmd[6:]))
                else:
                    print("\n🤖 Thinking...")
                    print(agent.get_response(cmd) + "\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
