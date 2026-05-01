#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 SYNC ENGINE - Git Push/Pull with Auto-Versioning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /root/ish-dev

# Get current version
CURRENT_VERSION=$(cat docs/status.json | grep version | head -1 | cut -d'"' -f4)
echo "📌 Current version: $CURRENT_VERSION"

# Calculate new version
MAJOR=$(echo $CURRENT_VERSION | cut -d'.' -f1 | sed 's/v//')
MINOR=$(echo $CURRENT_VERSION | cut -d'.' -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d'.' -f3)
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="v$MAJOR.$MINOR.$NEW_PATCH"
echo "📌 New version: $NEW_VERSION"
echo ""

# Auto-backup before sync
echo "💾 Creating pre-sync backup..."
BACKUP_DIR="/root/ish-dev/backups/pre_sync"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/pre_sync_$TIMESTAMP.tar.gz" \
    /root/ish-dev/docs/DNA.md \
    /root/ish-dev/docs/logs.txt \
    /root/ish-dev/projects.json 2>/dev/null
echo "✅ Pre-sync backup created: $TIMESTAMP"

# Keep last 7 backups
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete 2>/dev/null

# Pull latest
echo ""
echo "📥 Pulling latest changes..."
git pull origin main --quiet
echo "✅ Pull complete"

# Add changes
echo ""
echo "📤 Adding changes..."
git add -A
echo "✅ Files staged"

# Commit
echo ""
echo "📝 Committing changes..."
git commit -m "$NEW_VERSION: Auto-sync from iSH - $(date '+%Y-%m-%d %H:%M:%S')" --quiet
echo "✅ Commit complete"

# Create tag
echo ""
echo "🏷️ Creating tag: $NEW_VERSION"
git tag -a "$NEW_VERSION" -m "$NEW_VERSION: Auto-sync from iSH" --quiet
echo "✅ Tag created"

# Push
echo ""
echo "📤 Pushing to GitHub..."
git push origin main --quiet
git push origin "$NEW_VERSION" --quiet
echo "✅ Push complete"

# Update status.json
sed -i "s/\"version\": \"$CURRENT_VERSION\"/\"version\": \"$NEW_VERSION\"/" docs/status.json

# Webhook notification (if configured)
WEBHOOK_URL="${WEBHOOK_URL:-}"
if [ -n "$WEBHOOK_URL" ]; then
    curl -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{\"content\":\"🏀 Hoopstreet Sync: $CURRENT_VERSION → $NEW_VERSION\"}" \
        2>/dev/null
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYNC COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📌 Version: $CURRENT_VERSION → $NEW_VERSION"
echo " 🏷️ Tag created: $NEW_VERSION"
echo " 💾 Backup created: $TIMESTAMP"
echo " 📝 DNA.md updated"
echo " 📋 logs.txt updated"
echo " 📊 status.json updated"
echo ""
echo "Press Enter to continue..."
read dummy
