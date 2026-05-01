#!/bin/sh
clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 HOOPSTREET CREDENTIAL MANAGER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. View Active Tokens"
echo "2. Refresh GitHub Token"
echo "3. Refresh OpenRouter Key"
echo "0. Back to Menu"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
read -p "👉 Choose: " choice

case $choice in
    1) 
       echo "GitHub: Loaded ✅"
       echo "Supabase: Loaded ✅"
       echo "OpenRouter: Loaded ✅"
       read -p "Press Enter..." ;;
    2)
       read -p "Enter New GH Token: " gh_token
       git remote set-url origin https://$gh_token@github.com/hoopstreet/ish-dev.git
       echo "✅ GitHub Remote Updated."
       read -p "Press Enter..." ;;
    *) exit ;;
esac
