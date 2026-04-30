#!/bin/sh
cd /root/ish-dev

git add .
git diff --cached --quiet || git commit -m "auto sync $(date +%s)"
git push

echo "🔄 synced"
