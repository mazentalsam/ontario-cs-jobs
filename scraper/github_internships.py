import requests
import sqlite3
import os
import re
from datetime import datetime

RAW_URL = "https://raw.githubusercontent.com/negarprh/Canadian-Tech-Internships-2026/main/README.md"

# ---------------------------
# DB connection helper
# ---------------------------
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# Save job into DB
# ---------------------------
def save_job(title, company, location, link, source, date_posted):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs
            (title, company, location, link, source, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, company, location, link, source, date_posted))
        conn.commit()
    except Exception as e:
        print("❌ DB insert error:", e)
    finally:
        conn.close()

# ---------------------------
# Scrape GitHub Internship List
# ---------------------------
def scrape_github_list():
    print("\n🔍 Scraping GitHub Canadian Internships list...")

    res = requests.get(RAW_URL, timeout=15)
    if res.status_code != 200:
        print("❌ Failed to fetch GitHub README")
        return

    lines = res.text.splitlines()
    started = False
    internships = []

    for line in lines:
        # Detect table header robustly
        if "| Company |" in line and "| Role |" in line:
            started = True
            continue

        if not started:
            continue

        if not line.startswith("|"):
            continue

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 4:
            continue

        company = parts[0]
        title = parts[1]
        location = parts[2]
        link_cell = parts[3]

        # Skip sub-rows (↳)
        if company == "↳":
            continue

        # Extract ALL links in markdown cell
        links = re.findall(r"\((https?://[^)]+)\)", link_cell)

        # We need at least 2:
        # 1) badge image
        # 2) real job URL
        if len(links) < 2:
            continue

        real_job_url = links[-1]  # 🔥 THIS IS THE REAL JOB LINK

        internships.append((company, title, location, real_job_url))

    print(f"📌 Found {len(internships)} valid internships")

    today = datetime.now().strftime("%Y-%m-%d")
    saved = 0

    for company, title, location, link in internships:
        print(f"💾 Saving: {title} @ {company} ({location})")
        save_job(
            title=title,
            company=company,
            location=location,
            link=link,
            source="GitHub Internships List",
            date_posted=today
        )
        saved += 1

    print(f"✅ GitHub scraping complete. Saved {saved} internships.\n")


if __name__ == "__main__":
    scrape_github_list()
