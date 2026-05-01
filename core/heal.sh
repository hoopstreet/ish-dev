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

# === DISASTER RECOVERY ===
echo ""
echo "🛡️ Checking system health..."

# Check critical files
CRITICAL_FILES=(
    "/root/ish-dev/core/menu.sh"
    "/root/ish-dev/core/smart_executor.py"
    "/root/ish-dev/docs/status.json"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ CRITICAL: $file missing"
        # Attempt recovery from latest snapshot
        SNAPSHOT=$(ls -t /root/ish-dev/recovery/snapshot_*.tar.gz 2>/dev/null | head -1)
        if [ -n "$SNAPSHOT" ]; then
            echo "🔄 Attempting recovery from: $SNAPSHOT"
            tar -xzf "$SNAPSHOT" -C / 2>/dev/null
            echo "✅ Recovery attempted"
        fi
    fi
done

# Auto-create recovery snapshot
RECOVERY_DIR="/root/ish-dev/recovery"
mkdir -p "$RECOVERY_DIR"
SNAPSHOT="$RECOVERY_DIR/snapshot_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$SNAPSHOT" \
    /root/ish-dev/core \
    /root/ish-dev/docs \
    /root/ish-dev/config 2>/dev/null
echo "✅ Recovery snapshot created"

# Keep only last 5 snapshots
ls -t "$RECOVERY_DIR"/snapshot_*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null
