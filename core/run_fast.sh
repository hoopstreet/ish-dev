#!/bin/sh
clear
echo "╔════════════════════════════════════╗"
echo "║   🎨 VISUAL SELF-HEALING AGENT    ║"
echo "║      Fast Mode for iSH iPhone     ║"
echo "╚════════════════════════════════════╝"
echo ""

export OPENROUTER_API_KEY='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'

if [ -n "$OPENROUTER_API_KEY" ]; then
    echo "✅ API Key: ${OPENROUTER_API_KEY:0:20}..."
else
    echo "⚠️  No API key (rule-based fixes only)"
fi

echo ""
python3 /root/fast_visual.py
