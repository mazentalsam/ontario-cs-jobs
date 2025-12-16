import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from database.db import save_job


# ---------------------------
# Google Careers scraper (Next.js JSON extraction)
# ---------------------------
def scrape_google():
    print("\n🔍 Scraping Google Careers internships...")

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

    # Google embeds all job data inside __NEXT_DATA__
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script_tag or not script_tag.string:
        print("❌ Could not find NEXT_DATA JSON")
        return

    try:
        data = json.loads(script_tag.string)
    except Exception as e:
        print("❌ Failed to parse NEXT_DATA JSON:", e)
        return

    # Navigate Next.js structure
    try:
        jobs = data["props"]["pageProps"]["jobSearchResponse"]["jobs"]
    except KeyError:
        print("❌ Could not locate job data in JSON")
        return

    print(f"📌 Found {len(jobs)} internship postings")

    today = datetime.now().strftime("%Y-%m-%d")
    saved = 0

    CS_KEYWORDS = [
        "software", "engineer", "swe",
        "developer", "data", "ml", "intern"
    ]

    for job in jobs:
        title = (job.get("title") or "").strip()
        if not title:
            continue

        title_lower = title.lower()
        if not any(k in title_lower for k in CS_KEYWORDS):
            continue

        locations = job.get("locations") or []
        location = ", ".join(locations) if locations else "Unknown"

        job_id = job.get("id")
        if not job_id:
            continue

        link = f"https://careers.google.com/jobs/results/{job_id}/"

        print(f"💾 Saving: {title} @ Google ({location})")

        save_job(
            title=title,
            company="Google",
            location=location,
            link=link,
            source="Google Careers",
            date_posted=today
        )

        saved += 1

    print(f"✅ Google scraping complete. Saved {saved} internships.\n")


# ---------------------------
# Run directly
# ---------------------------
if __name__ == "__main__":
    scrape_google()
