#!/bin/sh

extract_json_text() {
  echo "$1" | sed -n 's/.*"text"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
}

fallback_text() {
  echo "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}
