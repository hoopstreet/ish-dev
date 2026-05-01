# 🤖 AI Agent Learning Guide for Hoopstreet

## Purpose of This Document

This document helps AI assistants understand the Hoopstreet iSH Auto Healing Agent system so they can effectively help users.

---
## System Overview

**What is Hoopstreet?**
A complete autonomous mobile development system that runs inside iSH (iOS shell emulator) on iPhone/iPad.

**Core Capabilities:**
- Execute multi-phase code phase by phase (prevents iSH crashes)
- Auto-heal common bugs automatically
- Sync to GitHub with auto-versioning
- Backup to Supabase cloud
- Track evolution through DNA.md

---

## Architecture

### Three-Layer Design
```

iSH Device (Controller) → GitHub (Source of Truth) → Supabase (Cloud Backup)

```

### Directory Structure
```

/root/ish-dev/
├── core/          # Main scripts (8 files)
├── agents/        # AI modules (11 files)
├── docs/          # DNA.md, logs.txt, status.json
├── config/        # Supabase config
├── backups/       # Auto-backups
├── recovery/      # Disaster recovery snapshots
└── projects.json  # Connected GitHub repos

```

---

## Key Files for Understanding

| File | Purpose | What to Look For |
|------|---------|------------------|
| `docs/DNA.md` | Evolution log | Version history, changes, mutations |
| `docs/logs.txt` | Activity log | Success/failure records, timestamps |
| `docs/status.json` | Current state | Version, health, component status |
| `projects.json` | Connected projects | GitHub repo URLs and names |
| `core/smart_executor.py` | Main executor | Phase detection, AI integration |

---

## How to Help Users

### Common User Questions & Answers

**Q: "The code executor isn't working"**
A: Check if they're using `# Phase N` format and ending with `END`

**Q: "Git push failed"**
A: They need to add GITHUB_TOKEN in Option 6

**Q: "How do I run long code without crashing?"**
A: Split into phases with `# Phase 1`, `# Phase 2`, etc.

**Q: "Where are my credentials stored?"**
A: `/root/.hoopstreet/creds/credentials.txt` (encrypted)

**Q: "How do I recover from a bad update?"**
A: Run Option 3 (Heal) which auto-restores from snapshots

---

## Diagnostic Commands for AI to Suggest

```bash
# Check system health
/root/ish-dev/core/status.sh

# View recent activity
tail -20 /root/ish-dev/docs/logs.txt

# Check version history
git tag -l --sort=-v:refname | head -10

# Run full diagnostic
/root/ish-dev/scripts/collect_all_data.sh

# Check if files are intact
ls -la /root/ish-dev/core/
```

---
Understanding the Code Executor

Input Format

```
# Phase 1
command1

# Phase 2
command2

END
```

Output Indicators

· ✅ = Success
· ❌ = Failure
· ⣾⣽⣻⢿⡿⣟⣯⣷ = Spinner (executing)
· 🤖 AI SUGGESTION = AI error analysis
· 🔮 = Code prediction

---

Understanding Auto-Versioning

Sync engine (Option 2) automatically:

1. Reads current version from status.json
2. Increments patch (v10.0.1 → v10.0.2)
3. Creates backup
4. Commits changes
5. Creates git tag
6. Pushes to GitHub

---

Troubleshooting Flow

```
User reports issue
    ↓
Check logs.txt for errors
    ↓
Run Option 3 (Heal)
    ↓
If still broken, run Option 4 (Status)
    ↓
Check specific component
    ↓
Suggest fix or reinstall
```

---

Important Notes for AI

1. Always suggest splitting code into phases - iSH crashes with large blocks
2. Never suggest running large scripts directly - Use the code executor
3. Credentials are stored securely - Don't ask users to share them
4. The system is autonomous - It self-heals, don't overcomplicate
5. Philippines timezone is default - PHT (UTC+8)

---

Version Compatibility

Version Range Features
v1.0.0 - v5.0.0 Basic execution
v6.0.0 - v8.0.0 GitHub integration
v9.0.0 - v9.3.2 Supabase + Mobile UI
v10.0+ Enterprise + AI

---

Quick Reference Card

```bash
# Most useful commands for AI to suggest
/root/menu                           # Launch system
tail -20 /root/ish-dev/docs/logs.txt # View recent activity
/root/ish-dev/core/status.sh         # Full status
/root/ish-dev/core/heal.sh           # Auto-repair
```

---

This document helps AI assistants understand the Hoopstreet system. For user documentation, see README.md
