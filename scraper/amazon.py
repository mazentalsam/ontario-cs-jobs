import requests
import sqlite3
import os
from datetime import datetime

# ---------------------------
# DB connection helper
# ---------------------------
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# Save job into database
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
        print("❌ Insert error:", e)
    finally:
        conn.close()

# ---------------------------
# Amazon JSON API scraper
# ---------------------------
def scrape_amazon():
    print("\n🔍 Scraping Amazon Internships (JSON API)...")

    api_url = "https://www.amazon.jobs/en/search.json?base_query=intern&loc_query=canada"

    headers = { "User-Agent": "Mozilla/5.0" }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
    except Exception as e:
        print("❌ Request failed:", e)
        return

    if response.status_code != 200:
        print("❌ Amazon API returned:", response.status_code)
        return

    data = response.json()
    jobs = data.get("jobs", [])
    print(f"📌 Found {len(jobs)} Amazon postings in API response")

    today = datetime.now().strftime("%Y-%m-%d")
    count_saved = 0

    keywords = ["software", "engineer", "developer", "sde", "data", "machine", "ml", "intern"]

    for job in jobs:
        title = job.get("title", "").strip()
        location = job.get("normalized_location", "").strip()
        link = "https://www.amazon.jobs" + job.get("job_path", "")

        # Filter CS roles
        if not any(k in title.lower() for k in keywords):
            continue

        print(f"💾 Saving: {title} ({location})")

        save_job(
            title,
            "Amazon",
            location,
            link,
            "Amazon API",
            today
        )
        count_saved += 1

    print(f"✅ Amazon scraping complete. Saved {count_saved} jobs.\n")

# Run directly
if __name__ == "__main__":
    scrape_amazon()
