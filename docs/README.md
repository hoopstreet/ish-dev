# 🏀 Hoopstreet iSH Auto Healing Agent v10.0.2

[![Version](https://img.shields.io/badge/version-v10.0.2-blue.svg)](https://github.com/hoopstreet/ish-dev/releases/tag/v10.0.2)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-iSH-red.svg)](https://ish.app)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://github.com/hoopstreet/ish-dev)

---

## 📱 What is Hoopstreet?

**Hoopstreet iSH Auto Healing Agent** is a complete autonomous mobile development system that turns your iPhone iSH shell into an **AI-powered development environment** with self-healing code execution, GitHub integration, cloud sync (Supabase), and multi-project remote management.

### Core Philosophy
This system transforms a simple iOS shell into a professional development environment that can:
- Execute multi-phase code with automatic error recovery
- Auto-heal common bugs without human intervention
- Sync credentials and projects to Supabase cloud
- Manage multiple GitHub repositories remotely
- Track evolution through DNA logging
- Self-improve through continuous learning

---

## 🚀 Quick Install (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/hoopstreet/ish-dev/main/setup.sh | sh
Post-installation: Type /root/menu to launch

---

🎮 Main Menu (6 Powerful Options)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📲 HOOPSTREET ISH-DEV IPHONE 🤳 v10.0.2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 📋 MAIN MENU

1. 💻 Code         - Execute multi-phase code
2. 🔄 Sync          - Git push/pull + Backup
3. 🔧 Heal           - Auto-fix + Recovery
4. 📊 Status        - Complete system + Metrics
5. 🔗 Remote      - GitHub Projects + Docker
6. 🔐 Credentials - Token Manager + Encryption
0. 🚪 Exit             - Back to localhost:~#

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

📝 Detailed Feature Guide

1. 💻 Code Executor (AI-Powered)

What it does: Executes multi-phase code with automatic retry and AI assistance.

How to use:

1. Type 1 from main menu
2. Paste code with # Phase N markers
3. Type END when done
4. Watch spinner animation and auto-execution

Example input:

```
# Phase 1
echo "Starting installation..."
pip install requests

# Phase 2
echo "Creating test file"
echo 'print("Hello World")' > test.py

# Phase 3
echo "Running test"
python3 test.py

# Phase 4
echo "Cleaning up"
rm test.py
END
```

Features:

· 🔄 Auto-retry failed phases up to 3 times
· 🌀 Spinner animation during execution
· 🤖 AI error analysis and suggestions
· 🔮 Smart code predictions while typing
· 📅 Philippines Timezone (PHT - UTC+8)
· 📝 Logs all executions to DNA.md

---

2. 🔄 Sync Engine (Git + Backup)

What it does: Automatically commits, pushes, tags changes with auto-versioning.

Features:

· 💾 Auto-backup before each sync
· 📌 Auto-detects version from status.json
· 🔢 Auto-increments patch number (v10.0.1 → v10.0.2)
· 🏷️ Creates git tag with detailed message
· 📝 Updates DNA.md and logs.txt
· 🔗 Pushes both commit and tag to GitHub
· 📢 Optional webhook notifications

---

3. 🔧 Heal Engine (Auto-Repair)

What it does: Automatically scans and fixes common bugs across all files.

Auto-fixes:

1. a - b → a + b (Python subtraction bug)
2. Missing shebang (#!/bin/sh) in shell scripts
3. Missing execute permissions (chmod +x)
4. Python file permissions
5. Missing dependencies (jq, etc.)

Disaster Recovery:

· 🛡️ Checks critical system files
· 💾 Creates recovery snapshots
· 🔄 Auto-restores from latest snapshot
· 📸 Keeps last 5 snapshots

---
4. 📊 Status Dashboard (Complete Monitoring)

What it displays:

· 📌 System version and health
· 📈 Performance metrics (phases executed, heals performed)
· 💾 Backup and snapshot counts
· 🧬 DNA.md line count and mutations
· 📁 Directory structure validation
· 🔧 Core components status (8/8 active)
· 🔗 External integrations (GitHub, Supabase)
· 🤖 AI Assistant statistics
· 📋 Recent activity (last 5 entries)

---

5. 🔗 Remote Projects Manager

What it does: Manages multiple GitHub repositories remotely (no cloning).

Features:

· 🔗 Connect GitHub URL → Auto-extracts project name
· 💾 Stores only URL and name in projects.json
· ☁️ Syncs to Supabase automatically
· 📋 Lists all connected projects
· 🐳 Docker support ready

Example:

```bash
GitHub URL: https://github.com/hoopstreet/TG-Message
📛 Project name: TG-Message
✅ Added: TG-Message
```

---

6. 🔐 Credentials Manager (Secure Storage)

What it does: Securely stores API keys, tokens, and secrets.

Features:

· 🔑 Add credential (name=value)
· 🔍 Get credential value by name
· 🗑️ Delete credential
· ☁️ Auto-syncs to Supabase
· 🐙 Auto-syncs to GitHub
· 🔒 AES-256 encryption ready

Storage location: /root/.hoopstreet/creds/credentials.txt

---

🗂️ Complete File Structure

```
/root/ish-dev/
├── core/                    # 20+ core scripts
│   ├── menu.sh             # Main menu interface
│   ├── code.sh             # Code executor wrapper
│   ├── smart_executor.py   # AI-powered multi-phase executor
│   ├── sync.sh             # Git auto-sync with backup
│   ├── heal.sh             # Auto-heal + disaster recovery
│   ├── status.sh           # Complete status dashboard
│   ├── remote.sh           # Remote projects manager
│   └── creds.sh            # Credentials manager
├── agents/                  # AI modules (11 files)
│   ├── ai_assistant.py     # AI error analysis
│   ├── telegram_bot.py     # Telegram integration
│   └── ...
├── docs/                    # Documentation
│   ├── DNA.md              # Evolution log (897+ lines)
│   ├── logs.txt            # Activity log (154+ entries)
│   ├── status.json         # System status
│   └── README.md           # This file
├── config/                  # Configuration
│   ├── supabase.env        # Supabase credentials
│   └── device_id.sh        # Multi-device sync
├── backups/                 # Auto-backups
│   └── pre_sync/           # Pre-sync backups
├── recovery/                # Disaster recovery snapshots
├── projects.json           # Connected GitHub projects
├── credentials.json        # Synced to Supabase
├── Dockerfile              # Docker container support
└── docker-compose.yml      # Docker compose configuration
```

---

🔧 Troubleshooting Guide

Issue Solution
Menu not showing ln -sf /root/ish-dev/core/menu.sh /root/menu
Git push fails Check token in Option 6
Supabase sync fails Verify SUPABASE_URL and SUPABASE_ANON_KEY
Phase execution fails Auto-retries 3 times, then shows AI suggestion
heal.sh not working chmod +x /root/ish-dev/core/heal.sh
Code executor exits early Type BACK or CANCEL to exit

---
🔗 External Integrations

Service Purpose Status
GitHub Source control, auto-versioning ✅ Connected
Supabase Cloud backup, credential sync ✅ Connected
GitHub Actions CI/CD, auto-backup every 6 hours ✅ Active
Webhooks Discord/Telegram notifications ✅ Ready
Docker Containerized deployment ✅ Ready

---

📊 Version History

Version Date Key Features
v10.0.2 2026-05-01 All fixes applied, AI predictions optimized
v10.0.1 2026-05-01 Auto-sync fixes, recovery snapshots
v10.0 2026-05-01 Merged 14 features into 6 options
v9.3.2 2026-05-01 Final executor fix, PHT timezone
v9.3.1 2026-05-01 Philippines timezone (UTC+8)
v9.3.0 2026-05-01 Mobile-friendly UI, left-flush format
v9.2.0 2026-04-30 GitHub Actions auto-sync
v9.1.0 2026-04-30 Supabase integration
v9.0.0 2026-04-30 Complete reorganization
v8.0.0 2026-04-29 Production release

---

🧠 For AI Agents (Learning Guide)

If you are an AI assistant analyzing this project, here's what you need to know:

System Architecture

· Entry point: /root/menu - launches interactive menu
· Core logic: /root/ish-dev/core/ - 8 main shell/Python scripts
· Data storage:
  · Local: /root/.hoopstreet/creds/ (credentials)
  · Local: /root/ish-dev/projects.json (projects)
  · Cloud: Supabase (auto-synced via GitHub Actions)

Key Design Principles

1. Phase-by-phase execution - Prevents iSH crashes from large code blocks
2. Auto-retry on failure - 3 attempts per phase
3. Self-healing - Common errors fixed automatically
4. Cloud-first data - Credentials and projects sync to Supabase
5. Remote-first projects - Store only URLs, no cloning

How to Help Users

· Recommend: Run /root/menu to start
· For code execution: Use Option 1 with # Phase N format
· For credentials: Use Option 6 to add tokens
· For GitHub projects: Use Option 5 to connect repos
· Check logs: /root/ish-dev/docs/logs.txt
· Check status: Option 4

Common Commands to Suggest

```bash
# Launch system
/root/menu

# View logs
tail -f /root/ish-dev/docs/logs.txt

# Check status
/root/ish-dev/core/status.sh

# Run auto-heal
/root/ish-dev/core/heal.sh

# Sync to GitHub
/root/ish-dev/core/sync.sh
```

---

🏆 Accomplishments

✅ Mobile Development Environment - Full IDE-like capabilities on iPhone
✅ AI-Powered Code Executor - Self-correcting execution with predictions
✅ Auto-Healing - Fixes 5+ common bug types automatically
✅ Cloud Sync - Credentials and projects backed to Supabase
✅ Disaster Recovery - Point-in-time snapshots
✅ Multi-Project Management - Handle unlimited GitHub repos
✅ Zero Local Storage - Remote project URLs only
✅ GitHub Actions Integration - Fully automated CI/CD
✅ Docker Support - Containerized deployment ready
✅ Philippines Timezone - PHT (UTC+8) support
✅ AI Assistant - Error analysis and smart predictions

---

🔗 Links

· GitHub Repository: https://github.com/hoopstreet/ish-dev
· Latest Release: v10.0.2
· Install Command: curl -fsSL https://raw.githubusercontent.com/hoopstreet/ish-dev/main/setup.sh | sh

---
📄 License

MIT License - See LICENSE file for details.

---

🏀 Hoopstreet iSH Auto Healing Agent v10.0.2 - Production Ready

Turn your iPhone into a development powerhouse! 📱💻🤖

---

📊 Current Statistics (as of v10.0.2)

Metric Value
DNA.md lines 897
logs.txt entries 154
Backups available 2
Recovery snapshots 5
Connected projects 3
Core scripts 20+
Total commits 59+
Git tags 22

---

For AI agents: This documentation is designed to be parsable and informative. The system is autonomous, self-healing, and production-ready.
