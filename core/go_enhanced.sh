#!/bin/sh
clear
echo "════════════════════════════════════════"
echo "     🤖 iSH AUTO HEALING AGENT v4.0"
echo "════════════════════════════════════════"
echo ""
echo "Commands:"
echo "  e  - Enhanced master (with spinners & retry)"
echo "  m  - Basic master"
echo "  s  - Status"
echo "  h  - Heal"
echo "  t  - Test 20 phases"
echo "  q  - Quit"
echo ""

while true; do
    printf "> "
    read c
    case $c in
        e) /root/master_enhanced.sh ;;
        m) /root/master.sh ;;
        s) /root/status.sh ;;
        h) /root/heal.sh ;;
        t) /root/master_enhanced.sh < /root/complete_20_phases.multi ;;
        q) echo "Bye!"; break ;;
        *) echo "Use: e, m, s, h, t, q" ;;
    esac
done
