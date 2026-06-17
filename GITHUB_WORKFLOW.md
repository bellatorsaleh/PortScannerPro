# GHOST_SCANNER (PortScannerPro) — Complete GitHub Workflow & Member Division Guide

---

## 👥 TEAM DIVISION (3 Members)

### ═══════════════════════════════════════════════
### MEMBER 1 — GROUP LEAD  →  Syed Ali Saleh Abbas Naqvi
### "Scanner Core + Database"
### ═══════════════════════════════════════════════
**Files Owned:**
- main.py
- modules/database.py
- modules/scanner.py
- README.md
- requirements.txt
- .gitignore
- GITHUB_WORKFLOW.md

**Branch Name:** `feature/scanner-core`

**Responsibilities:**
- Create GitHub repository (public)
- Add all collaborators
- Set up the base project structure
- Build the scanning engine (scanner.py)
- Build the SQLite database layer (database.py)
- Write README.md and final documentation
- Merge all Pull Requests into main

---

### ═══════════════════════════════════════════════
### MEMBER 2  →  Muhammad Ahmad Asim
### "Main Window + Scanner Tab + Extra Tools"
### ═══════════════════════════════════════════════
**Files Owned:**
- modules/main_window.py
- modules/scan_tab.py

**Branch Name:** `feature/scan-tab`

**Responsibilities:**
- Build the main application window with elite hacker terminal theme
- Build the entire Scanner Tab (Screen 1), including:
  - Port Scan module — live results, risk coloring, progress tracking
  - Ping Tool module — ICMP diagnostics
  - Net Info module — local/external IP and DNS resolution
  - Banner Grab module — service fingerprinting
- CSV and JSON export buttons
- Live terminal-style scan log

---

### ═══════════════════════════════════════════════
### MEMBER 3  →  Muhammad Ali Inam
### "History + Dashboard + Settings"
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

## PHASE 1: SYED ALI SALEH ABBAS NAQVI (GROUP LEAD) — SETUP REPOSITORY

```bash
# ── STEP 1: Install Git (if not installed) ──────────────────
# Windows: Download from https://git-scm.com/download/win

# ── STEP 2: Configure Git globally (do once) ────────────────
git config --global user.name "Syed Ali Saleh Abbas Naqvi"
git config --global user.email "your.email@gmail.com"

# ── STEP 3: Go to project folder & init git ─────────────────
cd Desktop/PortScannerPro
git init
git branch -M main

# ── STEP 4: First commit ─────────────────────────────────────
git add .
git commit -m "Initial commit: Add complete PortScannerPro project structure"

# ── STEP 5: Create GitHub repository ────────────────────────
# Go to: https://github.com/new
# Repository name: PortScannerPro
# Set to: PUBLIC
# Do NOT initialize with README
# Click: Create repository

# ── STEP 6: Link local repo to GitHub and push ──────────────
git remote add origin https://github.com/bellatorsaleh/PortScannerPro.git
git push -u origin main

# ── STEP 7: Add collaborators on GitHub ─────────────────────
# GitHub → Settings → Collaborators → Add people
# Add Muhammad Ahmad Asim's GitHub username
# Add Muhammad Ali Inam's GitHub username
```

---

## PHASE 2: SYED ALI SALEH ABBAS NAQVI — WORK ON YOUR BRANCH

```bash
git checkout -b feature/scanner-core

git add modules/scanner.py
git commit -m "feat: Add multi-threaded port scanning engine with banner grabbing"

git add modules/database.py
git commit -m "feat: Add SQLite database layer for scan history and settings"

git add main.py
git commit -m "feat: Add main entry point"

git add README.md requirements.txt GITHUB_WORKFLOW.md
git commit -m "docs: Add complete README and workflow guide"

git push -u origin feature/scanner-core

# Open a Pull Request on GitHub → title: "feat: Scanner core - database, engine"
# Ask a teammate to review → Merge pull request
```

---

## PHASE 3: MUHAMMAD AHMAD ASIM — CLONE & START WORK

```bash
# ── Accept the GitHub invitation in your email first ────────

git config --global user.name "Muhammad Ahmad Asim"
git config --global user.email "your.email@gmail.com"

cd Desktop
git clone https://github.com/bellatorsaleh/PortScannerPro.git
cd PortScannerPro

git checkout -b feature/scan-tab

# Edit modules/main_window.py and modules/scan_tab.py

git add modules/main_window.py
git commit -m "feat: Add elite hacker terminal theme main window"

git add modules/scan_tab.py
git commit -m "feat: Add scanner tab with port scan, ping, net info, banner grab tools"

git push -u origin feature/scan-tab

# Open Pull Request on GitHub
# Title: "feat: Main window + Scanner Tab with extra recon tools"
```

---

## PHASE 4: MUHAMMAD ALI INAM — CLONE & START WORK

