#!/bin/sh
# SUPABASE SYNC SCRIPT - Central Database Integration

CONFIG_FILE="/root/ish-dev/config/supabase.env"
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
PROJECTS_FILE="/root/ish-dev/projects.json"

# Load Supabase config
if [ -f "$CONFIG_FILE" ]; then
    . "$CONFIG_FILE"
    echo "✅ Loaded Supabase config"
else
    echo "❌ Supabase not configured. Run: /root/ish-dev/core/supabase_sync.sh setup"
    exit 1
fi

# Sync credentials to Supabase
sync_credentials() {
    echo "🔄 Syncing credentials to Supabase..."
    
    if [ ! -f "$CREDS_FILE" ]; then
        echo "  No local credentials found"
        return
    fi
    
    while IFS='=' read -r name value; do
        if [ -n "$name" ]; then
            curl -s -X POST "${SUPABASE_URL}/rest/v1/credentials" \
                -H "apikey: $SUPABASE_ANON_KEY" \
                -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
                -H "Content-Type: application/json" \
                -d "{\"name\":\"$name\",\"value\":\"$value\",\"notes\":\"Auto-synced from iSH\"}" 2>/dev/null
            echo "  ✅ Synced: $name"
        fi
    done < "$CREDS_FILE"
    
    echo "✅ Credentials sync complete"
}

# Pull credentials from Supabase
pull_credentials() {
    echo "🔄 Pulling credentials from Supabase..."
    
    mkdir -p /root/.hoopstreet/creds
    > "$CREDS_FILE"
    
    curl -s "${SUPABASE_URL}/rest/v1/credentials?select=name,value" \
        -H "apikey: $SUPABASE_ANON_KEY" \
        -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
        2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for item in data:
        print(f\"{item['name']}={item['value']}\")
except:
    pass
" >> "$CREDS_FILE"
    
    echo "✅ Credentials pulled from Supabase"
}

# Sync projects to Supabase
sync_projects() {
    echo "🔄 Syncing projects to Supabase..."
    
    if [ ! -f "$PROJECTS_FILE" ]; then
        echo '{"projects":[]}' > "$PROJECTS_FILE"
    fi
    
    python3 -c "
import json, urllib.request
with open('$PROJECTS_FILE') as f:
    data = json.load(f)
    projects = data.get('projects', [])
url = '$SUPABASE_URL'
key = '$SUPABASE_ANON_KEY'
for p in projects:
    payload = json.dumps({'name': p.get('name'), 'repo_url': p.get('repo', p.get('repo_url')), 'local_path': p.get('local')}).encode()
    req = urllib.request.Request(f'{url}/rest/v1/projects', data=payload, method='POST')
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Content-Type', 'application/json')
    try:
        urllib.request.urlopen(req, timeout=5)
        print(f'  Synced: {p.get(\"name\")}')
    except Exception as e:
        print(f'  Failed: {p.get(\"name\")}')
"
    echo "✅ Projects sync complete"
}

# Pull projects from Supabase
pull_projects() {
    echo "🔄 Pulling projects from Supabase..."
    
    curl -s "${SUPABASE_URL}/rest/v1/projects?select=name,repo_url,local_path" \
        -H "apikey: $SUPABASE_ANON_KEY" \
        -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
        2>/dev/null > /tmp/supabase_projects.json
    
    python3 -c "
import json
with open('/tmp/supabase_projects.json') as f:
    projects = json.load(f)
with open('$PROJECTS_FILE', 'w') as f:
    json.dump({'projects': projects}, f, indent=2)
print(f'✅ Pulled {len(projects)} projects')
"
    echo "✅ Projects pulled from Supabase"
}

# Show status
show_status() {
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "  🗄️ SUPABASE STATUS"
    echo "═══════════════════════════════════════════════════════"
    echo "  URL: ${SUPABASE_URL}"
    echo ""
    echo "  Tables: credentials, projects, system_state, dna_logs, activity_logs"
    echo ""
}

# Setup Supabase (interactive)
setup_supabase() {
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "  🗄️ SUPABASE SETUP"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    printf "Enter Supabase URL: "
    read url
    printf "Enter Supabase Anon Key: "
    read key
    
    cat > "$CONFIG_FILE" << EOF
SUPABASE_URL="$url"
SUPABASE_ANON_KEY="$key"
EOF
    
    echo ""
    echo "✅ Supabase configured!"
}

case "$1" in
    setup) setup_supabase ;;
    sync-creds) sync_credentials ;;
    pull-creds) pull_credentials ;;
    sync-projects) sync_projects ;;
    pull-projects) pull_projects ;;
    sync-all) sync_credentials; sync_projects ;;
    pull-all) pull_credentials; pull_projects ;;
    status) show_status ;;
    *) 
        echo ""
        echo "═══════════════════════════════════════════════════════"
        echo "  🗄️ SUPABASE SYNC UTILITY"
        echo "═══════════════════════════════════════════════════════"
        echo ""
        echo "Commands:"
        echo "  setup          - Configure Supabase"
        echo "  sync-creds     - Sync credentials to Supabase"
        echo "  pull-creds     - Pull credentials from Supabase"
        echo "  sync-projects  - Sync projects to Supabase"
        echo "  pull-projects  - Pull projects from Supabase"
        echo "  sync-all       - Sync everything"
        echo "  pull-all       - Pull everything"
        echo "  status         - Show Supabase status"
        echo ""
        ;;
esac
