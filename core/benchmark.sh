#!/bin/bash
# Performance benchmarking

echo "🏃 HOOPSTREET BENCHMARK"

# Test 10-phase execution
START=$(date +%s%N)
echo -e "# Phase 1\necho '1'\n# Phase 2\necho '2'\n# Phase 3\necho '3'\n# Phase 4\necho '4'\n# Phase 5\necho '5'\n# Phase 6\necho '6'\n# Phase 7\necho '7'\n# Phase 8\necho '8'\n# Phase 9\necho '9'\n# Phase 10\necho '10'\nEND" | python3 /root/ish-dev/core/smart_executor.py > /dev/null 2>&1
END=$(date +%s%N)
TIME=$((($END - $START)/1000000))

echo "10-phase execution: ${TIME}ms"
echo "Average per phase: $(($TIME/10))ms"
