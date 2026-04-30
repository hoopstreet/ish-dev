#!/bin/sh
clear
echo "════════════════════════════════════════════════════════"
echo "     🔧 HEAL ENGINE - AUTO REPAIR"
echo "════════════════════════════════════════════════════════"
echo ""
COUNT=0

for file in /root/hoopstreet/*.py /root/ish-dev/*.py 2>/dev/null; do
    if [ -f "$file" ]; then
        if grep -q "a - b" "$file" 2>/dev/null; then
            sed -i 's/a - b/a + b/g' "$file"
            echo "  Fixed: $(basename "$file")"
            COUNT=$((COUNT + 1))
        fi
    fi
done

echo ""
echo "✅ Applied $COUNT fixes"
echo ""
read -p "Press Enter to continue..."
