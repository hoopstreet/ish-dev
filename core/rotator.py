import json
import base64
import os

ENC_PATH = "/root/Ai-Coder/core/config.enc"

class SmartRotator:
    def __init__(self):
        self.config = {}
        try:
            if os.path.exists(ENC_PATH):
                with open(ENC_PATH, "r") as f:
                    encoded_data = f.read()
                    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
                    self.config = json.loads(decoded_data)
            else:
                print(f"❌ Error: {ENC_PATH} missing.")
        except Exception as e:
            print(f"❌ Decryption Error: {e}")
        self.gemini_index = 0

    def get_gemini_key(self):
        keys = self.config.get("GEMINI_KEYS", [])
        return keys[self.gemini_index] if keys else None

    def rotate_on_fail(self):
        keys = self.config.get("GEMINI_KEYS", [])
        if keys:
            self.gemini_index = (self.gemini_index + 1) % len(keys)
            print(f"🔄 Switched to Gemini Key #{self.gemini_index}")
