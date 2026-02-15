"""Pytest configuration and fixtures."""

import os
import pytest


@pytest.fixture(autouse=True)
def reset_settings_cache():
    """Clear lru_cache on get_settings so env overrides take effect."""
    from app.core.config import get_settings
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def default_test_env(monkeypatch):
    """Set env vars so app can load (LLM, search, vector store)."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("SEARCH_PROVIDER", "local")
    monkeypatch.setenv("VECTOR_STORE", "faiss")
