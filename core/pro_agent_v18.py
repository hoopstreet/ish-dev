import json, subprocess, sys
from datetime import datetime

def get_key():
    try:
        with open("/root/.hoopstreet/creds/credentials.txt", "r") as f:
            for line in f:
                if "GEMINI_API_KEY" in line:
                    return line.split("=")[1].strip()
    except: return None

def ask_gemini(prompt):
    key = get_key()
    if not key: return "❌ Error: GEMINI_API_KEY not found."
    
    # Using v1 stable endpoint and Gemini 2.5 Flash for 2026 stability
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={key}"
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }
    
    # Standard iSH curl call
    cmd = ['curl', '-s', '-X', 'POST', url, '-H', 'Content-Type: application/json', '-d', json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        resp = json.loads(result.stdout)
        if 'error' in resp:
            return f"⚠️ API Error {resp['error']['code']}: {resp['error']['message']}"
        return resp['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ Parsing Error. Raw output summary: {result.stdout[:150]}"

if __name__ == "__main__":
    print(f"🏀 HOOPSTREET OMNI-AGENT v18.0.2 [FIXED]")
    print(f"📅 Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("──────────────────────────────")
    while True:
        query = input("🚀 > ")
        if query.lower() in ['exit', '0', 'back']: break
        if not query.strip(): continue
        print("🤔 Thinking...")
        print(f"\n{ask_gemini(query)}\n")
