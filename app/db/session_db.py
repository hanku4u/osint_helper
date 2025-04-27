import sqlite3
import os
import datetime

DB_DIR = "sessions"
os.makedirs(DB_DIR, exist_ok=True)

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

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS txt_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                name TEXT,
                value TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS srv_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                name TEXT,
                target TEXT,
                port TEXT,
                address TEXT
            )
        ''')

        conn.commit()

# Insertion functions
def insert_target(target):
    with get_connection() as conn:
        conn.execute('INSERT INTO targets (target) VALUES (?)', (target,))
        conn.commit()

def insert_domain(domain):
    with get_connection() as conn:
        conn.execute('INSERT INTO domains (domain) VALUES (?)', (domain,))
        conn.commit()

def insert_email(email):
    with get_connection() as conn:
        conn.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        conn.commit()

def insert_ip(ip):
    with get_connection() as conn:
        conn.execute('INSERT INTO ips (ip) VALUES (?)', (ip,))
        conn.commit()

def insert_host(host):
    with get_connection() as conn:
        conn.execute('INSERT INTO hosts (host) VALUES (?)', (host,))
        conn.commit()

def insert_txt_record(domain, name, value):
    with get_connection() as conn:
        conn.execute('INSERT INTO txt_records (domain, name, value) VALUES (?, ?, ?)', (domain, name, value))
        conn.commit()

def insert_srv_record(domain, name, target, port, address):
    with get_connection() as conn:
        conn.execute('INSERT INTO srv_records (domain, name, target, port, address) VALUES (?, ?, ?, ?, ?)', (domain, name, target, port, address))
        conn.commit()