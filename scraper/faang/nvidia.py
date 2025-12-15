import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from datetime import datetime

# ------------------------------------------------
# DB connection
# ------------------------------------------------
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------------------------
# Save job
# ------------------------------------------------
def save_job(title, company, location, link, source, date_posted):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO jobs
            (title, company, location, link, source, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, company, location, link, source, date_posted),
        )
        conn.commit()
    except Exception as e:
        print("❌ Insert error:", e)
    finally:
        conn.close()

# ------------------------------------------------
# Scrape NVIDIA University Jobs
# ------------------------------------------------
def scrape_nvidia():
    print("\n🔍 Scraping NVIDIA University Internships...")

    url = "https://nvidia.wd5.myworkdayjobs.com/en-US/UniversityJobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"❌ NVIDIA returned status {res.status_code}")
        return

    soup = BeautifulSoup(res.text, "html.parser")

    # Job cards
    jobs = soup.select("li[data-automation-id='jobPosting']")

    print(f"📌 Found {len(jobs)} NVIDIA postings")

    cs_keywords = [
        "software",
        "engineer",
        "developer",
        "intern",
        "ml",
        "machine",
        "deep learning",
        "data",
        "robotics",
        "cuda",
        "systems",
        "computer",
    ]

    today = datetime.now().strftime("%Y-%m-%d")
    saved = 0

    for job in jobs:
        title_el = job.select_one("a[data-automation-id='jobTitle']")
        location_el = job.select_one("div[data-automation-id='locations']")

        if not title_el:
            continue

        title = title_el.text.strip()
        link = "https://nvidia.wd5.myworkdayjobs.com" + title_el["href"]

        location = location_el.text.strip() if location_el else "Unknown"

        # Only CS-related roles
        if not any(k in title.lower() for k in cs_keywords):
            continue

        print(f"💾 Saving: {title} ({location})")

        save_job(
            title=title,
            company="NVIDIA",
            location=location,
            link=link,
            source="NVIDIA University",
            date_posted=today,
        )

        saved += 1

    print(f"✅ NVIDIA scraping complete. Saved {saved} internships.\n")


if __name__ == "__main__":
    scrape_nvidia()
