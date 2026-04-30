#!/bin/sh
while true; do
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "     🏀 HOOPSTREET AGENT v9.2"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  1. 💻 Code        - Execute multi-phase code"
    echo "  2. 🔄 Sync        - Git push/pull"
    echo "  3. 🔧 Heal        - Auto-fix common bugs"
    echo "  4. 📊 Status      - Complete system status"
    echo "  5. 🔗 Remote      - GitHub Projects"
    echo "  6. 🔐 Credentials - Token Manager"
    echo "  0. 🚪 Exit"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose: "
    read choice

    case $choice in
        1) /root/ish-dev/core/code.sh ;;
        2) /root/ish-dev/core/sync.sh ;;
        3) /root/ish-dev/core/heal.sh ;;
        4) /root/ish-dev/core/status.sh ;;
        5) /root/ish-dev/core/remote.sh ;;
        6) /root/ish-dev/core/creds.sh ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid"; sleep 1 ;;
    esac
done
