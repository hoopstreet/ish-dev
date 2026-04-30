#!/bin/sh
cd /tmp/project 2>/dev/null || { echo "No project loaded."; exit 1; }
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
git add .
VERSION="v1.0.$(date +%s)"
git commit -m "$VERSION auto-sync" 2>/dev/null
git tag -a "$VERSION" -m "auto" 2>/dev/null
git push origin main --tags 2>/dev/null || git push origin master --tags 2>/dev/null
echo "SYNC COMPLETE: $VERSION"
read dummy
