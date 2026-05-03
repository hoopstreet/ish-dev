#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

run_parallel_dag() {
  INPUT="$1"

  echo "⚡ PARALLEL DAG v2 START"

  RUN_ID=$(date +%s)
  WORKDIR="core/kernel/runtime/$RUN_ID"
  mkdir -p "$WORKDIR"

  PLAN_FILE="$WORKDIR/plan.txt"
  CODE_FILE="$WORKDIR/code.txt"
  TEST_FILE="$WORKDIR/test.txt"

  # PARALLEL EXECUTION

  (
    PLAN=$(safe_call planner "$INPUT")
    echo "$PLAN" > "$PLAN_FILE"
  ) &

  (
    CODE=$(safe_call coder "$INPUT")
    echo "$CODE" > "$CODE_FILE"
  ) &

  (
    TEST=$(safe_call tester "$INPUT")
    echo "$TEST" > "$TEST_FILE"
  ) &

  wait

  PLAN=$(cat "$PLAN_FILE")
  CODE=$(cat "$CODE_FILE")
  TEST=$(cat "$TEST_FILE")

  echo ""
  echo "📦 PLAN: $PLAN"
  echo "💻 CODE: $CODE"
  echo "🧪 TEST: $TEST"

  FINAL=$(safe_call reviewer "$PLAN | $CODE | $TEST")

  echo ""
  echo "━━━━━━━━ FINAL OUTPUT ━━━━━━━━"
  echo "$FINAL"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  mkdir -p core/kernel/logs

  echo "$(date) | INPUT=$INPUT | OUTPUT=$(echo "$FINAL" | tr '\n' ' ')" \
  >> core/kernel/logs/parallel.log
}
