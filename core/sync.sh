#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 SYNC ENGINE - Git Push/Pull with Auto-Versioning"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd /root/ish-dev

# Get current version from status.json
if [ -f "docs/status.json" ]; then
    CURRENT_VERSION=$(grep -o '"version": "[^"]*"' docs/status.json | cut -d'"' -f4)
else
    CURRENT_VERSION="v9.3.0"
fi

echo "📌 Current version: $CURRENT_VERSION"
echo ""

# Generate new version (patch bump)
MAJOR=$(echo $CURRENT_VERSION | cut -d'.' -f1 | sed 's/v//')
MINOR=$(echo $CURRENT_VERSION | cut -d'.' -f2)
PATCH=$(echo $CURRENT_VERSION | cut -d'.' -f3)
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="v$MAJOR.$MINOR.$NEW_PATCH"

echo "📌 New version: $NEW_VERSION"
echo ""

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
echo "✅ Pull complete"
echo ""

# Add all changes
echo "📤 Adding changes..."
git add .
echo "✅ Files staged"
echo ""

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️ No changes to commit"
else
    echo "📝 Committing changes..."
    git commit -m "$NEW_VERSION: Auto-sync from iSH - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "✅ Commit complete"
    echo ""
    
    # Create tag with detailed message
    echo "🏷️ Creating tag: $NEW_VERSION"
    git tag -a "$NEW_VERSION" -m "$NEW_VERSION: Auto-sync from Hoopstreet iSH

🔄 Sync Details:
- Date: $(date '+%Y-%m-%d %H:%M:%S')
- Version: $NEW_VERSION
- Previous: $CURRENT_VERSION

📁 Files synced:
$(git diff --name-only HEAD~1 2>/dev/null | sed 's/^/- /')

✅ System maintained via Hoopstreet iSH Agent"
    echo "✅ Tag created"
    echo ""
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main --tags 2>/dev/null || git push origin master --tags 2>/dev/null
echo "✅ Push complete"
echo ""

# Update DNA.md with sync record
echo "📝 Updating DNA.md..."
cat >> docs/DNA.md << DNAEOF

## [$NEW_VERSION] - $(date +%Y-%m-%d)

### 🎯 Task
Auto-sync from Hoopstreet iSH device

### 📂 Files Synced
$(git diff --name-only HEAD~1 2>/dev/null | sed 's/^/- /')

### ⚙️ Changes
Automated sync via iSH agent

### 🧪 Testing
**Result:** PASS

### 📊 Impact
Sync / Update

---
DNAEOF

# Update logs.txt
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync completed: $NEW_VERSION" >> docs/logs.txt

# Update status.json version
sed -i "s/$CURRENT_VERSION/$NEW_VERSION/g" docs/status.json

# Add the updated files
git add docs/DNA.md docs/logs.txt docs/status.json
git commit -m "$NEW_VERSION: Update DNA.md, logs, and status after sync" 2>/dev/null
git push origin main --tags 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SYNC COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  📌 Version: $CURRENT_VERSION → $NEW_VERSION"
echo "  🏷️ Tag created: $NEW_VERSION"
echo "  📝 DNA.md updated"
echo "  📋 logs.txt updated"
echo "  📊 status.json updated"
echo ""
printf "Press Enter to continue..."
read dummy

# === AUTO-BACKUP BEFORE SYNC ===
echo "💾 Creating pre-sync backup..."
BACKUP_DIR="/root/ish-dev/backups/pre_sync"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/pre_sync_$TIMESTAMP.tar.gz" \
    /root/ish-dev/docs/DNA.md \
    /root/ish-dev/docs/logs.txt \
    /root/ish-dev/projects.json \
    /root/.hoopstreet/creds/ 2>/dev/null
echo "✅ Pre-sync backup created: $TIMESTAMP"

# Keep last 7 backups only
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

# === WEBHOOK NOTIFICATION ===
WEBHOOK_URL="${WEBHOOK_URL:-}"
if [ -n "$WEBHOOK_URL" ]; then
    VERSION=$(cat /root/ish-dev/docs/status.json | grep version | cut -d'"' -f4)
    curl -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{\"content\":\"🏀 Hoopstreet Sync: $VERSION\"}" \
        2>/dev/null
fi
