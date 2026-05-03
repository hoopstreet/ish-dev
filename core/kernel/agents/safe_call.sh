#!/bin/sh

cd ~/ish-dev || exit

safe_call() {
  echo "$2"  # fallback if API fails
}
