import requests
import re
from datetime import datetime
from database.db import save_job

RAW_URL = "https://raw.githubusercontent.com/negarprh/Canadian-Tech-Internships-2026/main/README.md"


def scrape_github_list():
    print("\n🔍 Scraping GitHub Canadian Internships list...")

    try:
        res = requests.get(RAW_URL, timeout=15)
    except Exception as e:
        print("❌ Request failed:", e)
        return

    if res.status_code != 200:
        print("❌ Failed to fetch GitHub README")
        return

    lines = res.text.splitlines()
    started = False
    internships = []

    for line in lines:
        # Detect table header
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

        # Skip sub-rows
        if company == "↳":
            continue

        # Extract links from markdown cell
        links = re.findall(r"\((https?://[^)]+)\)", link_cell)

        # Last link is the real job URL
        if len(links) < 1:
            continue

        real_job_url = links[-1]

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
