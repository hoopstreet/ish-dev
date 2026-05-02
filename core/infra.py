import requests
import json
import base64
import os
from core.rotator import SmartRotator

class CloudInfra:
    def __init__(self):
        self.rotator = SmartRotator()
        # Fallback to empty dict if config loading failed
        self.config = getattr(self.rotator, 'config', {})
        self.nf_token = self.config.get("NORTHFLANK_TOKEN")
        self.docker = self.config.get("DOCKERHUB", {})

    def get_nf_headers(self):
        return {
            "Authorization": f"Bearer {self.nf_token}",
            "Content-Type": "application/json"
        }

    def list_projects(self):
        if not self.nf_token:
            print("❌ No Northflank Token found.")
            return None
        url = "https://api.northflank.com/v1/projects"
        try:
            response = requests.get(url, headers=self.get_nf_headers())
            if response.status_code == 200:
                print("✅ Northflank Connection: Active")
                return response.json()
        except:
            pass
        return None

    def trigger_docker_build(self):
        print(f"🐳 Ready for DockerHub: {self.docker.get('USERNAME')}")
        return True
