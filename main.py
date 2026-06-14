"""
PortScannerPro - Advanced Network Port Scanner
A feature-rich Tkinter GUI application for network security analysis.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add modules path
sys.path.insert(0, os.path.dirname(__file__))

from modules.database import DatabaseManager
from modules.splash_screen import SplashScreen
from modules.main_window import MainWindow


def main():
    root = tk.Tk()
    root.withdraw()  # Hide main window during splash

    db = DatabaseManager()
    db.initialize()

    def launch_main():
        root.deiconify()
        app = MainWindow(root, db)
        root.mainloop()

    splash = SplashScreen(root, callback=launch_main)
    root.mainloop()


if __name__ == "__main__":
    main()
