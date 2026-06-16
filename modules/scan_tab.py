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

PRESET_RANGES = {
    "Common Ports (1-1024)":        (1, 1024),
    "Well-known (1-100)":           (1, 100),
    "Web Ports (80,443,8080)":      (80, 9000),
    "Database Ports (3306-5432)":   (3306, 5432),
    "Full Scan (1-65535)":          (1, 65535),
    "Custom":                        None
}


class ScanTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.scanner = None
        self._results_buffer = []
        self._scanning = False
        self._start_time = None
        self._build_ui()

    def _build_ui(self):

        # ── TOP CONTROLS BAR ─────────────────────────────────
        top = tk.Frame(self.frame, bg=BG_PANEL)
        top.pack(fill="x", padx=0, pady=0)

        # Row 1 — Target + Preset
        row1 = tk.Frame(top, bg=BG_PANEL)
        row1.pack(fill="x", padx=10, pady=(8, 4))

        tk.Label(row1, text="TARGET:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.target_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(row1, textvariable=self.target_var,
                  width=22).pack(side="left", padx=(0, 6))

        tk.Button(row1, text="Resolve",
                  bg=BG_CARD, fg=ACCENT_CYAN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._resolve_hostname).pack(side="left", padx=(0, 10))

        self.resolved_label = tk.Label(row1, text="",
                                       bg=BG_PANEL, fg=ACCENT_GREEN,
                                       font=("Courier", 9))
        self.resolved_label.pack(side="left", padx=(0, 10))

        tk.Label(row1, text="PRESET:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.preset_var = tk.StringVar(value="Common Ports (1-1024)")
        preset_cb = ttk.Combobox(row1, textvariable=self.preset_var,
                                  values=list(PRESET_RANGES.keys()),
                                  state="readonly", width=22)
        preset_cb.pack(side="left", padx=(0, 6))
        preset_cb.bind("<<ComboboxSelected>>", self._on_preset)

        # Row 2 — Port range + scan type + options + BUTTONS
        row2 = tk.Frame(top, bg=BG_PANEL)
        row2.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(row2, text="FROM:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.port_start_var = tk.IntVar(value=1)
        ttk.Entry(row2, textvariable=self.port_start_var,
                  width=7).pack(side="left", padx=(0, 6))

        tk.Label(row2, text="TO:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.port_end_var = tk.IntVar(value=1024)
        ttk.Entry(row2, textvariable=self.port_end_var,
                  width=7).pack(side="left", padx=(0, 12))

        tk.Label(row2, text="TYPE:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.scan_type_var = tk.StringVar(value="TCP Connect")
        ttk.Combobox(row2, textvariable=self.scan_type_var,
                     values=["TCP Connect", "Quick Sweep", "Stealth (limited)"],
                     state="readonly", width=14).pack(side="left", padx=(0, 12))

        self.banner_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row2, text="Banners",
                        variable=self.banner_var).pack(side="left", padx=(0, 6))

        tk.Label(row2, text="TIMEOUT:", bg=BG_PANEL, fg=TEXT_DIM,
                 font=("Courier", 9, "bold")).pack(side="left", padx=(0, 4))
        self.timeout_var = tk.DoubleVar(value=1.0)
        ttk.Combobox(row2, textvariable=self.timeout_var,
                     values=[0.5, 1.0, 2.0, 3.0], width=5).pack(side="left", padx=(0, 12))

        # ══ START SCAN BUTTON ══
        self.scan_btn = tk.Button(row2, text="▶  START SCAN",
                                   bg=ACCENT_CYAN, fg=BG_DARK,
                                   font=("Courier", 11, "bold"),
                                   relief="flat", cursor="hand2",
                                   padx=14, pady=5,
                                   command=self._start_scan)
        self.scan_btn.pack(side="left", padx=(0, 6))

        # ══ STOP SCAN BUTTON ══
        self.stop_btn = tk.Button(row2, text="■  STOP",
                                   bg=ACCENT_RED, fg="#ffffff",
                                   font=("Courier", 11, "bold"),
                                   relief="flat", cursor="hand2",
                                   padx=10, pady=5,
                                   state="disabled",
                                   command=self._stop_scan)
        self.stop_btn.pack(side="left", padx=(0, 6))

        # Export buttons
        tk.Button(row2, text="⬇ CSV",
                  bg=BG_CARD, fg=ACCENT_GREEN,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._export_csv).pack(side="left", padx=(0, 4))
        tk.Button(row2, text="⬇ JSON",
                  bg=BG_CARD, fg=ACCENT_ORANGE,
                  font=("Courier", 9), relief="flat", cursor="hand2",
                  command=self._export_json).pack(side="left")

        # ── STATS BAR ─────────────────────────────────────────
        tk.Frame(self.frame, bg=ACCENT_CYAN, height=1).pack(fill="x")

        stats_frame = tk.Frame(self.frame, bg=BG_PANEL, height=50)
        stats_frame.pack(fill="x")
        stats_frame.pack_propagate(False)

        self.stat_vars = {
            "open":    tk.StringVar(value="0"),
            "scanned": tk.StringVar(value="0"),
            "total":   tk.StringVar(value="0"),
            "elapsed": tk.StringVar(value="0.0s"),
        }
        stat_defs = [
            ("OPEN PORTS",  "open",    ACCENT_GREEN),
            ("SCANNED",     "scanned", ACCENT_CYAN),
            ("TOTAL PORTS", "total",   TEXT_DIM),
            ("ELAPSED",     "elapsed", ACCENT_ORANGE),
        ]
        for label, key, color in stat_defs:
            sf = tk.Frame(stats_frame, bg=BG_PANEL)
            sf.pack(side="left", padx=24, pady=6)
            tk.Label(sf, textvariable=self.stat_vars[key],
                     bg=BG_PANEL, fg=color,
                     font=("Courier", 16, "bold")).pack()
            tk.Label(sf, text=label, bg=BG_PANEL, fg=TEXT_DIM,
                     font=("Courier", 7)).pack()

        # ── PROGRESS BAR ──────────────────────────────────────
        prog_frame = tk.Frame(self.frame, bg=BG_DARK)
        prog_frame.pack(fill="x", padx=10, pady=4)
        self.progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(prog_frame, variable=self.progress_var,
                        maximum=100).pack(fill="x")
        self.progress_label = tk.Label(prog_frame, text="",
                                        bg=BG_DARK, fg=TEXT_DIM,
                                        font=("Courier", 8))
        self.progress_label.pack(anchor="e")

        # ── RESULTS TABLE ─────────────────────────────────────
        tree_frame = tk.Frame(self.frame, bg=BG_DARK)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 4))

        cols = ("port", "state", "service", "risk", "response", "banner")
        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                  show="headings", selectmode="browse")
        hdrs = [("PORT", 70), ("STATE", 70), ("SERVICE", 120),
                ("RISK", 90), ("RESPONSE (ms)", 110), ("BANNER / INFO", 350)]
        for (h, w), c in zip(hdrs, cols):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, minwidth=40)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                             command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("critical", foreground=ACCENT_RED)
        self.tree.tag_configure("high",     foreground=ACCENT_ORANGE)
        self.tree.tag_configure("medium",   foreground=ACCENT_YELLOW)
        self.tree.tag_configure("low",      foreground=ACCENT_GREEN)
        self.tree.tag_configure("info",     foreground=ACCENT_CYAN)
        self.tree.tag_configure("open",     background="#0a1a0e")

        # ── LOG CONSOLE ───────────────────────────────────────
        log_frame = tk.Frame(self.frame, bg=BG_PANEL, height=90)
        log_frame.pack(fill="x", padx=10, pady=(0, 6))
        log_frame.pack_propagate(False)

        tk.Label(log_frame, text="SCAN LOG", bg=BG_PANEL, fg=ACCENT_CYAN,
                 font=("Courier", 8, "bold")).pack(anchor="w", padx=6, pady=2)

        self.log_text = tk.Text(log_frame, bg=BG_CARD, fg=TEXT_DIM,
                                 font=("Courier", 8), height=3,
                                 relief="flat", state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.log_text.tag_config("cyan",   foreground=ACCENT_CYAN)
        self.log_text.tag_config("green",  foreground=ACCENT_GREEN)
        self.log_text.tag_config("red",    foreground=ACCENT_RED)
        self.log_text.tag_config("orange", foreground=ACCENT_ORANGE)

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
            self.resolved_label.config(
                text=f"✔ Resolved: {ip}", fg=ACCENT_GREEN)
        except Exception:
            self.resolved_label.config(
                text="✘ Cannot resolve", fg=ACCENT_RED)

    def _log(self, msg, tag="cyan"):
        self.log_text.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{ts}] {msg}\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _start_scan(self):
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("Input Error", "Please enter a target.")
            return
        try:
            p_start = int(self.port_start_var.get())
            p_end   = int(self.port_end_var.get())
            if p_start < 1 or p_end > 65535 or p_start > p_end:
                raise ValueError
        except Exception:
            messagebox.showwarning("Input Error", "Invalid port range (1-65535).")
            return

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

        self._log(f"Scanning {target} ports {p_start}-{p_end}", "cyan")

        self.scanner = PortScanner(
            host=target,
            port_start=p_start,
            port_end=p_end,
            timeout=float(self.timeout_var.get()),
            max_threads=100,
            grab_banners=self.banner_var.get(),
            on_result=self._on_result,
            on_progress=self._on_progress,
            on_complete=self._on_complete
        )

        t = threading.Thread(target=self.scanner.run, daemon=True)
        t.start()

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
        tags  = (risk, "open") if state == "open" else (risk,)
        banner = r.get("banner", "")[:80]
        self.tree.insert("", "end",
                          values=(r["port"], state.upper(), r["service"],
                                  risk.upper(), f"{r['response_time']} ms",
                                  banner or "—"),
                          tags=tags)
        self.tree.yview_moveto(1.0)

    def _on_progress(self, scanned, total, open_count):
        import time
        pct     = (scanned / total) * 100
        elapsed = round(time.time() - self._start_time, 1)
        self.frame.after(0, self._update_stats,
                          scanned, total, open_count, pct, elapsed)

    def _update_stats(self, scanned, total, open_count, pct, elapsed):
        self.stat_vars["open"].set(str(open_count))
        self.stat_vars["scanned"].set(str(scanned))
        self.stat_vars["total"].set(str(total))
        self.stat_vars["elapsed"].set(f"{elapsed}s")
        self.progress_var.set(pct)
        self.progress_label.config(text=f"{pct:.1f}%  ({scanned}/{total})")

    def _on_complete(self, results, scan_time=0,
                     total_scanned=0, ip=None, error=None):
        self.frame.after(0, self._finalize,
                          results, scan_time, total_scanned, ip, error)

    def _finalize(self, results, scan_time, total_scanned, ip, error):
        self._scanning = False
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        if error:
            self._log(f"ERROR: {error}", "red")
            return

        self._log(
            f"Done! {len(results)} open ports in {scan_time}s | IP: {ip}",
            "green")

        try:
            target  = self.target_var.get().strip()
            p_start = int(self.port_start_var.get())
            p_end   = int(self.port_end_var.get())
            sid = self.db.save_scan_session(
                target=target,
                port_range=f"{p_start}-{p_end}",
                scan_type=self.scan_type_var.get(),
                total_ports=total_scanned,
                open_ports=len(results),
                scan_time=scan_time
            )
            self.db.save_scan_results(sid, results)
            self._log(f"Saved to database (session #{sid})", "cyan")
        except Exception as e:
            self._log(f"DB error: {e}", "orange")

    def _export_csv(self):
        if not self._results_buffer:
            messagebox.showinfo("No Data", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.csv")
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["port", "state", "service",
                               "risk", "response_time", "banner"])
            writer.writeheader()
            writer.writerows(self._results_buffer)
        self._log(f"Exported CSV -> {path}", "green")

    def _export_json(self):
        if not self._results_buffer:
            messagebox.showinfo("No Data", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.json")
        if not path:
            return
        with open(path, "w") as f:
            json.dump({
                "target": self.target_var.get(),
                "timestamp": datetime.now().isoformat(),
                "results": self._results_buffer
            }, f, indent=2)
        self._log(f"Exported JSON -> {path}", "green")