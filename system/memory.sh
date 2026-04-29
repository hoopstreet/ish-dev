#!/bin/sh
echo "=== COMMAND MEMORY ==="
tail -20 /root/ish-dev/memory/history.log 2>/dev/null
read -p "Enter..."
