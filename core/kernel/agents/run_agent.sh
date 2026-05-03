#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh
. core/kernel/tools/router.sh

echo "🤖 AGENT MODE (AUTONOMOUS OS)"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "AGENT> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  # STEP 1: THINK
  PLAN=$(safe_call planner "$INPUT")

  # STEP 2: ACT
  ACTION=$(safe_call reviewer "Decide action: sync, creds, or none for: $PLAN")

  # STEP 3: EXECUTE TOOL IF NEEDED
  if echo "$ACTION" | grep -qi "sync"; then
    echo "🔄 AUTO SYNC TRIGGERED"
    run_tool sync "$INPUT"
  fi

  if echo "$ACTION" | grep -qi "creds"; then
    echo "🔐 ACCESSING CREDENTIALS"
    CREDS=$(run_tool creds)
  fi

  # STEP 4: GENERATE OUTPUT
  OUTPUT=$(safe_call coder "$PLAN $CREDS")

  echo "💡 $OUTPUT"

  mkdir -p core/kernel/memory
  echo "$(date) | $INPUT => $OUTPUT" >> core/kernel/memory/agent.log

done
