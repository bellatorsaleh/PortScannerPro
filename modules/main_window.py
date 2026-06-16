"""
Main Window - Primary application frame with tabbed navigation.
"""

import tkinter as tk
from tkinter import ttk

from modules.scan_tab import ScanTab
from modules.history_tab import HistoryTab
from modules.dashboard_tab import DashboardTab
from modules.settings_tab import SettingsTab

# === DARK CYBER THEME ===
BG_DARK      = "#0a0e1a"
BG_PANEL     = "#0d1422"
BG_CARD      = "#111827"
ACCENT_CYAN  = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_RED   = "#ff4466"
ACCENT_ORANGE= "#ff9900"
TEXT_PRIMARY = "#e0f0ff"
TEXT_DIM     = "#4a6a7a"
TEXT_MUTED   = "#2a4a5a"
BORDER       = "#1a2a3a"


class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self._setup_root()
        self._apply_styles()
        self._build_ui()

    def _setup_root(self):
        self.root.title("PortScannerPro — Advanced Network Security Analyzer | Developed by Muhammad Ahmad")
        self.root.geometry("1100x740")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG_DARK)

        # Icon (text-based since no image file)
        try:
            self.root.iconbitmap(default=None)
        except Exception:
            pass

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY,
                        font=("Courier", 10))
        style.configure("TFrame", background=BG_DARK)
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY,
                        font=("Courier", 10))
        style.configure("TButton",
                        background=BG_CARD, foreground=ACCENT_CYAN,
                        relief="flat", borderwidth=0, padding=(12, 6),
                        font=("Courier", 10, "bold"))
        style.map("TButton",
                  background=[("active", "#1a2a4a"), ("pressed", "#0a1a2a")],
                  foreground=[("active", ACCENT_CYAN)])

        style.configure("Accent.TButton",
                        background=ACCENT_CYAN, foreground=BG_DARK,
                        font=("Courier", 10, "bold"), padding=(16, 8))
        style.map("Accent.TButton",
                  background=[("active", "#00aacc"), ("pressed", "#008899")])

        style.configure("Stop.TButton",
                        background=ACCENT_RED, foreground="#ffffff",
                        font=("Courier", 10, "bold"), padding=(16, 8))

        style.configure("TEntry",
                        fieldbackground=BG_CARD, foreground=TEXT_PRIMARY,
                        insertcolor=ACCENT_CYAN, borderwidth=1,
                        relief="flat", font=("Courier", 11))
        style.map("TEntry", fieldbackground=[("focus", "#151f2e")])

        style.configure("TCombobox",
                        fieldbackground=BG_CARD, foreground=TEXT_PRIMARY,
                        background=BG_CARD, selectbackground=ACCENT_CYAN,
                        font=("Courier", 10))

        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=BG_PANEL, foreground=TEXT_DIM,
                        padding=(18, 10), font=("Courier", 10, "bold"),
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG_CARD)],
                  foreground=[("selected", ACCENT_CYAN)])

        style.configure("Treeview",
                        background=BG_CARD, foreground=TEXT_PRIMARY,
                        fieldbackground=BG_CARD, rowheight=26,
                        font=("Courier", 10))
        style.configure("Treeview.Heading",
                        background=BG_PANEL, foreground=ACCENT_CYAN,
                        font=("Courier", 10, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", "#1a3a5a")],
                  foreground=[("selected", ACCENT_CYAN)])

        style.configure("TProgressbar",
                        background=ACCENT_CYAN, troughcolor=BG_PANEL,
                        borderwidth=0, thickness=6)

        style.configure("TCheckbutton",
                        background=BG_DARK, foreground=TEXT_PRIMARY,
                        font=("Courier", 10))
        style.configure("TScale",
                        background=BG_DARK, troughcolor=BG_PANEL)
        style.configure("TSeparator", background=BORDER)
        style.configure("TLabelframe",
                        background=BG_DARK, foreground=ACCENT_CYAN,
                        borderwidth=1, relief="solid",
                        font=("Courier", 10, "bold"))
        style.configure("TLabelframe.Label",
                        background=BG_DARK, foreground=ACCENT_CYAN,
                        font=("Courier", 10, "bold"))

    def _build_ui(self):
        # ── Top header bar ──────────────────────────────
        header = tk.Frame(self.root, bg=BG_PANEL, height=52)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="◈  PORT SCANNER PRO",
                 bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 16, "bold")).pack(side="left", padx=18, pady=12)

        tk.Label(header, text="Advanced Network Security Analyzer",
                 bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9)).pack(side="left", padx=4)

        tk.Label(header, text="v2.0",
                 bg=BG_PANEL, fg=TEXT_MUTED,
                 font=("Courier", 9)).pack(side="right", padx=18)

        # ── Separator ───────────────────────────────────
        tk.Frame(self.root, bg=ACCENT_CYAN, height=1).pack(fill="x")

        # ── Notebook (tabs) ─────────────────────────────
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.scan_tab     = ScanTab(self.nb, self.db)
        self.history_tab  = HistoryTab(self.nb, self.db)
        self.dashboard_tab= DashboardTab(self.nb, self.db)
        self.settings_tab = SettingsTab(self.nb, self.db)

        self.nb.add(self.scan_tab.frame,      text="  ◉ SCANNER  ")
        self.nb.add(self.history_tab.frame,   text="  ◫ HISTORY  ")
        self.nb.add(self.dashboard_tab.frame, text="  ◈ DASHBOARD  ")
        self.nb.add(self.settings_tab.frame,  text="  ⚙ SETTINGS  ")

        def on_tab_change(e):
            tab = self.nb.index(self.nb.select())
            if tab == 1:
                self.history_tab.refresh()
            elif tab == 2:
                self.dashboard_tab.refresh()

        self.nb.bind("<<NotebookTabChanged>>", on_tab_change)

        # ── Status bar ──────────────────────────────────
        status_bar = tk.Frame(self.root, bg=BG_PANEL, height=24)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        tk.Frame(status_bar, bg=ACCENT_CYAN, width=3).pack(side="left")
        self.status_var = tk.StringVar(value="Ready  |  Idle")
        tk.Label(status_bar, textvariable=self.status_var,
                 bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 8)).pack(side="left", padx=10)

        tk.Label(status_bar,
                 text="PortScannerPro © 2025  |  Python + Tkinter + SQLite",
                 bg=BG_PANEL, fg=TEXT_MUTED,
                 font=("Courier", 8)).pack(side="right", padx=10)
        
# Updated scan tab module by Muhammad Ahmad