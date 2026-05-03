#!/bin/sh
. core/gemini.sh
. core/memory.sh

PROMPT="$1"
CONTEXT=$(get_context)

SYSTEM="You are an AI DevOps controller. Available modules: heal, sync, status, remote, credentials, code, analyze.
Return ONLY valid JSON:
{
  \"action\": \"module_name\",
  \"command\": \"specific_command\",
  \"code\": \"optional code\",
  \"response\": \"user message\",
  \"remember\": \"what to save\"
}"

RESPONSE=$(ask_gemini "$PROMPT" "$SYSTEM")
echo "$RESPONSE" | jq . 2>/dev/null || echo '{"error":"Invalid response"}'
