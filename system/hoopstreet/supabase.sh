#!/bin/sh
if [ "$1" = "setup" ]; then
    printf "Supabase URL: "; read url
    printf "Supabase Key: "; read key
    mkdir -p /root/.secrets
    echo "SUPABASE_URL=$url" > /root/.secrets/supabase.env
    echo "SUPABASE_KEY=$key" >> /root/.secrets/supabase.env
    echo "✅ Supabase configured"
else
    echo "Usage: setup | sync"
fi
read dummy
"🔄 Syncing DNA.md to Supabase..."
    
    if [ -f /root/ish-dev/DNA.md ]; then
        DNA_CONTENT=$(cat /root/ish-dev/DNA.md | sed 's/"/\\"/g' | tr '\n' ' ')
        
        curl -s -X POST "${SUPABASE_URL}/rest/v1/dna_logs" \
            -H "apikey: $SUPABASE_SERVICE_KEY" \
            -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"content\":\"$DNA_CONTENT\",\"project\":\"ish-dev\",\"version\":\"v4.0.0\"}"
        
        echo "✅ DNA.md synced"
    else
        echo "❌ DNA.md not found"
    fi
}

sync_logs() {
    echo "🔄 Syncing logs.txt to Supabase..."
    
    if [ -f /root/ish-dev/logs.txt ]; then
        tail -5 /root/ish-dev/logs.txt | while read line; do
            curl -s -X POST "${SUPABASE_URL}/rest/v1/logs" \
                -H "apikey: $SUPABASE_SERVICE_KEY" \
                -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
                -H "Content-Type: application/json" \
                -d "{\"message\":\"$line\",\"project\":\"ish-dev\",\"timestamp\":\"$(date -Iseconds)\"}"
        done
        echo "✅ Logs synced"
    else
        echo "❌ logs.txt not found"
    fi
}

case "$1" in
    setup) setup_supabase ;;
    sync-dna) sync_dna ;;
    sync-logs) sync_logs ;;
    sync) sync_dna; sync_logs ;;
    *) echo "Usage: setup | sync-dna | sync-logs | sync" ;;
esac
