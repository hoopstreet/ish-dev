#!/bin/sh
if [ "$1" = "setup" ]; then
    printf "Supabase URL: "; read url
    printf "Supabase Key: "; read key
    mkdir -p /root/.secrets
    echo "SUPABASE_URL=$url" > /root/.secrets/supabase.env
    echo "SUPABASE_KEY=$key" >> /root/.secrets/supabase.env
    echo "✅ Supabase configured"
else
    echo "Usage: setup | sync"
fi
read dummy
