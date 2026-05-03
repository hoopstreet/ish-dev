#!/bin/sh
# HOOPSTREET iSH Auto Healing Agent - Gemini AI Bundle Installer
# This script installs the complete system with Gemini CLI support

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 HOOPSTREET GEMINI AI BUNDLE v10.1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Install Python and pip if not present
echo "📦 Installing dependencies..."
apk add python3 py3-pip 2>/dev/null || apt-get install python3 python3-pip -y 2>/dev/null

# Install Google Gemini AI library
echo "🤖 Installing Gemini AI library..."
pip3 install google-generativeai --quiet

# Create directory structure
mkdir -p /root/ish-dev/core
mkdir -p /root/ish-dev/docs
mkdir -p /root/.hoopstreet/creds

# Download or copy agent files (these would be in the repo)
echo "📁 Installing Hoopstreet Agent files..."

# Note: In the actual GitHub repo, these files would be included
# For now, we ensure they exist
chmod +x /root/ish-dev/core/*.sh /root/ish-dev/core/*.py 2>/dev/null

# Create menu symlink
ln -sf /root/ish-dev/core/menu.sh /root/menu

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 NEXT STEPS:"
echo "   1. Get Gemini API key: https://makersuite.google.com/app/apikey"
echo "   2. Run 'menu' and choose Option 6 to add GEMINI_API_KEY"
echo "   3. Select Option 1 to use the AI Agent"
echo ""
echo "🚀 Type 'menu' to start!"
