#!/bin/sh

cd /root/ish-dev

echo "🔄 Auto Git Recovery System"

git add .

VERSION="v$(date +%Y.%m.%d.%H%M)"

git commit -m "AUTO COMMIT $VERSION - self-healing system"
git tag -a "$VERSION" -m "Auto tag $VERSION"

git push origin main --tags

echo "✅ Git synced with version $VERSION"
