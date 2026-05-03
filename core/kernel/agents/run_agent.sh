#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/dag/v2/engine.sh
. core/kernel/autogit/coder.sh
. core/kernel/evolution/loop.sh

echo "🧠 MULTI-AGENT OS v12"
echo "Type exit to quit"

while true; do
  printf "AGENT> "
  read INPUT

  [ "$INPUT" = "exit" ] && exit

  # SYSTEM COMMANDS
  echo "$INPUT" | grep -qi "sync" && sh core/kernel/tools/git_push.sh "agent sync"
  echo "$INPUT" | grep -qi "heal" && sh core/heal.sh
  echo "$INPUT" | grep -qi "trash" && sh core/kernel/brain.sh

  # DAG EXECUTION
  run_parallel "$INPUT"

done
