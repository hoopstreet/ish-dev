#!/bin/bash
# Performance metrics collection

METRICS_FILE="/root/ish-dev/docs/metrics.json"

collect_metrics() {
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"cpu\": $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1),"
    echo "  \"memory\": $(free -m | awk 'NR==2{printf "%.2f", $3*100/$2 }'),"
    echo "  \"disk\": $(df -h / | awk 'NR==2{print $5}' | tr -d '%'),"
    echo "  \"phases_executed\": $(grep -c "Phase.*SUCCESS" /root/ish-dev/docs/logs.txt),"
    echo "  \"total_heals\": $(grep -c "✅ Fixed" /root/ish-dev/docs/logs.txt)"
    echo "}"
}

show_metrics() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 PERFORMANCE METRICS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    collect_metrics | jq '.' 2>/dev/null || collect_metrics
}

case "$1" in
    collect) collect_metrics >> "$METRICS_FILE" ;;
    show) show_metrics ;;
    *) show_metrics ;;
esac
