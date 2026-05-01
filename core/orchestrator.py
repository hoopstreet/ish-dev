import os
from dotenv import load_dotenv
from supabase import create_client

# 1. Credentials (Using Service Role Key for full access)
load_dotenv()
SUPABASE_URL = "https://ixdukafvxqermhgoczou.supabase.co/"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk"

class AiOrchestrator:
    def __init__(self, project_name):
        self.project = project_name
        print(f"--- Hoopstreet AI-Coder: {self.project} Active ---")
        try:
            # Service role bypasses RLS permissions
            self.db = create_client(SUPABASE_URL, SUPABASE_KEY)
            print(f"✅ Supabase Link: Connected (Admin Access)")
        except Exception as e:
            print(f"❌ Connection Error: {e}")

    def get_project_context(self):
        """Fetch project details from the 'projects' table"""
        try:
            response = self.db.table('projects').select('*').eq('name', self.project).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"⚠️ Query Error: {e}")
            return None

if __name__ == "__main__":
    coder = AiOrchestrator("Ai-Coder")
    context = coder.get_project_context()
    if context:
        print(f"🚀 Context Sync Successful: {context['name']} ready.")
    else:
        print(f"💡 Project '{coder.project}' not found in 'public.projects'.")
