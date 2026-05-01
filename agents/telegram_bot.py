#!/usr/bin/env python3
import requests, json, os
from datetime import datetime

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, text):
        url = f"{self.base_url}/sendMessage"
        data = {"chat_id": self.chat_id, "text": text}
        try:
            requests.post(url, json=data)
        except:
            pass
    
    def send_status(self):
        with open("/root/ish-dev/docs/status.json", 'r') as f:
            status = json.load(f)
        msg = f"🏀 Hoopstreet Status\nVersion: {status['version']}\nHealth: {status['health']}"
        self.send_message(msg)

# Usage: python3 telegram_bot.py "message"
if __name__ == "__main__":
    import sys
    token = os.environ.get('TELEGRAM_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
    if token and chat_id and len(sys.argv) > 1:
        bot = TelegramBot(token, chat_id)
        bot.send_message(sys.argv[1])
