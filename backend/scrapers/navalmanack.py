"""Scrape The Almanack of Naval Ravikant from navalmanack.com."""

import httpx
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper, ScrapedDocument

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Skip non-content pages
SKIP_SLUGS = [
    "important-notes-on-this-book-disclaimer",
    "foreword",
    "erics-note-about-this-book",
    "table-of-contents",
]


class NavalmanackScraper(BaseScraper):
    TOC_URL = "https://www.navalmanack.com/almanack-of-naval-ravikant/table-of-contents"

    def __init__(self):
        super().__init__(persona_id="naval-ravikant")

    def scrape(self) -> list[ScrapedDocument]:
        print("Scraping Navalmanack table of contents...")
        documents = []

        try:
            resp = httpx.get(self.TOC_URL, timeout=30, headers=HEADERS, follow_redirects=True)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error fetching TOC: {e}")
            return documents

        soup = BeautifulSoup(resp.text, "html.parser")
        chapter_urls = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/almanack-of-naval-ravikant/" in href:
                full = href if href.startswith("http") else "https://www.navalmanack.com" + href
                slug = full.rstrip("/").split("/")[-1]
                if slug not in SKIP_SLUGS and full not in chapter_urls and full != self.TOC_URL:
                    chapter_urls.append(full)

        # Deduplicate
        chapter_urls = list(dict.fromkeys(chapter_urls))
        print(f"Found {len(chapter_urls)} chapters to scrape")

        for url in chapter_urls:
            try:
                docs = self._scrape_chapter(url)
                documents.extend(docs)
                if docs:
                    print(f"  {url.split('/')[-1]}: {len(docs)} passages")
            except Exception as e:
                print(f"  Error on {url}: {e}")

        print(f"Total: {len(documents)} passages from Navalmanack")
        return documents

    def _scrape_chapter(self, url: str) -> list[ScrapedDocument]:
        resp = httpx.get(url, timeout=30, headers=HEADERS, follow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Squarespace uses sqs-html-content divs for the actual body text
        html_content_divs = soup.find_all("div", class_="sqs-html-content")
        if not html_content_divs:
            return []

        documents = []
        chapter_title = url.rstrip("/").split("/")[-1].replace("-", " ").title()

        for content in html_content_divs:
            for tag in content(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

        for content in html_content_divs:
            for el in content.find_all(["p", "blockquote", "li", "h2", "h3"]):
                text = el.get_text(strip=True)
                if len(text) < 30:
                    continue
                # Skip boilerplate
                if any(kw in text.lower() for kw in [
                    "subscribe", "cookie", "privacy", "share this",
                    "click here", "sign up", "newsletter",
                    "thank you for visiting", "pay it forward",
                ]):
                    continue

                doc_type = "quote" if el.name == "blockquote" else "article"
                documents.append(ScrapedDocument(
                    content=text,
                    source=f"The Almanack of Naval Ravikant - {chapter_title}",
                    persona_id=self.persona_id,
                    doc_type=doc_type,
                    metadata={"url": url, "chapter": chapter_title},
                ))

        return documents


if __name__ == "__main__":
    s = NavalmanackScraper()
    docs = s.scrape()
    if docs:
        s.save(docs, "navalmanack.json")
