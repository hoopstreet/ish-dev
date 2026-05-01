#!/bin/sh
clear
echo "╔════════════════════════════════════════════╗"
echo "║     🌟 MULTI-MODEL HEALING AGENT 🌟       ║"
echo "║   Gemini Free → Keys → OpenRouter Free    ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "📋 Failover Strategy:"
echo "   1️⃣ Gemini Free API (key rotation)"
echo "   2️⃣ OpenRouter Free (gemini-2.0-flash)"
echo "   3️⃣ OpenRouter Paid (if available)"
echo ""

python3 /root/multi_agent.py
