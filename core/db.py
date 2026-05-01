import requests
from core.rotator import SmartRotator

class CloudDB:
    def __init__(self):
        self.rotator = SmartRotator()
        self.conf = self.rotator.config.get("SUPABASE", {})
        self.url = self.conf.get("URL")
        self.key = self.conf.get("SERVICE_ROLE")

    def log_event(self, event_type, details):
        if not self.url: return
        headers = {"apikey": self.key, "Authorization": f"Bearer {self.key}"}
        payload = {"event_type": event_type, "details": details}
        try:
            requests.post(f"{self.url}/rest/v1/logs", headers=headers, json=payload, timeout=3)
        except: pass
