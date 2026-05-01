#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏀 HOOPSTREET COMPLETE UPGRADE v9.3.2 → v10.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run all tests
/root/ish-dev/tests/test_all.sh

# Create recovery snapshot
/root/ish-dev/core/recovery.sh snapshot

# Update status
/root/ish-dev/core/status.sh

echo ""
echo "✅ UPGRADE COMPLETE!"
echo "📦 New features available:"
echo "   • Encrypted credentials"
echo "   • Auto-backup scheduler"
echo "   • Disaster recovery"
echo "   • AI assistant"
echo "   • Telegram bot"
echo "   • Docker support"
echo ""
echo "Type /root/menu to start"
