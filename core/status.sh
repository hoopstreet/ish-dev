#!/bin/sh
# COMPLETE STATUS DASHBOARD - Shows everything needed to maintain the system

clear
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "  📊 HOOPSTREET iSH DEV SYSTEM - COMPLETE STATUS REPORT"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# ============================================================
# 1. SYSTEM VERSION & HEALTH
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  📌 SYSTEM VERSION & HEALTH                                                  │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

# Version from status.json
if [ -f "/root/ish-dev/docs/status.json" ]; then
    VERSION=$(grep -o '"version": "[^"]*"' /root/ish-dev/docs/status.json | cut -d'"' -f4)
    STATUS=$(grep -o '"status": "[^"]*"' /root/ish-dev/docs/status.json | cut -d'"' -f4)
    echo "  🏷️  Version: $VERSION"
    echo "  💚 Status: $STATUS"
else
    echo "  🏷️  Version: v9.2.0"
    echo "  💚 Status: production"
fi

# Last DNA update
if [ -f "/root/ish-dev/docs/DNA.md" ]; then
    LAST_DNA=$(grep "^## \[v" /root/ish-dev/docs/DNA.md | head -1 | sed 's/## //')
    echo "  📝 Last DNA Update: $LAST_DNA"
fi

# Last log entry
if [ -f "/root/ish-dev/docs/logs.txt" ]; then
    LAST_LOG=$(tail -1 /root/ish-dev/docs/logs.txt | cut -d' ' -f1-5)
    echo "  📋 Last Activity: $LAST_LOG"
fi
echo ""

# ============================================================
# 2. CORE COMPONENTS STATUS (What's Working)
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  🔧 CORE COMPONENTS STATUS                                                   │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

# Check each core script
for script in menu.sh code.sh sync.sh heal.sh status.sh remote.sh creds.sh supabase_sync.sh; do
    if [ -f "/root/ish-dev/core/$script" ]; then
        echo "  ✅ $script - OK"
    else
        echo "  ❌ $script - MISSING"
    fi
done
echo ""

# ============================================================
# 3. DATA STORES STATUS
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  💾 DATA STORES STATUS                                                       │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""
# Credentials
if [ -f "/root/.hoopstreet/creds/credentials.txt" ]; then
    CRED_COUNT=$(cat /root/.hoopstreet/creds/credentials.txt 2>/dev/null | grep -c "=")
    echo "  🔐 Credentials: $CRED_COUNT stored"
    echo "     📁 /root/.hoopstreet/creds/credentials.txt"
else
    echo "  🔐 Credentials: NONE (use Option 6 to add)"
fi

# Projects
if [ -f "/root/ish-dev/projects.json" ]; then
    PROJ_COUNT=$(python3 -c "import json; f=open('/root/ish-dev/projects.json'); d=json.load(f); print(len(d.get('projects', [])))" 2>/dev/null)
    echo "  📁 Projects: $PROJ_COUNT connected"
    echo "     📁 /root/ish-dev/projects.json"
else
    echo "  📁 Projects: NONE (use Option 5 to connect)"
fi

# DNA.md
if [ -f "/root/ish-dev/docs/DNA.md" ]; then
    DNA_SIZE=$(wc -l < /root/ish-dev/docs/DNA.md 2>/dev/null)
    echo "  🧬 DNA.md: $DNA_SIZE lines"
fi

# logs.txt
if [ -f "/root/ish-dev/docs/logs.txt" ]; then
    LOG_SIZE=$(wc -l < /root/ish-dev/docs/logs.txt 2>/dev/null)
    echo "  📝 logs.txt: $LOG_SIZE entries"
fi
echo ""

# ============================================================
# 4. EXTERNAL INTEGRATIONS STATUS
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  🔗 EXTERNAL INTEGRATIONS                                                    │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

# GitHub
if [ -d "/root/ish-dev/.git" ]; then
    REMOTE=$(git -C /root/ish-dev remote -v 2>/dev/null | head -1 | awk '{print $2}')
    echo "  🐙 GitHub: Connected"
    echo "     📍 $REMOTE"
else
    echo "  🐙 GitHub: Not configured"
fi

# Supabase
if [ -f "/root/ish-dev/config/supabase.env" ]; then
    . /root/ish-dev/config/supabase.env
    if [ -n "$SUPABASE_URL" ]; then
        echo "  🗄️ Supabase: Connected"
        echo "     📍 $SUPABASE_URL"
    else
        echo "  🗄️ Supabase: Not configured"
    fi
else
    echo "  🗄️ Supabase: Not configured"
fi
echo ""

# 
============================================================
# 5. DIRECTORY STRUCTURE VERIFICATION
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  📁 DIRECTORY STRUCTURE                                                      │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

for dir in core docs agents utils config backups projects; do
    if [ -d "/root/ish-dev/$dir" ]; then
        FILE_COUNT=$(find /root/ish-dev/$dir -type f 2>/dev/null | wc -l)
        echo "  ✅ /ish-dev/$dir/ - $FILE_COUNT files"
    else
        echo "  ❌ /ish-dev/$dir/ - MISSING"
    fi
done
echo ""

# ============================================================
# 6. RECENT ACTIVITY (Last 5 events)
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  📋 RECENT ACTIVITY (Last 5 events)                                          │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""

if [ -f "/root/ish-dev/docs/logs.txt" ]; then
    tail -5 /root/ish-dev/docs/logs.txt | while read line; do
        echo "  • $line"
    done
else
    echo "  No logs found"
fi
echo ""

# ============================================================
# 7. WHAT'S MISSING / NEEDS ATTENTION
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  ⚠️  MISSING / NEEDS ATTENTION                                               │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""
MISSING_COUNT=0

# Check for missing core scripts
for script in menu.sh code.sh sync.sh heal.sh status.sh remote.sh creds.sh; do
    if [ ! -f "/root/ish-dev/core/$script" ]; then
        echo "  ❌ Missing: core/$script"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

# Check for missing config
if [ ! -f "/root/ish-dev/config/supabase.env" ]; then
    echo "  ⚠️ Supabase not configured (run: core/supabase_sync.sh setup)"
    MISSING_COUNT=$((MISSING_COUNT + 1))
fi

# Check for missing symlink
if [ ! -L "/root/menu" ]; then
    echo "  ⚠️ Symlink missing (run: ln -sf /root/ish-dev/core/menu.sh /root/menu)"
    MISSING_COUNT=$((MISSING_COUNT + 1))
fi

if [ $MISSING_COUNT -eq 0 ]; then
    echo "  ✅ All systems operational!"
fi
echo ""

# ============================================================
# 8. QUICK FIX COMMANDS
# ============================================================
echo "┌─────────────────────────────────────────────────────────────────────────────┐"
echo "│  🔧 QUICK FIX COMMANDS                                                       │"
echo "└─────────────────────────────────────────────────────────────────────────────┘"
echo ""
echo "  To fix missing components:"
echo "    /root/ish-dev/core/supabase_sync.sh setup  # Configure Supabase"
echo "    ln -sf /root/ish-dev/core/menu.sh /root/menu  # Fix menu symlink"
echo "    chmod +x /root/ish-dev/core/*.sh  # Fix permissions"
echo ""
echo "  To view logs:"
echo "    tail -f /root/ish-dev/docs/logs.txt"
echo ""
echo "  To sync data:"
echo "    cd /root/ish-dev && git push origin main"
echo ""

echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
printf "Press Enter to continue..."
read dummy
