#!/bin/sh

cd ~/ish-dev || exit

run_tool() {
  case "$1" in
    sync) sh core/kernel/tools/git_push.sh ;;
    creds) sh core/kernel/tools/creds.sh ;;
    heal) sh core/heal.sh ;;
    status) sh core/status.sh ;;
    remote) sh core/remote.sh ;;
    *) echo "Unknown tool" ;;
  esac
}
