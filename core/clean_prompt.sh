#!/bin/sh
# Simple clean prompt - no fancy banners that get read as commands

clear
echo "=== iSH Auto Healing Agent ==="
echo "Commands: master, setup, heal, status, exit"
echo ""

while true; do
    printf "localhost:~# "
    read user_input
    
    case "$user_input" in
        "master"|"phase")
            /root/master_phase.sh
            ;;
        "setup")
            /root/run_complete_setup.sh
            ;;
        "heal")
            echo "🔧 Running auto-heal..."
            python3 -c "
from pathlib import Path
p = Path('/root/broken.py')
if p.exists() and 'a - b' in p.read_text():
    p.write_text(p.read_text().replace('a - b', 'a + b'))
    print('✅ Fixed broken.py')
else:
    print('✅ No fix needed')
"
            ;;
        "status")
            echo ""
            echo "=== STATUS ==="
            echo "Python: $(python3 --version 2>&1)"
            if [ -f /root/broken.py ]; then
                echo "broken.py: $(cat /root/broken.py)"
            fi
            if [ -f /root/DNA.md ]; then
                echo "DNA.md: exists ($(wc -l < /root/DNA.md) lines)"
            fi
            echo ""
            ;;
        "exit"|"quit")
            echo "Goodbye!"
            break
            ;;
        "")
            continue
            ;;
        *)
            echo "Unknown: $user_input"
            echo "Use: master, setup, heal, status, exit"
            ;;
    esac
done
