"""Scrape Farnam Street blog articles for multiple personas."""

import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, ScrapedDocument

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class FSBlogScraper(BaseScraper):
    """Generic FS Blog scraper that takes persona_id and a list of URLs."""

    def __init__(self, persona_id: str, urls: list[str]):
        super().__init__(persona_id=persona_id)
        self.urls = urls

    def scrape(self) -> list[ScrapedDocument]:
        print(f"Scraping Farnam Street blog for {self.persona_id}...")
        documents = []

        for url in self.urls:
            try:
                docs = self._scrape_article(url)
                documents.extend(docs)
                print(f"  {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}: {len(docs)} passages")
            except Exception as e:
                print(f"  Error on {url}: {e}")

        print(f"Total: {len(documents)} passages from FS Blog for {self.persona_id}")
        return documents

    def _scrape_article(self, url: str) -> list[ScrapedDocument]:
        resp = httpx.get(url, timeout=30, follow_redirects=True, headers=HEADERS)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        article = soup.find("article") or soup.find("div", {"class": "entry-content"})
        if not article:
            article = soup.find("main") or soup

        for tag in article(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        documents = []
        for p in article.find_all(["p", "blockquote", "li"]):
            text = p.get_text(strip=True)
            if len(text) < 40:
                continue
            if any(kw in text.lower() for kw in [
                "subscribe", "cookie", "privacy policy", "share this",
                "click here", "newsletter", "terms of service",
            ]):
                continue

            doc_type = "quote" if p.name == "blockquote" else "article"
            documents.append(ScrapedDocument(
                content=text,
                source=f"Farnam Street Blog",
                persona_id=self.persona_id,
                doc_type=doc_type,
                metadata={"url": url},
            ))

        return documents


class FSBlogMungerScraper(FSBlogScraper):
    def __init__(self):
        super().__init__(
            persona_id="charlie-munger",
            urls=[
                "https://fs.blog/charlie-munger-mental-models/",
                "https://fs.blog/charlie-munger-recommended-books/",
                "https://fs.blog/munger-operating-system/",
                "https://fs.blog/charlie-munger-dubridge-lecture/",
                "https://fs.blog/charlie-munger-if-i-were-teaching-business-school/",
                "https://fs.blog/charlie-munger-mental-toolbox/",
                "https://fs.blog/charlie-munger-notions/",
                "https://fs.blog/charlie-munger-thinking-backward-forward/",
                "https://fs.blog/charlie-munger-wisdom/",
                "https://fs.blog/great-talks/academic-economics-charlie-munger/",
                "https://fs.blog/great-talks/guarantee-life-misery-charlie-munger/",
            ],
        )


class FSBlogBuffettScraper(FSBlogScraper):
    def __init__(self):
        super().__init__(
            persona_id="warren-buffett",
            urls=[
                "https://fs.blog/warren-buffett-information/",
                "https://fs.blog/2013/05/the-buffett-formula-how-to-get-smarter/",
            ],
        )


if __name__ == "__main__":
    for Cls, fname in [
        (FSBlogMungerScraper, "fsblog_munger.json"),
        (FSBlogBuffettScraper, "fsblog_buffett.json"),
    ]:
        s = Cls()
        docs = s.scrape()
        if docs:
            s.save(docs, fname)
