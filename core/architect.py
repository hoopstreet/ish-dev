import os
import requests
import json

class ArchitectAgent:
    def __init__(self):
        # We fetch the key directly from the .env we injected earlier
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={self.api_key}"

    def plan_task(self, user_prompt):
        """Analyzes a request and returns a structured JSON plan."""
        system_prompt = (
            "You are the AI-Coder Architect. Your job is to take a coding request "
            "and break it down into a specific plan. Output only valid JSON with "
            "the keys: 'summary', 'affected_files', and 'steps'."
        )
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nUser Request: {user_prompt}"}]
            }]
        }

        try:
            response = requests.post(self.url, json=payload, timeout=30)
            result = response.json()
            # Extracting the text content
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            # Cleaning potential markdown code blocks from JSON response
            clean_json = text_response.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except Exception as e:
            return {"error": str(e), "summary": "Failed to generate plan."}

if __name__ == "__main__":
    # Test run
    architect = ArchitectAgent()
    print("🤖 Architect testing connection...")
    test_plan = architect.plan_task("Create a simple landing page for my AI project.")
    print(json.dumps(test_plan, indent=4))
