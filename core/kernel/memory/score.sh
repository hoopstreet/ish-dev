#!/bin/sh

cd ~/ish-dev || exit

score_output() {
  INPUT="$1"
  OUTPUT="$2"

  LEN=$(echo "$OUTPUT" | wc -c)

  # simple weighted score
  SCORE=$((LEN / 10))

  echo "$(date) | SCORE=$SCORE | INPUT=$INPUT | OUTPUT=$OUTPUT" \
  >> core/kernel/logs/score.log

  echo "$SCORE"
}
