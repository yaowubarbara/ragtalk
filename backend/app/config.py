from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    llm_model: str = "meta-llama/llama-3.1-8b-instruct"
    chroma_db_path: str = "./chroma_db"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # RAG pipeline settings
    rag_top_k: int = 5
    hybrid_search_top_k: int = 20
    rrf_k: int = 60

    # Feature flags
    enable_query_rewrite: bool = True
    enable_hybrid_search: bool = True
    enable_reranker: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
