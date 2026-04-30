#!/bin/sh

cd ~/ish-dev || exit 1

# load env
if [ -f /root/.hoopstreet/creds/.env ]; then
    export GEMINI_KEYS=$(grep GEMINI_KEYS /root/.hoopstreet/creds/.env | cut -d= -f2 | tr -d '"')
    export OPENROUTER_KEYS=$(grep OPENROUTER_KEYS /root/.hoopstreet/creds/.env | cut -d= -f2 | tr -d '"')
fi

echo "✅ HOOPSTREET READY"
