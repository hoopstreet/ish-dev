#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/ui/ui.sh
. core/kernel/agents/safe_call.sh
. core/kernel/rl/memory.sh
. core/kernel/rl/score.sh
. core/kernel/tools/router.sh

echo "🤖 AI AGENT (FINAL OS MODE)"
echo "Type 'exit' to return menu"

while true; do
  echo ""
  printf "AGENT> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && break

  log "Memory lookup..."
  BEST=$(best_match "$INPUT")

  if [ -n "$BEST" ]; then
    echo "🧠 Memory:"
    echo "💡 $BEST"
    continue
  fi

  log "Thinking..."
  OUTPUT=$(safe_call coder "$INPUT")

  echo "💡 $OUTPUT"

  SCORE=$(score "$OUTPUT")
  echo "📊 Score: $SCORE"

  store_memory "$INPUT" "$OUTPUT" "$SCORE"

  # AUTO CONTROL
  echo "$INPUT" | grep -qi "sync" && run_tool sync
  echo "$INPUT" | grep -qi "heal" && run_tool heal
  echo "$INPUT" | grep -qi "status" && run_tool status
  echo "$INPUT" | grep -qi "remote" && run_tool remote

done
