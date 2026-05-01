#!/bin/ash

echo "🛠️ Starting Master Configuration..."

# 1. Create directory structure correctly
mkdir -p core/agents core/database core/utils production mechanic projects logs vault

# 2. Inject Credentials into .env
cat << 'EOT' > .env
# Gemini Keys (using first available)
GEMINI_API_KEY=AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas

# Telegram
TELEGRAM_BOT_TOKEN=8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4
TELEGRAM_CHAT_ID=8296776401

# Supabase
SUPABASE_URL=https://ixdukafvxqermhgoczou.supabase.co/
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk
SUPABASE_SECRET_KEY=sb_secret_Om4aMida0BSZW-33z2I9Rw_j-PS8KNk

# Infrastructure
OPENROUTER_KEY=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
NORTHFLANK_TOKEN=nf-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiYzUyZjNiNTYtNmNhZC00OGUyLTkzYzEtNmNjMTQzMTliNDdjIiwiZW50aXR5SWQiOiI2OTk4ZjA3NWNiZjJhODEwZjE5NTk5ZWIiLCJlbnRpdHlUeXBlIjoidGVhbSIsInRva2VuSWQiOiI2OWVkYWVmNWJiMGNkMWQ4YjhjYzgwYjYiLCJ0b2tlbkludGVybmFsSWQiOiJhaWkiLCJyb2xlSWQiOiI2OWVhNDU2MDdkNmNmOTJiNGIxZGIwMGIiLCJyb2xlRW50aXR5SWQiOiI2OTk4ZjA3NWNiZjJhODEwZjE5NTk5ZWIiLCJyb2xlRW50aXR5VHlwZSI6InRlYW0iLCJyb2xlSW50ZXJuYWxJZCI6ImN1c3RvbS1mdWxsIiwidHlwZSI6InJiYWMiLCJpYXQiOjE3NzcxODQ1MDF9.c3pUrHrUiH2VVOvP2HfsGk6E3-Q6_uo6OeZUBlbTfRo
DOCKERHUB_TOKEN=dckr_pat_IfVzYz0cWQ_zKbHmN0yqmaf--vI

RUN_MODE=local
EOT

echo "✅ .env configured with Xenia's keys."

# 3. Create the Mechanic CLI
cat << 'EOT' > mechanic/cli.py
import os
import sys

def main():
    print("🛰️  AI-CODER MECHANIC | Xenia Edition")
    print("-" * 30)
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    
    if cmd == "status":
        print("✅ Core Environment: Ready")
        print(f"📂 Active Path: {os.getcwd()}")
    elif cmd == "push":
        os.system("git add .")
        os.system('git commit -m "🧬 Evolution Update"')
        os.system("git push origin main")
    else:
        print("Commands: status, push")

if __name__ == "__main__":
    main()
EOT

# 4. Setup Git Authentication
git config --global user.email "hoopstreet143@gmail.com"
git config --global user.name "hoopstreet"
# Credential helper to store the token
git remote set-url origin https://hoopstreet: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@github.com/hoopstreet/Ai-Coder.git

echo "✅ Git credentials configured."
echo "🚀 Running setup_env.py..."
python3 setup_env.py
