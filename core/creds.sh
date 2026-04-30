#!/bin/sh
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
mkdir -p /root/.hoopstreet/creds

while true; do
    clear
    echo "════════════════════════════════════════════════════════"
    echo "     🔐 CREDENTIALS MANAGER"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "Current Credentials:"
    if [ -f "$CREDS_FILE" ]; then
        cat "$CREDS_FILE" | cut -d'=' -f1 | head -10
    else
        echo "  (none)"
    fi
    echo ""
    echo "1) Add | 2) Get | 3) Delete | 0) Back"
    printf "Choose: "
    read c
    case $c in
        1)
            echo ""
            printf "Name: "
            read name
            printf "Value: "
            read value
            echo "$name=$value" >> "$CREDS_FILE"
            echo "✅ Added: $name"
            
            cd /root/ish-dev
            python3 -c "
import json
creds = {}
with open('/root/.hoopstreet/creds/credentials.txt') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            creds[k] = {'value': v, 'notes': 'Auto-synced'}
with open('credentials.json', 'w') as f:
    json.dump({'credentials': creds}, f, indent=2)
"
            git add credentials.json
            git commit -m "Add: $name" 2>/dev/null
            git push origin main 2>/dev/null
            echo "✅ Auto-synced to GitHub"
            ;;
        2)
            echo ""
            printf "Name: "
            read name
            grep "^$name=" "$CREDS_FILE" | cut -d'=' -f2 || echo "Not found"
            ;;
        3)
            echo ""
            printf "Name: "
            read name
            if grep -q "^$name=" "$CREDS_FILE"; then
                sed -i "/^$name=/d" "$CREDS_FILE"
                cd /root/ish-dev
                python3 -c "
import json
creds = {}
with open('/root/.hoopstreet/creds/credentials.txt') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            creds[k] = {'value': v, 'notes': 'Auto-synced'}
with open('credentials.json', 'w') as f:
    json.dump({'credentials': creds}, f, indent=2)
"
                git add credentials.json
                git commit -m "Delete: $name" 2>/dev/null
                git push origin main 2>/dev/null
                echo "✅ Deleted and synced"
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
