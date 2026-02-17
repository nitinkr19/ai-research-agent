import requests
import numpy as np
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

client = OpenAI()

class EmbeddingProvider:

    @staticmethod
    def embed(text: str) -> np.ndarray:
        logger.info("embedding_provider_call going")
        if settings.embedding_provider == "ollama":
            return EmbeddingProvider._ollama_embed(text)

        elif settings.embedding_provider == "openai":
            return EmbeddingProvider._openai_embed(text)

        else:
            raise ValueError("Unsupported embedding provider")
    
    @staticmethod
    def dim() -> int:
        logger.info(f"embedding_provider_dim {settings.embedding_provider}")
        if settings.embedding_provider == "ollama":
            return 768

        elif settings.embedding_provider == "openai":
            return 1536

        else:
            raise ValueError("Unsupported embedding provider")

    @staticmethod
    def _ollama_embed(text: str) -> np.ndarray:
        response = requests.post(
            f"{settings.ollama_base_url}/api/embeddings",
            json={
                "model": settings.embedding_model,
                "prompt": text
            }
        )
        print("OLLAMA STATUS:", response.status_code)
        if "embedding" not in response.json():
            raise ValueError(f"Ollama embedding failed: {response.json()}")
        
        embedding = response.json()["embedding"]
        return np.array(embedding, dtype="float32")

    @staticmethod
    def _openai_embed(text: str) -> np.ndarray:
        response = client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        embedding = response.data[0].embedding
        return np.array(embedding, dtype="float32")
