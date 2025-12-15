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
        print("❌ Insert error:", e)
    finally:
        conn.close()


# ---------------------------
# Shopify scraper
# ---------------------------
def scrape_shopify():
    print("\n🔍 Scraping Shopify (SmartRecruiters API)...")

    api_url = "https://api.smartrecruiters.com/v1/companies/Shopify/postings"

    try:
        response = requests.get(api_url, timeout=15)
    except Exception as e:
        print("❌ Request failed:", e)
        return

    if response.status_code != 200:
        print("❌ Shopify API returned:", response.status_code)
        return

    data = response.json()
    jobs = data.get("content", [])

    print(f"📌 Found {len(jobs)} jobs in Shopify API")

    today = datetime.now().strftime("%Y-%m-%d")
    count_saved = 0

    keywords = ["intern", "student", "co-op", "software", "engineer", "developer"]

    for job in jobs:
        title = job.get("name", "").strip()
        link = job.get("ref", {}).get("id", "")
        link = f"https://jobs.smartrecruiters.com/Shopify/{link}"

        location_info = job.get("location", {})
        location = location_info.get("city") or "Unknown"

        # Filter CS jobs / internships
        if not any(k in title.lower() for k in keywords):
            continue

        company = "Shopify"
        source = "Shopify API"

        print(f"💾 Saving: {title} @ Shopify ({location})")

        save_job(title, company, location, link, source, today)
        count_saved += 1

    print(f"✅ Shopify scraping complete. Saved {count_saved} jobs.\n")


# Run directly
if __name__ == "__main__":
    scrape_shopify()
