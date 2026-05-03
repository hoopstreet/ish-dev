#!/bin/sh

cd ~/ish-dev || exit

echo "🧪 SYSTEM TEST START"

. core/kernel/engines/dag.sh

run_dag "system health check"
