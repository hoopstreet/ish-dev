#!/bin/sh

cd ~/ish-dev || exit

MEM="core/kernel/memory/store.log"

store_memory() {
  echo "$1 | $2 | $3" >> "$MEM"
}

best_match() {
  grep "$1" "$MEM" 2>/dev/null | tail -1 | cut -d'|' -f2
}
