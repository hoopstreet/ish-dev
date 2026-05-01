#!/bin/sh
# HOOPSTREET AGENT LAUNCHER - Unified Entry Point

echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET iSH AUTO HEALING AGENT v8.2"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Loading system..."

# Check if running in iSH
if [ ! -f /etc/alpine-release ]; then
    echo "⚠️ Warning: Not running in iSH environment"
fi

# Launch menu
exec /root/ish-dev/core/menu.sh
