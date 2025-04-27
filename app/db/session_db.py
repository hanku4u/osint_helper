# app/db/session_db.py

import sqlite3
import os
import datetime

DB_DIR = "sessions"
os.makedirs(DB_DIR, exist_ok=True)

# DB_PATH is now initialized dynamically
DB_PATH = None

def set_db_path(path=None):
    global DB_PATH
    if path:
        DB_PATH = os.path.join(DB_DIR, path)
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        DB_PATH = os.path.join(DB_DIR, f"session_{timestamp}.db")

def get_connection():
    if not DB_PATH:
        raise Exception("Database path not set. Call set_db_path() first.")
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS harvester_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                value TEXT,
                source TEXT
            )
        ''')
        conn.commit()

def insert_harvester_result(result_type, value, source):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO harvester_results (type, value, source)
            VALUES (?, ?, ?)
        ''', (result_type, value, source))
        conn.commit()

def fetch_all_harvester_results():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT type, value, source FROM harvester_results')
        return cursor.fetchall()
