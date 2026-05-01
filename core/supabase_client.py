import os
from supabase import create_client

class SupabaseManager:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "https://ixdukafvxqermhgoczou.supabase.co/")
        self.key = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M iOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91 Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3M iwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1 LF3RJnQNacBc-dHk")
        self.client = create_client(self.url, self.key)

    def get_project(self, name):
        try:
            return self.client.table("projects").select("*").eq("name", name).execute().data
        except: return []

    def save_log(self, project_name, level, msg):
        try:
            self.client.table("logs").insert({"level": level, "module": project_name, "message": msg}).execute()
        except: pass

    def update_memory(self, project_id, data):
        try:
            self.client.table("memory").upsert({"project_id": project_id, "data": data}).execute()
        except: pass
