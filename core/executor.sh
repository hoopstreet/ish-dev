#!/bin/sh
ACTION="$1"
COMMAND="$2"
CODE="$3"

case "$ACTION" in
    heal)
        sh core/heal.sh 2>&1
        ;;
    sync)
        sh core/sync.sh 2>&1
        ;;
    status)
        cat docs/status.json 2>/dev/null || echo '{"status":"unknown"}'
        ;;
    remote)
        sh core/remote.sh 2>&1
        ;;
    credentials)
        sh core/creds.sh 2>&1
        ;;
    code)
        TMP="/tmp/exec_$$.sh"
        echo "$CODE" > "$TMP"
        sh "$TMP" 2>&1
        rm -f "$TMP"
        ;;
    analyze)
        if echo "$COMMAND" | grep -q "github"; then
            curl -s "https://api.github.com/repos/hoopstreet/ish-dev" | jq '{name:.name, stars:.stargazers_count, forks:.forks_count}'
        else
            echo "📁 Core scripts: $(ls core/*.sh 2>/dev/null | wc -l)"
        fi
        ;;
    *)
        echo "Unknown action: $ACTION"
        ;;
esac
