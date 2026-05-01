#!/bin/sh
export OPENROUTER_API_KEY='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'
echo "🤖 Starting OpenRouter agent..."
python3 /root/or_agent.py broken.py
