# ◈ PortScannerPro

**Advanced Network Port Scanner & Security Analyzer**  
*Final Term Project — Open Source Software Development (OSSD) · CLO4*

---

## 📌 Project Description

PortScannerPro is a full-featured, GUI-based network port scanner built entirely in Python with Tkinter. It provides real-time port scanning, service detection, banner grabbing, risk assessment, scan history management, and analytics — all through a sleek cyber-themed dark interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-threaded Scanning** | Scans hundreds of ports concurrently using `ThreadPoolExecutor` |
| **Service Detection** | Identifies 70+ services by port number |
| **Banner Grabbing** | Captures service banners for reconnaissance |
| **Risk Assessment** | Color-codes ports as Critical / High / Medium / Info |
| **Live Results** | Results appear in real time as ports are discovered |
| **Scan History** | All scans stored in SQLite; browse and replay anytime |
| **Analytics Dashboard** | KPI cards, bar charts, top services frequency analysis |
| **Export to CSV/JSON** | One-click export of scan results |
| **Saved Targets** | Save frequently scanned hosts for quick access |
| **Hostname Resolution** | Resolve DNS names to IPs before scanning |
| **Animated Splash Screen** | Professional startup loading animation |
| **Settings Persistence** | Timeout, threads, and options saved to SQLite |
| **Custom Port Ranges** | Presets or manual range entry |

---

## 🖥️ Screenshots

> Add screenshots after running the application — place images in `assets/` folder.

```
[ Scan Tab ]       [ History Tab ]     [ Dashboard Tab ]    [ Settings Tab ]
Live results       Past scan sessions  KPI cards + charts   App config + targets
```

---

## 🛠️ Technologies Used

| Category | Technology |
|---|---|
| Language | Python 3.8+ |
| GUI Framework | Tkinter (ttk + tk) |
| Database | SQLite3 (built-in) |
| Concurrency | `concurrent.futures.ThreadPoolExecutor` |
| Networking | `socket` (standard library) |
| Version Control | Git + GitHub |

**No external dependencies required!** Everything uses Python's standard library.

---

## ⚙️ Setup & Running

### Prerequisites
- Python 3.8 or newer
- No pip installs needed (all standard library)

### Clone & Run
```bash
git clone https://github.com/YOUR_USERNAME/PortScannerPro.git
cd PortScannerPro
python main.py
```

### Project Structure
```
PortScannerPro/
├── main.py                  # Entry point
├── README.md
├── requirements.txt
├── data/                    # SQLite database (auto-created)
│   └── portscanner.db
├── assets/                  # Screenshots / icons
└── modules/
    ├── __init__.py
    ├── database.py          # SQLite data layer
    ├── scanner.py           # Core scanning engine
    ├── splash_screen.py     # Animated startup screen
    ├── main_window.py       # Root window + theme
    ├── scan_tab.py          # 🖥 Screen 1: Scanner
    ├── history_tab.py       # 🖥 Screen 2: History
    ├── dashboard_tab.py     # 🖥 Screen 3: Dashboard
    └── settings_tab.py      # 🖥 Screen 4: Settings
```

---

## 🗺️ Application Screens

### Screen 1 — Scanner Tab
- Target input with hostname resolution
- Port preset selector + custom range
- Scan type (TCP Connect, Quick Sweep, Stealth)
- Live Treeview showing open ports in real time
- Color-coded risk levels
- Progress bar + stats (open, scanned, elapsed)
- Export to CSV and JSON

### Screen 2 — History Tab
- Master-detail view: sessions → open ports
- Delete sessions from history
- View banner grabs from past scans

### Screen 3 — Dashboard Tab
- 4 KPI cards: total scans, open ports, targets, avg time
- Activity table (last 20 scans)
- Top 8 services bar chart
- Open ports per session bar chart

### Screen 4 — Settings Tab
- Persist default timeout, threads, banner options
- Saved Targets manager (add/delete hosts)
- About info

---

## 🌐 GitHub Workflow

- **Branching strategy:** `main` → feature branches per member
- **PRs required** for all merges into `main`
- **Issues** used for task tracking

### Branches
| Branch | Owner | Feature |
|---|---|---|
| `feature/scanner-core` | Member 1 | Core scanning engine |
| `feature/gui-main` | Member 2 | Main window + scan tab |
| `feature/history-dashboard` | Member 3 | History + dashboard tabs |

---

## 👥 Team Contributions

| Member | Role | Contributions |
|---|---|---|
| **[Name 1]** | Group Lead | Project planning, scanner engine, database module |
| **[Name 2]** | Developer | Main window, scan tab, export features |
| **[Name 3]** | Developer | History tab, dashboard, settings, splash screen |

---

## 🔗 Links

- Repository: `https://github.com/YOUR_USERNAME/PortScannerPro`
- Issues: `https://github.com/YOUR_USERNAME/PortScannerPro/issues`
- Pull Requests: `https://github.com/YOUR_USERNAME/PortScannerPro/pulls`

---

## ⚠️ Disclaimer

This tool is built for **educational purposes** as part of a university project.  
Only scan systems you own or have explicit written permission to test.

---

## 📄 License

MIT License — Open Source. See `LICENSE` file.
