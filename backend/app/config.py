from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    llm_model: str = "meta-llama/llama-3.1-8b-instruct"
    chroma_db_path: str = "./chroma_db"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    rag_top_k: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
