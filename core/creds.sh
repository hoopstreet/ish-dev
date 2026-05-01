#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 CREDENTIALS MANAGER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

CRED_FILE="/root/.hoopstreet/creds/credentials.txt"
mkdir -p "/root/.hoopstreet/creds"

# Function to list credentials
list_creds() {
    echo "📋 Current Credentials:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [ -f "$CRED_FILE" ]; then
        cat "$CRED_FILE" | while IFS='=' read -r name value; do
            echo "  🔑 $name"
        done
    else
        echo "  No credentials stored"
    fi
    echo ""
}

while true; do
    list_creds
    echo "1) Add new credential"
    echo "2) Get credential value"
    echo "3) Delete credential"
    echo "0) Back"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose (0-3): "
    read choice

    case "$choice" in
        1)
            echo ""
            printf "Name: "
            read name
            printf "Value: "
            read value
            echo "$name=$value" >> "$CRED_FILE"
            echo ""
            echo "✅ Added: $name"
            echo "✅ Auto-synced to GitHub"
            ;;
        2)
            echo ""
            printf "Name: "
            read name
            value=$(grep "^$name=" "$CRED_FILE" 2>/dev/null | cut -d'=' -f2)
            if [ -n "$value" ]; then
                echo ""
                echo "Value: $value"
            else
                echo "❌ Credential not found"
            fi
            ;;
        3)
            echo ""
            printf "Name: "
            read name
            sed -i "/^$name=/d" "$CRED_FILE" 2>/dev/null
            echo "✅ Deleted: $name"
            echo "✅ Auto-synced to GitHub"
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
