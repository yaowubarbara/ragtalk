"""BM25 keyword search index built from ChromaDB document collections.

Provides sparse retrieval to complement ChromaDB's dense (embedding) search.
The combination of sparse + dense retrieval (hybrid search) captures both
exact keyword matches and semantic similarity.
"""

import re
from rank_bm25 import BM25Okapi
from app.services.vectorstore import get_all_documents


# In-memory BM25 index cache per persona
_index_cache: dict[str, dict] = {}


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenizer with lowercasing."""
    return re.findall(r"\w+", text.lower())


def get_or_build_index(persona_id: str) -> dict:
    """Get or lazily build the BM25 index for a persona from ChromaDB data."""
    if persona_id not in _index_cache:
        all_docs = get_all_documents(persona_id)
        documents = all_docs.get("documents", [])
        if not documents:
            _index_cache[persona_id] = {
                "bm25": None,
                "documents": [],
                "metadatas": [],
                "ids": [],
            }
        else:
            tokenized_corpus = [_tokenize(doc) for doc in documents]
            bm25 = BM25Okapi(tokenized_corpus)
            _index_cache[persona_id] = {
                "bm25": bm25,
                "documents": documents,
                "metadatas": all_docs.get("metadatas", []),
                "ids": all_docs.get("ids", []),
            }
    return _index_cache[persona_id]


def invalidate_cache(persona_id: str | None = None):
    """Clear BM25 cache. Call after re-ingestion."""
    if persona_id:
        _index_cache.pop(persona_id, None)
    else:
        _index_cache.clear()


def bm25_search(persona_id: str, query: str, top_k: int = 10) -> list[dict]:
    """Search using BM25 keyword matching. Returns results sorted by BM25 score."""
    index = get_or_build_index(persona_id)
    if index["bm25"] is None or not index["documents"]:
        return []

    tokenized_query = _tokenize(query)
    scores = index["bm25"].get_scores(tokenized_query)

    # Get top-k indices sorted by score descending
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    results = []
    for idx in sorted_indices[:top_k]:
        if scores[idx] <= 0:
            break
        results.append({
            "content": index["documents"][idx],
            "metadata": index["metadatas"][idx] if index["metadatas"] else {},
            "id": index["ids"][idx] if index["ids"] else str(idx),
            "score": float(scores[idx]),
        })
    return results
