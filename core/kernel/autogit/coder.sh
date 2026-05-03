#!/bin/sh

cd ~/ish-dev || exit

. core/kernel/agents/safe_call.sh

AUTO_EDIT() {
  FILE="$1"
  TASK="$2"

  [ -f "$FILE" ] || return

  CONTENT=$(cat "$FILE")

  PATCH=$(safe_call coder "Improve this code safely:\n$CONTENT\nTASK:$TASK")

  echo "$PATCH" > "$FILE"

  git add "$FILE"
  git commit -m "auto patch: $TASK" 2>/dev/null
}

AUTO_EDIT_ALL() {
  find core -type f -name "*.sh" | while read f; do
    AUTO_EDIT "$f" "optimize script safely"
  done
}
