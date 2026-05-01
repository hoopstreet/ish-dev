#!/bin/sh
# COMPLETE FIX - Push clean files to ish-dev

cd /root

# Create fresh clean directory
rm -rf ish-dev-clean
mkdir -p ish-dev-clean/agent
cd ish-dev-clean

# Create setup.sh
cat > setup.sh << 'SETUPEOF'
#!/bin/sh
echo "═══════════════════════════════════════════════════════"
echo "     🏀 HOOPSTREET iSH DEV SYSTEM"
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
SETUPEOF
chmod +x setup.sh

# Create agent/menu.sh
cat > agent/menu.sh << 'MENUEOF'
#!/bin/sh
while true; do
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "     🏀 HOOPSTREET iSH DEV SYSTEM"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  1. 💻 Code       - Execute multi-phase code"
    echo "  2. 📊 Status     - Show system status"
    echo "  3. 🔧 Heal       - Fix broken.py"
    echo "  4. 🚪 Exit       - Exit to shell"
    echo ""
    printf "👉 Choose (1-4): "
    read choice
    case $choice in
        1) /root/ish-dev/core/code.sh ;;
        2) echo "System OK"; sleep 2 ;;
        3) python3 /root/ish-dev/core/heal.py 2>/dev/null; sleep 2 ;;
        4) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid choice"; sleep 1 ;;
    esac
done
MENUEOF
chmod +x agent/menu.sh

# Create agent/code.sh
cat > agent/code.sh << 'CODEEOF'
#!/bin/sh
echo ""
echo "════════════════════════════════════════════════════════"
echo "     🚀 CODE EXECUTOR"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Paste your multi-phase code (type END on new line):"
echo ""
python3 /root/ish-dev/core/run.py
CODEEOF
chmod +x agent/code.sh
