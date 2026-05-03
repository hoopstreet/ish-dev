#!/bin/sh

spinner() {
  while :; do
    for s in / - \\ \|; do
      printf "\r$s"
      sleep 0.1
    done
  done
}

log() {
  echo "⚡ $1"
}
