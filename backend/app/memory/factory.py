from app.memory.faiss_store import FaissVectorStore
from app.core.config import settings

def get_vector_store():
    # Later this can switch via ENV
    provider = settings.vector_store.lower()

    if provider == "faiss":
        return FaissVectorStore(dim=1536)

    else:
        raise ValueError("Invalid VECTOR_STORE")
