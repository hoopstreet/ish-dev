#!/bin/sh

safe_call() {
  ROLE="$1"
  INPUT="$2"

  cd ~/ish-dev || exit

  KEY_FILE=".hoopstreet/creds/credentials.txt"

  OPENROUTER_API_KEY=$(grep OPENROUTER "$KEY_FILE" 2>/dev/null | cut -d= -f2)

  if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ Missing OpenRouter API Key"
    return 1
  fi

  PROMPT="You are a $ROLE in an AI Operating System.
Return ONLY execution-ready output.

TASK:
$INPUT"

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
