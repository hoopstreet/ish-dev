import httpx, json

class GeminiBrain:
    def __init__(self):
        self.api_key = "" # System injected
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={self.api_key}"

    def generate_code(self, prompt, context=""):
        system_prompt = "You are an expert Python developer. Return ONLY raw code without markdown blocks."
        payload = {
            "contents": [{ "parts": [{ "text": f"Context: {context}\nTask: {prompt}" }] }],
            "systemInstruction": { "parts": [{ "text": system_prompt }] }
        }
        try:
            r = httpx.post(self.url, json=payload, timeout=30)
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"# Error generating code: {str(e)}"
