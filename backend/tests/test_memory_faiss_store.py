"""Tests for app.memory.faiss_store."""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np


@patch("app.memory.faiss_store.requests.post")
def test_faiss_store_add_and_search(mock_post):
    """FaissVectorStore add and search with mocked embeddings."""
    mock_post.return_value.json.return_value = {
        "embedding": [0.1] * 3072
    }
    mock_post.return_value.status_code = 200

    with patch("app.memory.faiss_store.settings") as mock_settings:
        mock_settings.ollama_base_url = "http://localhost:11434"
        mock_settings.embedding_model = "nomic-embed-text"

        from app.memory.faiss_store import FaissVectorStore

        store = FaissVectorStore(dim=3072)
        store.add("hello world")
        store.add("machine learning")

        results = store.search("hello", k=2)
        assert len(results) >= 1
        assert "hello world" in results or "machine learning" in results


def test_faiss_store_search_empty_returns_empty():
    """FaissVectorStore.search on empty store returns []."""
    from app.memory.faiss_store import FaissVectorStore

    store = FaissVectorStore(dim=3072)
    results = store.search("query", k=3)
    assert results == []
