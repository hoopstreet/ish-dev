#!/bin/sh

cd ~/ish-dev || exit
. core/dag/engine/resolve.sh

echo "🧠 DAG ENGINE v3.1 (STABLE + FIXED PARSER)"
echo "Planner → Coder → Tester → Reviewer"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "⚡ DAG> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  run_dag "$INPUT"
done
