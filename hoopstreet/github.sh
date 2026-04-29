#!/bin/sh
if [ -f /root/.secrets/github.token ]; then
    TOKEN=$(cat /root/.secrets/github.token)
    echo "Fetching repositories..."
    curl -s -H "Authorization: token $TOKEN" "https://api.github.com/user/repos?per_page=10" | grep -o '"name": "[^"]*' | cut -d'"' -f4
else
    echo "No GitHub token found."
fi
read dummy
ub.com/user/repos?per_page=30" | \
    grep -o '"name": "[^"]*' | cut -d'"' -f4 > /root/projects_list.txt

echo "✅ Found $(wc -l < /root/projects_list.txt) repositories"
cat /root/projects_list.txt | head -10
