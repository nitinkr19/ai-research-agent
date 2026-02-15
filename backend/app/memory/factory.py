from app.memory.faiss_store import FaissVectorStore

def get_vector_store():
    # Later this can switch via ENV
    return FaissVectorStore(dim=768)
