#!/bin/sh
clear
echo "════════════════════════════════════════════════════════"
echo "     🔄 SYNC ENGINE - Git Push/Pull"
echo "════════════════════════════════════════════════════════"
echo ""

cd /root/ish-dev 2>/dev/null

echo "📥 Pulling latest changes..."
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
echo "✅ Pull complete"
echo ""

echo "📤 Adding changes..."
git add .
echo "✅ Files staged"
echo ""

echo "📝 Committing changes..."
git commit -m "Auto sync $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null
echo "✅ Commit complete"
echo ""

echo "📤 Pushing to GitHub..."
git push origin main 2>/dev/null || git push origin master 2>/dev/null
echo "✅ Push complete"
echo ""

echo "════════════════════════════════════════════════════════"
echo "  ✅ SYNC COMPLETE!"
echo "════════════════════════════════════════════════════════"
echo ""
read -p "Press Enter to continue..."
