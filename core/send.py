#!/usr/bin/env python3
import asyncio
import random
import logging
from telethon import TelegramClient
from telethon.tl.functions.contacts import AddContactRequest

# YOUR CREDENTIALS
API_ID = 39849897
API_HASH = '21eb2d7f293519cc5eb575c9639e1423'
BOT_TOKEN = '8306476254:AAFLnK109G7jQo4gGvRUrzfHfd8kXfZ_UtY'
OWNER_ID = 5861858910

# Initialize Client
client = TelegramClient('hoopstreet_session', API_ID, API_HASH)

async def send_bulk_messages(usernames, message):
    if not client.is_connected():
        await client.start()
    
    for username in usernames:
        try:
            print(f"Targeting: {username}")
            # Safety Step: Add Contact
            await client(AddContactRequest(
                id=username, 
                first_name="Hoopstreet", 
                last_name="", 
                phone="", 
                add_phone_privacy_exception=False
            ))
            
            # Send Message
            await client.send_message(username, message)
            print(f"Sent to {username}")
            
            # Anti-Ban Delay (2-5 minutes)
            wait = random.randint(120, 300)
            await asyncio.sleep(wait)
            
        except Exception as e:
            print(f"Error with {username}: {e}")
            await asyncio.sleep(30)

async def main():
    # This keeps the client alive to listen for your Bot commands
    await client.start()
    print("Hoopstreet System Online. Waiting for triggers...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
