#!/bin/sh
clear
echo "════════════════════════════════════════════════════════"
echo "     🔗 REMOTE PROJECTS MANAGER"
echo "════════════════════════════════════════════════════════"
echo ""

mkdir -p /root/projects

echo "📁 Projects in /root/projects:"
ls -la /root/projects/ 2>/dev/null | grep "^d" | awk '{print "  " $9}' || echo "  (empty)"
echo ""
echo "1) Clone repository"
echo "2) Load project to /tmp/project"
echo "0) Back"
printf "Choose: "
read r
case $r in
    1)
        printf "GitHub URL: "
        read url
        cd /root/projects && git clone "$url"
        ;;
    2)
        printf "Project name: "
        read proj
        if [ -d "/root/projects/$proj" ]; then
            rm -rf /tmp/project
            cp -r "/root/projects/$proj" /tmp/project
            echo "✅ Loaded to /tmp/project"
        fi
        ;;
esac
read -p "Press Enter..."

# Sync to Supabase after adding project
if [ -f "/root/ish-dev/core/supabase_sync.sh" ]; then
    /root/ish-dev/core/supabase_sync.sh sync-projects 2>/dev/null
fi
