"""
Splash Screen - Animated startup screen for PortScannerPro.
"""

import tkinter as tk
import threading
import time


class SplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)
        self.splash.configure(bg="#0a0e1a")

        # Center on screen
        w, h = 520, 320
        sw = self.splash.winfo_screenwidth()
        sh = self.splash.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.splash.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()
        self._animate()

    def _build_ui(self):
        canvas = tk.Canvas(self.splash, width=520, height=320,
                           bg="#0a0e1a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Decorative grid lines
        for i in range(0, 520, 40):
            canvas.create_line(i, 0, i, 320, fill="#0d1a2e", width=1)
        for i in range(0, 320, 40):
            canvas.create_line(0, i, 520, i, fill="#0d1a2e", width=1)

        # Glowing border
        canvas.create_rectangle(2, 2, 518, 318, outline="#00d4ff", width=2)
        canvas.create_rectangle(6, 6, 514, 314, outline="#004466", width=1)

        # Icon / Logo area
        canvas.create_text(260, 75, text="⬡", font=("Courier", 52, "bold"),
                           fill="#00d4ff")
        canvas.create_text(260, 75, text="◈", font=("Courier", 28, "bold"),
                           fill="#0a0e1a")

        # Title
        canvas.create_text(260, 145, text="PORT SCANNER PRO",
                           font=("Courier", 22, "bold"), fill="#00d4ff")
        canvas.create_text(260, 170, text="Advanced Network Security Analyzer",
                           font=("Courier", 10), fill="#4a90a4")

        # Version
        canvas.create_text(260, 192, text="v2.0  |  Python + Tkinter  |  SQLite",
                           font=("Courier", 8), fill="#2a5566")

        # Progress bar background
        canvas.create_rectangle(60, 240, 460, 258, fill="#0d1a2e",
                                outline="#004466", width=1)

        self.progress_bar = canvas.create_rectangle(60, 240, 60, 258,
                                                     fill="#00d4ff", outline="")
        self.progress_glow = canvas.create_rectangle(60, 240, 60, 258,
                                                      fill="#005577", outline="")

        self.status_label = canvas.create_text(260, 278,
                                               text="Initializing...",
                                               font=("Courier", 9),
                                               fill="#4a90a4")

        # Corner decorations
        for cx, cy in [(20, 20), (500, 20), (20, 300), (500, 300)]:
            canvas.create_text(cx, cy, text="◇", font=("Courier", 10),
                               fill="#00d4ff")

        self.canvas = canvas

    def _animate(self):
        steps = [
            (10, "Loading core modules..."),
            (30, "Initializing database..."),
            (55, "Loading service definitions..."),
            (75, "Preparing scanner engine..."),
            (90, "Building GUI components..."),
            (100, "Ready. Launching...")
        ]

        def run():
            for pct, msg in steps:
                x_end = 60 + int(400 * pct / 100)
                self.canvas.coords(self.progress_bar, 60, 240, x_end, 258)
                self.canvas.coords(self.progress_glow, max(60, x_end - 30),
                                   240, x_end, 258)
                self.canvas.itemconfig(self.status_label, text=msg)
                self.splash.update()
                time.sleep(0.35)

            time.sleep(0.3)
            self.splash.destroy()
            self.callback()

        t = threading.Thread(target=run, daemon=True)
        t.start()
