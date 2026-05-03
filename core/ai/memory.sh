#!/bin/sh

FILE="memory/ai_memory.json"

mkdir -p memory

if [ ! -f "$FILE" ]; then
  echo "{}" > "$FILE"
fi

KEY=$(date +%s)

echo "{
  \"$KEY\": {
    \"input\": \"$1\",
    \"time\": \"$(date)\"
  }
}" >> "$FILE"
