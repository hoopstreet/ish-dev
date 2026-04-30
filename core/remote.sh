#!/bin/sh
PROJECTS_FILE="/root/ish-dev/projects.json"
mkdir -p /root/projects
[ ! -f "$PROJECTS_FILE" ] && echo '{"projects":[]}' > "$PROJECTS_FILE"

while true; do
    clear
    echo "════════════════════════════════════════════════════════"
    echo "     🔗 REMOTE PROJECTS MANAGER"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "Projects:"
    ls /root/projects/ 2>/dev/null | head -10 || echo "  (empty)"
    echo ""
    echo "1) Clone | 2) Load | 0) Back"
    printf "Choose: "
    read r
    case $r in
        1)
            printf "GitHub URL: "
            read url
            cd /root/projects
            REPO=$(echo "$url" | sed 's/.*\///' | sed 's/\.git//')
            git clone "$url" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "✅ Cloned: $REPO"
                python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
data['projects'].append({'name': '$REPO', 'repo_url': '$url'})
with open('$PROJECTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
                cd /root/ish-dev
                git add projects.json
                git commit -m "Add project: $REPO" 2>/dev/null
                git push origin main 2>/dev/null
                echo "✅ Auto-synced to GitHub"
            else
                echo "Clone failed"
            fi
            ;;
        2)
            printf "Project name: "
            read proj
            if [ -d "/root/projects/$proj" ]; then
                rm -rf /tmp/project
                cp -r "/root/projects/$proj" /tmp/project
                echo "✅ Loaded to /tmp/project"
            else
                echo "Not found"
            fi
            ;;
        0) break ;;
        *) echo "Invalid" ;;
    esac
    echo ""
    read -p "Press Enter..."
done
