from scraper.nvidia import scrape_nvidia
from scraper.amazon import scrape_amazon
from scraper.github_internships import scrape_github_list
from scraper.google import scrape_google
from scraper.shopify import scrape_shopify
from scraper.wealthsimple import scrape_wealthsimple

def main():
    print("\n🚀 Running all scrapers...\n")

    scrape_nvidia()
    scrape_amazon()
    scrape_github_list()
    scrape_google()
    scrape_shopify()
    scrape_wealthsimple()

    print("\n✔ All scrapers finished!\n")

if __name__ == "__main__":
    main()
