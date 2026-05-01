#!/bin/sh
while true; do
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "     🏀 HOOPSTREET iSH DEV SYSTEM v5.0"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  1. 💻 Code       - Execute multi-phase code"
    echo "  2. 📊 Status     - View system status, logs, DNA, roadmap"
    echo "  3. 🔧 Heal       - Auto-fix broken.py"
    echo "  4. 🔄 Sync       - Git push/pull with auto-version"
    echo "  5. 🗄️ Supabase   - Cloud sync (setup/sync)"
    echo "  6. 🔗 GitHub     - Connect to GitHub"
    echo "  0. 🚪 Exit       - Exit to shell"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    printf "👉 Choose (0-6): "
    read choice

    case $choice in
        1) /root/hoopstreet/code.sh ;;
        2) /root/hoopstreet/status.sh ;;
        3) clear; python3 /root/hoopstreet/heal.py; echo ""; read dummy ;;
        4) /root/hoopstreet/sync.sh ;;
        5)
            clear
            echo "1) Setup | 2) Sync"
            read s
            case $s in
                1) /root/hoopstreet/supabase.sh setup ;;
                2) /root/hoopstreet/supabase.sh sync ;;
            esac
            read dummy
            ;;
        6)
            clear
            /root/hoopstreet/github.sh
            read dummy
            ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid"; sleep 1 ;;
    esac
done
