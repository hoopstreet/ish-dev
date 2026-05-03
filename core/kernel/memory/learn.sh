#!/bin/sh

cd ~/ish-dev || exit

INPUT="$1"
OUTPUT="$2"

echo "{\"input\":\"$INPUT\",\"output\":\"$OUTPUT\",\"score\":1}" \
>> core/kernel/memory/memory.json
