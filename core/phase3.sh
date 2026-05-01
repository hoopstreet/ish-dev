#!/bin/sh

# Create README.md
cat > README.md << 'READMEEOF'
# Hoopstreet iSH Dev System

A mobile development system for iSH on iOS.

## Quick Install

curl -fsSL https://raw.githubusercontent.com/hoopstreet/ish-dev/main/setup.sh | sh

## Usage

Type /root/menu to start.
READMEEOF

echo ""
echo "═══════════════════════════════════════════════════════"
echo "     SUCCESS! Pushed to ish-dev"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Repository: https://github.com/hoopstreet/ish-dev"
echo "  Local command: /root/menu"
echo ""
echo "  Install on any iSH device:"
echo "  curl -fsSL https://raw.githubusercontent.com/hoopstreet/ish-dev/main/setup.sh | sh"
echo ""
