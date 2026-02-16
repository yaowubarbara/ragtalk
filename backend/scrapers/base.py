from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class ScrapedDocument:
    content: str
    source: str
    persona_id: str
    doc_type: str  # "quote", "letter", "article"
    metadata: dict = field(default_factory=dict)


class BaseScraper(ABC):
    def __init__(self, persona_id: str, output_dir: str = "data/raw"):
        self.persona_id = persona_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def scrape(self) -> list[ScrapedDocument]:
        pass

    def save(self, documents: list[ScrapedDocument], filename: str):
        path = self.output_dir / filename
        data = [
            {
                "content": doc.content,
                "source": doc.source,
                "persona_id": doc.persona_id,
                "doc_type": doc.doc_type,
                "metadata": doc.metadata,
            }
            for doc in documents
        ]
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(documents)} documents to {path}")
        return path
