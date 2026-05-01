#!/bin/sh
clear
echo "════════════════════════════════════════"
echo "     🤖 iSH AUTO HEALING AGENT"
echo "════════════════════════════════════════"
echo ""
echo "Commands:"
echo "  master  - Run phase executor"
echo "  setup   - Complete setup"
echo "  heal    - Fix broken.py"
echo "  status  - Show status"
echo "  test    - Run test phases"
echo "  exit    - Quit"
echo ""

while true; do
    printf "localhost:~# "
    read cmd
    
    case "$cmd" in
        master) /root/master.sh ;;
        setup) /root/setup.sh ;;
        heal) /root/heal.sh ;;
        status) /root/status.sh ;;
        test) /root/master.sh < /root/test.phases ;;
        exit|quit) echo "Goodbye!"; break ;;
        "") continue ;;
        *) echo "Unknown: $cmd. Use: master, setup, heal, status, test, exit" ;;
    esac
done
