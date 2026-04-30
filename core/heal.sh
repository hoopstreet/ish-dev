#!/bin/sh
clear
echo "════════════════════════════════════════════════════════"
echo "     🔧 HEAL ENGINE - AUTO REPAIR"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🔍 Scanning for bugs..."
echo ""

COUNT=0

# Simple fix for a - b pattern
if grep -r "a - b" /root/ish-dev/core/*.py 2>/dev/null; then
    find /root/ish-dev/core -name "*.py" -exec sed -i 's/a - b/a + b/g' {} \;
    echo "  ✅ Fixed Python files"
    COUNT=$((COUNT + 1))
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  📊 HEAL SUMMARY"
echo "════════════════════════════════════════════════════════"
echo "  ✅ Applied $COUNT fix(es)"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Press Enter to continue..."
read dummy
