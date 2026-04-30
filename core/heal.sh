#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 HEAL ENGINE - AUTO REPAIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

COUNT=0

echo "🔍 Scanning for bugs..."
echo ""

# 1. Fix a - b -> a + b in Python files
echo "1. Checking for a - b bugs..."
find /root/ish-dev -name "*.py" -type f 2>/dev/null | while read file; do
    if grep -q "a - b" "$file" 2>/dev/null; then
        sed -i 's/a - b/a + b/g' "$file"
        echo "  Fixed: $(basename "$file") (a - b → a + b)"
        COUNT=$((COUNT + 1))
    fi
done

# 2. Add shebang to shell scripts
echo ""
echo "2. Checking shell scripts for shebang..."
if [ -d "/root/ish-dev/core" ]; then
    for file in /root/ish-dev/core/*.sh; do
        if [ -f "$file" ]; then
            if ! grep -q "^#!/bin/" "$file" 2>/dev/null; then
                sed -i '1i#!/bin/sh' "$file"
                echo "  Fixed: $(basename "$file") (added shebang)"
                COUNT=$((COUNT + 1))
            fi
        fi
    done
fi

# 3. Fix execute permissions
echo ""
echo "3. Checking execute permissions..."
if [ -d "/root/ish-dev/core" ]; then
    for file in /root/ish-dev/core/*.sh; do
        if [ -f "$file" ]; then
            if [ ! -x "$file" ]; then
                chmod +x "$file"
                echo "  Fixed: $(basename "$file") (added execute permission)"
                COUNT=$((COUNT + 1))
            fi
        fi
    done
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HEAL SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total fixes applied: $COUNT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
printf "Press Enter to continue..."
read dummy
