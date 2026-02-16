"""Main ingestion pipeline: read raw JSON → clean → chunk → upsert to ChromaDB."""

import json
import hashlib
from pathlib import Path

from ingestion.cleaner import clean_text, is_useful
from ingestion.chunker import chunk_document
from app.services.vectorstore import get_collection


RAW_DATA_DIR = Path("data/raw")


def generate_id(text: str, source: str) -> str:
    """Generate a deterministic ID for deduplication."""
    return hashlib.md5(f"{source}:{text}".encode()).hexdigest()


def ingest_file(filepath: Path):
    """Process one raw JSON file and upsert to ChromaDB."""
    print(f"\nProcessing {filepath.name}...")

    with open(filepath) as f:
        documents = json.load(f)

    if not documents:
        print(f"  No documents in {filepath.name}")
        return

    persona_id = documents[0]["persona_id"]
    collection = get_collection(persona_id)

    ids = []
    texts = []
    metadatas = []
    seen_ids = set()

    for doc in documents:
        cleaned = clean_text(doc["content"])
        if not is_useful(cleaned):
            continue

        chunks = chunk_document(cleaned, doc["doc_type"])

        for chunk in chunks:
            doc_id = generate_id(chunk, doc["source"])
            if doc_id in seen_ids:
                continue
            seen_ids.add(doc_id)
            ids.append(doc_id)
            texts.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "doc_type": doc["doc_type"],
                "persona_id": doc["persona_id"],
            })

    if not ids:
        print(f"  No valid chunks from {filepath.name}")
        return

    # Upsert in batches of 500
    batch_size = 500
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_texts = texts[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]
        collection.upsert(ids=batch_ids, documents=batch_texts, metadatas=batch_meta)

    print(f"  Upserted {len(ids)} chunks to collection '{persona_id}'")


def main():
    if not RAW_DATA_DIR.exists():
        print(f"No raw data directory found at {RAW_DATA_DIR}")
        print("Run scrapers first: python -m scrapers.run_all")
        return

    json_files = list(RAW_DATA_DIR.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {RAW_DATA_DIR}")
        return

    print(f"Found {len(json_files)} data files to ingest")
    for filepath in json_files:
        ingest_file(filepath)

    print("\nIngestion complete!")


if __name__ == "__main__":
    main()
