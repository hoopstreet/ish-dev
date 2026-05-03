#!/bin/sh

cd ~/ish-dev || exit

safe_call() {
  ROLE="$1"
  INPUT="$2"

  PROMPT="You are a $ROLE in an AI OS. Be concise.\nTASK:\n$INPUT"

  RESPONSE=$(curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"openai/gpt-4o-mini\",
      \"messages\": [
        {\"role\": \"user\", \"content\": \"$PROMPT\"}
      ]
    }")

  echo "$RESPONSE" | sed -n 's/.*"content":"\([^"]*\)".*/\1/p'
}
