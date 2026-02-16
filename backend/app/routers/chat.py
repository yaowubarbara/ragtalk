import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.rag import generate_response, load_persona

router = APIRouter()


@router.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        load_persona(request.persona_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Persona not found: {request.persona_id}")

    async def event_stream():
        try:
            async for token in generate_response(
                persona_id=request.persona_id,
                user_message=request.message,
                conversation_history=request.conversation_history,
            ):
                data = json.dumps({"token": token})
                yield f"data: {data}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
