"""Scrape Warren Buffett content from buffettfaq.com and other sources."""

import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, ScrapedDocument

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class BuffettFAQScraper(BaseScraper):
    """Scrape buffettfaq.com — a curated collection of Buffett's actual words from
    shareholder letters, annual meetings, interviews, and articles."""

    URL = "https://buffettfaq.com/"

    def __init__(self):
        super().__init__(persona_id="warren-buffett")

    def scrape(self) -> list[ScrapedDocument]:
        print(f"Scraping BuffettFAQ: {self.URL}")
        documents = []

        try:
            resp = httpx.get(self.URL, timeout=60, follow_redirects=True, headers=HEADERS)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error fetching BuffettFAQ: {e}")
            return documents

        soup = BeautifulSoup(resp.text, "html.parser")

        for p in soup.find_all(["p", "blockquote"]):
            text = p.get_text(strip=True)
            if len(text) < 50:
                continue
            # Skip boilerplate
            if any(kw in text.lower() for kw in [
                "buffettfaq.com", "copyright", "disclaimer", "subscribe",
                "click here", "share this", "cookie", "privacy",
                "all rights reserved", "admin", "contact",
            ]):
                continue

            doc_type = "quote" if p.name == "blockquote" else "interview"
            documents.append(ScrapedDocument(
                content=text,
                source="BuffettFAQ.com - Warren Buffett in His Own Words",
                persona_id=self.persona_id,
                doc_type=doc_type,
                metadata={"url": self.URL},
            ))

        print(f"Found {len(documents)} passages from BuffettFAQ")
        return documents


class OldSchoolValueBuffettScraper(BaseScraper):
    """Scrape Buffett quotes from Old School Value."""

    URL = "https://www.oldschoolvalue.com/investing-strategy/warren-buffett-quotes/"

    def __init__(self):
        super().__init__(persona_id="warren-buffett")

    def scrape(self) -> list[ScrapedDocument]:
        print(f"Scraping Old School Value Buffett quotes: {self.URL}")
        documents = []

        try:
            resp = httpx.get(self.URL, timeout=30, follow_redirects=True, headers=HEADERS)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            return documents

        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.find("article") or soup.find("div", class_="entry-content") or soup

        for tag in content(["script", "style", "nav", "footer"]):
            tag.decompose()

        for el in content.find_all(["p", "blockquote", "li"]):
            text = el.get_text(strip=True)
            if len(text) < 40:
                continue
            if any(kw in text.lower() for kw in [
                "subscribe", "cookie", "privacy", "share this",
                "click here", "newsletter", "comment", "related post",
                "old school value", "disclosure",
            ]):
                continue

            documents.append(ScrapedDocument(
                content=text,
                source="Old School Value - Warren Buffett Quotes",
                persona_id=self.persona_id,
                doc_type="quote",
                metadata={"url": self.URL},
            ))

        print(f"Found {len(documents)} passages from Old School Value")
        return documents


if __name__ == "__main__":
    for Cls, fname in [
        (BuffettFAQScraper, "buffettfaq.json"),
        (OldSchoolValueBuffettScraper, "osv_buffett.json"),
    ]:
        s = Cls()
        docs = s.scrape()
        if docs:
            s.save(docs, fname)
