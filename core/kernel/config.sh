#!/bin/sh

cd ~/ish-dev || exit

set -a
[ -f .env ] && . .env
set +a

SYSTEM_NAME="ISH-AI-OS"
VERSION="3.0-KERNEL"
LOG_DIR="core/kernel/logs"
MEM_DIR="core/kernel/memory"

mkdir -p "$LOG_DIR" "$MEM_DIR"
