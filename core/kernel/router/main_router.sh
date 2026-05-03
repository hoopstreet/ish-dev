#!/bin/sh

cd ~/ish-dev || exit

run_sync() {
  sh core/kernel/tools/git_push.sh "auto sync from menu"
}

run_agent() {
  sh core/kernel/agents/run_agent.sh
}

run_heal() {
  sh core/heal.sh
}

run_status() {
  sh core/status.sh
}

run_remote() {
  sh core/remote.sh
}

run_creds() {
  sh core/kernel/tools/creds.sh
}

echo "📲 HOOPSTREET ISH-DEV v10.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 🧠 AI Agent"
echo "2. 🔄 Sync"
echo "3. 🔧 Heal"
echo "4. 📊 Status"
echo "5. 🔗 Remote"
echo "6. 🔐 Credentials"
echo "0. Exit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

while true; do
  printf "👉 Choose: "
  read MODE

  case "$MODE" in
    1) run_agent ;;
    2) run_sync ;;
    3) run_heal ;;
    4) run_status ;;
    5) run_remote ;;
    6) run_creds ;;
    0) exit ;;
    *) echo "❌ Invalid option" ;;
  esac

  echo ""
done
