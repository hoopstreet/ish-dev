#!/bin/sh

call_agent() {
  ROLE="$1"
  INPUT="$2"

  sh core/swarm/orchestrator.sh <<EOF_INPUT
$INPUT
exit
EOF_INPUT
}

run_parallel() {
  INPUT="$1"

  echo "⚡ PARALLEL EXECUTION START"

  PLAN=$(call_agent planner "$INPUT") &
  CODE=$(call_agent coder "$INPUT") &
  TEST=$(call_agent tester "$INPUT") &

  wait

  echo ""
  echo "📦 MERGING RESULTS"
  echo "PLAN: $PLAN"
  echo "CODE: $CODE"
  echo "TEST: $TEST"
}

