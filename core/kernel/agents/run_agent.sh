#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

echo "🧠 ISH-DEV AI AGENT (OPENROUTER CORE)"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "AGENT> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  # 🧠 THINK (PLAN)
  PLAN=$(safe_call planner "$INPUT")

  # ⚙️ DECIDE ACTION
  ACTION=$(safe_call coder "Return ONLY one word: sync, heal, creds, status, none. Task: $PLAN")

  case "$ACTION" in
    *sync*)
      echo "🔄 SYNC TRIGGERED"
      sh core/kernel/tools/git_push.sh "auto: $INPUT"
      ;;

    *heal*)
      echo "🔧 RUNNING HEAL"
      sh core/heal.sh
      ;;

    *creds*)
      echo "🔐 OPEN CREDENTIALS"
      sh core/kernel/tools/creds.sh
      ;;

    *status*)
      sh core/status.sh
      ;;
  esac

  # 🧠 FINAL OUTPUT ONLY
  OUTPUT=$(safe_call coder "$PLAN")

  echo "💡 $OUTPUT"
done
