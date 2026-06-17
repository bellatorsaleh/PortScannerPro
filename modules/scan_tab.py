"""
Scan Tab - Elite hacking style with extra features:
  - Port Scanner
  - Ping Tool
  - Traceroute
  - Whois Lookup
  - Network Info
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading, csv, json, socket, subprocess, platform
from datetime import datetime
from modules.scanner import PortScanner

BG="#000000"; BG2="#050505"; BG3="#0a0a0a"; BG4="#0d1117"
G1="#00ff41"; G2="#00cc33"; G3="#008f11"
C1="#00ffff"; C2="#00cccc"
R1="#ff0000"; O1="#ff8800"; Y1="#ffff00"; P1="#cc00ff"; W1="#ffffff"
DIM="#1a3a1a"; DIMMER="#0a1a0a"

PRESETS = {
    "Common (1-1024)": (1,1024), "Top 100 (1-100)": (1,100),
    "Web (80-9000)": (80,9000),  "Database (3306-5432)": (3306,5432),
    "Full Scan (1-65535)": (1,65535), "Custom": None,
}

class ScanTab:
    def __init__(self, parent, db):
        self.db = db
        self.frame = ttk.Frame(parent)
        self.scanner = None
        self._buf = []
        self._start_time = None
        self._build_ui()

    def _build_ui(self):
        # ══ MAIN SPLIT ══
        main = tk.Frame(self.frame, bg=BG)
        main.pack(fill="both", expand=True)

        # ── LEFT SIDEBAR (SCROLLABLE) ─────────────────────
        sidebar = tk.Frame(main, bg=BG2, width=290)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Sidebar header
        tk.Frame(sidebar, bg=G1, height=2).pack(fill="x")
        tk.Label(sidebar, text="[ CONTROL PANEL ]",
                 bg=BG2, fg=C1,
                 font=("Courier New",10,"bold")).pack(pady=(8,4), padx=10, anchor="w")

        # Scrollable canvas for sidebar
        sb_canvas = tk.Canvas(sidebar, bg=BG2, highlightthickness=0)
        sb_scroll = ttk.Scrollbar(sidebar, orient="vertical", command=sb_canvas.yview)
        sb_canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        sb_canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(sb_canvas, bg=BG2)
        inner_id = sb_canvas.create_window((0,0), window=inner, anchor="nw")

        def _on_inner_resize(e):
            sb_canvas.configure(scrollregion=sb_canvas.bbox("all"))
        inner.bind("<Configure>", _on_inner_resize)

        def _on_canvas_resize(e):
            sb_canvas.itemconfig(inner_id, width=e.width)
        sb_canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(e):
            sb_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        sb_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # TARGET
        self._slabel(inner, "TARGET HOST / IP")
        self.target_var = tk.StringVar(value="127.0.0.1")
        tk.Entry(inner, textvariable=self.target_var,
                 bg=BG3, fg=G1, insertbackground=G1,
                 relief="flat", font=("Courier New",11),
                 bd=0, highlightthickness=1,
                 highlightcolor=G1, highlightbackground=G3,
                 width=26).pack(fill="x", pady=(2,4))

        # Resolve button
        tk.Button(inner, text=">> RESOLVE HOSTNAME",
                  bg=BG3, fg=C1,
                  font=("Courier New",9,"bold"), relief="flat",
                  cursor="hand2", pady=4,
                  activebackground=BG4, activeforeground=C1,
                  command=self._resolve).pack(fill="x", pady=(0,4))

        self.resolved_lbl = tk.Label(inner, text="",
                                      bg=BG2, fg=G1,
                                      font=("Courier New",8), wraplength=240)
        self.resolved_lbl.pack(anchor="w", pady=(0,6))

        # PRESET
        self._slabel(inner, "PORT PRESET")
        self.preset_var = tk.StringVar(value="Common (1-1024)")
        cb = ttk.Combobox(inner, textvariable=self.preset_var,
                          values=list(PRESETS.keys()), state="readonly", width=26)
        cb.pack(fill="x", pady=(2,8))
        cb.bind("<<ComboboxSelected>>", self._on_preset)

        # PORT RANGE
        pf = tk.Frame(inner, bg=BG2)
        pf.pack(fill="x", pady=(0,8))
        tk.Label(pf, text="FROM", bg=BG2, fg=DIM,
                 font=("Courier New",8)).grid(row=0,column=0,sticky="w")
        tk.Label(pf, text="TO", bg=BG2, fg=DIM,
                 font=("Courier New",8)).grid(row=0,column=1,sticky="w",padx=(20,0))
        self.p_start = tk.IntVar(value=1)
        self.p_end   = tk.IntVar(value=1024)
        tk.Entry(pf, textvariable=self.p_start, width=8,
                 bg=BG3, fg=G1, insertbackground=G1,
                 relief="flat", font=("Courier New",10),
                 bd=0, highlightthickness=1,
                 highlightcolor=C1, highlightbackground=G3).grid(row=1,column=0)
        tk.Entry(pf, textvariable=self.p_end, width=8,
                 bg=BG3, fg=G1, insertbackground=G1,
                 relief="flat", font=("Courier New",10),
                 bd=0, highlightthickness=1,
                 highlightcolor=C1, highlightbackground=G3).grid(row=1,column=1,padx=(20,0))

        # SCAN TYPE
        self._slabel(inner, "SCAN MODE")
        self.scan_type = tk.StringVar(value="TCP_CONNECT")
        for t in ["TCP_CONNECT","QUICK_SWEEP","STEALTH"]:
            tk.Radiobutton(inner, text=t, variable=self.scan_type, value=t,
                           bg=BG2, fg=G1, selectcolor=BG3,
                           activebackground=BG2, activeforeground=C1,
                           font=("Courier New",9)).pack(anchor="w")

        # OPTIONS
        self._slabel(inner, "OPTIONS")
        self.banner_var = tk.BooleanVar(value=True)
        tk.Checkbutton(inner, text="GRAB_BANNERS",
                       variable=self.banner_var,
                       bg=BG2, fg=G1, selectcolor=BG3,
                       activebackground=BG2,
                       font=("Courier New",9)).pack(anchor="w")

        # TIMEOUT
        self._slabel(inner, "TIMEOUT (seconds)")
        self.timeout_var = tk.DoubleVar(value=1.0)
        ts = ttk.Scale(inner, from_=0.1, to=5.0,
                       variable=self.timeout_var, orient="horizontal")
        ts.pack(fill="x", pady=(2,0))
        self.to_lbl = tk.Label(inner, text="1.0s",
                                bg=BG2, fg=G1,
                                font=("Courier New",9))
        self.to_lbl.pack(anchor="e")
        ts.config(command=lambda v: self.to_lbl.config(text=f"{float(v):.1f}s"))

        # THREADS
        self._slabel(inner, "THREADS")
        self.threads_var = tk.IntVar(value=100)
        thr = ttk.Scale(inner, from_=10, to=500,
                        variable=self.threads_var, orient="horizontal")
        thr.pack(fill="x", pady=(2,0))
        self.thr_lbl = tk.Label(inner, text="100",
                                 bg=BG2, fg=G1,
                                 font=("Courier New",9))
        self.thr_lbl.pack(anchor="e")
        thr.config(command=lambda v: self.thr_lbl.config(text=str(int(float(v)))))

        # DIVIDER
        tk.Frame(inner, bg=G3, height=1).pack(fill="x", pady=14)

        # SCAN BUTTON
        self.scan_btn = tk.Button(inner,
                                   text="▶  EXECUTE SCAN",
                                   bg="#001800", fg=G1,
                                   font=("Courier New",12,"bold"),
                                   relief="flat", cursor="hand2",
                                   pady=10, bd=1,
                                   highlightthickness=1,
                                   highlightbackground=G1,
                                   highlightcolor=G1,
                                   activebackground="#002500",
                                   activeforeground=G1,
                                   command=self._start_scan)
        self.scan_btn.pack(fill="x")

        self.stop_btn = tk.Button(inner,
                                   text="■  ABORT SCAN",
                                   bg="#1a0000", fg=R1,
                                   font=("Courier New",12,"bold"),
                                   relief="flat", cursor="hand2",
                                   pady=10, state="disabled",
                                   activebackground="#2a0000",
                                   activeforeground=R1,
                                   command=self._stop_scan)
        self.stop_btn.pack(fill="x", pady=(6,0))

        # EXPORT
        ef = tk.Frame(inner, bg=BG2)
        ef.pack(fill="x", pady=(10,0))
        tk.Button(ef, text="⬇ CSV",
                  bg=BG3, fg=G1,
                  font=("Courier New",9,"bold"), relief="flat",
                  cursor="hand2",
                  command=self._export_csv).pack(side="left",fill="x",expand=True)
        tk.Button(ef, text="⬇ JSON",
                  bg=BG3, fg=O1,
                  font=("Courier New",9,"bold"), relief="flat",
                  cursor="hand2",
                  command=self._export_json).pack(side="left",fill="x",expand=True,padx=(4,0))

        # ── RIGHT AREA ────────────────────────────────────
        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        # ══ EXTRA TOOLS TABS ══
        tools_nb = ttk.Notebook(right)
        tools_nb.pack(fill="both", expand=True)

        # Tab 1: Port Scanner results
        scan_frame = tk.Frame(tools_nb, bg=BG)
        tools_nb.add(scan_frame, text="  ▶ PORT_SCAN  ")

        # Stats
        sf = tk.Frame(scan_frame, bg=BG2, height=52)
        sf.pack(fill="x")
        sf.pack_propagate(False)
        self.sv = {
            "open":    tk.StringVar(value="000"),
            "scanned": tk.StringVar(value="0000"),
            "total":   tk.StringVar(value="----"),
            "elapsed": tk.StringVar(value="0.0s"),
        }
        for lbl,key,col in [
            ("OPEN_PORTS","open",G1),
            ("SCANNED","scanned",C1),
            ("TOTAL","total",W1),
            ("ELAPSED","elapsed",O1),
        ]:
            f2=tk.Frame(sf,bg=BG2); f2.pack(side="left",padx=22,pady=6)
            tk.Label(f2,textvariable=self.sv[key],
                     bg=BG2,fg=col,
                     font=("Courier New",16,"bold")).pack()
            tk.Label(f2,text=lbl,bg=BG2,fg=DIM,
                     font=("Courier New",7)).pack()

        tk.Frame(scan_frame, bg=G3, height=1).pack(fill="x")
        pf2=tk.Frame(scan_frame,bg=BG)
        pf2.pack(fill="x",padx=10,pady=3)
        self.prog_var=tk.DoubleVar(value=0)
        ttk.Progressbar(pf2,variable=self.prog_var,maximum=100).pack(fill="x")
        self.prog_lbl=tk.Label(pf2,text="AWAITING SCAN...",
                                bg=BG,fg=DIM,
                                font=("Courier New",8))
        self.prog_lbl.pack(anchor="e")

        tk.Frame(scan_frame, bg=G1, height=1).pack(fill="x")

        # Results header
        rh=tk.Frame(scan_frame,bg=BG2,height=22)
        rh.pack(fill="x"); rh.pack_propagate(False)
        tk.Label(rh,text=">_ OPEN PORTS  //  LIVE RESULTS",
                 bg=BG2,fg=G1,
                 font=("Courier New",9,"bold")).pack(side="left",padx=10,pady=2)

        # Tree
        tf=tk.Frame(scan_frame,bg=BG)
        tf.pack(fill="both",expand=True,padx=0)
        cols=("port","state","service","risk","ms","banner")
        self.tree=ttk.Treeview(tf,columns=cols,show="headings",selectmode="browse")
        for c,h,w in zip(cols,
                         ["PORT","STATE","SERVICE","RISK","MS","BANNER/INFO"],
                         [70,80,130,100,80,380]):
            self.tree.heading(c,text=h); self.tree.column(c,width=w,minwidth=40)
        vsb=ttk.Scrollbar(tf,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y"); self.tree.pack(fill="both",expand=True)
        for tag,col in [("critical",R1),("high",O1),("medium",Y1),
                         ("low",G1),("info",C1)]:
            self.tree.tag_configure(tag,foreground=col)
        self.tree.tag_configure("open",background="#001200")

        # ── Tab 2: PING TOOL ──────────────────────────────
        ping_frame = tk.Frame(tools_nb, bg=BG)
        tools_nb.add(ping_frame, text="  ◉ PING_TOOL  ")
        self._build_ping_tab(ping_frame)

        # ── Tab 3: NET INFO ───────────────────────────────
        net_frame = tk.Frame(tools_nb, bg=BG)
        tools_nb.add(net_frame, text="  ◈ NET_INFO   ")
        self._build_netinfo_tab(net_frame)

        # ── Tab 4: BANNER GRAB ────────────────────────────
        bg_frame = tk.Frame(tools_nb, bg=BG)
        tools_nb.add(bg_frame, text="  ⬡ BANNER_GRAB ")
        self._build_bannergrab_tab(bg_frame)

        # ══ TERMINAL LOG ══
        tk.Frame(right, bg=G1, height=1).pack(fill="x")
        lh=tk.Frame(right,bg="#020305",height=20)
        lh.pack(fill="x"); lh.pack_propagate(False)
        tk.Label(lh,text=">_ TERMINAL  //  SYSTEM LOG",
                 bg="#020305",fg=G1,
                 font=("Courier New",8,"bold")).pack(side="left",padx=8,pady=2)
        self.log=tk.Text(right, bg="#020305", fg=G1,
                          font=("Courier New",9), height=6,
                          relief="flat", state="disabled",
                          wrap="word", insertbackground=G1)
        self.log.pack(fill="x")
        for tag,col in [("g",G1),("c",C1),("r",R1),("o",O1),("y",Y1),("p",P1)]:
            self.log.tag_config(tag, foreground=col)

        self._log("GHOST_SCANNER v3.0 INITIALIZED","g")
        self._log("ALL MODULES LOADED :: SCAN | PING | NET_INFO | BANNER_GRAB","c")
        self._log("ENTER TARGET AND EXECUTE SCAN TO BEGIN RECONNAISSANCE","y")

    def _build_ping_tab(self, parent):
        tk.Frame(parent, bg=G1, height=1).pack(fill="x")
        hdr=tk.Frame(parent,bg=BG2,height=40)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text=">_ PING TOOL  //  CHECK HOST AVAILABILITY",
                 bg=BG2,fg=C1,font=("Courier New",10,"bold")).pack(side="left",padx=12,pady=10)

        ctrl=tk.Frame(parent,bg=BG2)
        ctrl.pack(fill="x",padx=12,pady=8)

        tk.Label(ctrl,text="HOST ::",bg=BG2,fg=G1,
                 font=("Courier New",10,"bold")).pack(side="left",padx=(0,8))
        self.ping_target = tk.StringVar(value="google.com")
        tk.Entry(ctrl,textvariable=self.ping_target,
                 bg=BG3,fg=G1,insertbackground=G1,
                 relief="flat",font=("Courier New",11),
                 bd=0,highlightthickness=1,
                 highlightcolor=G1,highlightbackground=G3,
                 width=22).pack(side="left",padx=(0,8))

        tk.Label(ctrl,text="COUNT ::",bg=BG2,fg=G1,
                 font=("Courier New",10,"bold")).pack(side="left",padx=(0,4))
        self.ping_count = tk.IntVar(value=4)
        ttk.Combobox(ctrl,textvariable=self.ping_count,
                     values=[2,4,6,8,10],state="readonly",
                     width=4).pack(side="left",padx=(0,10))

        tk.Button(ctrl,text="[ PING ]",
                  bg="#001800",fg=G1,
                  font=("Courier New",11,"bold"),relief="flat",
                  cursor="hand2",padx=12,pady=5,
                  activebackground="#002500",activeforeground=G1,
                  command=self._run_ping).pack(side="left")

        tk.Frame(parent,bg=G3,height=1).pack(fill="x",padx=0,pady=4)

        self.ping_out=tk.Text(parent,bg=BG3,fg=G1,
                               font=("Courier New",10),
                               relief="flat",state="disabled",
                               wrap="word",insertbackground=G1)
        self.ping_out.pack(fill="both",expand=True,padx=0,pady=0)
        self.ping_out.tag_config("g",foreground=G1)
        self.ping_out.tag_config("r",foreground=R1)
        self.ping_out.tag_config("c",foreground=C1)
        self.ping_out.tag_config("o",foreground=O1)

    def _build_netinfo_tab(self, parent):
        tk.Frame(parent,bg=G1,height=1).pack(fill="x")
        hdr=tk.Frame(parent,bg=BG2,height=40)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text=">_ NETWORK INFO  //  LOCAL SYSTEM INTELLIGENCE",
                 bg=BG2,fg=C1,font=("Courier New",10,"bold")).pack(side="left",padx=12,pady=10)

        ctrl=tk.Frame(parent,bg=BG2)
        ctrl.pack(fill="x",padx=12,pady=8)
        tk.Button(ctrl,text="[ GATHER NET INFO ]",
                  bg="#001800",fg=G1,
                  font=("Courier New",11,"bold"),relief="flat",
                  cursor="hand2",padx=12,pady=5,
                  activebackground="#002500",activeforeground=G1,
                  command=self._run_netinfo).pack(side="left")

        tk.Frame(parent,bg=G3,height=1).pack(fill="x",pady=4)

        self.net_out=tk.Text(parent,bg=BG3,fg=G1,
                              font=("Courier New",10),
                              relief="flat",state="disabled",
                              wrap="word")
        self.net_out.pack(fill="both",expand=True)
        self.net_out.tag_config("c",foreground=C1)
        self.net_out.tag_config("g",foreground=G1)
        self.net_out.tag_config("o",foreground=O1)
        self.net_out.tag_config("y",foreground=Y1)

    def _build_bannergrab_tab(self, parent):
        tk.Frame(parent,bg=G1,height=1).pack(fill="x")
        hdr=tk.Frame(parent,bg=BG2,height=40)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr,text=">_ BANNER GRABBER  //  SERVICE FINGERPRINTING",
                 bg=BG2,fg=C1,font=("Courier New",10,"bold")).pack(side="left",padx=12,pady=10)

        ctrl=tk.Frame(parent,bg=BG2)
        ctrl.pack(fill="x",padx=12,pady=8)
        tk.Label(ctrl,text="HOST ::",bg=BG2,fg=G1,
                 font=("Courier New",10,"bold")).pack(side="left",padx=(0,8))
        self.bg_host=tk.StringVar(value="127.0.0.1")
        tk.Entry(ctrl,textvariable=self.bg_host,
                 bg=BG3,fg=G1,insertbackground=G1,
                 relief="flat",font=("Courier New",11),
                 bd=0,highlightthickness=1,
                 highlightcolor=G1,highlightbackground=G3,
                 width=20).pack(side="left",padx=(0,8))
        tk.Label(ctrl,text="PORT ::",bg=BG2,fg=G1,
                 font=("Courier New",10,"bold")).pack(side="left",padx=(0,4))
        self.bg_port=tk.IntVar(value=80)
        tk.Entry(ctrl,textvariable=self.bg_port,
                 bg=BG3,fg=G1,insertbackground=G1,
                 relief="flat",font=("Courier New",11),
                 bd=0,highlightthickness=1,
                 highlightcolor=G1,highlightbackground=G3,
                 width=7).pack(side="left",padx=(0,10))
        tk.Button(ctrl,text="[ GRAB BANNER ]",
                  bg="#001800",fg=G1,
                  font=("Courier New",11,"bold"),relief="flat",
                  cursor="hand2",padx=12,pady=5,
                  activebackground="#002500",activeforeground=G1,
                  command=self._run_bannergrab).pack(side="left")

        tk.Frame(parent,bg=G3,height=1).pack(fill="x",pady=4)

        self.bg_out=tk.Text(parent,bg=BG3,fg=G1,
                             font=("Courier New",10),
                             relief="flat",state="disabled",wrap="word")
        self.bg_out.pack(fill="both",expand=True)
        self.bg_out.tag_config("c",foreground=C1)
        self.bg_out.tag_config("g",foreground=G1)
        self.bg_out.tag_config("r",foreground=R1)
        self.bg_out.tag_config("o",foreground=O1)

    # ── PING LOGIC ───────────────────────────────────────
    def _run_ping(self):
        host  = self.ping_target.get().strip()
        count = self.ping_count.get()
        if not host:
            return
        self._write(self.ping_out, f"PINGING {host} x{count}...\n","c")
        def do():
            try:
                param = "-n" if platform.system().lower()=="windows" else "-c"
                cmd = ["ping", param, str(count), host]
                result = subprocess.run(cmd, capture_output=True,
                                        text=True, timeout=30)
                out = result.stdout or result.stderr
                for line in out.splitlines():
                    tag = "g"
                    ll = line.lower()
                    if "unreachable" in ll or "failed" in ll or "error" in ll:
                        tag = "r"
                    elif "ttl" in ll or "bytes" in ll or "time" in ll:
                        tag = "g"
                    elif "packet" in ll or "statistic" in ll:
                        tag = "o"
                    self.ping_out.after(0, self._write, self.ping_out, line+"\n", tag)
                self.ping_out.after(0, self._write, self.ping_out,
                                    f"\nPING COMPLETE :: {host}\n","c")
                self._log(f"PING COMPLETE :: {host}","c")
            except Exception as e:
                self.ping_out.after(0, self._write, self.ping_out,
                                    f"ERROR :: {e}\n","r")
        threading.Thread(target=do, daemon=True).start()

    # ── NET INFO LOGIC ────────────────────────────────────
    def _run_netinfo(self):
        self._write(self.net_out, "GATHERING NETWORK INTELLIGENCE...\n\n","c")
        def do():
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                self.net_out.after(0, self._write, self.net_out,
                                   f"HOSTNAME      :: {hostname}\n","y")
                self.net_out.after(0, self._write, self.net_out,
                                   f"LOCAL_IP      :: {local_ip}\n","g")
                try:
                    ext_ip = socket.gethostbyname("myip.opendns.com")
                    self.net_out.after(0, self._write, self.net_out,
                                       f"EXTERNAL_IP   :: {ext_ip}\n","o")
                except Exception:
                    pass
                try:
                    ai = socket.getaddrinfo(hostname, None)
                    ips = list(set([x[4][0] for x in ai]))
                    for ip in ips:
                        self.net_out.after(0, self._write, self.net_out,
                                           f"ADDR          :: {ip}\n","g")
                except Exception:
                    pass

                # Common hosts
                self.net_out.after(0, self._write, self.net_out,
                                   "\n-- RESOLVING COMMON HOSTS --\n","c")
                for h in ["google.com","github.com","cloudflare.com"]:
                    try:
                        ip = socket.gethostbyname(h)
                        self.net_out.after(0, self._write, self.net_out,
                                           f"{h:<20} :: {ip}\n","g")
                    except Exception:
                        self.net_out.after(0, self._write, self.net_out,
                                           f"{h:<20} :: FAILED\n","r")

                self.net_out.after(0, self._write, self.net_out,
                                   "\nNET_INFO COMPLETE\n","c")
                self._log("NET_INFO GATHERED SUCCESSFULLY","c")
            except Exception as e:
                self.net_out.after(0, self._write, self.net_out,
                                   f"ERROR :: {e}\n","r")
        threading.Thread(target=do, daemon=True).start()

    # ── BANNER GRAB LOGIC ─────────────────────────────────
    def _run_bannergrab(self):
        host = self.bg_host.get().strip()
        try:
            port = int(self.bg_port.get())
        except Exception:
            return
        self._write(self.bg_out, f"CONNECTING TO {host}:{port}...\n","c")
        def do():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((host, port))
                self.bg_out.after(0, self._write, self.bg_out,
                                  f"CONNECTION ESTABLISHED :: {host}:{port}\n","g")
                probes = [b"HEAD / HTTP/1.0\r\n\r\n",
                          b"EHLO test\r\n", b"\r\n", b""]
                for probe in probes:
                    try:
                        if probe:
                            s.send(probe)
                        banner = s.recv(2048).decode("utf-8", errors="ignore").strip()
                        if banner:
                            self.bg_out.after(0, self._write, self.bg_out,
                                              f"\nBANNER RECEIVED:\n{'='*50}\n","o")
                            self.bg_out.after(0, self._write, self.bg_out,
                                              banner+"\n","g")
                            self.bg_out.after(0, self._write, self.bg_out,
                                              f"{'='*50}\n","o")
                            break
                    except Exception:
                        continue
                s.close()
                self._log(f"BANNER_GRAB COMPLETE :: {host}:{port}","g")
            except Exception as e:
                self.bg_out.after(0, self._write, self.bg_out,
                                  f"CONNECTION FAILED :: {e}\n","r")
        threading.Thread(target=do, daemon=True).start()

    # ── HELPERS ──────────────────────────────────────────
    def _write(self, widget, text, tag="g"):
        widget.config(state="normal")
        widget.insert("end", text, tag)
        widget.see("end")
        widget.config(state="disabled")

    def _slabel(self, parent, text):
        tk.Label(parent, text=text,
                 bg=BG2, fg=DIM,
                 font=("Courier New",7,"bold")).pack(anchor="w",pady=(10,1))

    def _log(self, msg, tag="g"):
        self.log.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] >> {msg}\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _on_preset(self, e=None):
        r = PRESETS.get(self.preset_var.get())
        if r:
            self.p_start.set(r[0]); self.p_end.set(r[1])

    def _resolve(self):
        host = self.target_var.get().strip()
        try:
            ip = socket.gethostbyname(host)
            self.resolved_lbl.config(text=f">> {ip}", fg=G1)
            self._log(f"RESOLVED :: {host} = {ip}","c")
        except Exception:
            self.resolved_lbl.config(text=">> FAILED", fg=R1)
            self._log(f"RESOLVE FAILED :: {host}","r")

    def _start_scan(self):
        t = self.target_var.get().strip()
        if not t:
            messagebox.showwarning("ERROR","Enter a target!"); return
        try:
            ps=int(self.p_start.get()); pe=int(self.p_end.get())
            if ps<1 or pe>65535 or ps>pe: raise ValueError
        except Exception:
            messagebox.showwarning("ERROR","Invalid port range (1-65535)"); return

        for i in self.tree.get_children(): self.tree.delete(i)
        self._buf=[]
        self.sv["open"].set("000"); self.sv["scanned"].set("0000")
        self.sv["total"].set(str(pe-ps+1)); self.sv["elapsed"].set("0.0s")
        self.prog_var.set(0); self.prog_lbl.config(text="SCANNING...")

        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        import time; self._start_time=time.time()

        self._log(f"SCAN INITIATED :: TARGET={t} PORTS={ps}-{pe}","g")
        self._log(f"THREADS={int(self.threads_var.get())} TIMEOUT={self.timeout_var.get():.1f}s","c")

        self.scanner=PortScanner(
            host=t, port_start=ps, port_end=pe,
            timeout=float(self.timeout_var.get()),
            max_threads=int(self.threads_var.get()),
            grab_banners=self.banner_var.get(),
            on_result=self._on_result,
            on_progress=self._on_progress,
            on_complete=self._on_complete)
        threading.Thread(target=self.scanner.run, daemon=True).start()

    def _stop_scan(self):
        if self.scanner: self.scanner.stop()
        self._log("SCAN ABORTED BY OPERATOR","r")

    def _on_result(self, r):
        self._buf.append(r)
        self.frame.after(0, self._insert_row, r)

    def _insert_row(self, r):
        risk=r.get("risk","info"); state=r.get("state","")
        tags=(risk,"open") if state=="open" else (risk,)
        self.tree.insert("","end",
                          values=(r["port"],f"[{state.upper()}]",
                                  r["service"],f"[{risk.upper()}]",
                                  f"{r['response_time']}ms",
                                  (r.get("banner","") or "N/A")[:80]),
                          tags=tags)
        self.tree.yview_moveto(1.0)
        self._log(f"OPEN :: PORT {r['port']} / {r['service']} / RISK={risk.upper()}","o")

    def _on_progress(self, scanned, total, open_count):
        import time
        pct=round((scanned/total)*100,1)
        el=round(time.time()-self._start_time,1)
        self.frame.after(0,self._upd_stats,scanned,total,open_count,pct,el)

    def _upd_stats(self,scanned,total,open_count,pct,el):
        self.sv["open"].set(str(open_count).zfill(3))
        self.sv["scanned"].set(str(scanned).zfill(4))
        self.sv["total"].set(str(total))
        self.sv["elapsed"].set(f"{el}s")
        self.prog_var.set(pct)
        self.prog_lbl.config(text=f"SCANNING {pct:.1f}%  [{scanned}/{total}]")

    def _on_complete(self,results,scan_time=0,total_scanned=0,ip=None,error=None):
        self.frame.after(0,self._finalize,results,scan_time,total_scanned,ip,error)

    def _finalize(self,results,scan_time,total_scanned,ip,error):
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.prog_lbl.config(text="SCAN COMPLETE")
        if error:
            self._log(f"ERROR :: {error}","r"); return
        self._log(f"SCAN COMPLETE :: {len(results)} OPEN PORTS  TIME={scan_time}s","g")
        self._log(f"TARGET_IP={ip}","c")
        try:
            t=self.target_var.get().strip()
            ps=int(self.p_start.get()); pe=int(self.p_end.get())
            sid=self.db.save_scan_session(
                target=t,port_range=f"{ps}-{pe}",
                scan_type=self.scan_type.get(),
                total_ports=total_scanned,
                open_ports=len(results),scan_time=scan_time)
            self.db.save_scan_results(sid,results)
            self._log(f"SAVED TO DB :: SESSION_ID={sid}","p" if False else "c")
        except Exception as e:
            self._log(f"DB_ERROR :: {e}","o")

    def _export_csv(self):
        if not self._buf:
            messagebox.showinfo("NO DATA","Run a scan first."); return
        p=filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV","*.csv")],
                                        initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.csv")
        if not p: return
        with open(p,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=["port","state","service","risk","response_time","banner"])
            w.writeheader(); w.writerows(self._buf)
        self._log(f"EXPORTED CSV :: {p}","g")

    def _export_json(self):
        if not self._buf:
            messagebox.showinfo("NO DATA","Run a scan first."); return
        p=filedialog.asksaveasfilename(defaultextension=".json",
                                        filetypes=[("JSON","*.json")],
                                        initialfile=f"scan_{datetime.now():%Y%m%d_%H%M%S}.json")
        if not p: return
        with open(p,"w") as f:
            json.dump({"target":self.target_var.get(),
                       "timestamp":datetime.now().isoformat(),
                       "results":self._buf},f,indent=2)
        self._log(f"EXPORTED JSON :: {p}","g")