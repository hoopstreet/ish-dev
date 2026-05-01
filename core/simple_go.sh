#!/bin/sh
clear
echo "════════════════════════════════════════"
echo "     🤖 SIMPLE iSH AGENT"
echo "════════════════════════════════════════"
echo ""
echo "Commands:"
echo "  code  - Paste multi-phase code"
echo "  status- Show status"
echo "  heal  - Fix broken.py"
echo "  exit  - Quit"
echo ""

while true; do
    printf "> "
    read cmd
    case $cmd in
        code) /root/master_enhanced.sh ;;
        status) python3 /root/status.py ;;
        heal) python3 /root/heal.py ;;
        exit|quit) echo "Bye!"; break ;;
        *) echo "Use: code, status, heal, exit" ;;
    esac
done
