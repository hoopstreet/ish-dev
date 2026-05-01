import os
from supabase import create_client

url = os.getenv('SUPABASE_URL', "https://ixdukafvxqermhgoczou.supabase.co")
key = os.getenv('SUPABASE_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk")
supabase = create_client(url, key)

def add_to_queue(username):
    existing = supabase.table('queue').select('id').eq('username', username).execute()
    if not existing.data:
        supabase.table('queue').insert({'username': username, 'status': 'pending'}).execute()

def get_accounts():
    return supabase.table('accounts').select('*').execute().data

def save_account(phone_val, session_str):
    supabase.table('accounts').upsert({'session_string': session_str, 'is_active': True}).execute()

def get_next_target():
    res = supabase.table('queue').select('*').eq('status', 'pending').order('id').limit(1).execute()
    return res.data[0] if res.data else None

def update_queue(id, status):
    supabase.table('queue').update({'status': status}).eq('id', id).execute()

def set_setting(key, value):
    supabase.table('settings').upsert({'key': key, 'value': str(value)}, on_conflict='key').execute()

def get_setting(key):
    res = supabase.table('settings').select('value').eq('key', key).execute()
    return res.data[0]['value'] if res.data else None
