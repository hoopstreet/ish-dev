#!/bin/bash
# Webhook notifications for important events

WEBHOOK_URL=""  # Configure your Discord/Slack webhook

send_notification() {
    local message="$1"
    local webhook_url="${WEBHOOK_URL:-$2}"
    
    if [ -n "$webhook_url" ]; then
        curl -X POST "$webhook_url" \
            -H "Content-Type: application/json" \
            -d "{\"content\":\"🏀 Hoopstreet Alert: $message\"}"
    fi
}

# Send on critical events
notify_sync_complete() {
    send_notification "✅ Sync completed: v$(cat /root/ish-dev/docs/status.json | grep version | cut -d'"' -f4)"
}

notify_error() {
    send_notification "❌ Error detected: $1"
}
