#!/bin/sh

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

. core/swarm/memory.sh
. core/swarm/parser.sh
. core/swarm/tools.sh

echo "🧠 STABLE SWARM v1 (PRODUCTION CORE)"
echo "Planner → Coder → Tester → Reviewer"
echo "Type 'exit' to quit"

call_agent() {
  ROLE="$1"
  PROMPT="$2"

  curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are a $ROLE agent.
Return ONE short sentence only.
No JSON.
No formatting.

TASK:
$PROMPT\"
      }]
    }]
  }"
}

while true; do
  echo ""
  printf "🧠 SWARM> "
  read -r INPUT

  [ "$INPUT" = "exit" ] && exit

  echo "🧠 PLANNER..."
  PLAN_RAW=$(call_agent "planner" "$INPUT")
  PLAN=$(fallback_text "$PLAN_RAW")

  [ -z "$PLAN" ] && PLAN="$INPUT"

  echo "📦 PLAN: $PLAN"

  echo "💻 CODER..."
  CODE_RAW=$(call_agent "coder" "$PLAN")
  CODE=$(fallback_text "$CODE_RAW")

  echo "🧪 TESTER..."
  TEST_RAW=$(call_agent "tester" "$CODE")
  TEST=$(fallback_text "$TEST_RAW")

  echo "🧾 REVIEWER..."
  REVIEW_RAW=$(call_agent "reviewer" "$TEST")
  REVIEW=$(fallback_text "$REVIEW_RAW")

  echo ""
  echo "━━━━━━━━ RESULT ━━━━━━━━"
  echo "$REVIEW"
  echo "━━━━━━━━━━━━━━━━━━━━━━"

  log_swarm "$INPUT"
done
