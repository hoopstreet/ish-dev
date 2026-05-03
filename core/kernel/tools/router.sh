#!/bin/sh

cd ~/ish-dev || exit

run_tool() {
  TOOL="$1"

  case "$TOOL" in
    sync)
      sh core/kernel/tools/git_push.sh "auto sync"
      ;;
    creds)
      sh core/kernel/tools/creds.sh
      ;;
    status)
      sh core/status.sh 2>/dev/null || echo "No status yet"
      ;;
    heal)
      sh core/heal.sh 2>/dev/null || echo "No heal script"
      ;;
    *)
      echo "No tool"
      ;;
  esac
}
