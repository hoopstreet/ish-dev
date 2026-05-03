extract_text() {
  echo "$1" | sed -n 's/.*"text": "\([^"]*\)".*/\1/p'
}

extract_json() {
  echo "$1" | sed -n 's/.*\({.*}\).*/\1/p'
}
