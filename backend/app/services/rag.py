import json
from pathlib import Path
from collections.abc import AsyncGenerator

from app.config import get_settings
from app.services.vectorstore import query_collection
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


def build_context_block(documents: list[dict]) -> str:
    if not documents:
        return ""
    parts = ["## Reference Materials\nUse these real quotes and writings to inform your response:\n"]
    for i, doc in enumerate(documents, 1):
        source = doc["metadata"].get("source", "Unknown")
        parts.append(f"[{i}] (Source: {source})\n{doc['content']}\n")
    return "\n".join(parts)


def build_messages(
    persona: dict,
    user_message: str,
    conversation_history: list[ChatMessage],
    context_block: str,
) -> list[dict]:
    system_content = persona["system_prompt"]
    if context_block:
        system_content += f"\n\n{context_block}"

    messages = [{"role": "system", "content": system_content}]
    for msg in conversation_history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": user_message})
    return messages


async def generate_response(
    persona_id: str,
    user_message: str,
    conversation_history: list[ChatMessage],
) -> AsyncGenerator[str, None]:
    settings = get_settings()
    persona = load_persona(persona_id)

    # RAG retrieval
    documents = query_collection(persona_id, user_message, top_k=settings.rag_top_k)
    context_block = build_context_block(documents)

    # Build messages
    messages = build_messages(persona, user_message, conversation_history, context_block)

    # Stream LLM response
    async for token in stream_chat_completion(
        messages=messages,
        temperature=persona.get("temperature", 0.7),
        max_tokens=persona.get("max_tokens", 1024),
    ):
        yield token
