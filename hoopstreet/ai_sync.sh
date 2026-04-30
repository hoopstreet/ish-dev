#!/bin/sh
clear
echo "════════════════════════════════════════════════════════"
echo "     🤖 AI SYNC - GitHub Trigger"
echo "════════════════════════════════════════════════════════"
echo ""

cd /root/ish-dev
git add .
git commit -m "AI Sync $(date)" 2>/dev/null
git push origin main 2>/dev/null

echo "✅ AI Sync complete"
read -p "Press Enter..."
