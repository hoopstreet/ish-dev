#!/bin/sh

echo "=== MEMORY ==="
tail -n 20 memory/swarm.log 2>/dev/null

echo ""
echo "=== SYSTEM STATUS ==="
cat docs/status.json 2>/dev/null

echo ""
echo "=== FILE STRUCTURE ==="
find core -type f 2>/dev/null | head -30
