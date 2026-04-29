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
