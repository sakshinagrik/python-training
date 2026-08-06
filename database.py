import sqlite3
import os

def init_db():
    os.makedirs("instance", exist_ok=True)

    conn = sqlite3.connect("instance/coaching.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        photo TEXT,
        batch TEXT,
        total_fee INTEGER,
        paid_fee INTEGER,
        remaining_fee INTEGER,
        admission_date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()