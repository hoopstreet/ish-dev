#!/bin/sh

echo "=== RECOVERY MODE ==="

echo "Fixing repositories..."
echo "http://apk.ish.app/v3.14-2023-05-19/main" > /etc/apk/repositories
echo "http://apk.ish.app/v3.14-2023-05-19/community" >> /etc/apk/repositories

echo "Cleaning cache..."
rm -rf /var/cache/apk/*

echo "Reinstalling core libs..."
apk add --force-broken-world libacl libattr || true

echo "Recovery complete."
read -p "Enter..."
