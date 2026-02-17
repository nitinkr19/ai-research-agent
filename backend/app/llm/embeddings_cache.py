import os
import json
import hashlib
import numpy as np
from app.llm.embeddings import EmbeddingProvider
from app.core.config import settings

import logging

logger = logging.getLogger(__name__)

CACHE_FILE = f"embedding_cache_{settings.embedding_provider}_{settings.embedding_model}.json"

class CachedEmbeddingProvider:

    _cache = None

    @classmethod
    def _load_cache(cls):
        if cls._cache is None:
            if os.path.exists(CACHE_FILE):
                try:
                    with open(CACHE_FILE, "r") as f:
                        cls._cache = json.load(f)
                except Exception:
                    cls._cache = {}
            else:
                cls._cache = {}
        return cls._cache

    @staticmethod
    def _hash(text: str):
        composite = f"{settings.embedding_provider}:{settings.embedding_model}:{text}"
        return hashlib.sha256(composite.encode()).hexdigest()

    @classmethod
    def embed(cls, text: str) -> np.ndarray:
        cache = cls._load_cache()
        key = cls._hash(text)

        logger.info(f"CACHE_FILE path: {os.path.abspath(CACHE_FILE)}")
        if key in cache:
            logger.info("embedding_cache_hit")
            print("embedding_cache_hit")
                # extra={
                #     "provider": settings.embedding_provider,
                #     "model": settings.embedding_model,
                # }
            return np.array(cache[key], dtype="float32")
        
        logger.info("embedding_cache_miss")
        print("embedding_cache_miss")
            # extra={
            #     "provider": settings.embedding_provider,
            #     "model": settings.embedding_model,
            # }

        # Not cached → call actual provider
        vector = EmbeddingProvider.embed(text)

        cache[key] = vector.tolist()

        # Write back to disk
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f)
        except Exception:
            pass  # Never crash app due to cache write failure

        return vector
