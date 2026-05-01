#!/bin/ash
echo "[WATCHDOG] Guardian active. Monitoring Agent 1..." >> master.log
while true; do
  if ! pgrep -f master_controller.py > /dev/null; then
    echo "[WATCHDOG] Agent 1 offline. Re-launching Deep Recovery..." >> master.log
    nohup python3 master_controller.py >> master.log 2>&1 &
  fi
  sleep 60
done
