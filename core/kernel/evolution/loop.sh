#!/bin/sh

cd ~/ish-dev || exit

store() {
  echo "$1 | $2 | score:$3" >> core/kernel/memory/evolution.log
}

rank() {
  sort -k3 -n core/kernel/memory/evolution.log 2>/dev/null | tail -5
}
