import faiss
import numpy as np
import requests
from typing import List
from app.memory.base import BaseVectorStore
from app.core.config import settings
from app.llm.embeddings_cache import CachedEmbeddingProvider
from app.llm.embeddings import EmbeddingProvider
import logging

logger = logging.getLogger(__name__)

class FaissVectorStore(BaseVectorStore):

    def __init__(self, dim: int):
        self.dim = EmbeddingProvider.dim()
        print("dim")
        print(dim)
        self.index = faiss.IndexFlatL2(self.dim)
        self.text_chunks = []

    def embed(self, text: str):
        try:
            return CachedEmbeddingProvider.embed(text)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("embedding_failed")
            raise

    def add(self, text: str):
        vector = self.embed(text)
        self.index.add(np.array([vector]))
        self.text_chunks.append(text)

    def search(self, query: str, k: int = 3) -> List[str]:

        if len(self.text_chunks) == 0:
            return []

        query_vector = self.embed(query)

        distances, indices = self.index.search(
            np.array([query_vector]), k
        )

        results = []
        for idx in indices[0]:
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results
