#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 SYNC ENGINE - Git Push/Pull with Auto-Versioning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /root/ish-dev

# Get current version (default to v10.0.8 if missing)
if [ -f docs/status.json ]; then
    CURRENT_VERSION=$(cat docs/status.json | grep version | head -1 | cut -d'"' -f4)
else
    CURRENT_VERSION="v10.0.8"
fi

# If empty, use default
if [ -z "$CURRENT_VERSION" ]; then
    CURRENT_VERSION="v10.0.8"
fi

echo "📌 Current version: $CURRENT_VERSION"

# Calculate new version
MAJOR=$(echo $CURRENT_VERSION | cut -d'.' -f1 | sed 's/v//')
MINOR=$(echo $CURRENT_VERSION | cut -d'.' -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d'.' -f3)

# Handle empty values
MAJOR=${MAJOR:-10}
MINOR=${MINOR:-0}
PATCH=${PATCH:-8}

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

# Stash local changes
echo ""
echo "📦 Stashing local changes..."
git stash push -m "pre-sync-stash" 2>/dev/null

# Pull latest with rebase
echo "📥 Pulling latest changes..."
git pull --rebase origin main
echo "✅ Pull complete"

# Pop stash
echo ""
echo "📦 Applying local changes..."
git stash pop 2>/dev/null

# Add changes
echo ""
echo "📤 Adding changes..."
git add -A
echo "✅ Files staged"

# Commit
echo ""
echo "📝 Committing changes..."
git commit -m "$NEW_VERSION: Auto-sync from iSH - $(date '+%Y-%m-%d %H:%M:%S')"
echo "✅ Commit complete"

# Create tag
echo ""
echo "🏷️ Creating tag: $NEW_VERSION"
git tag -a "$NEW_VERSION" -m "$NEW_VERSION: Auto-sync from iSH"
echo "✅ Tag created"

# Push using stored token
echo ""
echo "📤 Pushing to GitHub..."
git push https://hoopstreet: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@github.com/hoopstreet/ish-dev.git main
git push https://hoopstreet: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@github.com/hoopstreet/ish-dev.git "$NEW_VERSION"
echo "✅ Push complete"

# Update status.json
sed -i "s/\"version\": \"$CURRENT_VERSION\"/\"version\": \"$NEW_VERSION\"/" docs/status.json

# Log to DNA.md and logs.txt
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync completed: $CURRENT_VERSION → $NEW_VERSION" >> docs/logs.txt
echo "" >> docs/DNA.md
echo "## $(date '+%Y-%m-%d %H:%M:%S')" >> docs/DNA.md
echo "Sync completed: $CURRENT_VERSION → $NEW_VERSION" >> docs/DNA.md

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
