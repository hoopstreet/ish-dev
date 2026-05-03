#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

run_parallel() {
  INPUT="$1"

  echo "🧠 PLANNING..."
  PLAN=$(safe_call planner "$INPUT")

  echo "💻 CODING..."
  CODE=$(safe_call coder "$PLAN")

  echo "🔍 REVIEWING..."
  REVIEW=$(safe_call reviewer "$CODE")

  echo ""
  echo "━━━━━━━━ RESULT ━━━━━━━━"
  echo "PLAN: $PLAN"
  echo "CODE: $CODE"
  echo "REVIEW: $REVIEW"
  echo "━━━━━━━━━━━━━━━━━━━━━━"
}
