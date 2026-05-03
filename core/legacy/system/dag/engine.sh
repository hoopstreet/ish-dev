#!/bin/sh

cd ~/ish-dev || exit

set -a
[ -f .env ] && . .env
set +a

. core/system/agents/agent.sh

run_dag() {
  INPUT="$1"

  echo "⚙️ SYSTEM DAG START"

  PLAN=$(extract_text "$(call_agent planner "$INPUT")")
  [ -z "$PLAN" ] && PLAN="$INPUT"
  echo "📦 PLAN: $PLAN"

  CODE=$(extract_text "$(call_agent coder "$PLAN")")
  [ -z "$CODE" ] && CODE="$PLAN"
  echo "💻 CODE: $CODE"

  TEST=$(extract_text "$(call_agent tester "$CODE")")
  [ -z "$TEST" ] && TEST="$CODE"
  echo "🧪 TEST: $TEST"

  REVIEW=$(extract_text "$(call_agent reviewer "$TEST")")
  [ -z "$REVIEW" ] && REVIEW="$TEST"
  echo "🧾 REVIEW: $REVIEW"

  echo ""
  echo "━━━━━━━━ FINAL OUTPUT ━━━━━━━━"
  echo "$REVIEW"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  mkdir -p memory
  echo "$(date): $INPUT => $REVIEW" >> memory/dag.log
}
