# PortScannerPro — Complete GitHub Workflow & Member Division Guide

---

## 👥 TEAM DIVISION (3 Members)

### ═══════════════════════════════════════════════
### MEMBER 1 — GROUP LEAD  →  "Scanner Core + Database"
### ═══════════════════════════════════════════════
**Files Owned:**
- main.py
- modules/database.py
- modules/scanner.py
- modules/splash_screen.py
- README.md
- requirements.txt
- .gitignore

**Branch Name:** `feature/scanner-core`

**Responsibilities:**
- Create GitHub repository
- Add all collaborators
- Set up the base project structure
- Build the scanning engine (scanner.py)
- Build the SQLite database layer (database.py)
- Build the animated splash screen
- Write README.md

---

### ═══════════════════════════════════════════════
### MEMBER 2  →  "Main Window + Scan Tab (Screen 1)"
### ═══════════════════════════════════════════════
**Files Owned:**
- modules/main_window.py
- modules/scan_tab.py

**Branch Name:** `feature/scan-tab`

**Responsibilities:**
- Build the main application window with tabbed layout
- Build the entire Scanner Tab (Screen 1)
- Target input, port presets, scan controls
- Live results treeview with color-coded risk
- Progress bar, stats panel
- CSV and JSON export buttons
- Scan log console

---

### ═══════════════════════════════════════════════
### MEMBER 3  →  "History + Dashboard + Settings (Screens 2,3,4)"
### ═══════════════════════════════════════════════
**Files Owned:**
- modules/history_tab.py
- modules/dashboard_tab.py
- modules/settings_tab.py

**Branch Name:** `feature/history-dashboard`

**Responsibilities:**
- Build History Tab (Screen 2) — past sessions viewer
- Build Dashboard Tab (Screen 3) — KPI cards + charts
- Build Settings Tab (Screen 4) — preferences + saved targets
- Ensure all tabs integrate with database.py

---

## 🚀 COMPLETE GITHUB WORKFLOW — STEP BY STEP

---

## PHASE 1: MEMBER 1 (GROUP LEAD) — SETUP REPOSITORY

```bash
# ── STEP 1: Install Git (if not installed) ──────────────────
# Windows: Download from https://git-scm.com/download/win
# Mac:
brew install git
# Linux/Ubuntu:
sudo apt install git

# ── STEP 2: Configure Git globally (do once) ────────────────
git config --global user.name "Your Full Name"
git config --global user.email "your.email@gmail.com"

# ── STEP 3: Create the project folder & init git ────────────
mkdir PortScannerPro
cd PortScannerPro

# Copy all provided project files into this folder first, then:
git init
git branch -M main

# ── STEP 4: Create .gitignore ───────────────────────────────
# Create a file named .gitignore with this content:
# __pycache__/
# *.pyc
# *.pyo
# data/portscanner.db
# .env
# .DS_Store
# Thumbs.db

# ── STEP 5: First commit ─────────────────────────────────────
git add .
git commit -m "Initial commit: Add complete PortScannerPro project structure"

# ── STEP 6: Create GitHub repository ────────────────────────
# Go to: https://github.com/new
# Repository name: PortScannerPro
# Set to: PUBLIC
# Do NOT initialize with README (you already have files)
# Click: Create repository

# ── STEP 7: Link local repo to GitHub and push ──────────────
git remote add origin https://github.com/YOUR_USERNAME/PortScannerPro.git
git push -u origin main

# ── STEP 8: Add collaborators on GitHub ─────────────────────
# GitHub → Settings → Collaborators → Add people
# Add Member 2's GitHub username
# Add Member 3's GitHub username
# They will receive an email invitation to accept
```

---

## PHASE 2: MEMBER 1 — WORK ON YOUR BRANCH

