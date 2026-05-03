#!/bin/sh

echo "=== MEMORY ==="
tail -n 20 memory/memory.log 2>/dev/null

echo ""
echo "=== DNA ==="
tail -n 20 docs/DNA.md 2>/dev/null

echo ""
echo "=== STATUS ==="
cat docs/status.json 2>/dev/null

echo ""
echo "=== CORE FILES ==="
find core -type f 2>/dev/null | head -20
