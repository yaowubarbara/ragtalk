from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    persona_id: str
    message: str
    conversation_history: list[ChatMessage] = []


class Citation(BaseModel):
    id: int
    source: str
    doc_type: str
    text: str


class PersonaResponse(BaseModel):
    id: str
    name: str
    title: str
    avatar_url: str
    description: str
    greeting: str


class PersonaListResponse(BaseModel):
    personas: list[PersonaResponse]
