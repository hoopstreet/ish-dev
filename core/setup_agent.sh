#!/bin/sh
# One-command setup to restore everything after logout

echo "🔧 Restoring iSH Auto Healing Agent..."

# Ensure all scripts exist
for script in master_enhanced.sh go_enhanced.sh status.sh heal.sh master.sh; do
    if [ ! -f "/root/$script" ]; then
        echo "⚠️ Missing: $script - please run full setup again"
    fi
done

# Ensure Python runner exists
if [ ! -f "/tmp/run_enhanced.py" ]; then
    echo "⚠️ Missing phase runner - run full setup"
fi

echo "✅ Agent ready!"
echo ""
echo "Commands:"
echo "  /root/go_enhanced.sh  - Start interactive menu"
echo "  /root/master_enhanced.sh - Paste multi-phase code directly"
echo "  /root/status.sh - Check status"
echo ""

# Optionally start the menu
if [ "$1" = "--start" ]; then
    /root/go_enhanced.sh
fi
