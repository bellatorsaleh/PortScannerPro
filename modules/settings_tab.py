"""
Settings Tab - Application preferences, saved targets, about info.
"""

import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK      = "#0a0e1a"
BG_PANEL     = "#0d1422"
BG_CARD      = "#111827"
ACCENT_CYAN  = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_RED   = "#ff4466"
ACCENT_ORANGE= "#ff9900"
TEXT_PRIMARY = "#e0f0ff"
TEXT_DIM     = "#4a6a7a"
BORDER       = "#1a2a3a"


class SettingsTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        top = tk.Frame(self.frame, bg=BG_PANEL, height=44)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="SETTINGS & TARGETS",
                 bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 12, "bold")).pack(side="left", padx=16, pady=10)
        tk.Frame(self.frame, bg=ACCENT_CYAN, height=1).pack(fill="x")

        cols_frame = tk.Frame(self.frame, bg=BG_DARK)
        cols_frame.pack(fill="both", expand=True, padx=14, pady=12)

        # ── LEFT: Settings ──────────────────────────────
        left = tk.Frame(cols_frame, bg=BG_DARK, width=380)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        self._card_header(left, "SCAN DEFAULTS")

        card = tk.Frame(left, bg=BG_CARD, padx=14, pady=12)
        card.pack(fill="x", pady=(4, 12))

        self._label(card, "DEFAULT TIMEOUT (seconds)")
        self.s_timeout = tk.DoubleVar(value=1.0)
        ttk.Scale(card, from_=0.1, to=5.0, variable=self.s_timeout,
                  orient="horizontal").pack(fill="x")
        self.s_timeout_lbl = tk.Label(card, text="1.0 s",
                                       bg=BG_CARD, fg=ACCENT_CYAN,
                                       font=("Courier", 9))
        self.s_timeout_lbl.pack(anchor="e")
        self.s_timeout.trace_add("write", lambda *a: self.s_timeout_lbl.config(
            text=f"{self.s_timeout.get():.1f} s"))

        self._label(card, "DEFAULT THREADS")
        self.s_threads = tk.IntVar(value=100)
        ttk.Scale(card, from_=10, to=500, variable=self.s_threads,
                  orient="horizontal").pack(fill="x")
        self.s_threads_lbl = tk.Label(card, text="100",
                                       bg=BG_CARD, fg=ACCENT_CYAN,
                                       font=("Courier", 9))
        self.s_threads_lbl.pack(anchor="e")
        self.s_threads.trace_add("write", lambda *a: self.s_threads_lbl.config(
            text=str(int(self.s_threads.get()))))

        self.s_banner = tk.BooleanVar(value=True)
        ttk.Checkbutton(card, text="Auto-grab service banners",
                        variable=self.s_banner).pack(anchor="w", pady=(10, 2))

        self.s_sound = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text="Sound alerts (open port found)",
                        variable=self.s_sound).pack(anchor="w")

        tk.Button(card, text="✔  Save Settings",
                  bg=ACCENT_CYAN, fg=BG_DARK,
                  font=("Courier", 10, "bold"), relief="flat",
                  cursor="hand2", pady=7,
                  command=self._save_settings).pack(fill="x", pady=(14, 0))

        # ── About card ──
        self._card_header(left, "ABOUT")
        about_card = tk.Frame(left, bg=BG_CARD, padx=14, pady=12)
        about_card.pack(fill="x")
        about_info = [
            ("App",      "PortScannerPro v2.0"),
            ("Language", "Python 3.x"),
            ("GUI",      "Tkinter"),
            ("Database", "SQLite3"),
            ("Authors",  "Team OSSD Group"),
            ("License",  "MIT Open Source"),
        ]
        for label, val in about_info:
            row = tk.Frame(about_card, bg=BG_CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{label:<10}",
                     bg=BG_CARD, fg=TEXT_DIM,
                     font=("Courier", 9)).pack(side="left")
            tk.Label(row, text=val, bg=BG_CARD, fg=TEXT_PRIMARY,
                     font=("Courier", 9)).pack(side="left")

        # ── RIGHT: Saved Targets ─────────────────────────
        right = tk.Frame(cols_frame, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        self._card_header(right, "SAVED TARGETS")

        # Add target form
        add_frame = tk.Frame(right, bg=BG_CARD, padx=12, pady=10)
        add_frame.pack(fill="x", pady=(4, 8))

        tk.Label(add_frame, text="Name", bg=BG_CARD, fg=TEXT_DIM,
                 font=("Courier", 8)).grid(row=0, column=0, sticky="w")
        tk.Label(add_frame, text="Target (IP/Host)", bg=BG_CARD, fg=TEXT_DIM,
                 font=("Courier", 8)).grid(row=0, column=1, sticky="w", padx=(12, 0))
        tk.Label(add_frame, text="Notes", bg=BG_CARD, fg=TEXT_DIM,
                 font=("Courier", 8)).grid(row=0, column=2, sticky="w", padx=(12, 0))

        self.t_name   = tk.StringVar()
        self.t_target = tk.StringVar()
        self.t_notes  = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.t_name,
                  width=16).grid(row=1, column=0, sticky="ew")
        ttk.Entry(add_frame, textvariable=self.t_target,
                  width=20).grid(row=1, column=1, sticky="ew", padx=(12, 0))
        ttk.Entry(add_frame, textvariable=self.t_notes,
                  width=20).grid(row=1, column=2, sticky="ew", padx=(12, 0))
        tk.Button(add_frame, text="+ Add",
                  bg=ACCENT_GREEN, fg=BG_DARK,
                  font=("Courier", 9, "bold"), relief="flat",
                  cursor="hand2",
                  command=self._add_target).grid(row=1, column=3,
                                                  padx=(10, 0), sticky="ew")

        # Targets treeview
        t_cols = ("id", "name", "target", "notes", "created")
        self.t_tree = ttk.Treeview(right, columns=t_cols,
                                    show="headings", height=14)
        for col, hdr, w in zip(t_cols,
                                ["ID", "NAME", "TARGET", "NOTES", "CREATED"],
                                [40, 120, 160, 200, 140]):
            self.t_tree.heading(col, text=hdr)
            self.t_tree.column(col, width=w, minwidth=30)
        self.t_tree.pack(fill="both", expand=True)

        btn_row = tk.Frame(right, bg=BG_DARK)
        btn_row.pack(fill="x", pady=6)
        tk.Button(btn_row, text="✘  Delete Selected",
                  bg=ACCENT_RED, fg="#ffffff",
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._delete_target).pack(side="left")

        self._refresh_targets()

    def _card_header(self, parent, text):
        tk.Label(parent, text=text, bg=BG_DARK, fg=ACCENT_CYAN,
                 font=("Courier", 9, "bold")).pack(anchor="w",
                                                    pady=(10, 2))

    def _label(self, parent, text):
        tk.Label(parent, text=text, bg=BG_CARD, fg=TEXT_DIM,
                 font=("Courier", 7, "bold")).pack(anchor="w", pady=(8, 1))

    def _load_settings(self):
        try:
            self.s_timeout.set(float(self.db.get_setting("timeout", 1.0)))
            self.s_threads.set(int(self.db.get_setting("threads", 100)))
            self.s_banner.set(self.db.get_setting("auto_detect_service", "1") == "1")
            self.s_sound.set(self.db.get_setting("sound_alerts", "0") == "1")
        except Exception:
            pass

    def _save_settings(self):
        self.db.set_setting("timeout", round(self.s_timeout.get(), 1))
        self.db.set_setting("threads", int(self.s_threads.get()))
        self.db.set_setting("auto_detect_service", "1" if self.s_banner.get() else "0")
        self.db.set_setting("sound_alerts", "1" if self.s_sound.get() else "0")
        messagebox.showinfo("Saved", "Settings saved successfully.")

    def _add_target(self):
        name   = self.t_name.get().strip()
        target = self.t_target.get().strip()
        notes  = self.t_notes.get().strip()
        if not name or not target:
            messagebox.showwarning("Input Error", "Name and Target are required.")
            return
        self.db.save_target(name, target, notes)
        self.t_name.set("")
        self.t_target.set("")
        self.t_notes.set("")
        self._refresh_targets()

    def _delete_target(self):
        sel = self.t_tree.selection()
        if not sel:
            messagebox.showinfo("Nothing selected", "Select a target first.")
            return
        tid = int(self.t_tree.item(sel[0])["values"][0])
        self.db.delete_saved_target(tid)
        self._refresh_targets()

    def _refresh_targets(self):
        for item in self.t_tree.get_children():
            self.t_tree.delete(item)
        rows = self.db.get_saved_targets()
        for row in rows:
            self.t_tree.insert("", "end", values=row)
