#!/bin/sh

cd ~/ish-dev || exit

while true; do
  clear

  echo "📲 HOOPSTREET ISH-DEV v7.2"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "1. 🧠 AI Agent"
  echo "2. 🔄 Sync (Git Push)"
  echo "3. 🔧 Heal"
  echo "4. 📊 Status"
  echo "5. 🔗 Remote"
  echo "6. 🔐 Credentials"
  echo "0. Exit"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  printf "👉 Choose: "

  read -r CHOICE

  case "$CHOICE" in

    1)
      sh core/kernel/agents/run_agent.sh
      ;;

    2)
      sh core/kernel/tools/git_push.sh "manual sync"
      read -p "Press Enter..."
      ;;

    3)
      echo "🔧 Running heal..."
      git pull origin main --rebase
      echo "✅ Healed"
      read -p "Press Enter..."
      ;;

    4)
      echo "📊 STATUS"
      git status
      echo ""
      tail -n 5 core/kernel/logs/dag.log 2>/dev/null
      read -p "Press Enter..."
      ;;

    5)
      git remote -v
      read -p "Press Enter..."
      ;;

    6)
      echo "🔐 ENV CHECK"
      env | grep KEY
      read -p "Press Enter..."
      ;;

    0)
      exit
      ;;

    *)
      echo "❌ Invalid option"
      sleep 1
      ;;

  esac

done
