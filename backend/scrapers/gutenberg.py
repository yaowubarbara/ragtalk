"""Scrape full texts from Project Gutenberg for Franklin, Marcus Aurelius, and Confucius."""

import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, ScrapedDocument

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class GutenbergScraper(BaseScraper):
    """Generic Gutenberg HTML book scraper."""

    def __init__(self, persona_id: str, books: list[dict]):
        """
        books: [{"url": "...", "title": "...", "doc_type": "book"}]
        """
        super().__init__(persona_id=persona_id)
        self.books = books

    def scrape(self) -> list[ScrapedDocument]:
        documents = []
        for book in self.books:
            try:
                docs = self._scrape_book(book)
                documents.extend(docs)
                print(f"  {book['title']}: {len(docs)} passages")
            except Exception as e:
                print(f"  Error scraping {book['title']}: {e}")
        print(f"Total: {len(documents)} passages for {self.persona_id}")
        return documents

    def _scrape_book(self, book: dict) -> list[ScrapedDocument]:
        print(f"Scraping: {book['title']}...")
        resp = httpx.get(book["url"], timeout=60, follow_redirects=True, headers=HEADERS)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove Gutenberg header/footer boilerplate
        for div in soup.find_all("div", class_=["pg-boilerplate", "pg-header", "pg-footer"]):
            div.decompose()
        for pre in soup.find_all("pre"):
            pre.decompose()

        documents = []
        # Extract paragraphs
        for p in soup.find_all(["p", "blockquote"]):
            text = p.get_text(strip=True)
            # Skip short/boilerplate
            if len(text) < 50:
                continue
            if any(kw in text.lower() for kw in [
                "gutenberg", "copyright", "license", "donate", "ebook",
                "plain text", "utf-8", "project gutenberg", "transcriber"
            ]):
                continue

            documents.append(ScrapedDocument(
                content=text,
                source=f"{book['title']} (Project Gutenberg)",
                persona_id=self.persona_id,
                doc_type=book.get("doc_type", "book"),
                metadata={"url": book["url"]},
            ))

        return documents


class FranklinGutenbergScraper(GutenbergScraper):
    def __init__(self):
        super().__init__(
            persona_id="benjamin-franklin",
            books=[
                {
                    "url": "https://www.gutenberg.org/cache/epub/20203/pg20203-images.html",
                    "title": "The Autobiography of Benjamin Franklin",
                    "doc_type": "autobiography",
                },
                {
                    "url": "https://www.gutenberg.org/cache/epub/12868/pg12868-images.html",
                    "title": "Poor Richard's Almanack",
                    "doc_type": "almanack",
                },
            ],
        )


class MarcusAureliusGutenbergScraper(GutenbergScraper):
    def __init__(self):
        super().__init__(
            persona_id="marcus-aurelius",
            books=[
                {
                    "url": "https://www.gutenberg.org/cache/epub/2680/pg2680-images.html",
                    "title": "Meditations by Marcus Aurelius",
                    "doc_type": "meditations",
                },
            ],
        )


class ConfuciusGutenbergScraper(GutenbergScraper):
    def __init__(self):
        super().__init__(
            persona_id="confucius",
            books=[
                {
                    "url": "https://www.gutenberg.org/cache/epub/3330/pg3330-images.html",
                    "title": "The Analects of Confucius (Legge translation)",
                    "doc_type": "analects",
                },
            ],
        )


if __name__ == "__main__":
    for Cls, fname in [
        (FranklinGutenbergScraper, "gutenberg_franklin.json"),
        (MarcusAureliusGutenbergScraper, "gutenberg_marcus_aurelius.json"),
        (ConfuciusGutenbergScraper, "gutenberg_confucius.json"),
    ]:
        s = Cls()
        docs = s.scrape()
        if docs:
            s.save(docs, fname)
