"""
Splash Screen - Animated startup screen for PortScannerPro.
"""

import tkinter as tk
import time


class SplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#0a0e1a")

        w, h = 520, 320
        sw = self.splash.winfo_screenwidth()
        sh = self.splash.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()
        self.splash.after(100, self._animate_step, 0)

    def _build_ui(self):
        canvas = tk.Canvas(self.splash, width=520, height=320,
                           bg="#0a0e1a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        for i in range(0, 520, 40):
            canvas.create_line(i, 0, i, 320, fill="#0d1a2e", width=1)
        for i in range(0, 320, 40):
            canvas.create_line(0, i, 520, i, fill="#0d1a2e", width=1)

        canvas.create_rectangle(2, 2, 518, 318, outline="#00d4ff", width=2)
        canvas.create_rectangle(6, 6, 514, 314, outline="#004466", width=1)

        canvas.create_text(260, 75, text="⬡",
                           font=("Courier", 52, "bold"), fill="#00d4ff")
        canvas.create_text(260, 75, text="◈",
                           font=("Courier", 28, "bold"), fill="#0a0e1a")

        canvas.create_text(260, 145, text="PORT SCANNER PRO",
                           font=("Courier", 22, "bold"), fill="#00d4ff")
        canvas.create_text(260, 170,
                           text="Advanced Network Security Analyzer",
                           font=("Courier", 10), fill="#4a90a4")
        canvas.create_text(260, 192,
                           text="v2.0  |  Python + Tkinter  |  SQLite",
                           font=("Courier", 8), fill="#2a5566")

        canvas.create_rectangle(60, 240, 460, 258,
                                fill="#0d1a2e", outline="#004466", width=1)

        self.progress_bar = canvas.create_rectangle(60, 240, 60, 258,
                                                     fill="#00d4ff", outline="")
        self.status_label = canvas.create_text(260, 278,
                                               text="Initializing...",
                                               font=("Courier", 9),
                                               fill="#4a90a4")
        for cx, cy in [(20, 20), (500, 20), (20, 300), (500, 300)]:
            canvas.create_text(cx, cy, text="◇",
                               font=("Courier", 10), fill="#00d4ff")

        self.canvas = canvas

    def _animate_step(self, step):
        steps = [
            (10, "Loading core modules..."),
            (30, "Initializing database..."),
            (55, "Loading service definitions..."),
            (75, "Preparing scanner engine..."),
            (90, "Building GUI components..."),
            (100, "Ready. Launching...")
        ]

        if step < len(steps):
            pct, msg = steps[step]
            x_end = 60 + int(400 * pct / 100)
            self.canvas.coords(self.progress_bar, 60, 240, x_end, 258)
            self.canvas.itemconfig(self.status_label, text=msg)
            self.splash.after(350, self._animate_step, step + 1)
        else:
            self.splash.after(300, self._finish)

    def _finish(self):
        self.splash.destroy()
        self.callback()