import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "..", "..",
        "database",
        "jobs.db"
    )
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def save_job(title, company, location, link, source, date_posted):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO jobs
        (title, company, location, link, source, date_posted)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, company, location, link, source, date_posted))
    conn.commit()
    conn.close()
