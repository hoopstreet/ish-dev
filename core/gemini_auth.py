#!/usr/bin/env python3
#!/usr/bin/env python3
"""
HOOPSTREET GEMINI CLI AUTHENTICATION
- Google OAuth login
- Gemini API Key support
- Vertex AI support
"""

import sys, os, subprocess, json, requests
from pathlib import Path

class GeminiAuth:
    def __init__(self):
        self.home = str(Path.home())
        self.config_dir = f"{self.home}/.gemini"
        self.env_file = f"{self.config_dir}/.env"
        
    def setup_oauth(self):
        """Setup OAuth authentication (requires browser)"""
        print("\n🔐 Setting up Google OAuth...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("This will open a browser window for Google login.")
        print("Make sure you're logged into your Google account.\n")
        
        try:
            # Use gcloud if available
            result = subprocess.run(["gcloud", "auth", "application-default", "login"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ OAuth setup successful!")
                return True
        except:
            pass
        
        # Alternative: guide user to get API key
        print("⚠️ gcloud not found. Use Gemini API key instead.\n")
        print("Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    
    def setup_api_key(self):
        """Setup Gemini API key"""
        print("\n🔑 Gemini API Key Setup")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Get your API key from: https://aistudio.google.com/app/apikey\n")
        
        api_key = input("Enter your Gemini API Key: ").strip()
        
        if api_key.startswith("AIzaSy"):
            # Save to .gemini/.env
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.env_file, 'w') as f:
                f.write(f'GEMINI_API_KEY="{api_key}"\n')
            os.chmod(self.env_file, 0o600)
            print(f"\n✅ API Key saved to {self.env_file}")
            return True
        else:
            print("❌ Invalid API key format. Should start with 'AIzaSy'")
            return False
    
    def setup_vertex_ai(self):
        """Setup Vertex AI authentication"""
        print("\n🏢 Vertex AI Setup")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        project_id = input("Google Cloud Project ID: ").strip()
        location = input("Region (e.g., us-central1): ").strip()

        
        if project_id:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.env_file, 'w') as f:
                f.write(f'GOOGLE_CLOUD_PROJECT="{project_id}"\n')
                f.write(f'GOOGLE_CLOUD_LOCATION="{location}"\n')
            print(f"\n✅ Vertex AI config saved to {self.env_file}")
            return True
        return False
    
    def run_gemini_cli(self):
        """Launch official Gemini CLI if installed"""
        print("\n🚀 Launching Gemini CLI...")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Check if gemini CLI is installed
        try:
            subprocess.run(["gemini", "--version"], capture_output=True, check=True)
            subprocess.run(["gemini"], check=False)
        except:
            print("⚠️ Gemini CLI not installed.")
            print("Install with: npm install -g @google/gemini-cli")
            print("Or use our autonomous agent: ai 'your question'")

def main():
    auth = GeminiAuth()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "oauth":
            auth.setup_oauth()
        elif cmd == "apikey":
            auth.setup_api_key()
        elif cmd == "vertex":
            auth.setup_vertex_ai()
        elif cmd == "run":
            auth.run_gemini_cli()
        else:
            print("Commands: oauth, apikey, vertex, run")
    else:
        print("\n🔐 HOOPSTREET GEMINI AUTHENTICATION")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. OAuth Login (Browser) - gemini_auth.py oauth")
        print("2. API Key Setup + gemini_auth.py apikey")
        print("3. Vertex AI Setup + gemini_auth.py vertex")
        print("4. Run Gemini CLI - gemini_auth.py run")

if __name__ == "__main__":
    main()
