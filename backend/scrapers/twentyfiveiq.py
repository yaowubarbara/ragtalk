"""Scrape Charlie Munger quotes from 25iq.com (Tren Griffin's collection)."""

import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, ScrapedDocument

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class TwentyFiveIQMungerScraper(BaseScraper):
    URL = "https://25iq.com/quotations/charlie-munger/"

    def __init__(self):
        super().__init__(persona_id="charlie-munger")

    def scrape(self) -> list[ScrapedDocument]:
        print(f"Scraping 25iq Munger quotes: {self.URL}")
        documents = []

        try:
            resp = httpx.get(self.URL, timeout=30, follow_redirects=True, headers=HEADERS)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error fetching 25iq: {e}")
            return documents

        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.find("div", class_="entry-content") or soup.find("article")
        if not content:
            print("Warning: no content div found")
            return documents

        # Extract numbered quotes (typically in <p> or <ol><li>)
        for el in content.find_all(["p", "li", "blockquote"]):
            text = el.get_text(strip=True)
            if len(text) < 30:
                continue
            # Skip navigation/boilerplate
            if any(kw in text.lower() for kw in [
                "share this:", "like this:", "related", "posted in",
                "click here", "subscribe", "comment", "pingback",
                "twitter", "facebook", "linkedin",
            ]):
                continue

            # Clean up numbered prefixes like "1." "23."
            cleaned = text
            if cleaned and cleaned[0].isdigit():
                # Remove leading "123. " pattern
                parts = cleaned.split(".", 1)
                if len(parts) == 2 and parts[0].strip().isdigit():
                    cleaned = parts[1].strip()
                    if cleaned.startswith('"'):
                        cleaned = cleaned

            if len(cleaned) < 30:
                continue

            documents.append(ScrapedDocument(
                content=cleaned,
                source="25iq.com - Charlie Munger Quotations (Tren Griffin)",
                persona_id=self.persona_id,
                doc_type="quote",
                metadata={"url": self.URL},
            ))

        print(f"Found {len(documents)} quotes from 25iq")
        return documents


if __name__ == "__main__":
    s = TwentyFiveIQMungerScraper()
    docs = s.scrape()
    if docs:
        s.save(docs, "twentyfiveiq_munger.json")
