"""Tests for app.core.config."""

import os
import pytest


def test_settings_loads_with_defaults(monkeypatch):
    """Settings uses defaults when env vars are unset."""
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("SEARCH_PROVIDER", raising=False)
    monkeypatch.delenv("VECTOR_STORE", raising=False)

    from app.core.config import get_settings
    get_settings.cache_clear()
    s = get_settings()

    assert s.llm_provider == "ollama"
    assert s.ollama_base_url == "http://localhost:11434"
    assert s.ollama_model == "llama2"
    get_settings.cache_clear()


def test_settings_respects_env(monkeypatch):
    """Settings reads from environment."""
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OLLAMA_MODEL", "mistral")
    monkeypatch.setenv("SEARCH_PROVIDER", "tavily")
    monkeypatch.setenv("VECTOR_STORE", "faiss")

    from app.core.config import get_settings
    get_settings.cache_clear()
    s = get_settings()

    assert s.llm_provider == "openai"
    assert s.ollama_model == "mistral"
    assert s.search_tool.lower() == "tavily"
    assert s.vector_store.lower() == "faiss"
    get_settings.cache_clear()
