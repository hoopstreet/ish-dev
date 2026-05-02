    def _call_gemini(self, prompt, idx):
        if self.gemini_failed[idx]:
            return None
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_keys[idx]}"
        data = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.2,"maxOutputTokens":800}}
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())['candidates'][0]['content']['parts'][0]['text'], None
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                self.gemini_failed[idx] = True
            return None, str(e)
    
    def _call_or(self, prompt):
        data = {"model":"google/gemini-2.0-flash-exp:free","messages":[{"role":"user","content":prompt}],"max_tokens":800}
        try:
            req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(data).encode(), headers={"Authorization":f"Bearer {self.or_key}","Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())['choices'][0]['message']['content'], None
        except:
            return None, "Failed"
    print("✅ Phase 4: API methods added")
