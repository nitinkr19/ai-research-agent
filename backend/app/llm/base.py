"""
Base interface for LLM providers.
All providers (OpenAI, Ollama) implement this protocol.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    # @abstractmethod
    # async def complete(
    #     self,
    #     messages: List[Dict[str, str]],
    #     **kwargs: Any,
    # ) -> str:
    #     """
    #     Generate a completion from the LLM.

    #     Args:
    #         messages: List of message dicts with 'role' and 'content'.
    #         **kwargs: Provider-specific options (temperature, max_tokens, etc.).

    #     Returns:
    #         The model's text response.
    #     """
    #     pass

    @abstractmethod
    def generate(self, messages: list[dict]) -> str:
        pass
        
    @abstractmethod
    def __repr__(self) -> str:
        """Human-readable provider description."""
        pass
