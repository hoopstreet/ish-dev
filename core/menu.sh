#!/bin/sh
while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET iSH-DEV | VERSION v10.5 (STABLE)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo " 📋 MAIN MENU"
    echo ""
    echo "1. 🤖 Agent       - Master Gemini CLI v12.1"
    echo "2. 🔄 Sync        - GitHub Push/Pull"
    echo "3. 🔧 Heal        - Auto-Repair Engine"
    echo "4. 📊 Status      - DNA & System Health"
    echo "5. 🔗 Remote      - GitHub Repository"
    echo "6. 🔐 Credentials - Token Manager"
    echo "0. 🚪 Exit"
    echo ""
    read -p "👉 Choose (0-6): " c
    case $c in
        1) python3 /root/ish-dev/core/agent_ultimate_v9.py ;;
        2) sh /root/ish-dev/core/sync.sh ;;
        3) sh /root/ish-dev/core/heal.sh ;;
        4) sh /root/ish-dev/core/status.sh ;;
        5) echo "Remote: ish-dev connected." && sleep 1 ;;
        6) sh /root/ish-dev/core/creds.sh ;;
        0) exit 0 ;;
    esac
done
