#!/bin/sh

cd ~/ish-dev || exit

git add .

MSG="$1"
[ -z "$MSG" ] && MSG="auto: AI OS update"

git commit -m "$MSG" 2>/dev/null

git pull origin main --rebase
git push origin main

echo "✅ Sync done"
