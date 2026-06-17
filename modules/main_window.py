"""
Main Window - Elite Hacking Terminal Theme
"""
import tkinter as tk
from tkinter import ttk
import time
import threading
import random
import socket

from modules.scan_tab import ScanTab
from modules.history_tab import HistoryTab
from modules.dashboard_tab import DashboardTab
from modules.settings_tab import SettingsTab

# === ELITE HACKER PALETTE ===
BG          = "#000000"
BG2         = "#050505"
BG3         = "#0a0a0a"
BG4         = "#0d1117"
G1          = "#00ff41"   # matrix green
G2          = "#00cc33"
G3          = "#008f11"
C1          = "#00ffff"   # cyan
C2          = "#00cccc"
R1          = "#ff0000"   # red alert
O1          = "#ff8800"   # orange
Y1          = "#ffff00"   # yellow
P1          = "#cc00ff"   # purple
W1          = "#ffffff"
DIM         = "#1a3a1a"
DIMMER      = "#0a1a0a"

class MainWindow:
    def __init__(self, root, db):
        self.root = root
        self.db   = db
        self._setup_root()
        self._apply_styles()
        self._build_ui()
        self._start_live_updates()

    def _setup_root(self):
        self.root.title("[ GHOST_SCANNER v3.0 ] — Elite Network Recon Tool")
        self.root.geometry("1280x860")
        self.root.minsize(1100, 720)
        self.root.configure(bg=BG)

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(".",              background=BG,   foreground=G1,  font=("Courier New", 10))
        s.configure("TFrame",         background=BG)
        s.configure("TLabel",         background=BG,   foreground=G1,  font=("Courier New", 10))
        s.configure("TButton",        background=BG3,  foreground=G1,  relief="flat", padding=(10,5), font=("Courier New",10,"bold"))
        s.map("TButton", background=[("active", BG4)], foreground=[("active", C1)])
        s.configure("TEntry",         fieldbackground=BG3, foreground=G1, insertcolor=G1, font=("Courier New",11))
        s.configure("TCombobox",      fieldbackground=BG3, foreground=G1, background=BG3, selectbackground="#001a00", font=("Courier New",10))
        s.configure("TNotebook",      background=BG,   borderwidth=0)
        s.configure("TNotebook.Tab",  background=BG2,  foreground=DIM, padding=(22,11), font=("Courier New",10,"bold"))
        s.map("TNotebook.Tab",        background=[("selected", BG4)], foreground=[("selected", G1)])
        s.configure("Treeview",       background=BG3,  foreground=G1,  fieldbackground=BG3, rowheight=24, font=("Courier New",10))
        s.configure("Treeview.Heading", background=BG4, foreground=C1, font=("Courier New",10,"bold"), relief="flat")
        s.map("Treeview",             background=[("selected","#001800")], foreground=[("selected",C1)])
        s.configure("TProgressbar",   background=G1,   troughcolor=BG3, borderwidth=0, thickness=6)
        s.configure("TCheckbutton",   background=BG,   foreground=G1,  font=("Courier New",10))
        s.configure("TScale",         background=BG,   troughcolor=BG3)
        s.configure("TScrollbar",     background=BG3,  troughcolor=BG, arrowcolor=G3)
        s.configure("TLabelframe",    background=BG,   foreground=G1,  borderwidth=1, relief="solid")
        s.configure("TLabelframe.Label", background=BG, foreground=C1, font=("Courier New",10,"bold"))

    def _build_ui(self):
        # ══════════════════════════════════════════
        # TOP BANNER — ASCII art style
        # ══════════════════════════════════════════
        banner = tk.Frame(self.root, bg=BG, height=90)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        left_banner = tk.Frame(banner, bg=BG)
        left_banner.pack(side="left", padx=14, pady=6)

        ascii_title = (
            " ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗\n"
            "██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝\n"
            "██║  ███╗███████║██║   ██║███████╗   ██║   \n"
            "██║   ██║██╔══██║██║   ██║╚════██║   ██║   \n"
            "╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   \n"
            " ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝  "
        )
        tk.Label(left_banner, text=ascii_title,
                 bg=BG, fg=G1,
                 font=("Courier New", 7, "bold"),
                 justify="left").pack(anchor="w")

        right_banner = tk.Frame(banner, bg=BG)
        right_banner.pack(side="right", padx=16, pady=6)

        # Live clock
        self.clock_var = tk.StringVar(value="00:00:00")
        tk.Label(right_banner, textvariable=self.clock_var,
                 bg=BG, fg=G1,
                 font=("Courier New", 22, "bold")).pack(anchor="e")

        # IP display
        try:
            myip = socket.gethostbyname(socket.gethostname())
        except Exception:
            myip = "127.0.0.1"
        tk.Label(right_banner, text=f"LOCAL_IP :: {myip}",
                 bg=BG, fg=C1,
                 font=("Courier New", 9)).pack(anchor="e")
        tk.Label(right_banner, text="GHOST_SCANNER v3.0  |  ELITE EDITION",
                 bg=BG, fg=DIM,
                 font=("Courier New", 8)).pack(anchor="e")

        # Middle info
        mid_banner = tk.Frame(banner, bg=BG)
        mid_banner.pack(side="left", padx=20, pady=10)
        tk.Label(mid_banner, text="SCANNER  |  NETWORK  |  RECON",
                 bg=BG, fg=C1,
                 font=("Courier New", 10, "bold")).pack(anchor="w")
        tk.Label(mid_banner, text="Educational Network Security Tool",
                 bg=BG, fg=DIM,
                 font=("Courier New", 9)).pack(anchor="w")

        self.status_var = tk.StringVar(value="● ONLINE")
        tk.Label(mid_banner, textvariable=self.status_var,
                 bg=BG, fg=G1,
                 font=("Courier New", 10, "bold")).pack(anchor="w", pady=(4,0))

        # ── Glowing separator ──
        sep = tk.Frame(self.root, bg=BG, height=6)
        sep.pack(fill="x")
        tk.Frame(sep, bg=G1, height=1).pack(fill="x")
        tk.Frame(sep, bg=G3, height=1).pack(fill="x", pady=(1,0))
        tk.Frame(sep, bg=BG, height=2).pack(fill="x")
        tk.Frame(sep, bg=G3, height=1).pack(fill="x")

        # ── Scrolling ticker ──
        ticker_frame = tk.Frame(self.root, bg=BG2, height=20)
        ticker_frame.pack(fill="x")
        ticker_frame.pack_propagate(False)
        self.ticker_var = tk.StringVar()
        self.ticker_var.set(
            "  >_ GHOST_SCANNER READY  //  NETWORK RECONNAISSANCE ACTIVE  //  "
            "ALL MODULES LOADED  //  DATABASE CONNECTED  //  "
            "ENTER TARGET IP TO BEGIN  //  ETHICAL USE ONLY  //  "
        )
        tk.Label(ticker_frame, textvariable=self.ticker_var,
                 bg=BG2, fg=G3,
                 font=("Courier New", 8)).pack(side="left", padx=4)

        # ══════════════════════════════════════════
        # NOTEBOOK
        # ══════════════════════════════════════════
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True)

        self.scan_tab      = ScanTab(self.nb, self.db)
        self.history_tab   = HistoryTab(self.nb, self.db)
        self.dashboard_tab = DashboardTab(self.nb, self.db)
        self.settings_tab  = SettingsTab(self.nb, self.db)

        self.nb.add(self.scan_tab.frame,      text="  ▶  SCANNER      ")
        self.nb.add(self.history_tab.frame,   text="  ☰  HISTORY      ")
        self.nb.add(self.dashboard_tab.frame, text="  ◈  DASHBOARD    ")
        self.nb.add(self.settings_tab.frame,  text="  ⚙  SETTINGS     ")

        tab_labels = [
            "SCANNER  //  READY TO SCAN",
            "HISTORY  //  PAST SESSIONS",
            "DASHBOARD  //  ANALYTICS",
            "SETTINGS  //  CONFIG",
        ]
        def on_tab(e):
            idx = self.nb.index(self.nb.select())
            self.ticker_var.set(f"  >_ {tab_labels[idx]}  //  " * 6)
            if idx == 1: self.history_tab.refresh()
            elif idx == 2: self.dashboard_tab.refresh()
        self.nb.bind("<<NotebookTabChanged>>", on_tab)

        # ══ BOTTOM STATUS BAR ══
        bot = tk.Frame(self.root, bg=BG2, height=24)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)
        tk.Frame(bot, bg=G1, width=3).pack(side="left", fill="y")
        self.bot_var = tk.StringVar(
            value="  STATUS: ONLINE  |  ENGINE: READY  |  DB: CONNECTED  |  THREADS: AVAILABLE")
        tk.Label(bot, textvariable=self.bot_var,
                 bg=BG2, fg=DIM,
                 font=("Courier New", 8)).pack(side="left")
        tk.Label(bot, text="GHOST_SCANNER © 2025  |  FOR EDUCATIONAL USE ONLY  ",
                 bg=BG2, fg=DIMMER,
                 font=("Courier New", 8)).pack(side="right")

    def _start_live_updates(self):
        def tick():
            while True:
                try:
                    self.clock_var.set(time.strftime("%H:%M:%S"))
                except Exception:
                    break
                time.sleep(1)
        threading.Thread(target=tick, daemon=True).start()