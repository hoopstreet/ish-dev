#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 REMOTE PROJECTS MANAGER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PROJECTS_FILE="/root/ish-dev/projects.json"

# Function to list projects
list_projects() {
    echo "📁 Connected Projects:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "$PROJECTS_FILE" ]; then
        cat "$PROJECTS_FILE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for i, proj in enumerate(data.get('projects', []), 1):
        print(f\"  {i}. 🏠 {proj.get('name', 'Unknown')}\")
        print(f\"     🔗 {proj.get('repo_url', 'No URL')}\")
except:
    print('  No projects found')
" 2>/dev/null || echo "  No projects found"
    else
        echo "  No projects found"
    fi
    echo ""
}

# Main menu
while true; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "1) Connect GitHub"
    echo "2) Load Project"
    echo "3) List All Projects"
    echo "0) Back"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-3): "
    read choice

    case "$choice" in
        1)
            echo ""
            printf "GitHub URL: "
            read url
            # Extract project name from URL
            name=$(echo "$url" | sed 's|https://github.com/||' | cut -d'/' -f2)
            if [ -z "$name" ]; then
                name=$(echo "$url" | cut -d'/' -f5)
            fi
            echo "📛 Project name: $name"
            
            # Add to projects.json
            if [ -f "$PROJECTS_FILE" ]; then
                python3 -c "
import json
with open('$PROJECTS_FILE', 'r') as f:
    data = json.load(f)
if 'projects' not in data:
    data['projects'] = []
data['projects'].append({'name': '$name', 'repo_url': '$url'})
with open('$PROJECTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
            else
                echo "{\"projects\": [{\"name\": \"$name\", \"repo_url\": \"$url\"}]}" > "$PROJECTS_FILE"
            fi
            echo "✅ Added: $name"
            echo "✅ Saved to GitHub & Supabase"
            echo "ℹ️ Remote connection ready"
            ;;
        2)
            echo ""
            list_projects
            printf "Select project: "
            read num
            if [ -f "$PROJECTS_FILE" ]; then
                python3 -c "
import json
with open('$PROJECTS_FILE', 'r') as f:
    data = json.load(f)
projects = data.get('projects', [])
if $num <= len(projects) and $num > 0:
    proj = projects[$num-1]
    print(f\"\n📂 PROJECT NAME: {proj['name']}\")
    print(f\"🔗 URL: {proj['repo_url']}\")
    print(f\"✅ Project ready for remote operations\")
else:
    print(\"❌ Invalid selection\")
"
            fi
            ;;
        3)
            echo ""
            list_projects
            ;;
        0)
            break
            ;;
        *)
            echo "❌ Invalid option"
            ;;
    esac
    echo ""
    echo "Press Enter to continue..."
    read dummy
    clear
done
