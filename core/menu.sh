#!/bin/sh
while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET ISH-DEV IPHONE 🤳 v10.0.6"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo " 📋 MAIN MENU"
    echo ""
    echo "1. 🤖 Agent       - AI Agent (Natural Language + Code)"
    echo "2. 🔄 Sync          - Git push/pull + Backup"
    echo "3. 🔧 Heal           - Auto-fix + Recovery"
    echo "4. 📊 Status        - Complete system + Metrics"
    echo "5. 🔗 Remote      - GitHub Projects + Docker"
    echo "6. 🔐 Credentials - Token Manager + Encryption"
    echo "0. 🚪 Exit             - Back to localhost:~#"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-6): "
    read choice

    case "$choice" in
        1) 
            clear
            python3 /root/ish-dev/core/agent_self_improving.py
            ;;
        2) 
            /root/ish-dev/core/sync.sh
            ;;
        3) 
            /root/ish-dev/core/heal.sh
            ;;
        4) 
            /root/ish-dev/core/status.sh
            ;;
        5) 
            /root/ish-dev/core/remote.sh
            ;;
        6) 
            /root/ish-dev/core/creds.sh
            ;;
        0) 
            echo ""
            echo "👋 Goodbye!"
            echo "localhost:~#"
            exit 0
            ;;
        *) 
            echo "❌ Invalid. Enter 0-6"
            sleep 1
            ;;
    esac
done
