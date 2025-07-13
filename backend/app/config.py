from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):

    serpapi_key: str | None = Field(default=None, env="SERP_API_KEY")         # cho web‑search fallback
    score_threshold: float = 0.28          # ngưỡng router
    
    # đường tới vector store
    chroma_dir: str = Field("./law_db", env="CHROMA_DIR")
    collection_name: str = "vn_law"

    # model embedding & reranker
    embed_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    rerank_model: str = "BAAI/bge-reranker-base"

    # LLM (Groq: mixtral‑8x7b / llama3‑70b‑instruct, …)
    llm_model: str = "mixtral-8x7b"
    llm_temperature: float = 0.0

    groq_api_key: str | None = Field(default=None, env="GROQ_API_KEY")    # hoặc OPENAI_API_KEY nếu dùng OpenAI

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
