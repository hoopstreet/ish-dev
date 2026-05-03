#!/bin/sh
while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📲 HOOPSTREET ISH-DEV v10.1.0"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "1. 🤖 AI Agent"
    echo "2. 🔄 Sync"
    echo "3. 🔧 Heal"
    echo "4. 📊 Status"
    echo "5. 🔗 Remote"
    echo "6. 🔐 Credentials"
    echo "0. Exit"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose: "
    read c
    case $c in
        1) python3 /root/ish-dev/core/orchestrator.py ;;
        2) sh /root/ish-dev/core/sync.sh ;;
        3) sh /root/ish-dev/core/heal.sh ;;
        4) sh /root/ish-dev/core/status.sh ;;
        5) sh /root/ish-dev/core/remote.sh ;;
        6) sh /root/ish-dev/core/creds.sh ;;
        0) clear; echo "👋 Type 'menu' to return"; exit 0 ;;
    esac
done
