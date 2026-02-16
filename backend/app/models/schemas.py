from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    persona_id: str
    message: str
    conversation_history: list[ChatMessage] = []


class PersonaResponse(BaseModel):
    id: str
    name: str
    title: str
    avatar_url: str
    description: str
    greeting: str


class PersonaListResponse(BaseModel):
    personas: list[PersonaResponse]
