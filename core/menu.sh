#!/bin/sh

while true; do
    printf "\033[2J\033[H"
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET ISH-DEV DASHBOARD v10.0.8"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 MAIN MENU OPTIONS:"
    echo "   1. 🤖 Agent          - AI Assistant"
    echo "   2. 🔄 Sync           - Git push/pull"
    echo "   3. 🔧 Heal           - Auto-repair"
    echo "   4. 📊 Status         - System info"
    echo "   5. 🔗 Remote         - GitHub Projects"
    echo "   6. 🔐 Credentials    - Token Manager"
    echo "   0. 🚪 Exit           - Back to shell"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-6): "
    read choice

    case "$choice" in
        1) clear; python3 /root/ish-dev/core/agent_self_improving.py ;;
        2) clear; /root/ish-dev/core/sync.sh ;;
        3) clear; /root/ish-dev/core/heal.sh ;;
        4) clear; /root/ish-dev/core/status.sh ;;
        5) clear; /root/ish-dev/core/remote.sh ;;
        6) clear; /root/ish-dev/core/creds.sh ;;
        0) 
            echo ""
            echo "👋 Back to shell. Type 'menu' to return."
            echo "localhost:~#"
            exit 0
            ;;
        *) 
            echo "❌ Invalid. Enter 0-6"
            sleep 1
            ;;
    esac
done
