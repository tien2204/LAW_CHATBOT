from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as chat_router

app = FastAPI(title="VN‑Law Chat RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

app.include_router(chat_router)
