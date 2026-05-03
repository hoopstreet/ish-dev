mkdir -p memory

log_swarm() {
  echo "$(date): $1" >> memory/swarm.log
}

read_swarm() {
  tail -n 50 memory/swarm.log
}
