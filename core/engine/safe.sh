safe_mkdir() {
  mkdir -p "$1"
}

safe_write() {
  DIR=$(dirname "$1")
  mkdir -p "$DIR"
  cat > "$1"
}
