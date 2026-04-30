#!/bin/sh
# SUPABASE SYNC SCRIPT - Central Database Integration

CONFIG_FILE="/root/ish-dev/config/supabase.env"
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
PROJECTS_FILE="/root/ish-dev/projects.json"

# Load Supabase config
if [ -f "$CONFIG_FILE" ]; then
    . "$CONFIG_FILE"
else
    echo "❌ Supabase not configured. Run: supabase-setup"
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
        echo "  No local projects found"
        return
    fi
    
    python3 -c "
import json, urllib.request
with open('$PROJECTS_FILE') as f:
    projects = json.load(f).get('projects', [])
url = '$SUPABASE_URL'
key = '$SUPABASE_ANON_KEY'
for p in projects:
    payload = json.dumps({'name': p.get('name'), 'repo_url': p.get('repo'), 'local_path': p.get('local')}).encode()
    req = urllib.request.Request(f'{url}/rest/v1/projects', data=payload, method='POST')
    req.add_header('apikey', key)
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('Content-Type', 'application/json')
    try:
        urllib.request.urlopen(req, timeout=5)
        print(f'  Synced: {p.get(\"name\")}')
    except:
        pass
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

# Log activity to Supabase
log_activity() {
    local event="$1"
    local level="${2:-INFO}"
    
    curl -s -X POST "${SUPABASE_URL}/rest/v1/activity_logs" \
        -H "apikey: $SUPABASE_ANON_KEY" \
        -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"event\":\"$event\",\"level\":\"$level\",\"details\":{\"source\":\"iSH\",\"timestamp\":\"$(date -Iseconds)\"}}" 2>/dev/null
}


# Get system state
get_system_state() {
    curl -s "${SUPABASE_URL}/rest/v1/system_state?select=key,value" \
        -H "apikey: $SUPABASE_ANON_KEY" \
        -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
        2>/dev/null | python3 -m json.tool
}

# Update system state
update_system_state() {
    local key="$1"
    local value="$2"
    
    curl -s -X PATCH "${SUPABASE_URL}/rest/v1/system_state?key=eq.${key}" \
        -H "apikey: $SUPABASE_ANON_KEY" \
        -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"value\":\"$value\",\"updated_at\":\"$(date -Iseconds)\"}" 2>/dev/null
}

# Show status
show_status() {
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "  🗄️ SUPABASE STATUS"
    echo "═══════════════════════════════════════════════════════"
    echo "  URL: $SUPABASE_URL"
    echo ""
    echo "  Tables:"
    echo "    • credentials - Token storage"
    echo "    • projects - GitHub projects"
    echo "    • system_state - Agent state"
    echo "    • dna_logs - Evolution tracking"
    echo "    • activity_logs - Activity log"
    echo ""
    get_system_state
    echo ""
}

# Setup Supabase (interactive)
setup_supabase() {
    clear
    echo "═══════════════════════════════════════════════════════"
    echo "  🗄️ SUPABASE SETUP"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    printf "Enter Supabase URL (e.g., https://xxxxx.supabase.co): "
    read url
    printf "Enter Supabase Anon Key: "
    read key
    
    cat > "$CONFIG_FILE" << EOF
SUPABASE_URL="$url"
SUPABASE_ANON_KEY="$key"
EOF
    
    echo ""
    echo "✅ Supabase configured!"
    echo ""
    echo "Next steps:"
    echo "  1. Run the SQL schema in Supabase SQL Editor"
    echo "  2. Test connection: supabase_sync.sh status"
    echo "  3. Sync credentials: supabase_sync.sh sync-creds"
    echo "  4. Sync projects: supabase_sync.sh sync-projects"
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
    log) log_activity "$2" "$3" ;;
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
        echo "  log <event>    - Log activity to Supabase"
        echo ""
        ;;
esac
