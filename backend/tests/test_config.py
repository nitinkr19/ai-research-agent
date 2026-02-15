"""Tests for app.core.config."""

import os
import pytest


def test_settings_loads_and_has_expected_properties(monkeypatch):
    """Settings loads and exposes required properties as strings."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "llama2")

    from app.core.config import get_settings
    get_settings.cache_clear()
    s = get_settings()

    assert isinstance(s.llm_provider, str)
    assert isinstance(s.ollama_base_url, str)
    assert isinstance(s.ollama_model, str)
    assert s.llm_provider == "ollama"
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
