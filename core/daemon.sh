#!/bin/sh
while true; do
    echo "🔄 Agent Watcher: Checking state..."
    cd /root/ish-dev
    
    # 1. Auto-Fix & Commit
    git add .
    git commit -m "🤖 AI: 24/7 Background Fix & Sync [$(date +%T)]" || echo "No changes."
    
    # 2. Auto-Merge & Push
    git pull origin main --rebase
    git push origin main
    
    # 3. Check for syntax errors and self-heal
    python3 -m compileall . > /tmp/check 2>&1
    if grep -q "SyntaxError" /tmp/check; then
        echo "⚠️  Syntax Error Found. Triggering AI..."
        sh /root/ish-dev/core/trigger.sh
    fi
    
    echo "💤 Agent sleeping for 60s..."
    sleep 60
done
