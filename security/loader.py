import os
from dotenv import load_dotenv

load_dotenv("/root/.hoopstreet/creds/.env")

class Secrets:
    def __init__(self):
        self.github = os.getenv("GITHUB_TOKEN")
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")

        self.gemini_keys = [k for k in os.getenv("GEMINI_KEYS","").split(",") if k]
        self.openrouter_keys = [k for k in os.getenv("OPENROUTER_KEYS","").split(",") if k]

secrets = Secrets()
