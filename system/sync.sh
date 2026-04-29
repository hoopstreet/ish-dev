#!/bin/sh
cd /root/ish-dev

git add .
git diff --cached --quiet || git commit -m "V15 evolve $(date +%s)"
git push

echo "🔄 Evolution synced"
