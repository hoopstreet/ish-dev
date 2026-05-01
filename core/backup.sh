#!/bin/sh
# BACKUP/RESTORE UTILITY

BACKUP_DIR="/root/ish-dev/core_backups"
mkdir -p "$BACKUP_DIR"

case "$1" in
    backup)
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_FILE="$BACKUP_DIR/hoopstreet_backup_$TIMESTAMP.tar.gz"
        tar -czf "$BACKUP_FILE" /root/ish-dev/core /root/ish-dev 2>/dev/null
        echo "✅ Backup created: $BACKUP_FILE"
        ;;
    restore)
        echo "Available backups:"
        ls -la "$BACKUP_DIR"/*.tar.gz 2>/dev/null | awk '{print "  " $9}'
        printf "\nEnter backup filename to restore: "
        read backup_file
        if [ -f "$backup_file" ]; then
            tar -xzf "$backup_file" -C /
            echo "✅ Restored from: $backup_file"
        else
            echo "❌ Backup not found"
        fi
        ;;
    list)
        echo "📁 Backups:"
        ls -la "$BACKUP_DIR"/*.tar.gz 2>/dev/null | awk '{print "  " $9 " - " $5 " bytes"}'
        if [ ! "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
            echo "  (no backups found)"
        fi
        ;;
    *)
        echo "Usage: backup.sh {backup|restore|list}"
        ;;
esac
