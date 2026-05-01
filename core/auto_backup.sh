#!/bin/bash
# Automatic backup scheduler for iSH

BACKUP_DIR="/root/ish-dev/backups/auto"
mkdir -p "$BACKUP_DIR"

auto_backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" \
        /root/ish-dev/docs/DNA.md \
        /root/ish-dev/docs/logs.txt \
        /root/ish-dev/projects.json \
        /root/.hoopstreet/creds/ 2>/dev/null
    echo "✅ Auto-backup: $TIMESTAMP"
}

# Keep last 7 days of backups
cleanup_old() {
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
}

auto_backup
cleanup_old
