#!/bin/sh

Main installer script

mkdir -p /tmp/hoopstreet
cd /tmp/hoopstreet

Download files

curl -O https://raw.githubusercontent.com/hoopstreet/ish-dev/main/agent/master_enhanced.sh
curl -O https://raw.githubusercontent.com/hoopstreet/ish-dev/main/agent/run_enhanced.py
curl -O https://raw.githubusercontent.com/hoopstreet/ish-dev/main/agent/status.py
curl -O https://raw.githubusercontent.com/hoopstreet/ish-dev/main/agent/heal.py

Install

cp master_enhanced.sh /root/
cp run_enhanced.py /tmp/
cp status.py /root/
cp heal.py /root/

chmod +x /root/master_enhanced.sh
chmod +x /root/status.py
chmod +x /root/heal.py

Create menu

cat > /root/menu << 'MENUEOF'
#!/bin/sh
clear
echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET iSH AUTO HEALING AGENT"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  1. 📝 Code    - Paste multi-phase code"
echo "  2. 📊 Status  - Show system status"
echo "  3. 🔧 Heal    - Fix broken.py"
echo "  4. 📋 Log     - View DNA log"
echo "  5. 🚪 Exit    - Exit to shell"
echo ""
printf "👉 Choose (1-5): "
read choice
case $choice in
1) /root/master_enhanced.sh ;;
2) python3 /root/status.py; read dummy ;;
3) python3 /root/heal.py; read dummy ;;
4) cat /root/DNA.md 2>/dev/null; read dummy ;;
5) exit 0 ;;
esac
MENUEOF
chmod +x /root/menu

echo "✅ Installation complete! Type: /root/menu"
