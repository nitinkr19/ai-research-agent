"""Tests for app.memory.base."""

import pytest
from app.memory.base import BaseVectorStore


class ConcreteVectorStore(BaseVectorStore):
    """Concrete implementation for testing."""

    def __init__(self):
        self._docs = []

    def add(self, text: str):
        self._docs.append(text)

    def search(self, query: str, k: int = 3):
        return [d for d in self._docs if query in d][:k]


def test_base_vector_store_can_be_subclassed():
    """BaseVectorStore can be subclassed and used."""
    store = ConcreteVectorStore()
    store.add("hello world")
    store.add("foo bar")
    assert store.search("hello", k=5) == ["hello world"]
    assert store.search("bar") == ["foo bar"]
