#!/bin/sh

cd ~/ish-dev || exit

run_tool() {
  TOOL="$1"
  ARG="$2"

  case "$TOOL" in

    sync)
      sh core/kernel/tools/git_push.sh "$ARG"
      ;;

    creds)
      sh core/kernel/tools/creds.sh 2>/dev/null
      ;;

    status)
      git status
      ;;

    heal)
      git pull origin main --rebase
      ;;

    *)
      echo "unknown tool"
      ;;

  esac
}