```bash
# ── Create your feature branch ──────────────────────────────
git checkout -b feature/scanner-core

# ── Make your changes (edit scanner.py, database.py, etc.) ──

# ── Stage and commit your work ──────────────────────────────
git add modules/scanner.py
git commit -m "feat: Add multi-threaded port scanning engine with banner grabbing"

git add modules/database.py
git commit -m "feat: Add SQLite database layer for scan history and settings"

git add modules/splash_screen.py
git commit -m "feat: Add animated cyber-themed splash screen"

git add main.py
git commit -m "feat: Add main entry point with splash → main window flow"

git add README.md requirements.txt
git commit -m "docs: Add complete README and requirements"

# ── Push your branch to GitHub ──────────────────────────────
git push -u origin feature/scanner-core

# ── Open a Pull Request on GitHub ───────────────────────────
# Go to: https://github.com/YOUR_USERNAME/PortScannerPro
# You'll see: "Compare & pull request" button → Click it
# Title: "feat: Scanner core - database, engine, splash screen"
# Description: List what you did
# Click: Create Pull Request
# Ask Member 2 or 3 to review and approve
# Then click: Merge pull request
```

---

## PHASE 3: MEMBER 2 — CLONE & START WORK

```bash
# ── STEP 1: Accept GitHub invitation (check your email) ──────

# ── STEP 2: Clone the repository ─────────────────────────────
git clone https://github.com/GROUP_LEAD_USERNAME/PortScannerPro.git
cd PortScannerPro

# ── STEP 3: Configure your identity ──────────────────────────
git config --global user.name "Member 2 Name"
git config --global user.email "member2@gmail.com"

# ── STEP 4: Create your feature branch ───────────────────────
git checkout -b feature/scan-tab

# ── STEP 5: Work on your files ───────────────────────────────
# Edit modules/main_window.py and modules/scan_tab.py

# ── STEP 6: Commit your work in stages ───────────────────────
git add modules/main_window.py
git commit -m "feat: Add main window with dark cyber theme and ttk styles"

git add modules/scan_tab.py
git commit -m "feat: Add scanner tab with live results, risk coloring, export"

# ── STEP 7: Push your branch ─────────────────────────────────
git push -u origin feature/scan-tab

# ── STEP 8: Keep your branch up to date with main ────────────
git fetch origin
git merge origin/main

# ── STEP 9: Open Pull Request ────────────────────────────────
# Go to GitHub → Compare & pull request
# Title: "feat: Main window + Scanner Tab (Screen 1)"
# Ask Group Lead to review
```

---

## PHASE 4: MEMBER 3 — CLONE & START WORK

```bash
# ── STEP 1: Accept GitHub invitation ─────────────────────────

# ── STEP 2: Clone the repository ─────────────────────────────
git clone https://github.com/GROUP_LEAD_USERNAME/PortScannerPro.git
cd PortScannerPro

# ── STEP 3: Configure your identity ──────────────────────────
git config --global user.name "Member 3 Name"
git config --global user.email "member3@gmail.com"

# ── STEP 4: Create your feature branch ───────────────────────
git checkout -b feature/history-dashboard

# ── STEP 5: Work on your files ───────────────────────────────
# Edit modules/history_tab.py, modules/dashboard_tab.py, modules/settings_tab.py

# ── STEP 6: Commit your work ─────────────────────────────────
git add modules/history_tab.py
git commit -m "feat: Add scan history tab with master-detail session viewer"

git add modules/dashboard_tab.py
git commit -m "feat: Add analytics dashboard with KPI cards and bar charts"

git add modules/settings_tab.py
git commit -m "feat: Add settings tab with persistence and saved targets manager"

# ── STEP 7: Push your branch ─────────────────────────────────
git push -u origin feature/history-dashboard

# ── STEP 8: Open Pull Request ────────────────────────────────
# Title: "feat: History, Dashboard, Settings tabs (Screens 2-4)"
```

---

## 📋 GITHUB ISSUES TO CREATE (for project management)

Go to GitHub → Issues → New Issue. Create these:

