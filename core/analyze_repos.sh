#!/bin/sh
# HOOPSTREET REPOSITORY ANALYZER
# Gathers all local and GitHub repository information

echo "═══════════════════════════════════════════════════════"
echo "  🔍 HOOPSTREET REPOSITORY ANALYZER"
echo "═══════════════════════════════════════════════════════"
echo ""

# Create analysis directory
mkdir -p /tmp/hoopstreet_analysis
cd /tmp/hoopstreet_analysis
# ============================================================
# 1. GATHER LOCAL REPOSITORIES
# ============================================================
echo "📁 Analyzing LOCAL repositories..."

echo "# LOCAL REPOSITORIES" > local_repos.txt
echo "===================" >> local_repos.txt
echo "" >> local_repos.txt

# Find all git repositories
find /root -name ".git" -type d 2>/dev/null | while read gitdir; do
    repo_dir=$(dirname "$gitdir")
    echo "📍 Repository: $repo_dir" >> local_repos.txt
    cd "$repo_dir"
    
    # Get git info
    echo "   Branch: $(git branch --show-current 2>/dev/null)" >> local_repos.txt
    echo "   Remote: $(git remote -v 2>/dev/null | head -1)" >> local_repos.txt
    echo "   Last commit: $(git log -1 --format='%h - %s (%cr)' 2>/dev/null)" >> local_repos.txt
    echo "   Files: $(find . -type f -name "*.py" -o -name "*.sh" -o -name "*.md" 2>/dev/null | wc -l) files" >> local_repos.txt
    echo "" >> local_repos.txt
done
# ============================================================
# 2. GATHER ALL PYTHON AND SHELL SCRIPTS
# ============================================================
echo "📝 Gathering ALL script files..."

# Collect all .py files
find /root -name "*.py" -type f 2>/dev/null | head -100 > all_py_files.txt

# Collect all .sh files
find /root -name "*.sh" -type f 2>/dev/null | head -50 > all_sh_files.txt

# Collect all .md files
find /root -name "*.md" -type f 2>/dev/null | head -30 > all_md_files.txt

# ============================================================
# 3. GET GITHUB REPOSITORIES (via API)
# ============================================================
echo "🐙 Fetching GitHub repositories..."

# Try with stored token first
if [ -f /root/.secrets/github.token ]; then
    TOKEN=$(cat /root/.secrets/github.token)
    curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/user/repos?per_page=100" > github_repos.json
else
    curl -s "https://api.github.com/users/hoopstreet/repos?per_page=100" > github_repos.json
fi

echo "# GITHUB REPOSITORIES" > github_repos.txt
echo "====================" >> github_repos.txt
echo "" >> github_repos.txt

cat github_repos.json | grep -o '"name":"[^"]*"' | cut -d'"' -f4 >> github_repos.txt
# ============================================================
# 4. CREATE COMPREHENSIVE SUMMARY
# ============================================================
echo "📊 Creating comprehensive summary..."

cat > summary.txt << 'SUMMARYEOF'
═══════════════════════════════════════════════════════════
  HOOPSTREET SYSTEM ANALYSIS - COMPLETE REPORT
═══════════════════════════════════════════════════════════

SYSTEM INFORMATION
───────────────────────────────────────────────────────────
EOF

echo "Date: $(date)" >> summary.txt
echo "Host: $(hostname)" >> summary.txt
echo "Python: $(python3 --version 2>&1)" >> summary.txt
echo "" >> summary.txt

echo "SYSTEM FILES" >> summary.txt
echo "───────────────────────────────────────────────────────────" >> summary.txt
echo "Total .py files: $(cat all_py_files.txt 2>/dev/null | wc -l)" >> summary.txt
echo "Total .sh files: $(cat all_sh_files.txt 2>/dev/null | wc -l)" >> summary.txt
echo "Total .md files: $(cat all_md_files.txt 2>/dev/null | wc -l)" >> summary.txt
echo "" >> summary.txt
# ============================================================
# 5. CREATE DATA PACKAGE
# ============================================================
echo "📦 Creating data package..."

# Create tar archive
tar -czf hoopstreet_analysis.tar.gz \
    local_repos.txt \
    github_repos.txt \
    summary.txt \
    all_py_files.txt \
    all_sh_files.txt \
    all_md_files.txt \
    github_repos.json 2>/dev/null

# Also include key files
mkdir -p key_files
cp /root/ish-dev/DNA.md key_files/ 2>/dev/null
cp /root/ish-dev/ROADMAP.md key_files/ 2>/dev/null
cp /root/ish-dev/status.json key_files/ 2>/dev/null
cp /root/ish-dev/logs.txt key_files/ 2>/dev/null
cp /root/hoopstreet/menu.sh key_files/ 2>/dev/null
cp /root/hoopstreet/agent.py key_files/ 2>/dev/null

tar -rzf hoopstreet_analysis.tar.gz key_files/ 2>/dev/null
# ============================================================
# 6. CREATE READABLE OUTPUT
# ============================================================
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✅ ANALYSIS COMPLETE"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📁 Data package: /tmp/hoopstreet_analysis/hoopstreet_analysis.tar.gz"
echo ""

# Display summary
cat summary.txt

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  📋 TO SEND DATA:"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Option 1 - Copy the content and paste in chat:"
echo "  cat /tmp/hoopstreet_analysis/summary.txt"
echo "  cat /tmp/hoopstreet_analysis/local_repos.txt"
echo ""
echo "Option 2 - Share via GitHub Gist:"
echo "  cat /tmp/hoopstreet_analysis/hoopstreet_analysis.tar.gz | base64"
echo ""
echo "Option 3 - Upload to a temporary storage:"
echo "  curl -F 'file=@/tmp/hoopstreet_analysis/hoopstreet_analysis.tar.gz' https://tmp.ninja/upload"
echo ""
