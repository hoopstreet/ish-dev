#!/bin/sh
echo "🎨 Starting Visual Self-Healing Agent"
echo "======================================"

export OPENROUTER_API_KEY='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'

# Check if key is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  No API key - using rule-based fixes only"
else
    echo "✅ OpenRouter API key loaded"
fi

echo ""
python3 /root/visual_agent.py
