#!/bin/sh

cd ~/ish-dev || exit
mkdir -p logs memory

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

# =========================
# REAL GEMINI TEXT EXTRACTOR (FIXED)
# =========================
extract_text() {
  echo "$1" \
  | tr '\n' ' ' \
  | sed -n 's/.*"text":[[:space:]]*"\([^"]*\)".*/\1/p'
}

# fallback if JSON structure changes
fallback_text() {
  echo "$1" | sed 's/.*"text"[[:space:]]*:[[:space:]]*"//;s/".*//'
}

# =========================
# CALL GEMINI (FIXED)
# =========================
call_agent() {
  ROLE="$1"
  INPUT="$2"

  curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are a $ROLE agent in a DAG system.

Return ONLY ONE short sentence.

Do NOT include JSON.

TASK:
$INPUT\"
      }]
    }]
  }"
}

# =========================
# DAG EXECUTION
# =========================
run_dag() {
  INPUT="$1"

  cd ~/ish-dev || exit

  echo "⚙️ DAG START"

  echo "🧠 PLANNER"
  PLAN_RAW=$(call_agent "planner" "$INPUT")
  PLAN=$(extract_text "$PLAN_RAW")
  [ -z "$PLAN" ] && PLAN=$(fallback_text "$PLAN_RAW")
  [ -z "$PLAN" ] && PLAN="$INPUT"
  echo "📦 PLAN: $PLAN"

  echo "💻 CODER"
  CODE_RAW=$(call_agent "coder" "$PLAN")
  CODE=$(extract_text "$CODE_RAW")
  [ -z "$CODE" ] && CODE=$(fallback_text "$CODE_RAW")
  [ -z "$CODE" ] && CODE="$PLAN"
  echo "💡 CODE: $CODE"

  echo "🧪 TESTER"
  TEST_RAW=$(call_agent "tester" "$CODE")
  TEST=$(extract_text "$TEST_RAW")
  [ -z "$TEST" ] && TEST=$(fallback_text "$TEST_RAW")
  [ -z "$TEST" ] && TEST="$CODE"
  echo "🧪 TEST: $TEST"

  echo "🧾 REVIEWER"
  REVIEW_RAW=$(call_agent "reviewer" "$TEST")
  REVIEW=$(extract_text "$REVIEW_RAW")
  [ -z "$REVIEW" ] && REVIEW=$(fallback_text "$REVIEW_RAW")
  [ -z "$REVIEW" ] && REVIEW="$TEST"
  echo "🧾 REVIEW: $REVIEW"

  echo ""
  echo "━━━━━━━━ FINAL OUTPUT ━━━━━━━━"
  echo "$REVIEW"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  echo "$(date): $INPUT => $REVIEW" >> memory/dag.log
}

