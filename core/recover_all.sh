#!/bin/sh
echo "🛠️ HOOPSTREET: Running Post-Recovery Cleanup..."

# 1. Ensure internal folder structure
mkdir -p /root/ish-dev/core /root/ish-dev/docs /root/ish-dev/recovery

# 2. Set strict permissions for all recovered scripts
chmod +x /root/ish-dev/core/*.sh
chmod +x /root/ish-dev/core/*.py

# 3. Re-map the global 'hoopstreet' command
ln -sf /root/ish-dev/core/menu.sh /usr/local/bin/hoopstreet

echo "✅ [SUCCESS] All fragments re-aligned and permissions set."

# 3. Re-map the global 'hoopstreet' command
ln -sf /root/ish-dev/core/menu.sh /usr/local/bin/hoopstreet

echo "✅ [SUCCESS] All fragments re-aligned and permissions set."
