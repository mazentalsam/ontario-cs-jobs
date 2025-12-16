import requests
from datetime import datetime
from database.db import save_job

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

    today = datetime.now().strftime("%Y-%m-%d")
    keywords = ["intern", "co-op", "coop", "student", "campus", "summer"]

    saved = 0

    for post in postings:
        title = (post.get("text") or "").strip()
        categories = post.get("categories") or {}
        location = (categories.get("location") or "").strip()
        link = post.get("hostedUrl") or ""

        # Debug visibility
        print(f"Found: {title} | Location: {location}")

        # Internship filter
        if not any(k in title.lower() for k in keywords):
            continue

        # Canada-only filter
        if not any(c in location.lower() for c in ["canada", "toronto"]):
            continue

        print(f"💾 Saving: {title} @ Wealthsimple ({location})")

        save_job(
            title=title,
            company="Wealthsimple",
            location=location,
            link=link,
            source="Wealthsimple (Lever)",
            date_posted=today
        )

        saved += 1

    print(f"✅ Wealthsimple complete. Saved {saved} internships.\n")


if __name__ == "__main__":
    scrape_wealthsimple()
