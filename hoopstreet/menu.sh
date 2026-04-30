#!/bin/sh
while true; do
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "     🧠 HOOPSTREET AGENT v8.1 (Auto-Retry + Self-Healing)"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  1. 💻 Code        - Smart executor (3 retries + auto-heal)"
    echo "  2. 🔄 Sync        - Git push/pull"
    echo "  3. 🔧 Heal        - Auto-fix common bugs"
    echo "  4. 📊 Status      - View DNA, roadmap, logs"
    echo "  5. 🔗 Remote      - GitHub Projects"
    echo "  6. 🔐 Credentials - Token Manager"
    echo "  7. 🤖 AI Sync     - Trigger GitHub sync"
    echo "  0. 🚪 Exit"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-7): "
    read choice

    case $choice in
        1) /root/hoopstreet/code.sh ;;
        2) /root/hoopstreet/sync.sh ;;
        3) /root/hoopstreet/heal.sh ;;
        4) /root/hoopstreet/status.sh ;;
        5) /root/hoopstreet/remote.sh ;;
        6) /root/hoopstreet/creds.sh ;;
        7) /root/hoopstreet/ai_sync.sh ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid. Enter 0-7"; sleep 1 ;;
    esac
done
