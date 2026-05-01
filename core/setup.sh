#!/bin/sh
echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET iSH DEV SYSTEM v5.0"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Installing Hoopstreet System..."

mkdir -p /root/ish-dev/core
cp -r agent/* /root/ish-dev/core/
chmod +x /root/ish-dev/core/*.sh 2>/dev/null
chmod +x /root/ish-dev/core/*.py 2>/dev/null
ln -sf /root/ish-dev/core/menu.sh /root/menu

echo ""
echo "✅ Installation complete!"
echo ""
echo "  Type: /root/menu"
echo ""
