#!/bin/sh
# HOOPSTREET AGENT v10.0.9 - Main Menu

while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET ISH-DEV DASHBOARD v10.0.9"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋MAIN MENU OPTIONS:"
    echo "   1. 💻 Code          - AI Multi-Phase Executor"
    echo "   2. 🔄 Sync          - Git push/pull + Backup"
    echo "   3. 🔧 Heal          - Auto-repair + Recovery"
    echo "   4. 📊 Status        - Complete system info"
    echo "   5. 🔗 Remote        - GitHub Projects Manager"
    echo "   6. 🔐 Credentials   - Token Manager"
    echo "   0. 🚪 Exit          - Back to shell"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    printf "👉 Choose (0-6): "
    read choice

    case $choice in
        1) python3 /root/ish-dev/core/smart_executor.py ;;
        2) sh /root/ish-dev/core/sync.sh ;;
        3) sh /root/ish-dev/core/heal.sh ;;
        4) sh /root/ish-dev/core/status.sh ;;
        5) sh /root/ish-dev/core/remote.sh ;;
        6) sh /root/ish-dev/core/creds.sh ;;
        0) echo "👋 Back to shell. Type 'menu' to return."; exit 0 ;;
        *) echo "❌ Invalid. Enter 0-6"; sleep 1 ;;
    esac
done
