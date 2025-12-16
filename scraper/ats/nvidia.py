import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database.db import save_job

def scrape_nvidia():
    print("\n🔍 Scraping NVIDIA University Internships...")

    url = "https://nvidia.wd5.myworkdayjobs.com/en-US/UniversityJobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ NVIDIA returned {res.status_code}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    jobs = soup.select("li[data-automation-id='jobPosting']")

    print(f"📌 Found {len(jobs)} NVIDIA postings")

    cs_keywords = [
        "software", "engineer", "developer", "intern",
        "ml", "data", "computer", "systems"
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

        if not any(k in title.lower() for k in cs_keywords):
            continue

        save_job(
            title=title,
            company="NVIDIA",
            location=location,
            link=link,
            source="NVIDIA University",
            date_posted=today
        )

        saved += 1

    print(f"✅ NVIDIA complete. Saved {saved} jobs.\n")


if __name__ == "__main__":
    scrape_nvidia()
