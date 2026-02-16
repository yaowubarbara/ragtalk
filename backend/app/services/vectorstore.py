import chromadb
from app.config import get_settings


_client: chromadb.ClientAPI | None = None


def get_chroma_client() -> chromadb.ClientAPI:
    global _client
    if _client is None:
        settings = get_settings()
        _client = chromadb.PersistentClient(path=settings.chroma_db_path)
    return _client


def get_collection(persona_id: str) -> chromadb.Collection:
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=persona_id,
        metadata={"hnsw:space": "cosine"},
    )


def query_collection(persona_id: str, query: str, top_k: int = 5) -> list[dict]:
    collection = get_collection(persona_id)
    if collection.count() == 0:
        return []
    results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))
    documents = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i] if results["metadatas"] else {}
        documents.append({"content": doc, "metadata": meta})
    return documents
