#!/bin/sh
while true; do
    printf "localhost:~# "
    read cmd
    case $cmd in
        code) /root/master_enhanced.sh ;;
        status) python3 /root/status.py ;;
        heal) python3 /root/heal.py ;;
        log) cat /root/DNA.md ;;
        help) /root/startup_menu.sh ;;
        exit) echo "Bye!"; break ;;
        "") continue ;;
        *) echo "Unknown: $cmd. Use: code, status, heal, log, help, exit" ;;
    esac
done
