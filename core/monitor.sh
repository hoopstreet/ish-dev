#!/bin/sh
# SYSTEM MONITOR - Check health and status

echo "═══════════════════════════════════════════════════════"
echo "  📊 HOOPSTREET SYSTEM MONITOR"
echo "═══════════════════════════════════════════════════════"
echo ""


echo "📈 System Health:"
echo "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "  Memory: $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}')"
echo "  Disk: $(df -h / | awk 'NR==2{print $5}')"
echo ""

echo "📁 Hoopstreet Status:"
echo "  Core scripts: $(ls -1 /root/hoopstreet/*.sh 2>/dev/null | wc -l) files"
echo "  Python scripts: $(ls -1 /root/hoopstreet/*.py 2>/dev/null | wc -l) files"
echo "  Documentation: $(ls -1 /root/ish-dev/*.md 2>/dev/null | wc -l) files"
echo ""

echo "📋 Last DNA Update:"
tail -3 /root/ish-dev/DNA.md 2>/dev/null || echo "  No DNA.md yet"
echo ""

echo "🔄 Git Status:"
cd /root/ish-dev
git status --short | head -5 || echo "  Clean"
echo ""

read -p "Press Enter to continue..."
