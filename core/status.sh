#!/bin/sh
clear
echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET STATUS DASHBOARD"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📊 SYSTEM STATUS"
cat /root/ish-dev/status.json 2>/dev/null || echo '{"status":"loading"}'
echo ""
echo "📋 RECENT LOGS"
tail -10 /root/ish-dev/logs.txt 2>/dev/null || echo "No logs"
echo ""
echo "🧬 DNA EVOLUTION LOG"
head -30 /root/ish-dev/DNA.md 2>/dev/null || echo "No DNA"
echo ""
printf "Press Enter..."
read dummy
