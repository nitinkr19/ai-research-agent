import faiss
import numpy as np
import requests
from typing import List
from app.memory.base import BaseVectorStore
from app.core.config import settings


class FaissVectorStore(BaseVectorStore):

    def __init__(self, dim: int = 3072):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []

    def embed(self, text: str):
        response = requests.post(
            f"{settings.ollama_base_url}/api/embeddings",
            json={
                "model": settings.embedding_model,
                "prompt": text
            }
        )

        embedding = response.json()["embedding"]
        return np.array(embedding, dtype="float32")

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
