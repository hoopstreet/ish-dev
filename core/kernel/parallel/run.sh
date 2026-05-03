#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/parallel/engine.sh

echo "🧠 PARALLEL DAG ENGINE v2"
echo "TRUE CONCURRENCY + MERGE"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "PARALLEL> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  run_parallel_dag "$INPUT"
done
