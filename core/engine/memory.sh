log_memory() {
  mkdir -p memory
  echo "$(date): $1" >> memory/memory.log
}

read_memory() {
  tail -n 50 memory/memory.log
}
