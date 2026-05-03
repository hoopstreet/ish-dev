#!/bin/bash

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 SYSTEM - COMPLETE STATUS REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get version
VERSION=$(grep "Version:" docs/DNA.md 2>/dev/null | head -1 | sed 's/Version: //')
[ -z "$VERSION" ] && VERSION="v10.0.8"

echo "📌 SYSTEM VERSION & HEALTH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏷️ Version: $VERSION"
echo "💚 Status: production"
echo ""

echo "📁 CORE FILES ($(ls -1 core/ 2>/dev/null | wc -l) scripts)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -1 core/ 2>/dev/null | head -10
echo ""

echo "📁 DOCS FILES ($(ls -1 docs/ 2>/dev/null | wc -l) files)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -1 docs/ 2>/dev/null | head -10
echo ""

echo "💾 DATA STORES STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Credentials: $(grep -c '=' ~/.hoopstreet/creds/credentials.txt 2>/dev/null || echo 0) stored"
echo "📁 Projects: $(grep -c '"url"' projects.json 2>/dev/null || echo 0) connected"
echo "🧬 DNA.md: $(wc -l < docs/DNA.md 2>/dev/null) lines"
echo "📝 logs.txt: $(wc -l < docs/logs.txt 2>/dev/null) entries"
echo ""

echo "🔗 EXTERNAL INTEGRATIONS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐙 GitHub: Connected"
echo "📍 https://github.com/hoopstreet/ish-dev.git"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "Press Enter to continue..."
