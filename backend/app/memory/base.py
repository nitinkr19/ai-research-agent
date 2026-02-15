from abc import ABC, abstractmethod
from typing import List

class BaseVectorStore(ABC):

    @abstractmethod
    def add(self, text: str):
        pass

    @abstractmethod
    def search(self, query: str, k: int = 3) -> List[str]:
        pass
