"""
MindMusk FastAPI backend.
GET  /health  — liveness check
POST /chat    — SSE streaming response via Sonnet orchestrator + Haiku retrieval
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import anthropic as anthropic_lib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator

from backend.retriever import Retriever
from backend.orchestrator import orchestrate

load_dotenv()

_retriever: Retriever | None = None
_sonnet: anthropic_lib.Anthropic | None = None
_haiku: anthropic_lib.Anthropic | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _retriever, _sonnet, _haiku
    vector_db = os.getenv("VECTOR_DB_PATH", "vector_db")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    _retriever = Retriever(
        vector_db_path=vector_db,
        api_key=os.getenv("VOYAGE_API_KEY", ""),
    )
    _sonnet = anthropic_lib.Anthropic(api_key=anthropic_key)
    _haiku = anthropic_lib.Anthropic(api_key=anthropic_key)

    print(f"[startup] {len(_retriever._layers)} layers loaded from {vector_db}/")
    yield


app = FastAPI(title="MindMusk API", lifespan=lifespan)

_cors_origins_env = os.getenv("CORS_ORIGINS", "")
_extra_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]
_allow_origins = ["http://localhost:3000", "https://*.vercel.app"] + _extra_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message cannot be empty")
        return v


async def sse_generator(user_message: str, history: list[dict]) -> AsyncGenerator[str, None]:
    for text in orchestrate(user_message, history, _retriever, _sonnet, _haiku):
        yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        sse_generator(req.message, req.history),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
