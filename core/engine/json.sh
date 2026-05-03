extract_ai_text() {
  echo "$1" | sed -n 's/.*"text"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
}

clean_json() {
  echo "$1" | tr -d '\n' | sed 's/```json//g' | sed 's/```//g'
}
