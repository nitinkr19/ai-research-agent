"""
Base interface for LLM providers.
All providers (OpenAI, Ollama) implement this protocol.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        pass
    
    @abstractmethod
    def generate_stream(self, messages: list[dict]) -> Generator[str, None, None]:
        pass
        
    @abstractmethod
    def __repr__(self) -> str:
        """Human-readable provider description."""
        pass
