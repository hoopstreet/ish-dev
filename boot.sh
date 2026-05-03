#!/bin/sh

cd ~/ish-dev || exit

set -a
[ -f .env ] && . .env
set +a

echo "🧠 ISH AI KERNEL v3 BOOTING..."
echo "--------------------------------"
echo "Select Mode:"
echo "1) Agent (AI Dev Mode)"
echo "2) Sequential Kernel"
echo "3) Parallel DAG v2"
echo "4) SYSTEM AUTO"
echo ""

printf "MODE> "
read MODE

case "$MODE" in

  1)
    sh core/kernel/agents/run_agent.sh
    ;;

  2)
    . core/kernel/engines/dag.sh
    while true; do
      printf "KERNEL> "
      read -r INPUT
      [ "$INPUT" = "exit" ] && exit
      run_dag "$INPUT"
    done
    ;;

  3)
    sh core/kernel/parallel/run.sh
    ;;

  4)
    . core/kernel/engines/dag.sh
    while true; do
      printf "AUTO> "
      read -r INPUT
      [ "$INPUT" = "exit" ] && exit
      run_dag "$INPUT"
    done
    ;;

  *)
    echo "❌ Invalid mode (1–4 only)"
    exit 1
    ;;

esac
