"""Tests for app.llm.factory."""

import pytest


def test_get_llm_provider_ollama(monkeypatch):
    """Factory returns OllamaProvider when LLM_PROVIDER=ollama."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.llm.factory import get_llm_provider
    from app.llm.ollama_provider import OllamaProvider

    p = get_llm_provider()
    assert isinstance(p, OllamaProvider)
    assert "OllamaProvider" in repr(p)

    get_settings.cache_clear()


def test_get_llm_provider_openai_requires_key(monkeypatch):
    """Factory raises when OpenAI selected but no API key."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.llm.factory import get_llm_provider

    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        get_llm_provider()

    get_settings.cache_clear()


def test_get_llm_provider_openai_with_key(monkeypatch):
    """Factory returns OpenAIProvider when OpenAI and key set."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.llm.factory import get_llm_provider
    from app.llm.openai_provider import OpenAIProvider

    p = get_llm_provider()
    assert isinstance(p, OpenAIProvider)

    get_settings.cache_clear()


def test_get_llm_provider_invalid(monkeypatch):
    """Factory raises for invalid provider."""
    monkeypatch.setenv("LLM_PROVIDER", "invalid")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.llm.factory import get_llm_provider

    with pytest.raises(ValueError, match="Invalid LLM_PROVIDER"):
        get_llm_provider()

    get_settings.cache_clear()
