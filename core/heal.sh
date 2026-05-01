#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 HEAL ENGINE - AUTO REPAIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔍 Scanning for bugs..."
echo ""

FIXES=0

# 1. Check for a - b bugs
echo "1. Checking for a - b bugs..."
find /root/ish-dev -name "*.py" -exec grep -l " - " {} \; 2>/dev/null | while read file; do
    if grep -q "[a-z] - [a-z]" "$file"; then
        sed -i 's/\([a-z]\) - \([a-z]\)/\1 + \2/g' "$file"
        echo "   ✅ Fixed: $file"
        FIXES=$((FIXES + 1))
    fi
done

# 2. Check shebang
echo ""
echo "2. Checking shell scripts for shebang..."
find /root/ish-dev/core -name "*.sh" 2>/dev/null | while read file; do
    if ! head -1 "$file" | grep -q "#!/bin"; then
        sed -i '1i#!/bin/sh' "$file"
        echo "   ✅ Fixed: $file (added shebang)"
        FIXES=$((FIXES + 1))
    fi
done

# 3. Check execute permissions
echo ""
echo "3. Checking execute permissions..."
find /root/ish-dev/core -name "*.sh" -exec chmod +x {} \; 2>/dev/null
find /root/ish-dev/agents -name "*.py" -exec chmod +x {} \; 2>/dev/null
echo "   ✅ Permissions verified"

# 4. Disaster Recovery - Check critical files
echo ""
echo "🛡️ Disaster Recovery Check..."
CRITICAL_FILES="/root/ish-dev/core/menu.sh /root/ish-dev/core/smart_executor.py /root/ish-dev/docs/status.json"
for file in $CRITICAL_FILES; do
    if [ ! -f "$file" ]; then
        echo "   ❌ CRITICAL: $(basename $file) missing"
        SNAPSHOT=$(ls -t /root/ish-dev/recovery/snapshot_*.tar.gz 2>/dev/null | head -1)
        if [ -n "$SNAPSHOT" ]; then
            echo "   🔄 Attempting recovery from: $(basename $SNAPSHOT)"
            tar -xzf "$SNAPSHOT" -C / 2>/dev/null
            echo "   ✅ Recovery attempted"
            FIXES=$((FIXES + 1))
        fi
    fi
done

# 5. Create recovery snapshot
RECOVERY_DIR="/root/ish-dev/recovery"
mkdir -p "$RECOVERY_DIR"
SNAPSHOT="$RECOVERY_DIR/snapshot_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$SNAPSHOT" /root/ish-dev/core /root/ish-dev/docs /root/ish-dev/config 2>/dev/null
echo "   ✅ Recovery snapshot created: $(basename $SNAPSHOT)"

# Keep last 5 snapshots
ls -t "$RECOVERY_DIR"/snapshot_*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 HEAL SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Total fixes applied: $FIXES"
echo "💾 Recovery snapshot: $(basename $SNAPSHOT)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Enter to continue..."
read dummy
