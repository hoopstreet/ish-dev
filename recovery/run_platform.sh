#!/bin/sh
echo "🚀 Starting Enterprise AI-Coder Platform..."
# Start the Telegram Bot in the background
python3 /root/Ai-Coder/bot/main.py &
# Trigger the Agent for a final health check
python3 /root/Ai-Coder/agent.py "System Online: GitHub & Telegram Linked"
