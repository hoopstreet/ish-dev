#!/bin/sh

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

. core/engine/tools.sh
. core/engine/memory.sh
. core/engine/json.sh

echo "🧠 STABLE HOOPSTREET AI OS STARTED"
echo "Type 'exit' to quit"

while true; do
  echo ""
  printf "🧠 AI> "
  read -r PROMPT

  [ "$PROMPT" = "exit" ] && exit

  CONTEXT=$(sh core/engine/context.sh)

  RESPONSE=$(curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are an AI system controller.

Return ONLY JSON:

{
  \\\"actions\\\": [
    {\\\"tool\\\": \\\"analyze\\\"}
  ]
}

TOOLS:
analyze, heal, sync, remote, creds

USER:
$PROMPT

CONTEXT:
$CONTEXT
\"
      }]
    }]
  }")

  TEXT=$(echo "$RESPONSE" | extract_ai_text)

  if [ -z "$TEXT" ]; then
    echo "⚠️ AI returned empty response"
    continue
  fi

  echo "📦 RESPONSE:"
  echo "$TEXT"

  echo "$TEXT" >> logs/last_raw.txt

  echo "$TEXT" | grep -o '"tool"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | cut -d'"' -f4 | while read TOOL
  do
    echo "⚙️ EXECUTING: $TOOL"
    run_tool "$TOOL"
  done

  log_memory "$PROMPT"

done
