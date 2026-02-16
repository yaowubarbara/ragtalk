"""Cross-encoder reranking module.

After initial retrieval (BM25 + embedding), a cross-encoder scores each
(query, document) pair jointly for fine-grained relevance ranking.

Two implementations:
1. LLM-based reranker (default) - uses the existing OpenRouter LLM
2. Cross-encoder model (optional) - uses sentence-transformers locally

The LLM reranker sends all candidates in a single prompt and asks for
a relevance ranking, which is both practical and effective.
"""

import re
from app.services.llm import chat_completion


async def rerank_with_llm(
    query: str,
    documents: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """Rerank documents using the LLM as a cross-encoder judge.

    Sends all candidates in one prompt and parses the returned ranking.
    Falls back to original order if parsing fails.
    """
    if len(documents) <= top_k:
        return documents

    # Build document list for the prompt (truncate long docs)
    doc_entries = []
    for i, doc in enumerate(documents):
        text = doc["content"][:300].replace("\n", " ")
        doc_entries.append(f"[{i + 1}] {text}")
    doc_list = "\n".join(doc_entries)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a relevance judge. Given a query and a list of documents, "
                "rank the documents by relevance to the query. "
                "Output ONLY the document numbers in order from most to least relevant, "
                "comma-separated. Example: 3,1,7,2,5"
            ),
        },
        {
            "role": "user",
            "content": f"Query: {query}\n\nDocuments:\n{doc_list}\n\nRanking:",
        },
    ]

    try:
        response = await chat_completion(messages, temperature=0.0, max_tokens=100)
        # Parse the ranking: extract numbers from the response
        numbers = [int(n) for n in re.findall(r"\d+", response)]
        # Filter valid indices and deduplicate while preserving order
        seen = set()
        ranked_indices = []
        for n in numbers:
            idx = n - 1  # 1-indexed → 0-indexed
            if 0 <= idx < len(documents) and idx not in seen:
                seen.add(idx)
                ranked_indices.append(idx)

        # Add any missing documents at the end
        for i in range(len(documents)):
            if i not in seen:
                ranked_indices.append(i)

        reranked = [documents[i] for i in ranked_indices]
        return reranked[:top_k]

    except Exception:
        # On any failure, return original order truncated
        return documents[:top_k]


_cross_encoder = None
_cross_encoder_loaded = False


def _load_cross_encoder():
    """Try to load sentence-transformers cross-encoder. Returns None if unavailable."""
    global _cross_encoder, _cross_encoder_loaded
    if _cross_encoder_loaded:
        return _cross_encoder
    _cross_encoder_loaded = True
    try:
        from sentence_transformers import CrossEncoder
        _cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    except ImportError:
        _cross_encoder = None
    return _cross_encoder


def rerank_with_cross_encoder(
    query: str,
    documents: list[dict],
    top_k: int = 5,
) -> list[dict] | None:
    """Rerank using a local cross-encoder model. Returns None if model unavailable."""
    model = _load_cross_encoder()
    if model is None:
        return None

    pairs = [(query, doc["content"]) for doc in documents]
    scores = model.predict(pairs)

    scored_docs = list(zip(documents, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in scored_docs[:top_k]]


async def rerank(
    query: str,
    documents: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """Rerank documents. Tries cross-encoder first, falls back to LLM reranker."""
    if not documents:
        return []

    # Try local cross-encoder (faster, no API cost)
    result = rerank_with_cross_encoder(query, documents, top_k)
    if result is not None:
        return result

    # Fall back to LLM-based reranking
    return await rerank_with_llm(query, documents, top_k)
