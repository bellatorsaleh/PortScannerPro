# ◈ GHOST_SCANNER (PortScannerPro v3.0)

### **Professional Network Scanning & Security Analysis Toolkit**

*Final Term Project — Open Source Software Development (OSSD) | CLO4*

---

## 📌 Overview

GHOST_SCANNER is a desktop-based network security application created in Python using Tkinter. It is designed to perform fast and efficient network reconnaissance through multiple built-in tools. The software combines port scanning, network testing, service identification, and system analysis in one place.

With its hacker-style terminal interface and live output system, it offers a practical environment for understanding network behavior and performing security checks.

---

## ✨ Main Features

| Feature                         | Details                                                                          |
| ------------------------------- | -------------------------------------------------------------------------------- |
| **Thread-Based Port Scanning**  | Scans multiple ports at the same time for better speed and performance           |
| **Port Service Recognition**    | Detects and labels 70+ common services based on port numbers                     |
| **Banner Detection Tool**       | Connects to services and collects banners for identification                     |
| **Ping Utility**                | Checks target availability using ICMP packets                                    |
| **Network Information Checker** | Shows hostname, internal IP, public IP, and DNS test results                     |
| **Port Risk Classification**    | Marks ports according to severity levels such as Critical, High, Medium, and Low |
| **Live Scan Monitoring**        | Displays results instantly during scanning                                       |
| **Scan History Database**       | Stores all completed scans in SQLite for later review                            |
| **Statistics Dashboard**        | Shows charts, KPIs, and service frequency reports                                |
| **Data Export Support**         | Allows exporting results into CSV and JSON files                                 |
| **Saved Host Manager**          | Stores frequently scanned targets for quick use                                  |
| **Terminal Theme UI**           | Matrix-inspired green interface with animated terminal effects                   |

---

## 🖼️ Screenshots

### Dashboard View

![Dashboard](assets/screenshot_dashboard.png)

### Port Scanner Interface

![Port Scan](assets/screenshot_port_scan.png)

### Ping Utility Window

![Ping Tool](assets/screenshot_ping_tool.png)

### Banner Detection Module

![Banner Grab](assets/screenshot_banner_grab.png)

---

## 🛠️ Tools & Technologies

| Category             | Technology                        |
| -------------------- | --------------------------------- |
| Programming Language | Python 3.8+                       |
| GUI Library          | Tkinter (ttk + tk)                |
| Database System      | SQLite3                           |
| Multithreading       | `ThreadPoolExecutor`, `threading` |
| Networking Modules   | `socket`, `subprocess`            |
| Version Control      | Git + GitHub                      |

**No third-party libraries are needed.** The whole project uses Python standard libraries.

---

## ⚙️ Installation Guide

### Requirements

* Python 3.8 or higher
* No extra package installation required

### Clone and Start

```bash
git clone https://github.com/bellatorsaleh/PortScannerPro.git
cd PortScannerPro
python main.py
```

---

## 📁 Project Layout

```bash
PortScannerPro/
├── main.py                  # Main file to start application
├── README.md
├── requirements.txt
├── GITHUB_WORKFLOW.md
├── data/
│   └── portscanner.db
├── assets/
│   ├── screenshot_dashboard.png
│   ├── screenshot_port_scan.png
│   ├── screenshot_ping_tool.png
│   └── screenshot_banner_grab.png
└── modules/
    ├── __init__.py
    ├── database.py
    ├── scanner.py
    ├── main_window.py
    ├── scan_tab.py
    ├── history_tab.py
    ├── dashboard_tab.py
    └── settings_tab.py
```

---

## 🖥️ System Modules

### Screen 1 — Scanner Panel

Contains 4 built-in tools:

* **Port Scanner** — Scan targets using presets or custom port ranges
* **Ping Tool** — Test connectivity and response time
* **Network Info** — View host and DNS-related information
* **Banner Grabber** — Capture service banners from target ports
* Supports CSV and JSON export
* Includes live terminal logs

---

### Screen 2 — History Section

* Displays all previous scan sessions
* Shows open ports found in each session
* Remove old records
* Access previous banner results

---

### Screen 3 — Analytics Dashboard

Provides:

* Total number of scans
* Number of open ports detected
* Total unique targets scanned
* Average scan duration
* Latest scan activity table
* Most common open services graph

---

### Screen 4 — Settings Panel

Includes:

* Timeout and thread configuration
* Banner grab options
* Manage saved target list
* Application information

---

## 🌍 GitHub Development Process

Project follows a branch-based workflow:

* `main` branch for stable code
* Separate feature branches for each team member
* Pull Requests required before merging
* GitHub Issues used for task organization

### Branches

| Branch                      | Assigned To                | Task                                                      |
| --------------------------- | -------------------------- | --------------------------------------------------------- |
| `feature/scanner-core`      | Syed Ali Saleh Abbas Naqvi | Core scanner logic, database, splash screen               |
| `feature/scan-tab`          | Muhammad Ahmad Asim        | UI design, scanner tab, ping tool, network tools, exports |
| `feature/history-dashboard` | Muhammad Ali Inam          | History records, dashboard analytics, settings module     |

---

## 👥 Team Work Distribution

| Member                         | Position    | Responsibilities                                                            |
| ------------------------------ | ----------- | --------------------------------------------------------------------------- |
| **Syed Ali Saleh Abbas Naqvi** | Team Leader | Planning, repository setup, scanner backend, database, documentation        |
| **Muhammad Ahmad Asim**        | Developer   | Main GUI, hacker theme, scanner tab, ping, net-info, banner module, exports |
| **Muhammad Ali Inam**          | Developer   | History management, dashboard analytics, settings page                      |

---

## 🔗 Project Links

* Repository: https://github.com/bellatorsaleh/PortScannerPro
* Issues: https://github.com/bellatorsaleh/PortScannerPro/issues
* Pull Requests: https://github.com/bellatorsaleh/PortScannerPro/pulls
