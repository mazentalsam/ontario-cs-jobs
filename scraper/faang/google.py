import requests
import sqlite3
import os
import json
from datetime import datetime
from bs4 import BeautifulSoup

# ---------------------------
# DB connection helper
# ---------------------------
def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# Save job to DB
# ---------------------------
def save_job(title, company, location, link, source, date_posted):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs (title, company, location, link, source, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, company, location, link, source, date_posted))
        conn.commit()
    except Exception as e:
        print("❌ DB insert error:", e)
    finally:
        conn.close()

# ---------------------------
# Google scraper (NEXT.js data extraction)
# ---------------------------
def scrape_google():
    print("\n🔍 Scraping Google Careers...")

    url = "https://careers.google.com/jobs/results/?employment_type=INTERN"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print("❌ Request failed:", e)
        return

    if response.status_code != 200:
        print("❌ Google returned:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Google embeds data inside a JSON script tag
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

    if not script_tag:
        print("❌ Could not find NEXT_DATA JSON script")
        return

    try:
        data = json.loads(script_tag.string)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return

    # Navigate the Next.js structure
    try:
        jobs = data["props"]["pageProps"]["jobSearchResponse"]["jobs"]
    except KeyError:
        print("❌ Could not locate job data in JSON")
        return

    print(f"📌 Found {len(jobs)} internship jobs")

    today = datetime.now().strftime("%Y-%m-%d")
    count_saved = 0

    for job in jobs:
        title = job.get("title", "").strip()
        company = "Google"
        locations = job.get("locations", [])
        location = ", ".join(locations) if locations else "Unknown"
        job_id = job.get("id", "")
        link = f"https://careers.google.com/jobs/results/{job_id}/"

        # Filter for CS / SWE roles
        title_lower = title.lower()
        keywords = ["software", "engineer", "swe", "developer", "data", "ml", "intern"]

        if not any(k in title_lower for k in keywords):
            continue

        print(f"💾 Saving: {title} @ Google ({location})")

        save_job(title, company, location, link, "Google Careers", today)
        count_saved += 1

    print(f"✅ Google scraping complete. Saved {count_saved} internships.\n")

# Run directly
if __name__ == "__main__":
    scrape_google()
