#!/bin/sh

cd ~/ish-dev || exit

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

extract_text() {
  echo "$1" | tr '\n' ' ' | sed -n 's/.*"text"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
}

call_agent() {
  ROLE="$1"
  INPUT="$2"

  curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are a $ROLE agent. Return ONE short sentence only.

TASK:
$INPUT\"
      }]
    }]
  }"
}

run_parallel_dag() {
  INPUT="$1"

  echo "⚡ PARALLEL DAG START"

  # ------------------------
  PLAN_FILE=/tmp/plan.txt
  CODE_FILE=/tmp/code.txt
  TEST_FILE=/tmp/test.txt

  # PLANNER
  (
    PLAN=$(extract_text "$(call_agent planner "$INPUT")")
    [ -z "$PLAN" ] && PLAN="$INPUT"
    echo "$PLAN" > "$PLAN_FILE"
  ) &

  # CODER
  (
    CODE=$(extract_text "$(call_agent coder "$INPUT")")
    [ -z "$CODE" ] && CODE="$INPUT"
    echo "$CODE" > "$CODE_FILE"
  ) &

  # TESTER
  (
    TEST=$(extract_text "$(call_agent tester "$INPUT")")
    [ -z "$TEST" ] && TEST="$INPUT"
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

  # MERGE STAGE
  FINAL=$(extract_text "$(call_agent reviewer "$PLAN | $CODE | $TEST")")

  echo ""
  echo "━━━━━━━━ FINAL OUTPUT ━━━━━━━━"
  echo "$FINAL"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  echo "$(date): $INPUT => $FINAL" >> memory/parallel_dag.log
}

