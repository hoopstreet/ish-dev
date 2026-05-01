#!/bin/bash
# Device identification for multi-device sync

DEVICE_ID_FILE="/root/.hoopstreet/device_id"
if [ ! -f "$DEVICE_ID_FILE" ]; then
    DEVICE_ID=$(uuidgen | tr -d '-' | cut -c1-16)
    echo "$DEVICE_ID" > "$DEVICE_ID_FILE"
    echo "✅ Device ID created: $DEVICE_ID"
else
    DEVICE_ID=$(cat "$DEVICE_ID_FILE")
fi

# Sync device info to Supabase
sync_device_info() {
    curl -X POST "https://ixdukafvxqermhgoczou.supabase.co/rest/v1/devices" \
        -H "apikey: $SUPABASE_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"device_id\":\"$DEVICE_ID\",\"last_sync\":\"$(date -Iseconds)\"}"
}
