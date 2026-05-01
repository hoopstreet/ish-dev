#!/bin/sh
while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🏀 HOOPSTREET AGENT v10.0"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. 💻 Code        - Execute + AI + Auto-test"
    echo "2. 🔄 Sync        - Git + Backup + Webhooks"
    echo "3. 🔧 Heal        - Auto-fix + Disaster Recovery"
    echo "4. 📊 Status      - Dashboard + Performance"
    echo "5. 🔗 Remote      - GitHub Projects + Docker"
    echo "6. 🔐 Credentials - Token Manager + Encryption"
    echo "0. 🚪 Exit"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-6): "
    read choice

    case "$choice" in
        1) /root/ish-dev/core/code.sh ;;
        2) /root/ish-dev/core/sync.sh ;;
        3) /root/ish-dev/core/heal.sh ;;
        4) /root/ish-dev/core/status.sh ;;
        5) /root/ish-dev/core/remote.sh ;;
        6) /root/ish-dev/core/creds.sh ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid. Enter 0-6"; sleep 1 ;;
    esac
done
