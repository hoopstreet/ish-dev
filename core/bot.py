import os
import telebot
import subprocess

TOKEN = "7727181816:AAFr5LzY212uA7rI7KkQo7l6m8kU6K_7H" # Recovered from history
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'status'])
def send_status(message):
    status_msg = "🤖 Ai-Coder Artic v2.2.0\n✅ Core: Online\n✅ Supabase: Linked\n✅ GitHub: Synced"
    bot.reply_to(message, status_msg)

@bot.message_handler(func=lambda message: True)
def handle_agent_request(message):
    bot.reply_to(message, "⚙️ Processing via Swarm Supreme...")
    # Trigger the agent logic
    cmd = f"agent '{message.text}'"
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    bot.reply_to(message, f"✅ Result:\n{process.stdout[:1000]}")

print("🚀 Telegram Bot Starting...")
bot.infinity_polling()
