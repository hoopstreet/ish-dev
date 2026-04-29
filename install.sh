#!/bin/sh

echo "🚀 HOOPSTREET V14 INSTALL STARTING..."

# folders
mkdir -p core ai engine security daemon memory logs .github/workflows runtime

# env loader
mkdir -p /root/.hoopstreet/creds

# dependencies
apk add --no-cache python3 py3-pip git curl bash

pip3 install requests python-dotenv

echo "✅ Base system installed"
