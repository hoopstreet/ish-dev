#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

PLAN_AGENT() {
  safe_call planner "$1"
}

CODE_AGENT() {
  safe_call coder "$1"
}

REVIEW_AGENT() {
  safe_call reviewer "$1"
}

VOTE() {
  echo "$1" | awk '{print length}'   # simple scoring baseline
}

run_multiagent() {
  INPUT="$1"

  echo "🧠 PLANNING..."
  PLAN=$(PLAN_AGENT "$INPUT")

  echo "📦 CODING..."
  CODE=$(CODE_AGENT "$PLAN")

  echo "🔍 REVIEWING..."
  REVIEW=$(REVIEW_AGENT "$CODE")

  SCORE_PLAN=$(VOTE "$PLAN")
  SCORE_CODE=$(VOTE "$CODE")
  SCORE_REVIEW=$(VOTE "$REVIEW")

  echo ""
  echo "━━━━━━━━ RESULTS ━━━━━━━━"
  echo "PLAN: $PLAN"
  echo "CODE: $CODE"
  echo "REVIEW: $REVIEW"
  echo ""
  echo "📊 SCORES"
  echo "PLAN=$SCORE_PLAN"
  echo "CODE=$SCORE_CODE"
  echo "REVIEW=$SCORE_REVIEW"

  BEST="$REVIEW"

  echo ""
  echo "🏆 FINAL OUTPUT"
  echo "$BEST"

  echo "$(date) | $INPUT | $BEST" >> core/kernel/logs/multiagent.log
}
