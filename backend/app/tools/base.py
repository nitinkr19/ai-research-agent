from abc import ABC, abstractmethod

class Tool(ABC):

    @abstractmethod
    def run(self, query: str) -> str:
        pass
