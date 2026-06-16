"""
Scan Tab - Main scanning interface: target input, controls, live results table.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import csv
import json
import socket
from datetime import datetime

from modules.scanner import PortScanner

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
BORDER       = "#1a2a3a"

RISK_COLORS = {
    "critical": ACCENT_RED,
    "high":     ACCENT_ORANGE,
    "medium":   ACCENT_YELLOW,
    "low":      ACCENT_GREEN,
    "info":     ACCENT_CYAN
}

PRESET_RANGES = {
    "Common Ports (1-1024)":       (1, 1024),
    "Well-known (1-100)":          (1, 100),
    "Top 20 Ports":                (20, 25),
    "Web Ports (80, 443, 8080...)": (80, 9000),
    "Database Ports (3306-5432)":  (3306, 5432),
    "Full Scan (1-65535)":         (1, 65535),
    "Custom":                      None
}


class ScanTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.scanner = None
        self._scan_thread = None
        self._results_buffer = []
        self._scanning = False
        self._build_ui()

    def _build_ui(self):
        # ── Left panel: controls ─────────────────────────────
        left = tk.Frame(self.frame, bg=BG_PANEL, width=300)
        left.pack(side="left", fill="y", padx=0, pady=0)
        left.pack_propagate(False)

        # Header
        tk.Frame(left, bg=ACCENT_CYAN, height=2).pack(fill="x")
        tk.Label(left, text="SCAN CONFIGURATION",
                 bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 10, "bold")).pack(pady=(12, 4), padx=12, anchor="w")

        inner = tk.Frame(left, bg=BG_PANEL)
        inner.pack(fill="both", expand=True, padx=12)

        # Target
        self._section_label(inner, "TARGET HOST / IP")
        self.target_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(inner, textvariable=self.target_var, width=28)
        target_entry.pack(fill="x", pady=(2, 8))

        # Resolve button
        tk.Button(inner, text="⬡  Resolve Hostname",
                  bg=BG_CARD, fg=ACCENT_CYAN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._resolve_hostname).pack(fill="x", pady=(0, 10))

        self.resolved_label = tk.Label(inner, text="",
                                       bg=BG_PANEL, fg=TEXT_DIM,
                                       font=("Courier", 8), wraplength=240)
        self.resolved_label.pack(anchor="w", pady=(0, 4))

        # Port preset
        self._section_label(inner, "PORT PRESET")
        self.preset_var = tk.StringVar(value="Common Ports (1-1024)")
        preset_cb = ttk.Combobox(inner, textvariable=self.preset_var,
                                 values=list(PRESET_RANGES.keys()),
                                 state="readonly", width=28)
        preset_cb.pack(fill="x", pady=(2, 8))
        preset_cb.bind("<<ComboboxSelected>>", self._on_preset)

        # Port range
        range_frame = tk.Frame(inner, bg=BG_PANEL)
        range_frame.pack(fill="x", pady=(0, 8))
        tk.Label(range_frame, text="FROM", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 8)).grid(row=0, column=0, sticky="w")
        tk.Label(range_frame, text="TO", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 8)).grid(row=0, column=1, sticky="w", padx=(20, 0))
        self.port_start_var = tk.IntVar(value=1)
        self.port_end_var   = tk.IntVar(value=1024)
        ttk.Entry(range_frame, textvariable=self.port_start_var,
                  width=8).grid(row=1, column=0)
        ttk.Entry(range_frame, textvariable=self.port_end_var,
                  width=8).grid(row=1, column=1, padx=(20, 0))

        # Scan type
        self._section_label(inner, "SCAN TYPE")
        self.scan_type_var = tk.StringVar(value="TCP Connect")
        for t in ["TCP Connect", "Quick Sweep", "Stealth (limited)"]:
            tk.Radiobutton(inner, text=t, variable=self.scan_type_var, value=t,
                           bg=BG_PANEL, fg=TEXT_PRIMARY, selectcolor=BG_CARD,
                           activebackground=BG_PANEL,
                           font=("Courier", 9)).pack(anchor="w")

        # Options
        self._section_label(inner, "OPTIONS")
        self.banner_var  = tk.BooleanVar(value=True)
        self.resolve_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(inner, text="Grab Service Banners",
                        variable=self.banner_var).pack(anchor="w")
        ttk.Checkbutton(inner, text="Resolve Hostnames",
                        variable=self.resolve_var).pack(anchor="w")

        # Timeout
        self._section_label(inner, "TIMEOUT (seconds)")
        self.timeout_var = tk.DoubleVar(value=1.0)
        timeout_scale = ttk.Scale(inner, from_=0.1, to=5.0,
                                  variable=self.timeout_var, orient="horizontal")
        timeout_scale.pack(fill="x", pady=(2, 0))
        self.timeout_label = tk.Label(inner, text="1.0 s",
                                      bg=BG_PANEL, fg=ACCENT_CYAN,
                                      font=("Courier", 9))
        self.timeout_label.pack(anchor="e")
        timeout_scale.config(command=lambda v: self.timeout_label.config(
            text=f"{float(v):.1f} s"))

        # Threads
        self._section_label(inner, "THREADS")
        self.threads_var = tk.IntVar(value=100)
        threads_scale = ttk.Scale(inner, from_=10, to=500,
                                  variable=self.threads_var, orient="horizontal")
        threads_scale.pack(fill="x", pady=(2, 0))
        self.threads_label = tk.Label(inner, text="100",
                                      bg=BG_PANEL, fg=ACCENT_CYAN,
                                      font=("Courier", 9))
        self.threads_label.pack(anchor="e")
        threads_scale.config(command=lambda v: self.threads_label.config(
            text=str(int(float(v)))))

        # Scan button
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=14)
        self.scan_btn = tk.Button(inner, text="▶  START SCAN",
                                  bg=ACCENT_CYAN, fg=BG_DARK,
                                  font=("Courier", 12, "bold"),
                                  relief="flat", cursor="hand2",
                                  pady=10, command=self._start_scan)
        self.scan_btn.pack(fill="x")

        self.stop_btn = tk.Button(inner, text="■  STOP SCAN",
                                  bg=ACCENT_RED, fg="#ffffff",
                                  font=("Courier", 12, "bold"),
                                  relief="flat", cursor="hand2",
                                  pady=10, state="disabled",
                                  command=self._stop_scan)
        self.stop_btn.pack(fill="x", pady=(6, 0))

        # Export buttons
        export_frame = tk.Frame(inner, bg=BG_PANEL)
        export_frame.pack(fill="x", pady=(10, 0))
        tk.Button(export_frame, text="⬇ CSV",
                  bg=BG_CARD, fg=ACCENT_GREEN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._export_csv).pack(side="left", fill="x", expand=True)
        tk.Button(export_frame, text="⬇ JSON",
                  bg=BG_CARD, fg=ACCENT_ORANGE,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._export_json).pack(side="left", fill="x",
                                                   expand=True, padx=(4, 0))

        # ── Right panel: results ─────────────────────────────
        right = tk.Frame(self.frame, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)

        # Stats row
        stats_frame = tk.Frame(right, bg=BG_PANEL, height=56)
        stats_frame.pack(fill="x")
        stats_frame.pack_propagate(False)

        self.stat_vars = {
            "open":     tk.StringVar(value="0"),
            "scanned":  tk.StringVar(value="0"),
            "total":    tk.StringVar(value="0"),
            "elapsed":  tk.StringVar(value="0.0s")
        }
        stat_defs = [
            ("OPEN PORTS",   "open",    ACCENT_GREEN),
            ("SCANNED",      "scanned", ACCENT_CYAN),
            ("TOTAL PORTS",  "total",   TEXT_DIM),
            ("ELAPSED",      "elapsed", ACCENT_ORANGE),
        ]
        for label, key, color in stat_defs:
            sf = tk.Frame(stats_frame, bg=BG_PANEL)
            sf.pack(side="left", padx=20, pady=8)
            tk.Label(sf, textvariable=self.stat_vars[key],
                     bg=BG_PANEL, fg=color,
                     font=("Courier", 18, "bold")).pack()
            tk.Label(sf, text=label, bg=BG_PANEL, fg=TEXT_DIM,
                     font=("Courier", 7)).pack()

        # Progress bar
        prog_frame = tk.Frame(right, bg=BG_DARK)
        prog_frame.pack(fill="x", padx=10, pady=4)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(prog_frame, variable=self.progress_var,
                                             maximum=100, length=400)
        self.progress_bar.pack(fill="x")
        self.progress_label = tk.Label(prog_frame, text="",
                                       bg=BG_DARK, fg=TEXT_DIM,
                                       font=("Courier", 8))
        self.progress_label.pack(anchor="e")

        # Results treeview
        tree_frame = tk.Frame(right, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        cols = ("port", "state", "service", "risk", "response", "banner")
        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                 show="headings", selectmode="browse")
        hdrs = [("PORT", 70), ("STATE", 70), ("SERVICE", 120),
                ("RISK", 80), ("RESPONSE (ms)", 110), ("BANNER / INFO", 300)]
        for (h, w), c in zip(hdrs, cols):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, minwidth=50)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Tag colors for risk
        self.tree.tag_configure("critical", foreground=ACCENT_RED)
        self.tree.tag_configure("high",     foreground=ACCENT_ORANGE)
        self.tree.tag_configure("medium",   foreground=ACCENT_YELLOW)
        self.tree.tag_configure("low",      foreground=ACCENT_GREEN)
        self.tree.tag_configure("info",     foreground=ACCENT_CYAN)
        self.tree.tag_configure("open",     background="#0a1a0e")

        # Log / console at bottom
        log_frame = tk.Frame(right, bg=BG_PANEL, height=110)
        log_frame.pack(fill="x", padx=10, pady=6)
        log_frame.pack_propagate(False)

        tk.Label(log_frame, text="SCAN LOG", bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 8, "bold")).pack(anchor="w", padx=6, pady=2)

        self.log_text = tk.Text(log_frame, bg=BG_CARD, fg=TEXT_DIM,
                                font=("Courier", 8), height=4,
                                relief="flat", state="disabled",
                                wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.log_text.tag_config("cyan",   foreground=ACCENT_CYAN)
        self.log_text.tag_config("green",  foreground=ACCENT_GREEN)
        self.log_text.tag_config("red",    foreground=ACCENT_RED)
        self.log_text.tag_config("orange", foreground=ACCENT_ORANGE)

        self._start_time = None

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 7, "bold")).pack(anchor="w", pady=(10, 1))

    def _on_preset(self, event=None):
        sel = self.preset_var.get()
        rng = PRESET_RANGES.get(sel)
        if rng:
            self.port_start_var.set(rng[0])
            self.port_end_var.set(rng[1])

    def _resolve_hostname(self):
        host = self.target_var.get().strip()
        try:
            ip = socket.gethostbyname(host)
            self.resolved_label.config(text=f"✔  Resolved: {ip}", fg=ACCENT_GREEN)
        except Exception:
            self.resolved_label.config(text="✘  Cannot resolve host", fg=ACCENT_RED)

    def _log(self, msg, tag="cyan"):
        self.log_text.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {msg}\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _start_scan(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("Input Error", "Please enter a target host/IP.")
            return
        try:
            p_start = self.port_start_var.get()
            p_end   = self.port_end_var.get()
            if p_start < 1 or p_end > 65535 or p_start > p_end:
                raise ValueError
        except Exception:
            messagebox.showwarning("Input Error", "Invalid port range (1–65535).")
            return

        # Clear previous
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._results_buffer = []
        self.stat_vars["open"].set("0")
        self.stat_vars["scanned"].set("0")
        self.stat_vars["total"].set(str(p_end - p_start + 1))
        self.stat_vars["elapsed"].set("0.0s")
        self.progress_var.set(0)

        self._scanning = True
        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        import time
        self._start_time = time.time()

        self._log(f"Scanning {target} | Ports {p_start}–{p_end} | "
                  f"Threads: {self.threads_var.get()}", "cyan")

        self.scanner = PortScanner(
            host=target,
            port_start=p_start,
            port_end=p_end,
            timeout=round(self.timeout_var.get(), 1),
            max_threads=self.threads_var.get(),
            grab_banners=self.banner_var.get(),
            on_result=self._on_result,
            on_progress=self._on_progress,
            on_complete=self._on_complete
        )

        self._scan_thread = threading.Thread(target=self.scanner.run, daemon=True)
        self._scan_thread.start()

    def _stop_scan(self):
        if self.scanner:
            self.scanner.stop()
        self._log("Scan stopped by user.", "orange")

    def _on_result(self, result):
        self._results_buffer.append(result)
        self.frame.after(0, self._insert_result, result)

    def _insert_result(self, r):
        risk  = r.get("risk", "info")
        state = r.get("state", "")
        tags  = (risk,)
        if state == "open":
            tags = (risk, "open")
        banner = r.get("banner", "")[:80]
        self.tree.insert("", "end",
                         values=(r["port"], state.upper(), r["service"],
                                 risk.upper(), f"{r['response_time']} ms",
                                 banner or "—"),
                         tags=tags)
        self.tree.yview_moveto(1.0)

    def _on_progress(self, scanned, total, open_count):
        import time
        pct = (scanned / total) * 100
        elapsed = round(time.time() - self._start_time, 1)
        self.frame.after(0, self._update_stats, scanned, total,
                         open_count, pct, elapsed)

    def _update_stats(self, scanned, total, open_count, pct, elapsed):
        self.stat_vars["open"].set(str(open_count))
        self.stat_vars["scanned"].set(str(scanned))
        self.stat_vars["total"].set(str(total))
        self.stat_vars["elapsed"].set(f"{elapsed}s")
        self.progress_var.set(pct)
        self.progress_label.config(text=f"{pct:.1f}%  ({scanned}/{total})")

    def _on_complete(self, results, scan_time=0, total_scanned=0,
                     ip=None, error=None):
        self.frame.after(0, self._finalize, results, scan_time,
                         total_scanned, ip, error)

    def _finalize(self, results, scan_time, total_scanned, ip, error):
        self._scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        if error:
            self._log(f"ERROR: {error}", "red")
            return

        self._log(f"Scan complete! {len(results)} open ports found in "
                  f"{scan_time}s  |  IP: {ip}", "green")

        # Save to DB
        try:
            target = self.target_var.get().strip()
            p_start = self.port_start_var.get()
            p_end   = self.port_end_var.get()
            session_id = self.db.save_scan_session(
                target=target,
                port_range=f"{p_start}-{p_end}",
                scan_type=self.scan_type_var.get(),
                total_ports=total_scanned,
                open_ports=len(results),
                scan_time=scan_time
            )
            self.db.save_scan_results(session_id, results)
            self._log(f"Results saved to database (session #{session_id}).", "cyan")
        except Exception as e:
            self._log(f"DB save error: {e}", "orange")

    def _export_csv(self):
        if not self._results_buffer:
            messagebox.showinfo("No Data", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.csv"
        )
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["port", "state", "service",
                                                    "risk", "response_time", "banner"])
            writer.writeheader()
            writer.writerows(self._results_buffer)
        self._log(f"Exported CSV → {path}", "green")

    def _export_json(self):
        if not self._results_buffer:
            messagebox.showinfo("No Data", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.json"
        )
        if not path:
            return
        with open(path, "w") as f:
            json.dump({
                "target": self.target_var.get(),
                "timestamp": datetime.now().isoformat(),
                "results": self._results_buffer
            }, f, indent=2)
        self._log(f"Exported JSON → {path}", "green")
