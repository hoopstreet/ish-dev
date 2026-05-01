#!/bin/sh
echo "📊 SYSTEM HEALTH & DNA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "VERSION: v10.5 Stable / CLI v12.1"
echo "DISK: $(df -h / | tail -1 | awk '{print $4}') available"
echo "DNA LOGS: $(wc -l < /root/ish-dev/docs/DNA.md) entries"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "Press Enter..." pause
