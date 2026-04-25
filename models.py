import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # users
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        balance REAL DEFAULT 0
    )
    ''')

    # requests
    c.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        type TEXT,
        amount REAL,
        txid TEXT,
        status TEXT DEFAULT 'pending'
    )
    ''')

    conn.commit()
    conn.close()
