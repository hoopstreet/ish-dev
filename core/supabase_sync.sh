#!/bin/sh
CONFIG_FILE="/root/ish-dev/config/supabase.env"
[ -f "$CONFIG_FILE" ] && . "$CONFIG_FILE"

case "$1" in
    status)
        echo ""
        echo "🗄️ SUPABASE STATUS"
        echo "URL: ${SUPABASE_URL:-Not configured}"
        echo "Auto-sync active via GitHub Actions"
        echo ""
        ;;
    *)
        echo "Run: git push origin main"
        ;;
esac
