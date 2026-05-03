#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh
. core/kernel/tools/git_push.sh

echo "🤖 AGENT MODE (AUTO DEV + GIT)"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "AGENT> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  OUTPUT=$(safe_call coder "$INPUT")

  echo "💡 $OUTPUT"

  mkdir -p core/kernel/memory
  echo "$(date) | $INPUT => $OUTPUT" >> core/kernel/memory/agent.log

  sh core/kernel/tools/git_push.sh "agent: $INPUT"
done
