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
# Save job into the database
# ---------------------------
def save_job(title, company, location, link, source, date_posted):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO jobs (title, company, location, link, source, date_posted)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, company, location, link, source, date_posted),
        )
        conn.commit()
    except Exception as e:
        print("❌ Error inserting job:", e)
    finally:
        conn.close()

# ---------------------------
# Wealthsimple scraper
# ---------------------------
def scrape_wealthsimple():
    print("\n🔍 Scraping Wealthsimple (Lever API)...")

    url = "https://api.lever.co/v0/postings/wealthsimple?mode=json"

    try:
        response = requests.get(url, timeout=15)
    except Exception as e:
        print("❌ Request error:", e)
        return

    if response.status_code != 200:
        print("❌ Failed to fetch Wealthsimple postings:", response.status_code)
        return

    try:
        postings = response.json()
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return

    print(f"📌 Found {len(postings)} total postings")

    count_saved = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    keywords = ["intern", "co-op", "coop", "student", "campus", "summer"]

    for post in postings:
        title = (post.get("text") or "").strip()
        categories = post.get("categories") or {}
        location = (categories.get("location") or "").strip()
        commitment = (categories.get("commitment") or "").lower()
        team = (categories.get("team") or "").lower()
        link = post.get("hostedUrl") or ""

        # Debug output (shows all found jobs)
        print(f"Found: {title} | Location: {location} | Commitment: {commitment}")

        # Filter for internships
        if not any(k in title.lower() for k in keywords):
            continue

        # Filter for Canada-only roles
        if "canada" not in location.lower() and "toronto" not in location.lower():
            continue

        company = "Wealthsimple"
        source = "Wealthsimple (Lever)"
        date_posted = today_str

        print(f"💾 Saving: {title} @ {company} ({location})")
        save_job(title, company, location, link, source, date_posted)
        count_saved += 1

    print(f"✅ Wealthsimple scraping complete. Saved {count_saved} internships.\n")

# Allow running directly
if __name__ == "__main__":
    scrape_wealthsimple()
