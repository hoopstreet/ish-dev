#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

run_dag() {
  INPUT="$1"

  echo "⚙️ KERNEL DAG START"

  PLAN=$(safe_call planner "$INPUT")
  echo "📦 PLAN: $PLAN"

  CODE=$(safe_call coder "$PLAN")
  echo "💻 CODE: $CODE"

  TEST=$(safe_call tester "$CODE")
  echo "🧪 TEST: $TEST"

  REVIEW=$(safe_call reviewer "$TEST")
  echo "🧾 REVIEW: $REVIEW"

  echo ""
  echo "━━━━━━━━ FINAL OUTPUT ━━━━━━━━"
  echo "$REVIEW"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  mkdir -p core/kernel/logs

  echo "$(date) | INPUT=$INPUT | OUTPUT=$(echo "$REVIEW" | tr '\n' ' ')" \
  >> core/kernel/logs/dag.log
}
