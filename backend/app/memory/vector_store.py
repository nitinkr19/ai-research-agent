"""
Vector store for embedding and retrieving research artifacts.
Can be extended to use Chroma, FAISS, or other backends.
"""

from typing import List, Optional
from abc import ABC, abstractmethod


class BaseVectorStore(ABC):
    """Abstract interface for vector storage."""

    @abstractmethod
    async def add(self, texts: List[str], metadata: Optional[List[dict]] = None) -> None:
        """Add texts with optional metadata to the store."""
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search for similar texts. Returns list of {text, score, metadata}."""
        pass


class InMemoryVectorStore(BaseVectorStore):
    """
    Simple in-memory vector store for prototyping.
    Uses keyword overlap as similarity (replace with real embeddings for production).
    """

    def __init__(self):
        self._documents: List[dict] = []

    async def add(self, texts: List[str], metadata: Optional[List[dict]] = None) -> None:
        """Store texts with optional metadata."""
        meta = metadata or [{}] * len(texts)
        for text, m in zip(texts, meta):
            self._documents.append({"text": text, "metadata": m})

    async def search(self, query: str, top_k: int = 5) -> List[dict]:
        """Search by keyword overlap (simplified; use embeddings for real similarity)."""
        q_words = set(query.lower().split())
        scored = []
        for doc in self._documents:
            d_words = set(doc["text"].lower().split())
            overlap = len(q_words & d_words) / max(len(q_words), 1)
            scored.append({"text": doc["text"], "score": overlap, "metadata": doc["metadata"]})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
