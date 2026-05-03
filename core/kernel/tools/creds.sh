#!/bin/sh

cd ~/ish-dev || exit

grep -E "SUPABASE|GEMINI|OPENROUTER" .env 2>/dev/null
