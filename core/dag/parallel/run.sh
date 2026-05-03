#!/bin/sh

cd ~/ish-dev || exit
. core/dag/parallel/engine.sh

echo "🧠 PARALLEL DAG ENGINE v1"
echo "TRUE CONCURRENT EXECUTION"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "⚡ PARALLEL> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  run_parallel_dag "$INPUT"
done
