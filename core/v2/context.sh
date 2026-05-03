#!/bin/sh

echo "=== DNA ==="
tail -n 30 docs/DNA.md 2>/dev/null

echo ""
echo "=== LOGS ==="
tail -n 30 docs/logs.txt 2>/dev/null

echo ""
echo "=== STATUS ==="
cat docs/status.json 2>/dev/null

echo ""
echo "=== FILE MAP ==="
find core -type f | head -30
