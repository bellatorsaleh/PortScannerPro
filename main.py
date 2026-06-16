"""
PortScannerPro - Advanced Network Port Scanner
"""

import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.database import DatabaseManager
from modules.main_window import MainWindow


def main():
    root = tk.Tk()
    root.withdraw()

    db = DatabaseManager()
    db.initialize()

    def launch_main():
        root.deiconify()
        app = MainWindow(root, db)

    root.after(500, launch_main)
    root.mainloop()


if __name__ == "__main__":
    main()