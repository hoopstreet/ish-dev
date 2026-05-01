#!/bin/sh

echo "=== OFFLINE MODE ==="

echo "Saving installed packages list..."
apk info -vv > /root/ish-dev/packages.txt

echo "Saving repo config..."
cp /etc/apk/repositories /root/ish-dev/repositories.bak

echo "Offline snapshot saved."
read -p "Enter..."
