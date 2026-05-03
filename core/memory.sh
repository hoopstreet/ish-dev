#!/bin/sh
MEMORY_FILE="memory/ai_memory.json"
CHAT_LOG="memory/chat_history.json"

init_memory() {
    [ -f "$MEMORY_FILE" ] || echo '{"conversations":[],"knowledge":{},"stats":{"total":0}}' > "$MEMORY_FILE"
}

save_conversation() {
    USER="$1"; AI="$2"
    TMP=$(mktemp)
    jq --arg u "$USER" --arg a "$AI" --arg t "$(date)" '.conversations += [{"user":$u,"ai":$a,"time":$t}]' "$MEMORY_FILE" > "$TMP"
    mv "$TMP" "$MEMORY_FILE"
}

save_knowledge() {
    KEY="$1"; VALUE="$2"
    TMP=$(mktemp)
    jq --arg k "$KEY" --arg v "$VALUE" '.knowledge[$k]=$v' "$MEMORY_FILE" > "$TMP"
    mv "$TMP" "$MEMORY_FILE"
}

get_context() {
    jq -r '.knowledge | to_entries[] | "\(.key): \(.value)"' "$MEMORY_FILE" 2>/dev/null | head -10
}
