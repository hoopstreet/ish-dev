#!/bin/sh

mkdir -p core/kernel/trash

find . -name "*.log" -type f | while read f; do
  mv "$f" core/kernel/trash/ 2>/dev/null
done
