#!/bin/sh

cd ~/ish-dev || exit

safe_call() {
  ROLE="$1"
  INPUT="$2"

  # Fallback (safe mode)
  echo "$INPUT"
}
