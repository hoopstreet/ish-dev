#!/bin/sh

while true; do
    cd /root/ish-dev

    git add .
    git diff --cached --quiet || git commit -m "auto sync"
    git push

    echo "[V14 WATCHER ACTIVE]"
    sleep 60
done
