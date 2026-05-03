#!/bin/sh

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

. core/dag/memory.sh
. core/dag/executor.sh

echo "🧠 DAG ENGINE v2 STARTED"
echo "Type 'exit' to quit"

run_sequence() {
  SEQ="$1"

  for NODE in $SEQ; do
    echo "➡️ DAG NODE: $NODE"
    run_node "$NODE"
    log_dag "executed:$NODE"
  done
}

while true; do
  echo ""
  printf "🧠 AI> "
  read -r PROMPT

  [ "$PROMPT" = "exit" ] && exit

  CONTEXT=$(sh core/dag/context.sh)

  RESPONSE=$(curl -s \
  "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"You are a DAG planner AI.

Return ONLY JSON array of execution order:

{
  \\\"steps\\\": [\\\"analyze\\\", \\\"heal\\\", \\\"sync\\\"]
}

RULE:
Only use: analyze, heal, sync, remote, creds

USER:
$PROMPT

CONTEXT:
$CONTEXT
\"
      }]
    }]
  }")

  STEPS=$(echo "$RESPONSE" | sed -n 's/.*"steps":\[\([^]]*\)\].*/\1/p' \
  | tr -d '"' | tr ',' ' ')

  if [ -z "$STEPS" ]; then
    echo "⚠️ DAG fallback: analyze"
    STEPS="analyze"
  fi

  echo "📦 DAG PLAN: $STEPS"

  run_sequence "$STEPS"

done
