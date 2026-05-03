#!/bin/sh

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

echo "🧠 HOOPSTREET v3 DAG ENGINE STARTED"
echo "Type 'exit' to quit"

run_tool() {
  case "$1" in
    analyze) sh core/status.sh ;;
    heal) sh core/heal.sh ;;
    sync) sh core/sync.sh ;;
    remote) sh core/remote.sh ;;
    creds) sh core/creds.sh ;;
    *) echo "⚠️ Unknown tool: $1" ;;
  esac
}

while true; do
  echo ""
  printf "🧠 AI> "
  read -r PROMPT

  [ "$PROMPT" = "exit" ] && exit

  CONTEXT=$(sh core/v2/context.sh)

  RESPONSE=$(curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are a DAG execution AI.

RULE:
Return ONLY JSON.

FORMAT:
{
  \\\"actions\\\": [
    {\\\"tool\\\": \\\"analyze\\\"},
    {\\\"tool\\\": \\\"heal\\\"}
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

  CLEAN=$(echo "$RESPONSE" | sh core/v2/clean_json.sh)

  echo "📦 PLAN:"
  echo "$CLEAN"

  echo "$CLEAN" > logs/last_plan.json

  echo "$CLEAN" | grep -o '"tool"[ ]*:[ ]*"[^"]*"' | cut -d'"' -f4 | while read TOOL
  do
    echo "⚙️ EXECUTING: $TOOL"
    run_tool "$TOOL"
  done

done
