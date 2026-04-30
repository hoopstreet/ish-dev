#!/bin/sh
# HOOPSTREET AGENT v9.0 - Unified Menu

while true; do
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "     🏀 HOOPSTREET iSH AUTO HEALING AGENT v9.0"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  📋 MAIN MENU"
    echo ""
    echo "  1. 💻 Code        - Smart executor (3 retries + auto-heal)"
    echo "  2. 🔄 Sync        - Git push/pull with auto-version"
    echo "  3. 🔧 Heal        - Auto-fix common bugs"
    echo "  4. 📊 Status      - View DNA, roadmap, logs"
    echo "  5. 🔗 Remote      - GitHub Projects Manager"
    echo "  6. 🔐 Credentials - Secure Token Storage"
    echo "  7. 🤖 AI Sync     - Trigger GitHub Actions"
    echo "  8. 💾 Backup      - Backup/Restore system"
    echo "  9. 📊 Monitor     - System health check"
  S. 🗄️ Supabase - Real-time cloud sync (auto on push)
    echo "  0. 🚪 Exit        - Exit to shell"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-9, S, SC, PC): "
    read choice

    case $choice in
        1) /root/ish-dev/core/code.sh ;;
        2) /root/ish-dev/core/sync.sh ;;
        3) /root/ish-dev/core/heal.sh ;;
        4) /root/ish-dev/core/status.sh ;;
        5) /root/ish-dev/core/remote.sh ;;
        6) /root/ish-dev/core/creds.sh ;;
        7) /root/ish-dev/core/ai_sync.sh ;;
        8) /root/ish-dev/core/backup.sh ;;
        9) /root/ish-dev/core/monitor.sh ;;
        S|s) /root/ish-dev/core/supabase_sync.sh status ;;
        SC|sc) /root/ish-dev/core/supabase_sync.sh sync-all ;;
        PC|pc) /root/ish-dev/core/supabase_sync.sh pull-all ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid. Enter 0-9"; sleep 1 ;;
    esac
done
