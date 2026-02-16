"""Advanced RAG pipeline with hybrid search, reranking, query rewriting, and citations.

Pipeline flow:
  User Query → Query Rewrite (LLM) → Hybrid Search (BM25 + Embedding)
  → RRF Fusion → Cross-Encoder Rerank → Context w/ Citations → LLM Generation

Each stage is independently toggleable via config flags.
"""

import json
from pathlib import Path
from collections.abc import AsyncGenerator

from app.config import get_settings
from app.services.hybrid_retriever import hybrid_search
from app.services.vectorstore import query_collection
from app.services.query_rewriter import rewrite_query
from app.services.reranker import rerank
from app.services.llm import stream_chat_completion
from app.models.schemas import ChatMessage

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
_persona_cache: dict = {}


def load_persona(persona_id: str) -> dict:
    if persona_id not in _persona_cache:
        path = PERSONAS_DIR / f"{persona_id.replace('-', '_')}.json"
        if not path.exists():
            raise FileNotFoundError(f"Persona not found: {persona_id}")
        with open(path) as f:
            _persona_cache[persona_id] = json.load(f)
    return _persona_cache[persona_id]


def list_personas() -> list[dict]:
    personas = []
    for path in PERSONAS_DIR.glob("*.json"):
        with open(path) as f:
            data = json.load(f)
        personas.append({
            "id": data["id"],
            "name": data["name"],
            "title": data["title"],
            "avatar_url": data["avatar_url"],
            "description": data["description"],
            "greeting": data["greeting"],
        })
    return personas


def build_context_block(documents: list[dict]) -> tuple[str, list[dict]]:
    """Build context block with numbered citations.

    Returns:
        (context_string, sources_list) where sources_list contains
        citation metadata for the frontend.
    """
    if not documents:
        return "", []

    parts = [
        "## Reference Materials",
        "Use these real quotes and writings to inform your response.",
        "When you use information from a reference, cite it with [N] notation.\n",
    ]
    sources = []
    for i, doc in enumerate(documents, 1):
        source = doc["metadata"].get("source", "Unknown")
        doc_type = doc["metadata"].get("doc_type", "text")
        parts.append(f"[{i}] (Source: {source}, Type: {doc_type})\n{doc['content']}\n")
        sources.append({
            "id": i,
            "source": source,
            "doc_type": doc_type,
            "text": doc["content"][:200],
        })

    return "\n".join(parts), sources


def build_messages(
    persona: dict,
    user_message: str,
    conversation_history: list[ChatMessage],
    context_block: str,
) -> list[dict]:
    system_content = persona["system_prompt"]
    if context_block:
        system_content += f"\n\n{context_block}"
    system_content += (
        "\n\nIMPORTANT: When referencing information from the Reference Materials, "
        "cite the source using [N] notation (e.g., [1], [2]). "
        "Blend citations naturally into your response."
    )

    messages = [{"role": "system", "content": system_content}]
    for msg in conversation_history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})
    return messages


async def retrieve_context(
    persona_id: str,
    persona_name: str,
    user_message: str,
) -> tuple[list[dict], str | None]:
    """Run the full retrieval pipeline: rewrite → hybrid search → rerank.

    Returns:
        (final_documents, rewritten_query)
    """
    settings = get_settings()
    rewritten_query = None

    # Stage 1: Query rewriting
    search_query = user_message
    if settings.enable_query_rewrite:
        try:
            rewritten_query = await rewrite_query(user_message, persona_name)
            search_query = rewritten_query
        except Exception:
            pass  # Fall back to original query

    # Stage 2: Retrieval (hybrid or embedding-only)
    if settings.enable_hybrid_search:
        candidates = hybrid_search(
            persona_id, search_query, top_k=settings.hybrid_search_top_k
        )
    else:
        candidates = query_collection(
            persona_id, search_query, top_k=settings.hybrid_search_top_k
        )

    # Stage 3: Reranking
    if settings.enable_reranker and len(candidates) > settings.rag_top_k:
        final_docs = await rerank(search_query, candidates, top_k=settings.rag_top_k)
    else:
        final_docs = candidates[: settings.rag_top_k]

    return final_docs, rewritten_query


async def generate_response(
    persona_id: str,
    user_message: str,
    conversation_history: list[ChatMessage],
) -> AsyncGenerator[str | dict, None]:
    """Full RAG pipeline: retrieve, build context, generate with citations.

    Yields:
        str tokens during generation, then a dict with sources metadata at the end.
    """
    persona = load_persona(persona_id)

    # Retrieval pipeline
    documents, rewritten_query = await retrieve_context(
        persona_id, persona["name"], user_message
    )

    # Build context with citation numbers
    context_block, sources = build_context_block(documents)

    # Build messages for LLM
    messages = build_messages(persona, user_message, conversation_history, context_block)

    # Stream LLM response
    async for token in stream_chat_completion(
        messages=messages,
        temperature=persona.get("temperature", 0.7),
        max_tokens=persona.get("max_tokens", 1024),
    ):
        yield token

    # After all tokens, yield sources metadata
    if sources:
        yield {
            "type": "sources",
            "sources": sources,
            "rewritten_query": rewritten_query,
        }
