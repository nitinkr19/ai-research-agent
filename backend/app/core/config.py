"""
Configuration management using environment variables.
Load settings from .env for LLM providers, API keys, and agent behavior.
"""

import os
from pathlib import Path
from functools import lru_cache


@lru_cache
def get_settings() -> "Settings":
    """Load and cache settings."""
    return Settings()


class Settings:
    """Application settings loaded from environment."""

    def __init__(self):
        self._load_env()

    def _load_env(self):
        """Load .env file if it exists."""
        env_path = Path(__file__).resolve().parent.parent.parent / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

    @property
    def llm_provider(self) -> str:
        """Which LLM provider to use: 'openai' or 'ollama'."""
        return os.getenv("LLM_PROVIDER", "ollama")

    @property
    def openai_api_key(self) -> str:
        """OpenAI API key (required when using OpenAI)."""
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def ollama_base_url(self) -> str:
        """Ollama API base URL."""
        return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    @property
    def ollama_model(self) -> str:
        """Ollama model name."""
        return os.getenv("OLLAMA_MODEL", "llama2")

    @property
    def openai_model(self) -> str:
        """OpenAI model name."""
        return os.getenv("OPENAI_MODEL", "gpt-4")
    
    @property
    def generation_model(self) -> str:
        """EMBEDDING_MODEL name."""
        return os.getenv("GENERATION_MODEL", "phi3:mini")

    @property
    def embedding_model(self) -> str:
        """EMBEDDING_MODEL name."""
        return os.getenv("EMBEDDING_MODEL", "phi3:mini")
    
    @property
    def vector_store(self) -> str:
        """vector_store name."""
        return os.getenv("VECTOR_STORE", "faiss")

    @property
    def search_tool(self) -> str:
        """search_tool name."""
        return os.getenv("SEARCH_PROVIDER", "local")


# Convenience instance
settings = get_settings()
