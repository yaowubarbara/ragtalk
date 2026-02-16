"""Run all scrapers and save raw data."""

from scrapers.gutenberg import (
    FranklinGutenbergScraper,
    MarcusAureliusGutenbergScraper,
    ConfuciusGutenbergScraper,
)
from scrapers.fsblog import FSBlogMungerScraper, FSBlogBuffettScraper
from scrapers.twentyfiveiq import TwentyFiveIQMungerScraper
from scrapers.navalmanack import NavalmanackScraper
from scrapers.buffett_sources import BuffettFAQScraper, OldSchoolValueBuffettScraper


def main():
    all_scrapers = [
        # Charlie Munger
        (FSBlogMungerScraper(), "fsblog_munger.json"),
        (TwentyFiveIQMungerScraper(), "twentyfiveiq_munger.json"),
        # Benjamin Franklin
        (FranklinGutenbergScraper(), "gutenberg_franklin.json"),
        # Marcus Aurelius
        (MarcusAureliusGutenbergScraper(), "gutenberg_marcus_aurelius.json"),
        # Warren Buffett
        (BuffettFAQScraper(), "buffettfaq_buffett.json"),
        (OldSchoolValueBuffettScraper(), "osv_buffett.json"),
        (FSBlogBuffettScraper(), "fsblog_buffett.json"),
        # Confucius
        (ConfuciusGutenbergScraper(), "gutenberg_confucius.json"),
        # Naval Ravikant
        (NavalmanackScraper(), "navalmanack_naval.json"),
    ]

    for scraper, filename in all_scrapers:
        print(f"\n{'='*60}")
        print(f"Running {scraper.__class__.__name__}...")
        print(f"{'='*60}")
        try:
            docs = scraper.scrape()
            if docs:
                scraper.save(docs, filename)
            else:
                print(f"No documents scraped by {scraper.__class__.__name__}")
        except Exception as e:
            print(f"Error in {scraper.__class__.__name__}: {e}")

    print("\nAll scrapers finished.")


if __name__ == "__main__":
    main()
