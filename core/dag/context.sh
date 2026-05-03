#!/bin/sh

echo "=== DAG MEMORY ==="
tail -n 20 memory/dag.log 2>/dev/null

echo ""
echo "=== SYSTEM STATUS ==="
cat docs/status.json 2>/dev/null

echo ""
echo "=== CORE STRUCTURE ==="
find core -type f | head -25
