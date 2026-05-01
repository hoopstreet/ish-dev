import asyncio, os, sys, threading
from fastapi import FastAPI
import uvicorn
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime, timedelta

app = FastAPI()
@app.get("/")
def health(): return {"status": "online"}

def start_web():
    uvicorn.run(app, host="0.0.0.0", port=8080)

API_ID = int(os.getenv('API_ID', 29748251))
API_HASH = os.getenv('API_HASH', 'ce97166a7552c061a3da822233c32873')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8664911522:AAHA9qT6L7dv-OlrfNv5lAOiDsg29SujCx8')
OWNER_ID = int(os.getenv('OWNER_ID', 8296776401))

sys.path.append('.')
try:
    import database
except ImportError:
    database = None

bot = TelegramClient('bot_commander', API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/status'))
async def status(event):
    if event.sender_id != OWNER_ID: return
    pht = (datetime.utcnow() + timedelta(hours=8)).strftime('%I:%M %p')
    await event.respond(f"✅ **Node Online**\n🕒 PHT: {pht}\n\nCommands:\n/add_qr\n/add_phone +number")

@bot.on(events.NewMessage(pattern='/add_qr'))
async def add_qr(event):
    if event.sender_id != OWNER_ID: return
    await event.respond("🔄 **Generating Link...**")
    client = TelegramClient(StringSession(), API_ID, API_HASH, device_model="iPhone 11")
    await client.connect()
    try:
        qr = await client.qr_login()
        await event.respond(f"🔗 **Action:** Tap & Confirm:\n\n`{qr.url}`")
        user = await qr.wait()
        session = client.session.save()
        if database: database.save_account(user.id, session)
        await event.respond(f"✅ Logged in as {user.first_name}")
    except Exception as e:
        await event.respond(f"❌ QR Error: {e}")
    finally:
        await client.disconnect()

@bot.on(events.NewMessage(pattern='/add_phone'))
async def add_phone(event):
    if event.sender_id != OWNER_ID: return
    parts = event.text.split(' ')
    if len(parts) < 2: return await event.respond("❌ Use: `/add_phone +639xxxx`")
    phone = parts[1]
    client = TelegramClient(StringSession(), API_ID, API_HASH, device_model="iPhone 11")
    await client.connect()
    try:
        await client.send_code_request(phone)
        async with bot.conversation(event.chat_id) as conv:
            await conv.send_message("📩 **Send the 5-digit code here:**")
            code = (await conv.get_response()).text.strip()
            try:
                user = await client.sign_in(phone, code)
            except Exception:
                await conv.send_message("🔑 **Enter 2FA Password:**")
                pwd = (await conv.get_response()).text.strip()
                user = await client.sign_in(password=pwd)
            session = client.session.save()
            if database: database.save_account(user.id, session)
            await conv.send_message(f"✅ Logged in as {user.first_name}")
    except Exception as e:
        await event.respond(f"❌ Error: {e}")
    finally:
        await client.disconnect()

async def run_bot():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.run_until_disconnected()

if __name__ == '__main__':
    threading.Thread(target=start_web, daemon=True).start()
    asyncio.run(run_bot())
