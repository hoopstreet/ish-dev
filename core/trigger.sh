#!/bin/sh
TOKEN=$(cat /root/.secrets/github.token)
OWNER="hoopstreet"
REPO="ish-dev"
# ⚠️ MAKE SURE THIS FILENAME MATCHES EXACTLY IN YOUR REPO
WORKFLOW="hoopstreet-auto-sync.yml" 

echo "🏀 Hoopstreet AI Sync Debugger"
echo "──────────────────────────────"

# 1. Check if the token can even see the repo
echo "🔍 Checking repo access..."
REPO_CHECK=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO)

if [ "$REPO_CHECK" != "200" ]; then
    echo "❌ Repo Access Failed (HTTP $REPO_CHECK)"
    echo "   Check if your token has 'repo' permissions."
    exit 1
fi

# 2. Check if the workflow file exists
echo "🔍 Checking workflow file: $WORKFLOW"
WF_CHECK=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/contents/.github/workflows/$WORKFLOW)

if [ "$WF_CHECK" != "200" ]; then
    echo "❌ Workflow file NOT FOUND (HTTP $WF_CHECK)"
    echo "   Ensure the file is at .github/workflows/$WORKFLOW"
    exit 1
fi

# 3. Attempt Trigger
echo "🚀 Dispatching workflow..."
RESPONSE=$(curl -s -w "%{http_code}" -o /dev/null -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW/dispatches \
  -d '{"ref":"main"}')

if [ "$RESPONSE" = "204" ]; then
    echo "✅ SUCCESS! AI Sync Started."
    echo "🔗 https://github.com/$OWNER/$REPO/actions"
else
    echo "❌ Trigger Failed (HTTP $RESPONSE)"
fi
sleep 2
