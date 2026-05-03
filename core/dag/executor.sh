#!/bin/sh

NODES_FILE="core/dag/nodes.json"

run_tool() {
  case "$1" in
    analyze) sh core/status.sh ;;
    heal) sh core/heal.sh ;;
    sync) sh core/sync.sh ;;
    remote) sh core/remote.sh ;;
    creds) sh core/creds.sh ;;
    *) echo "⚠️ Unknown tool: $1" ;;
  esac
}

# simple node runner
run_node() {
  NODE=$1
  echo "⚙️ Running node: $NODE"
  run_tool "$NODE"
}

