#!/bin/sh
cd /root/Ai-Coder
git init
git config --global user.email "hoopstreet143@gmail.com"
git config --global user.name "hoopstreet"
git add .
git commit -m "Build: Stable Commander (Hoopstreet Edition)"
git branch -M main
git remote remove origin 2>/dev/null
git remote add origin https://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@github.com/hoopstreet/Ai-Coder.git
git push -u origin main --force