| # | Title | Assign To | Label |
|---|---|---|---|
| 1 | Set up project structure and GitHub repo | Member 1 | setup |
| 2 | Implement SQLite database module | Member 1 | feature |
| 3 | Implement port scanning engine | Member 1 | feature |
| 4 | Build animated splash screen | Member 1 | feature |
| 5 | Build main window with theme | Member 2 | feature |
| 6 | Build Scanner Tab with live results | Member 2 | feature |
| 7 | Add CSV and JSON export | Member 2 | feature |
| 8 | Build History Tab | Member 3 | feature |
| 9 | Build Analytics Dashboard | Member 3 | feature |
| 10 | Build Settings Tab and saved targets | Member 3 | feature |
| 11 | Write README.md documentation | Member 1 | docs |
| 12 | Final integration testing | All | testing |

---

## 🔄 DAILY WORKFLOW (every member, every day)

```bash
# ── Morning: Pull latest changes ────────────────────────────
git fetch origin
git status

# ── Work on your files ───────────────────────────────────────
# (make edits...)

# ── After every meaningful change: commit ────────────────────
git add <filename>
git commit -m "type: short description of what you did"

# ── End of day: push ─────────────────────────────────────────
git push origin YOUR-BRANCH-NAME

# ── If main branch updated: sync your branch ─────────────────
git fetch origin
git merge origin/main
# If conflicts appear: fix them, then:
git add .
git commit -m "merge: sync with main branch"
git push origin YOUR-BRANCH-NAME
```

---

## ✅ COMMIT MESSAGE FORMAT

Use this format for all commits:

```
type: short description (max 60 chars)

Types:
  feat     → new feature
  fix      → bug fix
  docs     → documentation
  style    → formatting only
  refactor → code restructure
  test     → adding tests
  merge    → merging branches
  chore    → setup, config

Examples:
  feat: Add banner grabbing to scanner engine
  fix: Fix crash when port range is invalid
  docs: Update README with setup instructions
  merge: Sync feature/scan-tab with main
```

---

## 🔁 PULL REQUEST CHECKLIST

Before merging any PR:
- [ ] Code runs without errors
- [ ] Feature works as described
- [ ] No unrelated files changed
- [ ] Commit messages are clear
- [ ] At least 1 team member reviewed it

---

## 📁 FINAL REPOSITORY STRUCTURE ON GITHUB

```
PortScannerPro/  (public repo)
│
├── main.py                    ← Member 1
├── README.md                  ← Member 1
├── requirements.txt           ← Member 1
├── .gitignore                 ← Member 1
│
├── data/
│   └── .gitkeep              ← keeps folder tracked in git
│
├── assets/
│   └── (screenshots here)    ← All members add screenshots
│
└── modules/
    ├── __init__.py            ← Member 1
    ├── database.py            ← Member 1
    ├── scanner.py             ← Member 1
    ├── splash_screen.py       ← Member 1
    ├── main_window.py         ← Member 2
    ├── scan_tab.py            ← Member 2
    ├── history_tab.py         ← Member 3
    ├── dashboard_tab.py       ← Member 3
    └── settings_tab.py        ← Member 3
```

---

## 🎯 TIMELINE SUGGESTION

| Day | Member 1 | Member 2 | Member 3 |
|---|---|---|---|
| Day 1 | Create repo, push all files, create issues | Clone repo, start main_window.py | Clone repo, start history_tab.py |
| Day 2 | Refine scanner.py, add edge cases | Finish scan_tab.py, test live scan | Finish dashboard_tab.py charts |
| Day 3 | Finalize database.py, test DB | Test export CSV/JSON | Finish settings_tab.py |
| Day 4 | Open PR, review others' PRs | Open PR, review others' PRs | Open PR, review others' PRs |
| Day 5 | Merge all PRs, final testing | Help with testing | Help with testing + screenshots |
| Day 6 | Write Intra/Inter group reports | Submit contribution evidence | Submit contribution evidence |
