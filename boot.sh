#!/bin/sh

cd ~/ish-dev || exit

while true; do
clear

echo "📲 HOOPSTREET ISH-DEV v13 (REAL AI OS)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 🧠 AI Agent (OpenRouter)"
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
  1) sh core/kernel/agents/run_agent.sh ;;
  2) sh core/kernel/tools/git_push.sh "manual sync" ;;
  3) sh core/heal.sh ;;
  4) sh core/status.sh ;;
  5) sh core/remote.sh ;;
  6) sh core/kernel/tools/creds.sh ;;
  0) exit ;;
  *) echo "❌ Invalid"; sleep 1 ;;
esac

done
