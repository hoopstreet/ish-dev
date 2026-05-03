#!/bin/sh

cd ~/ish-dev || exit

export SYSTEM_NAME="ISH-DAG-ENGINE"
export VERSION="2.0"

API_KEY=$(grep GEMINI_API_KEY /root/.hoopstreet/creds/credentials.txt | cut -d= -f2)

