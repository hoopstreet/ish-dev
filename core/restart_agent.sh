#!/bin/sh
echo "🔄 Restarting Agent..."
echo ""
/root/setup_agent.sh
echo ""
echo "✅ Agent ready! Type 'start' or use /root/go_enhanced.sh"
echo ""
printf "localhost:~# "
