#!/bin/sh

cd ~/ish-dev || exit

set -a
[ -f .env ] && . .env
set +a

safe_call() {
  ROLE="$1"
  INPUT="$2"

  PROMPT="You are a $ROLE agent in an AI kernel system.
Return ONLY ONE short sentence.

TASK:
$INPUT"

  RESPONSE=$(curl -s --max-time 20 \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"contents\":[{\"parts\":[{\"text\":\"$PROMPT\"}]}]}")

  TEXT=$(echo "$RESPONSE" | tr '\n' ' ' \
  | sed -n 's/.*"text"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

  [ -z "$TEXT" ] && TEXT="$INPUT"

  echo "$TEXT"
}
