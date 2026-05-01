#!/bin/sh
echo "🔄 Synchronizing with GitHub..."
cd /root/ish-dev
git add .
git commit -m "System Merge & CLI Upgrade v12.1"
git push origin main
echo "✅ Sync Complete."
sleep 1
