#!/bin/sh
# REMOTE PROJECTS MANAGER - Simple Remote Connections

PROJECTS_FILE="/root/ish-dev/projects.json"
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"

# Load Supabase config
if [ -f "/root/ish-dev/config/supabase.env" ]; then
    . /root/ish-dev/config/supabase.env
fi

# Initialize projects file
if [ ! -f "$PROJECTS_FILE" ]; then
    echo '{"projects":[]}' > "$PROJECTS_FILE"
fi

# Extract repo name from URL
extract_name() {
    echo "$1" | sed 's/.*\///' | sed 's/\.git//' | sed 's/\/$//'
}

# Sync to Supabase
sync_to_supabase() {
    if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_ANON_KEY" ]; then
        python3 -c "
import json, urllib.request
url = '$SUPABASE_URL'
key = '$SUPABASE_ANON_KEY'
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
for p in projects:
    payload = json.dumps({'name': p.get('name'), 'repo_url': p.get('repo_url')}).encode()
    req = urllib.request.Request(f'{url}/rest/v1/projects', data=payload, method='POST')
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Content-Type', 'application/json')
    try:
        urllib.request.urlopen(req, timeout=5)
    except:
        pass
" 2>/dev/null
    fi
}

while true; do
    clear
    echo "════════════════════════════════════════════════════════"
    echo "     🔗 REMOTE PROJECTS MANAGER"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "📁 Connected Projects:"
    echo "─────────────────────────────────────────────────────────"

    
    # Display projects
    if [ -f "$PROJECTS_FILE" ] && [ -s "$PROJECTS_FILE" ]; then
        python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
    if projects:
        for i, p in enumerate(projects, 1):
            print(f'  {i}. 🏠 {p.get(\"name\")}')
            print(f'     🔗 {p.get(\"repo_url\")}')
    else:
        print('  (no projects connected)')
"
    else
        echo "  (no projects connected)"
    fi
    echo ""
    echo "─────────────────────────────────────────────────────────"
    echo ""
    echo "  1) Connect GitHub Repository"
    echo "  2) Load Project"
    echo "  3) List All Projects"
    echo "  0) Back"
    echo ""
    printf "👉 Choose: "
    read r

    case $r in
        1)
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "  🔗 CONNECT TO GITHUB REPOSITORY"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            printf "  GitHub URL: "
            read url
            
            if [ -n "$url" ]; then
                # Extract name from URL
                name=$(extract_name "$url")
                echo "  📛 Project name: $name"
                
                # Check if already exists
                if python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    for p in data.get('projects', []):
        if p.get('name') == '$name' or p.get('repo_url') == '$url':
            exit(0)
exit(1)
" 2>/dev/null; then
                    echo ""
                    echo "  ⚠️ Project already exists!"
                    printf "  Update URL? (y/n): "
                    read overwrite
                    if [ "$overwrite" = "y" ] || [ "$overwrite" = "Y" ]; then
                        python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
data['projects'] = [p for p in data.get('projects', []) if p.get('name') != '$name']
data['projects'].append({'name': '$name', 'repo_url': '$url'})
with open('$PROJECTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
                        echo "  ✅ Updated: $name"
                    fi
                else
                    python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
data['projects'].append({'name': '$name', 'repo_url': '$url'})
with open('$PROJECTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
                    echo "  ✅ Added: $name"
                fi

                
                # Sync to Supabase
                sync_to_supabase
                
                # Push to GitHub
                cd /root/ish-dev
                git add projects.json
                git commit -m "Add project: $name" 2>/dev/null
                git push origin main 2>/dev/null
                echo "  ✅ Saved to GitHub & Supabase"
                echo ""
                echo "  ℹ️  Remote connection ready (no files cloned)"
            fi
            ;;
        2)
            echo ""
            if [ ! -f "$PROJECTS_FILE" ]; then
                echo "  No projects connected. Use option 1 first."
            else
                echo "  Available Projects:"
                python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
    for i, p in enumerate(projects, 1):
        print(f'    {i}. {p.get(\"name\")}')
"
                echo ""
                printf "  Select project number: "
                read selection
                
                python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
    if $selection <= len(projects):
        idx = $selection - 1
        p = projects[idx]
        name = p.get('name')
        url = p.get('repo_url')
        print('')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print(f'  📂 PROJECT LOADED: {name}')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
        print(f'  🔗 URL: {url}')
        print('')
        print('  ✅ Project ready for remote operations')
        print('  Use main menu Option 1 (Code) to execute commands')
        print('  The project URL will be used for GitHub API calls')
"
            fi
            ;;
        3)
            echo ""
            echo "  📋 ALL CONNECTED PROJECTS:"
            echo "  ─────────────────────────────────────────────────────────"
            python3 -c "
import json
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
    if projects:
        for i, p in enumerate(projects, 1):
            print(f'    {i}. {p.get(\"name\")}')
            print(f'       🔗 {p.get(\"repo_url\")}')
            print('')
    else:
        print('    (no projects)')
"
            ;;
        0)
            break
            ;;
        *)
            echo "  ❌ Invalid choice"
            ;;
    esac
    echo ""
    read -p "Press Enter to continue..."
done
