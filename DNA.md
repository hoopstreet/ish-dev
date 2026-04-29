# 🧬 DNA.md — ish-dev Evolution Log

## [v5.0.0] - 2026-04-29
Production release with complete agent system.

## [v5.1.0] - 2026-04-29

### 🎯 Task
Replace Supabase with Universal Credentials Manager

### 📂 Files Changed
**created:**
- /root/hoopstreet/creds.sh - Credentials manager

**modified:**
- /root/hoopstreet/menu.sh - Updated to v5.1
- /root/ish-dev/DNA.md - Added v5.1 entry

### ⚙️ Changes
- Removed Supabase dependency
- Added local credentials storage
- Store: GitHub tokens, API keys, passwords
- Simple add/list/get/delete interface
- Basic obfuscation for iSH

### 📊 Impact
Feature - Independent credentials management

---

## [v5.3.0] - 2026-04-29

### 🎯 Task
Add GitHub Actions workflow for automatic Supabase sync

### 📂 Files Added
- .github/workflows/sync-credentials.yml

### ⚙️ Changes
- Automatic sync on push to main branch
- Manual trigger via workflow_dispatch
- Uses GitHub Secrets for Supabase credentials

### 📊 Impact
Automation - CI/CD for credentials

---

## [v6.0.0] - 2026-04-29

### 🎯 Task
Complete system restructure with enhanced features

### 📂 Files Changed
- menu.sh - New 6-option menu
- code.sh - Auto-test and auto-fix
- sync.sh - Auto-versioning with DNA/roadmap
- heal.sh - Self-healing for all files
- status.sh - Combined dashboard
- remote.sh - Projects manager
- creds.sh - Credentials manager

### ⚙️ Features
- Code: Auto-test, auto-fix
- Sync: Auto-version, DNA/roadmap append
- Heal: Self-healing across all files
- Status: Complete dashboard
- Remote: Project clone/add/connect
- Credentials: Universal store

### 📊 Impact
Major - Complete system overhaul

---
