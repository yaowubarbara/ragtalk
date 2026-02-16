"""Hybrid retrieval: combines BM25 (sparse) + embedding (dense) search via RRF.

Reciprocal Rank Fusion (RRF) merges multiple ranked lists into a single ranking
without needing to normalize scores across different retrieval methods.

Formula: RRF_score(d) = Σ 1 / (k + rank_i(d)) for each retrieval method i
"""

from app.config import get_settings
from app.services.vectorstore import query_collection
from app.services.bm25_index import bm25_search


def reciprocal_rank_fusion(
    *result_lists: list[dict],
    k: int = 60,
) -> list[dict]:
    """Fuse multiple ranked result lists using Reciprocal Rank Fusion.

    Args:
        *result_lists: Variable number of ranked document lists
        k: RRF constant (default 60, controls how much rank matters)

    Returns:
        Fused list sorted by combined RRF score
    """
    doc_scores: dict[str, dict] = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            doc_id = doc["id"]
            if doc_id not in doc_scores:
                doc_scores[doc_id] = {
                    "doc": doc,
                    "rrf_score": 0.0,
                    "sources": [],
                }
            doc_scores[doc_id]["rrf_score"] += 1.0 / (k + rank + 1)
            doc_scores[doc_id]["sources"].append(rank + 1)

    fused = sorted(doc_scores.values(), key=lambda x: x["rrf_score"], reverse=True)
    return [
        {**item["doc"], "rrf_score": item["rrf_score"]}
        for item in fused
    ]


def hybrid_search(persona_id: str, query: str, top_k: int | None = None) -> list[dict]:
    """Combine BM25 keyword search + ChromaDB embedding search via RRF.

    Returns more candidates than final top_k to feed into the reranker.
    """
    settings = get_settings()
    candidates = top_k or settings.hybrid_search_top_k

    # Dense retrieval (embedding similarity via ChromaDB)
    embedding_results = query_collection(persona_id, query, top_k=candidates)

    if not settings.enable_hybrid_search:
        return embedding_results[:candidates]

    # Sparse retrieval (BM25 keyword matching)
    bm25_results = bm25_search(persona_id, query, top_k=candidates)

    # Fuse with RRF
    fused = reciprocal_rank_fusion(
        embedding_results,
        bm25_results,
        k=settings.rrf_k,
    )

    return fused[:candidates]
