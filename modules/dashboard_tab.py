"""
Dashboard Tab - Statistics overview, top services, scan analytics.
"""

import tkinter as tk
from tkinter import ttk

BG_DARK      = "#0a0e1a"
BG_PANEL     = "#0d1422"
BG_CARD      = "#111827"
ACCENT_CYAN  = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_RED   = "#ff4466"
ACCENT_ORANGE= "#ff9900"
ACCENT_YELLOW= "#ffe033"
TEXT_PRIMARY = "#e0f0ff"
TEXT_DIM     = "#4a6a7a"
TEXT_MUTED   = "#2a4a5a"
BORDER       = "#1a2a3a"


class DashboardTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # Header
        top = tk.Frame(self.frame, bg=BG_PANEL, height=44)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="ANALYTICS DASHBOARD",
                 bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 12, "bold")).pack(side="left", padx=16, pady=10)
        tk.Button(top, text="⟳  Refresh", bg=BG_CARD, fg=ACCENT_CYAN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self.refresh).pack(side="right", padx=10, pady=8)
        tk.Frame(self.frame, bg=ACCENT_CYAN, height=1).pack(fill="x")

        scroll_canvas = tk.Canvas(self.frame, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical",
                                   command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(scroll_canvas, bg=BG_DARK)
        win_id = scroll_canvas.create_window((0, 0), window=self.inner,
                                              anchor="nw")

        def on_resize(e):
            scroll_canvas.itemconfig(win_id, width=e.width)
        scroll_canvas.bind("<Configure>", on_resize)

        def on_frame_resize(e):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        self.inner.bind("<Configure>", on_frame_resize)

        # ── KPI Cards row ──
        self.kpi_frame = tk.Frame(self.inner, bg=BG_DARK)
        self.kpi_frame.pack(fill="x", padx=16, pady=(16, 8))

        self.kpi_vars = {}
        kpis = [
            ("TOTAL SCANS",      "total_scans",      ACCENT_CYAN,   "⬡"),
            ("OPEN PORTS FOUND", "total_open_ports", ACCENT_GREEN,  "●"),
            ("UNIQUE TARGETS",   "unique_targets",   ACCENT_ORANGE, "◎"),
            ("AVG SCAN TIME",    "avg_scan_time",    ACCENT_YELLOW, "◷"),
        ]
        for label, key, color, icon in kpis:
            card = tk.Frame(self.kpi_frame, bg=BG_CARD,
                            relief="flat", padx=20, pady=12)
            card.pack(side="left", fill="x", expand=True, padx=6)
            tk.Label(card, text=icon, bg=BG_CARD, fg=color,
                     font=("Courier", 22)).pack()
            var = tk.StringVar(value="—")
            self.kpi_vars[key] = var
            tk.Label(card, textvariable=var, bg=BG_CARD, fg=color,
                     font=("Courier", 20, "bold")).pack()
            tk.Label(card, text=label, bg=BG_CARD, fg=TEXT_DIM,
                     font=("Courier", 7)).pack()

        # ── Divider ──
        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x",
                                                         padx=16, pady=8)

        # ── Two-column section ──
        cols = tk.Frame(self.inner, bg=BG_DARK)
        cols.pack(fill="both", expand=True, padx=16, pady=4)

        # Left: Recent activity
        left_col = tk.Frame(cols, bg=BG_DARK)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left_col, text="RECENT SCAN ACTIVITY",
                 bg=BG_DARK, fg=ACCENT_CYAN,
                 font=("Courier", 10, "bold")).pack(anchor="w", pady=(0, 6))

        act_cols = ("target", "open", "time", "when")
        self.act_tree = ttk.Treeview(left_col, columns=act_cols,
                                      show="headings", height=12)
        for col, hdr, w in zip(act_cols,
                                ["TARGET", "OPEN", "SCAN TIME", "TIMESTAMP"],
                                [150, 60, 90, 160]):
            self.act_tree.heading(col, text=hdr)
            self.act_tree.column(col, width=w, minwidth=40)
        self.act_tree.pack(fill="both", expand=True)

        # Right: Service frequency
        right_col = tk.Frame(cols, bg=BG_DARK, width=280)
        right_col.pack(side="left", fill="y")
        right_col.pack_propagate(False)

        tk.Label(right_col, text="TOP OPEN SERVICES",
                 bg=BG_DARK, fg=ACCENT_CYAN,
                 font=("Courier", 10, "bold")).pack(anchor="w", pady=(0, 6))

        self.services_frame = tk.Frame(right_col, bg=BG_DARK)
        self.services_frame.pack(fill="both", expand=True)

        # ── Port frequency bar chart (canvas) ──
        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x",
                                                         padx=16, pady=12)
        tk.Label(self.inner, text="SCAN OVERVIEW — OPEN PORTS FOUND PER SESSION",
                 bg=BG_DARK, fg=ACCENT_CYAN,
                 font=("Courier", 10, "bold")).pack(anchor="w", padx=16, pady=(0, 6))

        self.chart_canvas = tk.Canvas(self.inner, bg=BG_CARD,
                                       height=160, highlightthickness=0)
        self.chart_canvas.pack(fill="x", padx=16, pady=(0, 16))

    def refresh(self):
        # KPIs
        stats = self.db.get_statistics()
        self.kpi_vars["total_scans"].set(str(stats["total_scans"]))
        self.kpi_vars["total_open_ports"].set(str(stats["total_open_ports"]))
        self.kpi_vars["unique_targets"].set(str(stats["unique_targets"]))
        self.kpi_vars["avg_scan_time"].set(f"{stats['avg_scan_time']}s")

        # Recent activity
        for item in self.act_tree.get_children():
            self.act_tree.delete(item)
        rows = self.db.get_scan_history(limit=20)
        for row in rows:
            sid, target, port_range, scan_type, total_p, open_p, scan_t, ts = row
            self.act_tree.insert("", "end",
                                  values=(target, open_p, f"{scan_t}s", ts))

        # Top services from DB
        conn = self.db.get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT service, COUNT(*) as cnt
            FROM scan_results
            WHERE state = 'open' AND service != 'unknown'
            GROUP BY service ORDER BY cnt DESC LIMIT 8
        """)
        svc_rows = c.fetchall()
        conn.close()

        for w in self.services_frame.winfo_children():
            w.destroy()

        if svc_rows:
            max_cnt = svc_rows[0][1] if svc_rows else 1
            colors = [ACCENT_GREEN, ACCENT_CYAN, ACCENT_ORANGE,
                      ACCENT_YELLOW, ACCENT_RED,
                      "#aa88ff", "#ff88aa", "#88ffaa"]
            for i, (svc, cnt) in enumerate(svc_rows):
                row_f = tk.Frame(self.services_frame, bg=BG_DARK)
                row_f.pack(fill="x", pady=2)
                color = colors[i % len(colors)]
                tk.Label(row_f, text=f"{svc:<14}", bg=BG_DARK,
                         fg=TEXT_PRIMARY,
                         font=("Courier", 9)).pack(side="left")
                bar_w = max(4, int(120 * cnt / max_cnt))
                bar_cv = tk.Canvas(row_f, bg=BG_DARK, height=14,
                                   width=130, highlightthickness=0)
                bar_cv.pack(side="left")
                bar_cv.create_rectangle(0, 2, bar_w, 12,
                                         fill=color, outline="")
                tk.Label(row_f, text=str(cnt), bg=BG_DARK,
                         fg=TEXT_DIM,
                         font=("Courier", 8)).pack(side="left", padx=4)
        else:
            tk.Label(self.services_frame, text="No data yet.\nRun a scan first.",
                     bg=BG_DARK, fg=TEXT_DIM,
                     font=("Courier", 9), justify="center").pack(pady=20)

        # Mini bar chart: open ports per session
        self.chart_canvas.delete("all")
        if rows:
            data = [(r[1], r[5]) for r in rows[:15]][::-1]
            max_val = max(d[1] for d in data) if data else 1
            max_val = max(max_val, 1)
            W = self.chart_canvas.winfo_width() or 700
            H = 160
            bar_area_h = H - 40
            n = len(data)
            bar_w = max(6, (W - 40) // n - 4)

            for i, (target, open_p) in enumerate(data):
                x0 = 20 + i * ((W - 40) // n)
                bar_h = int(bar_area_h * open_p / max_val)
                y0 = H - 20 - bar_h
                y1 = H - 20
                color = ACCENT_CYAN if open_p > 0 else TEXT_MUTED
                self.chart_canvas.create_rectangle(
                    x0, y0, x0 + bar_w, y1,
                    fill=color, outline="")
                if open_p > 0:
                    self.chart_canvas.create_text(
                        x0 + bar_w // 2, y0 - 6,
                        text=str(open_p), fill=ACCENT_CYAN,
                        font=("Courier", 7))
                # Label (truncated target)
                self.chart_canvas.create_text(
                    x0 + bar_w // 2, H - 10,
                    text=target[:8], fill=TEXT_DIM,
                    font=("Courier", 6), angle=0)
