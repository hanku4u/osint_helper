import sqlite3
import os

def initialize_db():
    # Ensure the session directory exists
    os.makedirs("session", exist_ok=True)
    
    conn = sqlite3.connect("session/session.db")
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS domains (id INTEGER PRIMARY KEY, domain TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS subdomains (id INTEGER PRIMARY KEY, subdomain TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS ips (id INTEGER PRIMARY KEY, ip TEXT UNIQUE);
    CREATE TABLE IF NOT EXISTS dns_records (id INTEGER PRIMARY KEY, record_type TEXT, value TEXT);
    CREATE TABLE IF NOT EXISTS whois_data (id INTEGER PRIMARY KEY, key TEXT, value TEXT);
    CREATE TABLE IF NOT EXISTS nmap_results (id INTEGER PRIMARY KEY, port INTEGER, service TEXT, version TEXT);
    """)
    conn.commit()
    conn.close()

def insert_data(table, data):
    conn = sqlite3.connect("session/session.db")
    cursor = conn.cursor()
    for item in data:
        try:
            cursor.execute(f"INSERT OR IGNORE INTO {table} VALUES (NULL, ?)", (item,))
        except sqlite3.Error as e:
            print(f"Error inserting into {table}: {e}")
    conn.commit()
    conn.close()

def fetch_data(table):
    conn = sqlite3.connect("session/session.db")
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching data from {table}: {e}")
        return []
    finally:
        conn.close()
