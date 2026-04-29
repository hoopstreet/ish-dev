#!/bin/sh
echo "SYSTEM STATUS:"
echo "=============="
echo "Alpine: $(cat /etc/alpine-release)"
echo "Python: $(python3 --version)"
echo "Git: $(git --version)"
echo ""
read -p "Enter to continue..."
