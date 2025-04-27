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

# Fetching functions
def fetch_targets():
    with get_connection() as conn:
        return conn.execute('SELECT target FROM targets').fetchall()

def fetch_domains():
    with get_connection() as conn:
        return conn.execute('SELECT domain FROM domains').fetchall()

def fetch_emails():
    with get_connection() as conn:
        return conn.execute('SELECT email FROM emails').fetchall()

def fetch_ips():
    with get_connection() as conn:
        return conn.execute('SELECT ip FROM ips').fetchall()

def fetch_hosts():
    with get_connection() as conn:
        return conn.execute('SELECT host FROM hosts').fetchall()
