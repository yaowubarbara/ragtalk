"""Query rewriting module: transforms conversational queries into retrieval-optimized forms.

Techniques:
- Direct rewriting: conversational → keyword-rich search query
- HyDE (Hypothetical Document Embeddings): generate a hypothetical answer,
  then use it as the search query for better semantic matching.
"""

from app.services.llm import chat_completion


async def rewrite_query(original_query: str, persona_name: str) -> str:
    """Rewrite a conversational question into a retrieval-optimized search query."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a search query optimizer. Rewrite the user's conversational "
                "question into a clear, specific search query optimized for retrieving "
                f"relevant documents about {persona_name}'s teachings, writings, and philosophy. "
                "Keep the core intent. Output ONLY the rewritten query, nothing else."
            ),
        },
        {"role": "user", "content": original_query},
    ]
    rewritten = await chat_completion(messages, temperature=0.0, max_tokens=100)
    return rewritten.strip().strip('"').strip("'")


async def generate_hyde_document(query: str, persona_name: str) -> str:
    """Generate a hypothetical document that would answer the query (HyDE technique).

    The hypothetical answer is used as the search query, which often retrieves
    better results than the raw question because it's closer in embedding space
    to actual documents.
    """
    messages = [
        {
            "role": "system",
            "content": (
                f"You are {persona_name}. Write a short paragraph (2-3 sentences) "
                "that directly answers the following question in your authentic voice "
                "and style. Use specific concepts and terminology you are known for."
            ),
        },
        {"role": "user", "content": query},
    ]
    hyde_doc = await chat_completion(messages, temperature=0.3, max_tokens=150)
    return hyde_doc.strip()
