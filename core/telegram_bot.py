import telebot
import subprocess
import os
import sys

# Flush all prints immediately for logging
def log(msg):
    print(f">> {msg}")
    sys.stdout.flush()

TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
log("Initializing Bot...")

try:
    bot = telebot.TeleBot(TOKEN)
    
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        log(f"Received command from {message.chat.id}")
        bot.reply_to(message, "🚀 Ai-Coder Bot Active.\n\nSystem: Online\nGitHub: Connected\nSupabase: Syncing...")

    @bot.message_handler(func=lambda message: True)
    def handle_task(message):
        task = message.text
        log(f"Processing task: {task}")
        bot.reply_to(message, f"🛠 Running: {task}")
        try:
            res = subprocess.check_output(["python3", "/root/Ai-Coder/agent.py", task], stderr=subprocess.STDOUT)
            bot.reply_to(message, f"✅ Done:\n{res.decode()[-800:]}")
        except Exception as e:
            log(f"Error: {str(e)}")
            bot.reply_to(message, f"❌ Error: {str(e)}")

    log("Bot is now polling...")
    bot.infinity_polling()
except Exception as e:
    log(f"CRITICAL ERROR: {str(e)}")
