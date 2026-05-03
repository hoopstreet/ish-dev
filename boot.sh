#!/bin/sh

cd ~/ish-dev || exit

while true; do

echo ""
echo "📲 HOOPSTREET ISH-DEV FINAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 🧠 AI Agent"
echo "2. 🔄 Sync"
echo "3. 🔧 Heal"
echo "4. 📊 Status"
echo "5. 🔗 Remote"
echo "6. 🔐 Credentials"
echo "0. Exit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

printf "👉 Choose: "
read MODE

case "$MODE" in

  1)
    sh core/kernel/agents/run_agent.sh
    ;;

  2)
    sh core/kernel/tools/git_push.sh "manual sync"
    ;;

  3)
    sh core/heal.sh 2>/dev/null || echo "No heal yet"
    ;;

  4)
    echo "📊 Logs:"
    tail -n 10 core/kernel/memory/store.log 2>/dev/null
    ;;

  5)
    git remote -v
    ;;

  6)
    sh core/kernel/tools/creds.sh
    ;;

  0)
    exit
    ;;

  *)
    echo "❌ Invalid"
    ;;

esac

done
