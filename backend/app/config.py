from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # đường tới vector store
    chroma_dir: str = Field("./law_db", env="CHROMA_DIR")
    collection_name: str = "vn_law"

    # model embedding & reranker
    embed_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    rerank_model: str = "BAAI/bge-reranker-base"

    # LLM (Groq: mixtral‑8x7b / llama3‑70b‑instruct, …)
    llm_model: str = "mixtral-8x7b"
    llm_temperature: float = 0.0

    groq_api_key: str | None = None    # hoặc OPENAI_API_KEY nếu dùng OpenAI

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
