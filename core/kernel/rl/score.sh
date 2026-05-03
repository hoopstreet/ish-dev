#!/bin/sh

score() {
  LEN=$(echo "$1" | wc -c)

  if [ "$LEN" -gt 120 ]; then
    echo 9
  else
    echo 6
  fi
}
