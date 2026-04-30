#!/bin/sh
CREDS_FILE="/root/.hoopstreet/creds/credentials.txt"
mkdir -p /root/.hoopstreet/creds

clear
echo "════════════════════════════════════════════════════════"
echo "     🔐 CREDENTIALS MANAGER"
echo "════════════════════════════════════════════════════════"
echo ""
echo "1) Add credential"
echo "2) Get credential"
echo "3) List credentials"
echo "0) Back"
printf "Choose: "
read c

case $c in
    1)
        printf "Name: "; read n
        printf "Value: "; read v
        echo "$n=$v" >> "$CREDS_FILE"
        echo "✅ Added"
        ;;
    2)
        printf "Name: "; read n
        grep "^$n=" "$CREDS_FILE" | cut -d'=' -f2
        ;;
    3)
        cat "$CREDS_FILE" | cut -d'=' -f1
        ;;
esac
read -p "Press Enter..."

# Supabase sync after adding credential
if [ -f "/root/ish-dev/core/supabase_sync.sh" ]; then
    /root/ish-dev/core/supabase_sync.sh sync-creds 2>/dev/null
fi
