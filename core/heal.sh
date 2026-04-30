#!/bin/sh
# HEAL ENGINE - Auto-fix common bugs

clear
echo "════════════════════════════════════════════════════════"
echo "     🔧 HEAL ENGINE - AUTO REPAIR"
echo "════════════════════════════════════════════════════════"
echo ""

COUNT=0

echo "🔍 Scanning for bugs..."
echo ""

# Fix Python files - a - b → a + b
for file in /root/ish-dev/core/*.py /root/ish-dev/*.py /root/hoopstreet/*.py 2>/dev/null; do
    if [ -f "$file" ]; then
        if grep -q "a - b" "$file" 2>/dev/null; then
            sed -i 's/a - b/a + b/g' "$file"
            echo "  ✅ Fixed: $(basename "$file") (a - b → a + b)"
            COUNT=$((COUNT + 1))
        fi
    fi
done

# Fix shell scripts - add shebang if missing
for file in /root/ish-dev/core/*.sh /root/ish-dev/*.sh /root/hoopstreet/*.sh 2>/dev/null; do
    if [ -f "$file" ]; then
        if ! grep -q "^#!/bin/" "$file" 2>/dev/null; then
            sed -i '1i#!/bin/sh' "$file"
            echo "  ✅ Fixed: $(basename "$file") (added shebang)"
            COUNT=$((COUNT + 1))
        fi
    fi
done

# Fix JSON files - validate syntax
for file in /root/ish-dev/*.json 2>/dev/null; do
    if [ -f "$file" ]; then
        if ! python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
            echo "  ⚠️ Invalid JSON in: $(basename "$file")"
        fi
    fi
done

# Check DNA.md
if [ -f "/root/ish-dev/docs/DNA.md" ]; then
    if ! grep -q "^## \[v" /root/ish-dev/docs/DNA.md 2>/dev/null; then
        echo "" >> /root/ish-dev/docs/DNA.md
        echo "## [v9.2.0] - $(date +%Y-%m-%d)" >> /root/ish-dev/docs/DNA.md
        echo "### 🎯 Task" >> /root/ish-dev/docs/DNA.md
        echo "Auto-heal recovery" >> /root/ish-dev/docs/DNA.md
        echo "---" >> /root/ish-dev/docs/DNA.md
        echo "  ✅ Fixed: DNA.md structure"
        COUNT=$((COUNT + 1))
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  📊 HEAL SUMMARY"
echo "════════════════════════════════════════════════════════"
echo "  ✅ Total fixes applied: $COUNT"
echo "════════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to continue..."
