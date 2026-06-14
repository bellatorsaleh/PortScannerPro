"""
Database Manager - SQLite backend for scan history and settings.
"""

import sqlite3
import os
import json
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.db_path = os.path.join(base_dir, "data", "portscanner.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):
        """Create tables if they don't exist."""
        conn = self.get_connection()
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                port_range TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                total_ports INTEGER,
                open_ports INTEGER,
                scan_time REAL,
                timestamp TEXT NOT NULL,
                status TEXT DEFAULT 'completed'
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                port INTEGER NOT NULL,
                state TEXT NOT NULL,
                service TEXT,
                banner TEXT,
                response_time REAL,
                FOREIGN KEY (session_id) REFERENCES scan_sessions(id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS saved_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')

        # Default settings
        defaults = {
            "theme": "dark",
            "timeout": "1.0",
            "threads": "100",
            "auto_detect_service": "1",
            "sound_alerts": "0"
        }
        for k, v in defaults.items():
            c.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES (?, ?)", (k, v))

        conn.commit()
        conn.close()

    def save_scan_session(self, target, port_range, scan_type, total_ports,
                          open_ports, scan_time):
        conn = self.get_connection()
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''
            INSERT INTO scan_sessions
            (target, port_range, scan_type, total_ports, open_ports, scan_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (target, port_range, scan_type, total_ports, open_ports, scan_time, timestamp))
        session_id = c.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def save_scan_results(self, session_id, results):
        conn = self.get_connection()
        c = conn.cursor()
        for r in results:
            c.execute('''
                INSERT INTO scan_results
                (session_id, port, state, service, banner, response_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, r.get("port"), r.get("state"), r.get("service"),
                  r.get("banner", ""), r.get("response_time", 0)))
        conn.commit()
        conn.close()

    def get_scan_history(self, limit=50):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            SELECT id, target, port_range, scan_type, total_ports,
                   open_ports, scan_time, timestamp
            FROM scan_sessions
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_session_results(self, session_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''
            SELECT port, state, service, banner, response_time
            FROM scan_results WHERE session_id = ?
            ORDER BY port
        ''', (session_id,))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_setting(self, key, default=None):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else default

    def set_setting(self, key, value):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
                  (key, str(value)))
        conn.commit()
        conn.close()

    def save_target(self, name, target, notes=""):
        conn = self.get_connection()
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''
            INSERT INTO saved_targets (name, target, notes, created_at)
            VALUES (?, ?, ?, ?)
        ''', (name, target, notes, timestamp))
        conn.commit()
        conn.close()

    def get_saved_targets(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, target, notes, created_at FROM saved_targets ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        return rows

    def delete_saved_target(self, target_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM saved_targets WHERE id = ?", (target_id,))
        conn.commit()
        conn.close()

    def delete_scan_session(self, session_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM scan_results WHERE session_id = ?", (session_id,))
        c.execute("DELETE FROM scan_sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()

    def get_statistics(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM scan_sessions")
        total_scans = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM scan_results WHERE state = 'open'")
        total_open = c.fetchone()[0]
        c.execute("SELECT COUNT(DISTINCT target) FROM scan_sessions")
        unique_targets = c.fetchone()[0]
        c.execute("SELECT AVG(scan_time) FROM scan_sessions")
        avg_time = c.fetchone()[0] or 0
        conn.close()
        return {
            "total_scans": total_scans,
            "total_open_ports": total_open,
            "unique_targets": unique_targets,
            "avg_scan_time": round(avg_time, 2)
        }
