import requests
from datetime import datetime
from database.db import save_job


# ---------------------------
# Amazon JSON API scraper (Canada only)
# ---------------------------
def scrape_amazon():
    print("\n🔍 Scraping Amazon Internships (Canada only)...")

    api_url = (
        "https://www.amazon.jobs/en/search.json"
        "?base_query=intern"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

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
    saved = 0

    # CS-related keywords
    CS_KEYWORDS = [
        "software", "engineer", "developer",
        "sde", "data", "machine", "ml", "intern"
    ]

    # 🇨🇦 Canada location whitelist
    CANADA_KEYWORDS = [
        "canada",
        "toronto", "vancouver", "montreal", "ottawa",
        "waterloo", "mississauga", "brampton",
        "calgary", "edmonton",
        "ontario", "british columbia", "alberta", "quebec",
        "on,", "bc,", "qc,"
    ]

    for job in jobs:
        title = (job.get("title") or "").strip()
        location = (job.get("normalized_location") or "").strip()
        job_path = job.get("job_path") or ""

        if not title or not job_path:
            continue

        title_lower = title.lower()
        location_lower = location.lower()

        # Filter CS roles
        if not any(k in title_lower for k in CS_KEYWORDS):
            continue

        # Filter Canada-only locations
        if not any(c in location_lower for c in CANADA_KEYWORDS):
            continue

        link = "https://www.amazon.jobs" + job_path

        print(f"💾 Saving: {title} ({location})")

        save_job(
            title=title,
            company="Amazon",
            location=location,
            link=link,
            source="Amazon API",
            date_posted=today
        )

        saved += 1

    print(f"✅ Amazon scraping complete. Saved {saved} jobs.\n")


# ---------------------------
# Run directly
# ---------------------------
if __name__ == "__main__":
    scrape_amazon()
