#!/bin/bash
# Disaster recovery system

RECOVERY_DIR="/root/ish-dev/recovery"
mkdir -p "$RECOVERY_DIR"

snapshot() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tar -czf "$RECOVERY_DIR/snapshot_$TIMESTAMP.tar.gz" \
        /root/ish-dev/core \
        /root/ish-dev/docs \
        /root/ish-dev/config \
        /root/ish-dev/*.json 2>/dev/null
    echo "✅ Snapshot created: $TIMESTAMP"
}

restore() {
    SNAPSHOT="$1"
    if [ -f "$SNAPSHOT" ]; then
        tar -xzf "$SNAPSHOT" -C /
        echo "✅ System restored from: $SNAPSHOT"
    else
        echo "❌ Snapshot not found"
    fi
}

# Auto-snapshot before major changes
pre_update_snapshot() {
    snapshot
    echo "✅ Pre-update snapshot created"
}

case "$1" in
    snapshot) snapshot ;;
    restore) restore "$2" ;;
    pre-update) pre_update_snapshot ;;
    *) echo "Usage: $0 {snapshot|restore <file>|pre-update}" ;;
esac
