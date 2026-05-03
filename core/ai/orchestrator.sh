#!/bin/sh

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

while true; do
  echo ""
  printf "🧠 AI> "
  read -r PROMPT

  [ "$PROMPT" = "exit" ] && exit

  CONTEXT=$(sh core/ai/context.sh)

  echo "📡 Generating plan..."

  RESPONSE=$(curl -s \
    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=$API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"contents\": [{
        \"parts\": [{
          \"text\": \"You are a system AI orchestrator.

Convert user input into JSON ONLY:

{
  \\\"actions\\\": [
    {\\\"tool\\\": \\\"analyze\\\"},
    {\\\"tool\\\": \\\"heal\\\"},
    {\\\"tool\\\": \\\"sync\\\"}
  ]
}

AVAILABLE TOOLS:
- analyze
- heal
- sync
- remote
- creds

PROJECT CONTEXT:
$CONTEXT

USER REQUEST:
$PROMPT
\"
        }]
      }]
    }")

  PLAN=$(echo "$RESPONSE" | sed -n 's/.*"text": "//p' | sed 's/".*//')

  echo "📋 PLAN:"
  echo "$PLAN"

  echo "$PLAN" | grep -q "actions" || {
    echo "❌ Invalid plan"
    continue
  }

  echo "$PLAN" | grep -o '"tool": *"[^"]*"' | cut -d'"' -f4 | while read tool; do
    echo "⚙️ Running: $tool"
    sh core/tools/registry.sh "$tool"
  done

  echo "$PROMPT | $PLAN" >> logs/ai.log

done
