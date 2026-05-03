#!/bin/sh

cd ~/ish-dev || exit

git add .

MSG="$1"
[ -z "$MSG" ] && MSG="auto sync"

git commit -m "$MSG" 2>/dev/null

git pull origin main --rebase
git push origin main
