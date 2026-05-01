#!/bin/sh
echo "Creating Hoopstreet blueprint files..."

# Go to home directory
cd /root

# Clone the repository (if not exists)
if [ ! -d "ish-dev" ]; then
    git clone https://github.com/hoopstreet/ish-dev.git
fi
cd ish-dev

# Create README.md
cat > README.md << 'EOF'
# 🏀 Hoopstreet iSH Auto Healing Agent

A powerful self-healing agent for iSH (iOS shell) that automatically detects, fixes, and executes multi-phase code blocks with visual feedback and DNA logging.

## Quick Install