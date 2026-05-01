#!/bin/sh
if [ -f /root/.secrets/github.token ]; then
    TOKEN=$(cat /root/.secrets/github.token)
    echo "Fetching repositories..."
    curl -s -H "Authorization: token $TOKEN" "https://api.github.com/user/repos?per_page=10" | grep -o '"name": "[^"]*' | cut -d'"' -f4
else
    echo "No GitHub token found."
fi
read dummy
