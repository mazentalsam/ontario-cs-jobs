import requests
from datetime import datetime
from database.db import save_job

def scrape_shopify():
    print("\n🔍 Scraping Shopify internships...")

    api_url = "https://api.smartrecruiters.com/v1/companies/Shopify/postings"
    response = requests.get(api_url, timeout=15)

    if response.status_code != 200:
        print("❌ Shopify API failed")
        return

    data = response.json()
    jobs = data.get("content", [])

    today = datetime.now().strftime("%Y-%m-%d")
    keywords = ["intern", "student", "co-op", "software", "engineer"]

    saved = 0

    for job in jobs:
        title = job.get("name", "")
        if not any(k in title.lower() for k in keywords):
            continue

        job_id = job.get("ref", {}).get("id")
        link = f"https://jobs.smartrecruiters.com/Shopify/{job_id}"
        location = job.get("location", {}).get("city", "Unknown")

        save_job(
            title=title,
            company="Shopify",
            location=location,
            link=link,
            source="Shopify API",
            date_posted=today
        )

        saved += 1

    print(f"✅ Shopify complete. Saved {saved} jobs.\n")


if __name__ == "__main__":
    scrape_shopify()
