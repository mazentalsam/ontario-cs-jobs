import requests
import sqlite3
import os
from datetime import datetime

RAW_URL = "https://raw.githubusercontent.com/negarprh/Canadian-Tech-Internships-2026/main/README.md"


def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "jobs.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


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


def scrape_github_list():
    print("\n🔍 Scraping GitHub Canadian Internships list...")

    r = requests.get(RAW_URL)
    if r.status_code != 200:
        print("❌ Error fetching GitHub list")
        return

    lines = r.text.splitlines()

    internships = []
    started = False

    for line in lines:
        # Detect header
        if "Company" in line and "Role" in line and "Location" in line:
            started = True
            continue

        if started and line.startswith("|"):
            parts = [x.strip() for x in line.split("|")[1:-1]]

            if len(parts) < 4:
                continue

            company = parts[0]
            title = parts[1]      # role
            location = parts[2]   # correct location

            # Extract real link
            raw_link = parts[3]
            link = ""
            if "(" in raw_link:
                link = raw_link.split("(")[1].split(")")[0]

            # Skip sub-rows
            if company == "↳":
                continue

            # Skip useless rows
            if not link.startswith("http"):
                continue

            internships.append((company, title, location, link))

    print(f"📌 Parsed {len(internships)} valid internships")

    today = datetime.now().strftime("%Y-%m-%d")
    count = 0

    for company, title, location, link in internships:
        print(f"💾 Saving: {title} @ {company} ({location})")
        save_job(title, company, location, link, "GitHub Internships List", today)
        count += 1

    print(f"✅ GitHub scraping complete. Saved {count} internships.\n")


if __name__ == "__main__":
    scrape_github_list()
