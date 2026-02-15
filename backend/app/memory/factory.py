from app.memory.faiss_store import FaissVectorStore

def get_vector_store():
    # Later this can switch via ENV
    provider = os.getenv("VECTOR_STORE", "faiss")

    if provider == "faiss":
        return FaissVectorStore(dim=768)

    else:
        raise ValueError("Invalid VECTOR_STORE")
