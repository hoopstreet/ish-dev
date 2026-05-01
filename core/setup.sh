#!/bin/sh
echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET iSH DEV SYSTEM v5.0"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Installing Hoopstreet System..."

mkdir -p /root/hoopstreet
cp -r agent/* /root/hoopstreet/
chmod +x /root/hoopstreet/*.sh 2>/dev/null
chmod +x /root/hoopstreet/*.py 2>/dev/null
ln -sf /root/hoopstreet/menu.sh /root/menu

echo ""
echo "✅ Installation complete!"
echo ""
echo "  Type: /root/menu"
echo ""
