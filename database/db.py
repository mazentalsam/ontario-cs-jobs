import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jobs.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_job(title, company, location, link, source, date_posted):
    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO jobs
            (title, company, location, link, source, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, company, location, link, source, date_posted))
