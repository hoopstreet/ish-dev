#!/bin/sh
# Simple loop that returns to localhost:~# prompt after each command

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🔄 INTERACTIVE COMMAND LOOP FOR iSH                ║"
echo "║   Execute commands and automatically return to prompt       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

while true; do
    printf "\n┌─────────────────────────────────────────────────────────┐\n"
    printf "│  ✅ Ready for next command                                │\n"
    printf "└─────────────────────────────────────────────────────────┘\n"
    printf "\nlocalhost:~# "
    
    read user_input
    
    case "$user_input" in
        "master"|"phase")
            /root/master_phase.sh
            ;;
        "setup")
            /root/run_complete_setup.sh
            ;;
        "heal")
            echo "🔧 Running auto-heal on broken.py..."
            python3 -c "
from pathlib import Path
p = Path('/root/broken.py')
if p.exists() and 'a - b' in p.read_text():
    p.write_text(p.read_text().replace('a - b', 'a + b'))
    print('✅ Fixed broken.py')
else:
    print('✅ File already correct or not found')
"
            ;;
        "status")
            echo "📊 Current status:"
            echo "   - Python: $(python3 --version)"
            echo "   - Pytest: $(pip show pytest 2>/dev/null | grep Version || echo 'not installed')"
            if [ -f /root/broken.py ]; then
                echo "   - broken.py: $(cat /root/broken.py | head -1)"
            fi
            if [ -f /root/DNA.md ]; then
                echo "   - DNA log: exists"
            fi
            ;;
        "exit"|"quit")
            echo "👋 Goodbye!"
            break
            ;;
        "")
            continue
            ;;
        *)
            echo "❌ Unknown command: $user_input"
            echo ""
            echo "Available commands:"
            echo "  master  - Run phase executor"
            echo "  setup   - Run complete setup"
            echo "  heal    - Auto-heal broken.py"
            echo "  status  - Show system status"
            echo "  exit    - Return to shell"
            echo ""
            ;;
    esac
done
