#!/bin/sh

. core/kernel/config.sh

call_agent() {
  ROLE="$1"
  INPUT="$2"

  curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are $ROLE in an AI kernel system. Return ONE precise sentence only.

TASK:
$INPUT\"
      }]
    }]
  }"
}

extract_text() {
  echo "$1" | tr '\n' ' ' | sed -n 's/.*\"text\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p'
}
