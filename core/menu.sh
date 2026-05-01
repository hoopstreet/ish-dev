#!/bin/sh
while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET iSH-DEV | VERSION v10.5 (STABLE)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo " 📋 MAIN MENU"
    echo ""
    echo "1. 🤖 Agent       - Self-Improving AI Agent"
    echo "2. 🔄 Sync        - GitHub Push/Pull"
    echo "3. 🔧 Heal        - Auto-Repair Engine"
    echo "4. 📊 Status      - DNA & System Health"
    echo "5. 🔗 Remote      - TikTok Niche Configs"
    echo "6. 🔐 Credentials - Token Manager"
    echo "0. 🚪 Exit"
    echo ""
    printf "👉 Choose (0-6): "
    read choice
    case "$choice" in
        1) python3 /root/ish-dev/core/agent_ultimate_v9.py ;;
        2) sh /root/ish-dev/core/sync.sh ;;
        3) sh /root/ish-dev/core/heal.sh ;;
        4) sh /root/ish-dev/core/status.sh ;;
        5) ls /root/ish-dev/workspace/tiktok_niches/configs ;;
        6) ls -la /root/.hoopstreet/creds/ ;;
        0) break ;;
        *) echo "❌ Invalid selection"; sleep 1 ;;
    esac
done
