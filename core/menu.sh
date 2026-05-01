#!/bin/sh
# 🏀 HOOPSTREET iSH-DEV | STABILIZED MASTER v10.5

while true; do
    clear
    echo "🏀 HOOPSTREET iSH AUTO HEALING AGENT v10.5"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  📋 MAIN MENU"
    echo ""
    echo "  1. 🤖 Agent       - Smart executor (Input Code Mode)"
    echo "  2. 🔄 Sync        - Git push/pull with auto-version"
    echo "  3. 🔧 Heal        - Auto-fix common bugs / DNA Restore"
    echo "  4. 📊 Status      - View DNA, roadmap, logs"
    echo "  5. 🔗 Remote      - GitHub Projects Manager"
    echo "  6. 🔐 Credentials - Secure Token Storage"
    echo "  7. 🤖 AI Sync     - Trigger GitHub Actions"
    echo "  0. 🚪 Exit        - Exit to shell"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-7): "
    read choice

    case "$choice" in
        1)
            echo "🚀 Launching AI Agent... (Type your code then END)"
            echo "---------------------------------------------------"
            # Launch the actual python logic directly to avoid launcher crashes
            python3 /root/ish-dev/core/agent.py
            echo "---------------------------------------------------"
            echo "✅ Agent Session Ended. Press Enter to return to menu..."
            read junk
            ;;
        2)
            git pull origin main
            echo "Press Enter..." && read junk ;;
        3)
            sh /root/ish-dev/core/recover_all.sh
            echo "Press Enter..." && read junk ;;
        4)
            echo "📊 DNA STATUS: $(ls /root/ish-dev/core/ | wc -l) Fragments"
            read junk ;;
        5)
            sh /root/ish-dev/core/github_setup.sh
            read junk ;;
        6)
            python3 /root/ish-dev/core/load_keys.py
            read junk ;;
        7)
            git push origin main
            echo "AI Sync Triggered. Press Enter..."
            read junk ;;
        0)
            exit 0 ;;
        *)
            sleep 1 ;;
    esac
done
