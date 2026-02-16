from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, personas

app = FastAPI(title="AI Talk With You", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(personas.router)
app.include_router(chat.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
