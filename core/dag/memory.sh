mkdir -p memory

log_dag() {
  echo "$(date): $1" >> memory/dag.log
}

read_dag() {
  tail -n 50 memory/dag.log
}
