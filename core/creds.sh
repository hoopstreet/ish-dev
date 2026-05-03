#!/bin/sh
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
mkdir -p /root/.hoopstreet/creds

while true; do
    clear
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🔐 CREDENTIALS MANAGER"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # List existing credentials
    if [ -f "$CREDS_FILE" ]; then
        echo "📋 Current Credentials:"
        grep -E "^[A-Z_]+=" "$CREDS_FILE" 2>/dev/null | while IFS='=' read -r name value; do
            echo "   🔑 $name"
        done
    else
        echo "📋 No credentials stored yet"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "1) Add new credential"
    echo "2) Get credential value"
    echo "3) Delete credential"
    echo "0) Back"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "👉 Choose: "
    read choice

    case $choice in
        1)
            echo ""
            printf "Name (e.g., GEMINI_API_KEY): "
            read name
            printf "Value (paste your key): "
            read value
            # Remove existing entry if present
            sed -i "/^$name=/d" "$CREDS_FILE" 2>/dev/null
            # Add new entry
            echo "$name=$value" >> "$CREDS_FILE"
            echo "✅ Added: $name"
            echo "✅ Value length: ${#value} characters"
            sleep 1
            ;;
        2)
            echo ""
            printf "Name: "
            read name
            value=$(grep "^$name=" "$CREDS_FILE" 2>/dev/null | cut -d'=' -f2-)
            if [ -n "$value" ]; then
                echo "🔑 Value: ${value:0:50}..."
            else
                echo "❌ Not found"
            fi
            sleep 2
            ;;
        3)
            echo ""
            printf "Name: "
            read name
            sed -i "/^$name=/d" "$CREDS_FILE" 2>/dev/null
            echo "✅ Deleted: $name"
            sleep 1
            ;;
        0)
            break
            ;;
    esac
done
