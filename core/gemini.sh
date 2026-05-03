#!/bin/sh
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
get_api_key() {
    grep "GEMINI_API_KEY=" "$CREDS_FILE" 2>/dev/null | cut -d'=' -f2
}

ask_gemini() {
    PROMPT="$1"
    SYSTEM="$2"
    API_KEY=$(get_api_key)
    [ -z "$API_KEY" ] && echo '{"error":"No API key"}' && return 1
    
    FULL_PROMPT="${SYSTEM}\n\nUser: ${PROMPT}"
    
    curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "{\"contents\":[{\"parts\":[{\"text\":\"${FULL_PROMPT}\"}]}]}"
}
