#!/bin/sh

while true; do
    clear
    echo "==== HOOPSTREET V8 SAFE ===="
    echo "1. Run Code"
    echo "2. Status"
    echo "3. Recovery"
    echo "0. Exit"
    echo ""
    printf "Choose: "
    read c

    case $c in
        1) python3 /root/hoopstreet/agent.py ;;
        2) sh /root/hoopstreet/status.sh ;;
        3) sh /root/hoopstreet/recovery.sh ;;
        0) exit ;;
    esac
done
