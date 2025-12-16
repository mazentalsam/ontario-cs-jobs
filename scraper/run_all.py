from scraper.ats.nvidia import scrape_nvidia
from scraper.faang.amazon import scrape_amazon
from scraper.community.github_internships import scrape_github_list
from scraper.faang.google import scrape_google
from scraper.ats.shopify import scrape_shopify
from scraper.ats.wealthsimple import scrape_wealthsimple


def run_scraper(name, fn):
    print(f"\n🚀 Starting {name}...")
    try:
        fn()
        print(f"✅ {name} finished.")
    except Exception as e:
        print(f"❌ {name} failed:", e)


def main():
    print("\n🔥 Running all scrapers...\n")

    run_scraper("NVIDIA", scrape_nvidia)
    run_scraper("Amazon", scrape_amazon)
    run_scraper("GitHub Internships", scrape_github_list)
    run_scraper("Google", scrape_google)
    run_scraper("Shopify", scrape_shopify)
    run_scraper("Wealthsimple", scrape_wealthsimple)

    print("\n✔ All scrapers completed.\n")


if __name__ == "__main__":
    main()
