#!/bin/sh

echo "===== DNA ====="
tail -n 30 docs/DNA.md 2>/dev/null

echo ""
echo "===== LOGS ====="
tail -n 30 docs/logs.txt 2>/dev/null

echo ""
echo "===== STATUS ====="
cat docs/status.json 2>/dev/null

echo ""
echo "===== PROJECT TREE ====="
find core -type f 2>/dev/null | head -20
