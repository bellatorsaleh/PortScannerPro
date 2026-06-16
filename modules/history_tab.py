"""
History Tab - Browse, view, and manage past scan sessions.
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


class HistoryTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────
        top = tk.Frame(self.frame, bg=BG_PANEL, height=44)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="SCAN HISTORY",
                 bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 12, "bold")).pack(side="left", padx=16, pady=10)

        tk.Button(top, text="⟳  Refresh", bg=BG_CARD, fg=ACCENT_CYAN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self.refresh).pack(side="right", padx=6, pady=8)

        tk.Button(top, text="✘  Delete Selected",
                  bg=BG_CARD, fg=ACCENT_RED,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._delete_selected).pack(side="right", padx=6, pady=8)

        tk.Frame(self.frame, bg=ACCENT_CYAN, height=1).pack(fill="x")

        # ── Split pane ───────────────────────────────────
        pane = tk.Frame(self.frame, bg=BG_DARK)
        pane.pack(fill="both", expand=True, padx=10, pady=8)

        # Sessions list (left)
        left = tk.Frame(pane, bg=BG_DARK, width=420)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="SESSIONS", bg=BG_DARK, fg=TEXT_DIM,
                 font=("Courier", 8, "bold")).pack(anchor="w", pady=(0, 4))

        sess_cols = ("id", "target", "ports", "open", "time", "when")
        self.sess_tree = ttk.Treeview(left, columns=sess_cols,
                                       show="headings", height=24)
        sess_hdrs = [("ID", 40), ("TARGET", 130), ("PORT RANGE", 90),
                     ("OPEN", 50), ("SCAN TIME", 80), ("TIMESTAMP", 130)]
        for (h, w), c in zip(sess_hdrs, sess_cols):
            self.sess_tree.heading(c, text=h)
            self.sess_tree.column(c, width=w, minwidth=40)

        vsb = ttk.Scrollbar(left, orient="vertical",
                             command=self.sess_tree.yview)
        self.sess_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.sess_tree.pack(fill="both", expand=True)
        self.sess_tree.bind("<<TreeviewSelect>>", self._on_session_select)

        # Separator
        tk.Frame(pane, bg=BORDER, width=1).pack(side="left", fill="y",
                                                  padx=8)

        # Results detail (right)
        right = tk.Frame(pane, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="OPEN PORTS IN SESSION",
                 bg=BG_DARK, fg=TEXT_DIM,
                 font=("Courier", 8, "bold")).pack(anchor="w", pady=(0, 4))

        res_cols = ("port", "service", "banner", "response")
        self.res_tree = ttk.Treeview(right, columns=res_cols,
                                      show="headings", height=24)
        res_hdrs = [("PORT", 60), ("SERVICE", 120),
                    ("BANNER", 260), ("RESP (ms)", 80)]
        for (h, w), c in zip(res_hdrs, res_cols):
            self.res_tree.heading(c, text=h)
            self.res_tree.column(c, width=w, minwidth=40)

        vsb2 = ttk.Scrollbar(right, orient="vertical",
                              command=self.res_tree.yview)
        self.res_tree.configure(yscrollcommand=vsb2.set)
        vsb2.pack(side="right", fill="y")
        self.res_tree.pack(fill="both", expand=True)

        # Info strip
        self.info_label = tk.Label(right, text="Select a session to view results.",
                                   bg=BG_DARK, fg=TEXT_DIM,
                                   font=("Courier", 8))
        self.info_label.pack(anchor="w", pady=4)

    def refresh(self):
        for item in self.sess_tree.get_children():
            self.sess_tree.delete(item)
        rows = self.db.get_scan_history(limit=100)
        for row in rows:
            sid, target, port_range, scan_type, total_p, open_p, scan_t, ts = row
            self.sess_tree.insert("", "end", iid=str(sid),
                                   values=(sid, target, port_range,
                                           open_p, f"{scan_t}s", ts))

    def _on_session_select(self, event=None):
        sel = self.sess_tree.selection()
        if not sel:
            return
        session_id = int(sel[0])
        for item in self.res_tree.get_children():
            self.res_tree.delete(item)
        results = self.db.get_session_results(session_id)
        for r in results:
            port, state, service, banner, resp = r
            if state == "open":
                self.res_tree.insert("", "end",
                                     values=(port, service or "—",
                                             (banner or "—")[:80],
                                             f"{resp} ms"))
        self.info_label.config(
            text=f"Session #{session_id}  |  {len(results)} open port(s)")

    def _delete_selected(self):
        sel = self.sess_tree.selection()
        if not sel:
            messagebox.showinfo("Nothing selected", "Select a session first.")
            return
        if not messagebox.askyesno("Delete", "Delete selected session?"):
            return
        for sid in sel:
            self.db.delete_scan_session(int(sid))
        self.refresh()
        for item in self.res_tree.get_children():
            self.res_tree.delete(item)
        self.info_label.config(text="Session deleted.")
