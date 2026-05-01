#!/bin/sh
echo ""
echo "Simple iSH Agent"
echo ""
echo "Commands:"
echo "  s  - Status"
echo "  h  - Heal"
echo "  t  - Test phases"
echo "  m  - Master (paste code)"
echo "  q  - Quit"
echo ""

while true; do
    printf "> "
    read c
    case $c in
        s) /root/status.sh ;;
        h) /root/heal.sh ;;
        t) /root/master.sh < /root/test.phases ;;
        m) /root/master.sh ;;
        q) echo "Bye!"; break ;;
        *) echo "Use: s, h, t, m, q" ;;
    esac
done
