"""Tests for app.memory.vector_store (InMemoryVectorStore)."""

import pytest
from app.memory.vector_store import InMemoryVectorStore


@pytest.mark.asyncio
async def test_in_memory_vector_store_add_and_search():
    """InMemoryVectorStore stores and retrieves by keyword overlap."""
    store = InMemoryVectorStore()
    await store.add(["hello world", "machine learning basics"])
    results = await store.search("hello", top_k=2)
    assert len(results) >= 1
    assert results[0]["text"] == "hello world"
    assert "score" in results[0]


@pytest.mark.asyncio
async def test_in_memory_vector_store_empty_search():
    """InMemoryVectorStore returns [] when empty."""
    store = InMemoryVectorStore()
    results = await store.search("query", top_k=5)
    assert results == []
