#!/bin/sh
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
mkdir -p /root/.hoopstreet/creds

sync_to_github() {
    cd /root/ish-dev
    git add credentials.json 2>/dev/null
    git commit -m "Update credentials $(date)" 2>/dev/null
    git push origin main 2>/dev/null
}

update_credentials_json() {
    cd /root/ish-dev
    python3 -c "
import json
creds = {}
with open('$CREDS_FILE') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            creds[k] = {'value': v, 'notes': 'Auto-synced'}
with open('credentials.json', 'w') as f:
    json.dump({'credentials': creds}, f, indent=2)
"
}

while true; do
    clear
    echo "════════════════════════════════════════════════════════"
    echo "     🔐 CREDENTIALS MANAGER"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "📋 Current Credentials:"
    echo "─────────────────────────────────────────────────────────"
    
    if [ -f "$CREDS_FILE" ] && [ -s "$CREDS_FILE" ]; then
        num=1
        while IFS='=' read -r name value; do
            if [ -n "$name" ]; then
                echo "  $num. 🔑 $name"
                eval "cred_$num=\"$name\""
                num=$((num + 1))
            fi
        done < "$CREDS_FILE"
        total=$((num - 1))
    else
        echo "  (none)"
        total=0
    fi
    echo ""
    echo "─────────────────────────────────────────────────────────"
    echo ""
    echo "  1) Add new credential"
    echo "  2) Get credential value"
    echo "  3) Delete credential"
    echo "  0) Back"
    echo ""
    printf "👉 Choose: "
    read c

    case $c in
        1)
            echo ""
            printf "  Name: "
            read name
            printf "  Value: "
            read value
            printf "  Notes: "
            read notes
            
            if grep -q "^$name=" "$CREDS_FILE" 2>/dev/null; then
                echo ""
                printf "  ⚠️ Credential '$name' already exists. Overwrite? (y/n): "
                read overwrite
                if [ "$overwrite" = "y" ] || [ "$overwrite" = "Y" ]; then
                    sed -i "/^$name=/d" "$CREDS_FILE"
                    echo "$name=$value" >> "$CREDS_FILE"
                    echo "  ✅ Updated: $name"
                    update_credentials_json
                    sync_to_github
                    echo "  ✅ Auto-synced to GitHub"
                else
                    echo "  ❌ Kept existing"
                fi
            else
                echo "$name=$value" >> "$CREDS_FILE"
                echo "  ✅ Added: $name"
                update_credentials_json
                sync_to_github
                echo "  ✅ Auto-synced to GitHub"
            fi
            ;;
        2)
            echo ""
            if [ $total -eq 0 ]; then
                echo "  No credentials found"
            else
                echo "  Available credentials:"
                for i in $(seq 1 $total); do
                    eval name="\$cred_$i"
                    echo "    $i. $name"
                done
                echo ""
                printf "  Select number (1-$total) or enter name: "
                read input
                
                if echo "$input" | grep -q '^[0-9]\+$' && [ "$input" -le "$total" ]; then
                    eval name="\$cred_$input"
                else
                    name="$input"
                fi
                
                value=$(grep "^$name=" "$CREDS_FILE" 2>/dev/null | cut -d'=' -f2)
                if [ -n "$value" ]; then
                    echo ""
                    echo "  🔑 $name"
                    echo "  Value: $value"
                else
                    echo "  ❌ Credential not found"
                fi
            fi
            ;;
        3)
            echo ""
            if [ $total -eq 0 ]; then
                echo "  No credentials found"
            else
                echo "  Available credentials:"
                for i in $(seq 1 $total); do
                    eval name="\$cred_$i"
                    echo "    $i. $name"
                done
                echo ""
                printf "  Select number (1-$total) or enter name to delete: "
                read input
                
                if echo "$input" | grep -q '^[0-9]\+$' && [ "$input" -le "$total" ]; then
                    eval name="\$cred_$input"
                else
                    name="$input"
                fi
                
                if grep -q "^$name=" "$CREDS_FILE" 2>/dev/null; then
                    sed -i "/^$name=/d" "$CREDS_FILE"
                    echo "  ✅ Deleted: $name"
                    update_credentials_json
                    sync_to_github
                    echo "  ✅ Auto-synced to GitHub"
                else
                    echo "  ❌ Credential not found"
                fi
            fi
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
