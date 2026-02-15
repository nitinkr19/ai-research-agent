"""
Factory for creating the appropriate LLM provider based on config.
"""

from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.ollama_provider import OllamaProvider


def get_llm_provider() -> BaseLLMProvider:
    """
    Return the configured LLM provider.

    Returns:
        OpenAIProvider or OllamaProvider based on LLM_PROVIDER env var.
    """
    if settings.llm_provider.lower() == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY must be set when using OpenAI provider")
        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )
    elif settings.llm_provider.lower() == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )

    else:
        raise ValueError("Invalid LLM_PROVIDER")
