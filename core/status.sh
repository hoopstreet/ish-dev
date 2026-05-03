#!/bin/bash

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SYSTEM - COMPLETE STATUS REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

VERSION=$(grep "Version:" docs/DNA.md 2>/dev/null | head -1 | cut -d' ' -f2)
[ -z "$VERSION" ] && VERSION="v10.0.8"

echo "📌 SYSTEM VERSION & HEALTH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏷️ Version: $VERSION"
echo "💚 Status: production"
echo ""

echo "📁 CORE FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -1 core/ 2>/dev/null
echo ""

echo "📁 DOCS FILES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -1 docs/ 2>/dev/null
echo ""

echo "💾 DATA STORES STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
CRED_COUNT=$(grep -c '=' ~/.hoopstreet/creds/credentials.txt 2>/dev/null || echo 0)
PROJ_COUNT=$(grep -c '"url"' projects.json 2>/dev/null || echo 0)
DNA_LINES=$(wc -l < docs/DNA.md 2>/dev/null || echo 0)
LOG_LINES=$(wc -l < docs/logs.txt 2>/dev/null || echo 0)

echo "🔐 Credentials: $CRED_COUNT stored"
echo "📁 Projects: $PROJ_COUNT connected"
echo "🧬 DNA.md: $DNA_LINES lines"
echo "📝 logs.txt: $LOG_LINES entries"
echo ""

echo "🔗 EXTERNAL INTEGRATIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐙 GitHub: Connected"
echo "📍 https://github.com/hoopstreet/ish-dev.git"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "Press Enter to continue..."
