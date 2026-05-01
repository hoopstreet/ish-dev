#!/bin/sh
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 HOOPSTREET DATA COLLECTION v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

COLLECT_DIR="/tmp/hoopstreet_data_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$COLLECT_DIR"
cd /root/ish-dev

echo "📊 Collecting Git history..."
git log --oneline --all > "$COLLECT_DIR/git_log_all.txt"
git tag -l --sort=-v:refname > "$COLLECT_DIR/git_tags.txt"
git describe --tags > "$COLLECT_DIR/git_current_tag.txt"
git branch -a > "$COLLECT_DIR/git_branches.txt"
git remote -v > "$COLLECT_DIR/git_remotes.txt"

echo "📁 Collecting file structure..."
find /root/ish-dev -type f | sort > "$COLLECT_DIR/all_files.txt"
ls -la /root/ish-dev/core/ > "$COLLECT_DIR/core_listing.txt"

echo "📚 Collecting documentation..."
cp /root/ish-dev/docs/DNA.md "$COLLECT_DIR/" 2>/dev/null
cp /root/ish-dev/docs/logs.txt "$COLLECT_DIR/" 2>/dev/null
cp /root/ish-dev/docs/status.json "$COLLECT_DIR/" 2>/dev/null

echo "⚙️ Collecting configuration..."
cp /root/ish-dev/projects.json "$COLLECT_DIR/" 2>/dev/null

echo "💾 Collecting backup info..."
ls -la /root/ish-dev/backups/ > "$COLLECT_DIR/backups_list.txt" 2>/dev/null
ls -la /root/ish-dev/archive/ > "$COLLECT_DIR/archive_list.txt" 2>/dev/null

echo "🧬 Extracting version history..."
head -100 /root/ish-dev/docs/DNA.md > "$COLLECT_DIR/dna_head.txt"
tail -50 /root/ish-dev/docs/DNA.md > "$COLLECT_DIR/dna_tail.txt"

echo "🖥️ System information..."
uname -a > "$COLLECT_DIR/system_info.txt"
date > "$COLLECT_DIR/collection_date.txt"
python3 --version > "$COLLECT_DIR/python_version.txt"

echo "📈 Git statistics..."
git rev-list --all --count > "$COLLECT_DIR/commit_count.txt"
git log --oneline | wc -l > "$COLLECT_DIR/total_commits.txt"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" > "$COLLECT_DIR/SUMMARY.txt"
echo "📊 HOOPSTREET DATA COLLECTION SUMMARY" >> "$COLLECT_DIR/SUMMARY.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Collection date: $(date)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Current tag: $(git describe --tags 2>/dev/null)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Total commits: $(git rev-list --all --count)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Total tags: $(git tag | wc -l)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Total files: $(find /root/ish-dev -type f | wc -l)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "DNA.md lines: $(wc -l < /root/ish-dev/docs/DNA.md 2>/dev/null)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Logs.txt lines: $(wc -l < /root/ish-dev/docs/logs.txt 2>/dev/null)" >> "$COLLECT_DIR/SUMMARY.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$COLLECT_DIR/SUMMARY.txt"
echo "Last 10 DNA entries:" >> "$COLLECT_DIR/SUMMARY.txt"
tail -10 /root/ish-dev/docs/DNA.md 2>/dev/null | sed 's/^/  /' >> "$COLLECT_DIR/SUMMARY.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >> "$COLLECT_DIR/SUMMARY.txt"

cd /tmp
tar -czf "hoopstreet_data_$(date +%Y%m%d_%H%M%S).tar.gz" "$(basename "$COLLECT_DIR")"

echo ""
echo "✅ DATA COLLECTION COMPLETE!"
echo "📁 Data saved to: $COLLECT_DIR"
echo "📦 Archive: $(ls -t /tmp/hoopstreet_data_*.tar.gz | head -1)"
echo ""
echo "To view summary: cat $COLLECT_DIR/SUMMARY.txt"