```bash
# ── Accept the GitHub invitation in your email first ────────

git config --global user.name "Muhammad Ali Inam"
git config --global user.email "your.email@gmail.com"

cd Desktop
git clone https://github.com/bellatorsaleh/PortScannerPro.git
cd PortScannerPro

git checkout -b feature/history-dashboard

# Edit modules/history_tab.py, modules/dashboard_tab.py, modules/settings_tab.py

git add modules/history_tab.py
git commit -m "feat: Add scan history tab with master-detail session viewer"

git add modules/dashboard_tab.py
git commit -m "feat: Add analytics dashboard with KPI cards and bar charts"

git add modules/settings_tab.py
git commit -m "feat: Add settings tab with persistence and saved targets manager"

git push -u origin feature/history-dashboard

# Open Pull Request on GitHub
# Title: "feat: History, Dashboard, Settings tabs"
```

---

## 📋 GITHUB ISSUES TO CREATE (for project management)

Go to GitHub → Issues → New Issue. Create these:

| # | Title | Assign To | Label |
|---|---|---|---|
| 1 | Set up project structure and GitHub repo | Syed Ali Saleh Abbas Naqvi | setup |
| 2 | Implement SQLite database module | Syed Ali Saleh Abbas Naqvi | feature |
| 3 | Implement port scanning engine | Syed Ali Saleh Abbas Naqvi | feature |
| 4 | Build main window with elite hacker theme | Muhammad Ahmad Asim | feature |
| 5 | Build Scanner Tab with live results | Muhammad Ahmad Asim | feature |
| 6 | Add Ping, Net Info, Banner Grab tools | Muhammad Ahmad Asim | feature |
| 7 | Add CSV and JSON export | Muhammad Ahmad Asim | feature |
| 8 | Build History Tab | Muhammad Ali Inam | feature |
| 9 | Build Analytics Dashboard | Muhammad Ali Inam | feature |
| 10 | Build Settings Tab and saved targets | Muhammad Ali Inam | feature |
| 11 | Write README.md documentation | Syed Ali Saleh Abbas Naqvi | docs |
| 12 | Final integration testing | All | testing |

---

## 🔄 DAILY WORKFLOW (every member, every day)

```bash
# ── Morning: Pull latest changes ────────────────────────────
git fetch origin
git status

# ── Work on your files ───────────────────────────────────────

# ── After every meaningful change: commit ────────────────────
git add <filename>
git commit -m "type: short description of what you did"

# ── End of day: push ─────────────────────────────────────────
git push origin YOUR-BRANCH-NAME

# ── If main branch updated: sync your branch ─────────────────
git fetch origin
git merge origin/main
git add .
git commit -m "merge: sync with main branch"
git push origin YOUR-BRANCH-NAME
```

---

## ✅ COMMIT MESSAGE FORMAT

```
type: short description (max 60 chars)

Types:
  feat     → new feature
  fix      → bug fix
  docs     → documentation
  style    → formatting only
  refactor → code restructure
  merge    → merging branches
  chore    → setup, config
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
├── main.py                       ← Syed Ali Saleh Abbas Naqvi
├── README.md                     ← Syed Ali Saleh Abbas Naqvi
├── requirements.txt              ← Syed Ali Saleh Abbas Naqvi
├── GITHUB_WORKFLOW.md             ← Syed Ali Saleh Abbas Naqvi
├── .gitignore                    ← Syed Ali Saleh Abbas Naqvi
│
├── data/
│   └── .gitkeep
│
├── assets/
│   ├── screenshot_dashboard.png
│   ├── screenshot_port_scan.png
│   ├── screenshot_ping_tool.png
│   └── screenshot_banner_grab.png
│
└── modules/
    ├── __init__.py                ← Syed Ali Saleh Abbas Naqvi
    ├── database.py                 ← Syed Ali Saleh Abbas Naqvi
    ├── scanner.py                  ← Syed Ali Saleh Abbas Naqvi
    ├── main_window.py               ← Muhammad Ahmad Asim
    ├── scan_tab.py                   ← Muhammad Ahmad Asim
    ├── history_tab.py                ← Muhammad Ali Inam
    ├── dashboard_tab.py               ← Muhammad Ali Inam
    └── settings_tab.py                ← Muhammad Ali Inam
```

---

## 🎯 TIMELINE SUGGESTION

| Day | Syed Ali Saleh Abbas Naqvi | Muhammad Ahmad Asim | Muhammad Ali Inam |
|---|---|---|---|
| Day 1 | Create repo, push all files, create issues | Clone repo, start main_window.py | Clone repo, start history_tab.py |
| Day 2 | Refine scanner.py, add edge cases | Build ping/net-info/banner-grab tools | Finish dashboard_tab.py charts |
| Day 3 | Finalize database.py, test DB | Test all 4 scanner sub-tools | Finish settings_tab.py |
| Day 4 | Open PR, review others' PRs | Open PR, review others' PRs | Open PR, review others' PRs |
| Day 5 | Merge all PRs, final testing | Help with testing | Help with testing + screenshots |
| Day 6 | Write Intra/Inter group reports | Submit contribution evidence | Submit contribution evidence |
