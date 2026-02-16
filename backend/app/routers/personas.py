from fastapi import APIRouter
from app.services.rag import list_personas
from app.models.schemas import PersonaListResponse

router = APIRouter()


@router.get("/api/personas", response_model=PersonaListResponse)
async def get_personas():
    personas = list_personas()
    return PersonaListResponse(personas=personas)
