"""Tests for app.memory.factory."""

import pytest


def test_get_vector_store_faiss(monkeypatch):
    """Factory returns FaissVectorStore when VECTOR_STORE=faiss."""
    monkeypatch.setenv("VECTOR_STORE", "faiss")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.memory.factory import get_vector_store
    from app.memory.faiss_store import FaissVectorStore

    store = get_vector_store()
    assert isinstance(store, FaissVectorStore)

    get_settings.cache_clear()


def test_get_vector_store_invalid(monkeypatch):
    """Factory raises for invalid VECTOR_STORE."""
    monkeypatch.setenv("VECTOR_STORE", "invalid")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.memory.factory import get_vector_store

    with pytest.raises(ValueError, match="Invalid VECTOR_STORE"):
        get_vector_store()

    get_settings.cache_clear()
