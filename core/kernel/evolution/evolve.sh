#!/bin/sh

cd ~/ish-dev || exit

evolve_prompt() {

  BEST=$(sort -t= -k2 -nr core/kernel/logs/score.log 2>/dev/null | head -n 1)

  echo "$BEST" > core/kernel/evolution/best.txt

}
