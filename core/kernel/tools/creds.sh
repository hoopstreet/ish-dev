#!/bin/sh

cd ~/ish-dev || exit

if [ "$1" = "set" ]; then
  echo "$2" >> .env
  exit
fi

if [ "$1" = "get" ]; then
  grep "$2" .env 2>/dev/null
  exit
fi

echo "🔐 CREDENTIALS (SAFE MODE)"
grep -E "OPENROUTER|GEMINI|GITHUB" .env 2>/dev/null
